# 🎬 AI Subtitle Generator

An AI-powered tool that automatically generates **English subtitles** for videos or recorded audio using OpenAI Whisper and Node.js + React.

This project supports:
- 🎥 Uploading video files (MP4, MKV, etc.)
- 🎤 Recording voice/audio directly in the browser
- 🌐 Language options (Sinhala, Tamil, Hindi, English)
- 🧠 Automatic transcription and subtitle generation in `.srt` format
- 📡 Real-time progress updates using Server-Sent Events (SSE)
- ⚙️ Multi-language model support using OpenAI Whisper

---

## 🏗️ Project Structure

AI-Subtitle-Generator/
│
├── server.js # Node.js backend (handles upload & SSE)
├── generate_subtitles.py # Python script (transcription using Whisper)
├── client/ # React frontend
│ └── UploadForm.jsx # Main UI for uploading videos and tracking progress
│
├── uploads/ # Temporary video/audio uploads
├── subtitles/ # Generated subtitle files (.srt)
└── README.md # This file


---

## ⚙️ Setup Instructions

### 🧩 Prerequisites

- Node.js (v18+)
- Python 3.8+
- Git
- pip (Python package manager)
- Whisper + FFmpeg installed

---

### 🚀 Step 1. Clone the Repository

```bash
git clone https://github.com/kavizzz03/AI-Subtitle-Generator.git
cd AI-Subtitle-Generator
