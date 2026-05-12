#!/usr/bin/env python3
"""
Egyptian Arabic TTS Dataset Generator
Generates sentences using Gemini, converts to audio with ElevenLabs.
"""

import json
import re
import os
import sys
import argparse
import subprocess


# ── Auto-install dependencies ─────────────────────────────────────────────────
REQUIRED_PACKAGES = {
    "google.genai": "google-genai",
    "elevenlabs":   "elevenlabs",
}

def ensure_dependencies():
    missing = []
    for module, package in REQUIRED_PACKAGES.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"Installing missing packages: {', '.join(missing)}")
        # Clear corrupted pip cache to suppress deserialization warnings
        subprocess.call(
            [sys.executable, "-m", "pip", "cache", "purge"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet", "--no-warn-script-location", *missing],
            stderr=subprocess.DEVNULL,
        )
        print("✓ Packages installed\n")

ensure_dependencies()
# ─────────────────────────────────────────────────────────────────────────────

from google import genai
from elevenlabs.client import ElevenLabs
from elevenlabs import save


def clean_for_tts(text: str) -> str:
    # 1. Strip leading numbering (e.g. "1. " or Arabic-Indic "١. ")
    text = re.sub(r'^\d+\.\s*', '', text.strip())
    text = re.sub(r'^[\u0660-\u0669]+\.\s*', '', text)

    # 2. Remove symbols that confuse TTS
    text = re.sub(r'[\u00AB\u00BB\u201C\u201D\u2018\u2019\(\)\[\]{}_\\|<>~`^*+=@#$%&]', '', text)

    # 3. Normalize Arabic punctuation to standard equivalents (for natural pauses)
    text = text.replace('\u060C', ',')   # Arabic comma
    text = text.replace('\u061F', '?')   # Arabic question mark
    text = text.replace('\u061B', ';')   # Arabic semicolon
    text = text.replace('\u2026', '...') # ellipsis

    # 4. Remove tatweel/kashida (decorative stretch, not pronounced)
    text = re.sub(r'\u0640+', '', text)

    # 5. Remove tashkeel/diacritics (ElevenLabs handles undiacritized Arabic better)
    text = re.sub(r'[\u064B-\u065F]', '', text)

    # 6. Normalize Alef variants to plain Alef
    text = re.sub(r'[\u0623\u0625\u0622\u0671]', '\u0627', text)

    # 7. Normalize dotless Yaa to Yaa
    text = re.sub(r'\u0649', '\u064A', text)

    # 8. Normalize Waw with Hamza to plain Waw
    text = re.sub(r'\u0624', '\u0648', text)

    # 9. Remove zero-width and invisible Unicode characters
    text = re.sub(r'[\u200b-\u200f\ufeff]', '', text)

    # 10. Collapse repeated punctuation (e.g. "!!!" to "!")
    text = re.sub(r'([!?,.]){2,}', r'\1', text)

    # 11. Ensure sentence ends with punctuation for natural prosody
    text = text.strip()
    if text and text[-1] not in '.!?,;':
        text += '.'

    # 12. Collapse extra spaces
    text = re.sub(r' +', ' ', text).strip()

    return text


def main():
    parser = argparse.ArgumentParser(description="Generate Egyptian Arabic TTS dataset")
    parser.add_argument("--gemini-key",  default=os.getenv("GEMINI_API_KEY"),  help="Google Gemini API key")
    parser.add_argument("--eleven-key",  default=os.getenv("ELEVEN_API_KEY"),  help="ElevenLabs API key")
    parser.add_argument("--num",         type=int, default=12,                 help="Number of sentences (default: 12)")
    parser.add_argument("--voice-id",    default="cgSgspJ2msm6clMCkdW9",       help="ElevenLabs voice ID (default: Jessica)")
    parser.add_argument("--output-dir",  default="audio_output",               help="Directory for audio files (default: audio_output)")
    parser.add_argument("--output-json", default="egyptian_dataset.json",      help="Output JSON file (default: egyptian_dataset.json)")
    args = parser.parse_args()

    

    if not args.gemini_key:
        args.gemini_key = input("Enter your Gemini API key: ").strip()
    if not args.eleven_key:
        args.eleven_key = input("Enter your ElevenLabs API key: ").strip()

    if args.num == 12:  # still at default, ask the user
        while True:
            try:
                args.num = int(input("How many sentences to generate? ").strip())
                if args.num > 0:
                    break
                print("Please enter a number greater than 0.")
            except ValueError:
                print("Invalid input. Please enter a whole number.")

    # ── Step 1: Generate sentences with Gemini ───────────────────────────────
    print(f"Generating {args.num} Egyptian Arabic sentences...")

    genai_client = genai.Client(api_key=args.gemini_key)

    prompt = f"""
اكتب {args.num} جملة باللهجة المصرية العامية.

الشروط:
- كلام طبيعي جدًا
- من الحياة اليومية
- فيه أسئلة ومشاعر وأوامر
- قصيرة وطويلة
- بدون فصحى
- بدون ترقيم أو شرح
"""

    response = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    lines = response.text.split("\n")
    sentences = []
    seen = set()

    for line in lines:
        line = clean_for_tts(line)
        if line and line not in seen:
            seen.add(line)
            sentences.append(line)

    dataset = [
        {"id": idx + 1, "text": s, "audio_path": None, "status": "pending"}
        for idx, s in enumerate(sentences)
    ]

    # Append one combined full-text entry
    full_text = " ".join(item["text"] for item in dataset)
    dataset.append({"id": len(dataset) + 1, "text": full_text, "audio_path": None, "status": "pending"})

    print(f"✓ Generated {len(dataset) - 1} sentences + 1 full-text entry\n")

    # ── Step 2: Convert to audio with ElevenLabs ─────────────────────────────
    os.makedirs(args.output_dir, exist_ok=True)
    client = ElevenLabs(api_key=args.eleven_key)

    print(f"Converting to audio (voice: {args.voice_id})...")
    for item in dataset:
        out_path = os.path.join(args.output_dir, f"{item['id']:03d}.mp3")
        try:
            audio = client.text_to_speech.convert(
                text=item["text"],
                voice_id=args.voice_id,
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
            )
            save(audio, out_path)
            item["audio_path"] = out_path
            item["status"] = "success"
            print(f"  [{item['id']:03d}] ✓  {item['text'][:60]}")
        except Exception as e:
            item["status"] = f"failed: {e}"
            print(f"  [{item['id']:03d}] ✗  {e}")

    # ── Step 3: Save JSON dataset ─────────────────────────────────────────────
    with open(args.output_json, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    success_count = sum(1 for item in dataset if item["status"] == "success")
    print(f"\n✓ Saved {args.output_json} — {success_count}/{len(dataset)} succeeded")
    # ── Step 4: Generate review HTML & launch browser ────────────────────────
    generate_review_html(dataset, args.output_json)


def generate_review_html(dataset, json_path):
    import json as _json
    import threading
    import webbrowser
    from http.server import HTTPServer, BaseHTTPRequestHandler

    # ── Find a free port ──────────────────────────────────────────────────────
    import socket
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()

    json_abs  = os.path.abspath(json_path)
    html_path = os.path.splitext(json_abs)[0] + "_review.html"

    # ── Read the template ─────────────────────────────────────────────────────
    template_candidates = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "review_template.html"),
    ]
    template_html = None
    for p in template_candidates:
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                template_html = f.read()
            break

    if template_html is None:
        print("⚠ review_template.html not found — skipping HTML generation.")
        return

    # ── Inject dataset JSON and port ─────────────────────────────────────────
    dataset_json = _json.dumps(dataset, ensure_ascii=False)
    html = template_html \
        .replace("'__DATASET_PATH__'", _json.dumps(json_abs)) \
        .replace("__DATASET_JSON__", dataset_json) \
        .replace("__PORT__", str(port))

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n✓ Review page saved → {html_path}")

    # ── Tiny HTTP server to handle /save ──────────────────────────────────────
    class SaveHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            if self.path == "/save":
                length = int(self.headers.get("Content-Length", 0))
                body   = self.rfile.read(length)
                try:
                    data = _json.loads(body)
                    with open(json_abs, "w", encoding="utf-8") as f:
                        _json.dump(data, f, ensure_ascii=False, indent=2)
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"ok")
                    print(f"  [save] JSON updated ({len(data)} entries)")
                except Exception as e:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(str(e).encode())
            else:
                self.send_response(404); self.end_headers()

        def do_OPTIONS(self):
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin",  "*")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()

        def log_message(self, *args): pass  # silence request logs

    server = HTTPServer(("localhost", port), SaveHandler)

    def run_server():
        print(f"  [server] Save server running on port {port} — keep this window open while reviewing.")
        server.serve_forever()

    t = threading.Thread(target=run_server, daemon=True)
    t.start()

    # ── Open browser ──────────────────────────────────────────────────────────
    webbrowser.open(f"file:///{html_path.replace(chr(92), '/')}")
    print("  [browser] Review page opened in your browser.")
    print("  Press Ctrl+C to stop the server when done reviewing.\n")

    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n✓ Server stopped. Goodbye!")
        server.shutdown()


if __name__ == "__main__":
    main()
