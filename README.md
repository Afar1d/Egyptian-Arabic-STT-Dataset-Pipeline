# Egyptian-Arabic-STT-Dataset-Pipeline


📌 Project Overview

This project implements an end-to-end Synthetic Speech Data Pipeline (S.S.D.P.) for generating high-quality Egyptian Arabic speech datasets designed for Speech-to-Text (STT) training workflows.

The system automates the full cycle from text generation to audio synthesis and dataset packaging using mostly free-tier AI tools, while focusing on output quality, structure, and usability.

It also addresses challenges specific to Egyptian Arabic dialects, including pronunciation variability, slang handling, and synthetic speech limitations.

⚙️ Pipeline Stages
🧠 Generate Egyptian Arabic prompts using Gemini API
🧹 Clean and preprocess generated text data
🆔 Assign unique IDs for each text sample
🔊 Convert text to speech using ElevenLabs TTS
🗂️ Structure dataset with consistent (ID → text → audio mapping)
📄 Generate metadata in JSON format
📦 Package all audio samples into a compressed ZIP dataset
🧪 Provide a lightweight review interface for validating pairs
🚀 Export final dataset ready for STT model training
🏗️ Architecture Overview
[ Gemini API ]
      ↓
(Text Generation - Egyptian Arabic Prompts)
      ↓
[ Text Preprocessing & Cleaning ]
      ↓
[ ID Assignment & Structuring ]
      ↓
[ ElevenLabs TTS Engine ]
      ↓
(Audio Generation)
      ↓
[ Storage Layer ]
   ├── JSON Metadata File
   ├── Audio Files (.wav/.mp3)
   └── ZIP Archive (Dataset Samples)
      ↓
[ Review Interface ]
      ↓
[ Final Export → STT Training Dataset ]
📁 Repository Structure
source_code/ → Core pipeline implementation
README.md → Project documentation
data.json → Structured dataset metadata (ID, text, audio mapping)
audio_samples.zip → Generated speech dataset samples
IDs mapping → Unique identifiers for each text/audio pair
🎯 Key Features
Fully automated speech dataset generation pipeline
Egyptian Arabic dialect-aware text generation
Structured dataset format suitable for ML training
Lightweight validation interface for quality control
Optimized for free-tier AI APIs and tools
💡 Notes

This project was designed with a focus on:

Practical AI pipeline engineering
Dataset generation for real-world STT systems
Balancing quality vs. cost using free-tier services
Experimentation with Arabic dialect speech synthesis
