# 🎙️ Egyptian-Arabic-STT-Dataset-Pipeline

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)
![AI Pipeline](https://img.shields.io/badge/AI-Speech%20Generation-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📌 Project Overview

This project implements an **end-to-end Synthetic Speech Data Pipeline (S.S.D.P.)** for generating high-quality **Egyptian Arabic speech datasets** designed for Speech-to-Text (STT) training workflows.

The system automates the full cycle from **text generation → audio synthesis → dataset packaging** using mostly free-tier AI tools, while maintaining strong focus on output quality, structure, and usability.

It also addresses challenges specific to **Egyptian Arabic dialects**, including pronunciation variability, slang handling, and synthetic speech limitations.

---

## ⚙️ Pipeline Stages

- 🧠 Generate Egyptian Arabic prompts using **Gemini API**
- 🧹 Clean and preprocess generated text data
- 🆔 Assign unique IDs for each text sample
- 🔊 Convert text to speech using **ElevenLabs TTS**
- 🗂️ Structure dataset with consistent **(ID → text → audio mapping)**
- 📄 Generate metadata in **JSON format**
- 📦 Package all audio samples into a compressed **ZIP dataset**
- 🧪 Provide a lightweight review interface for validating text/audio pairs
- 🚀 Export final dataset ready for STT model training

---

## 📁 Repository Structure

- `source_code/` → Core pipeline implementation  
- `README.md` → Project documentation  
- `data.json` → Structured dataset metadata (ID, text, audio mapping)  
- `audio_samples.zip` → Generated speech dataset samples  
- `IDs mapping` → Unique identifiers for each text/audio pair  

---

## 🎯 Key Features

- Fully automated speech dataset generation pipeline  
- Egyptian Arabic dialect-aware text generation  
- Structured dataset format suitable for ML training  
- Lightweight validation interface for quality control  
- Optimized for free-tier AI APIs and services  

---

## 💡 Notes

This project was designed with a focus on:

- Practical AI pipeline engineering  
- Real-world STT dataset generation  
- Balancing quality vs. cost using free-tier services  
- Experimentation with Arabic dialect speech synthesis  

---

## 🚀 Future Improvements

- Improve pronunciation consistency for Egyptian dialect edge cases  
- Enhance review interface with scoring system for audio quality  
- Expand dataset size with diverse conversational domains  
- Add support for multi-speaker voice synthesis  

---


https://github.com/user-attachments/assets/020554b3-d369-4897-b1ed-e6e6cd078237


