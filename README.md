# 🎬 MP4 Video & Audio Merger GUI

A simple, lightweight Python GUI tool to merge separate video and audio files (e.g., from Vimeo, YouTube, or other DASH downloads) into a single, perfectly synced MP4 file.

This tool uses FFmpeg to perform a **lossless and incredibly fast merge** (it copies the streams without re-encoding them). It also features a smart workaround for the common Windows `FFmpeg` PATH issue by using the `imageio-ffmpeg` Python package.

## ✨ Features

- **Simple GUI:** Built with Tkinter, no command-line knowledge required.
- **Lightning Fast:** Uses `-c copy` to merge streams without losing quality or re-encoding.
- **Zero PATH Headaches:** Automatically uses the FFmpeg binary bundled with `imageio-ffmpeg`, bypassing Windows environment variable issues.
- **Auto-Fill Output:** Automatically suggests an output filename based on your video file.
- **Cross-Platform:** Works on Windows, macOS, and Linux.

## 📸 Screenshot

*(Add a screenshot of your UI here by dragging and dropping the image into GitHub)*

## 🛠️ Prerequisites

- **Python 3.6 or higher** installed on your system.
- **Pip** (Python package installer).

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sibany/Python-Video-Audio-Merger.git
   cd Python-Video-Audio-Merger
   python Python-Video-Audio-Merger.py
