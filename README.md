> [🇨🇳 中文说明](README.zh.md)

<p align="center">
  <img src="https://img.shields.io/badge/version-2.1-blue" alt="v2.1"/>
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT"/>
  <img src="https://img.shields.io/badge/python-3.7+-orange" alt="Python 3.7+"/>
  <img src="https://img.shields.io/github/stars/huajielong/video-highlight?style=social" alt="Stars"/>
  <img src="https://img.shields.io/badge/Tunee_AI-integrated-purple" alt="Tunee AI"/>
  <img src="https://img.shields.io/badge/FFmpeg-7.0%2B-brightgreen" alt="FFmpeg 7.0+"/>
  <img src="https://img.shields.io/badge/Claude%20Code-Skill-orange" alt="Claude Code Skill"/>
</p>

<h1 align="center">🎬 Video Highlight Skill</h1>
<p align="center"><b>Automatically clip highlight reels with beat-synced BGM — AI-powered video editing tool</b></p>
<p align="center">
  ⚡ One-Click Generation · 🎵 Dual-Source BGM · 🎨 5 Styles · 🔊 4 Presets
</p>

<p align="center">
  <a href="#-quick-start">🚀 Quick Start</a> •
  <a href="#-core-features">⚡ Core Features</a> •
  <a href="#-music-styles">🎵 Music Styles</a> •
  <a href="#-mix-presets">🔊 Mix Presets</a> •
  <a href="#-installation">📦 Installation</a> •
  <a href="#-faq">❓ FAQ</a>
</p>

---

## 🤔 How Long Does It Take to Clip a Highlight Reel?

Creating an exciting video compilation with beat-synced BGM using traditional editing software is tedious and time-consuming:

| You might run into... | Video Highlight solves it |
|:----------------------|:--------------------------|
| ❓ Manually hunting for highlight clips, reviewing frame by frame | ✅ **Smart Scene Detection** — Automatically identifies exciting segments, analysis in seconds |
| ❓ Finding the right BGM and syncing beats manually | ✅ **Dual-Source BGM** — Tunee AI professional generation or local quick synthesis, auto beat-matching |
| ❓ No audio mixing experience, getting volume balance wrong | ✅ **4 Mix Presets** — social/cinematic/vlog/action, one-click apply |
| ❓ Wanting different style videos but don't know where to start | ✅ **5 Music Styles** — epic/chill/electronic/cinematic/sports |
| ❓ The analysis → editing → scoring → export pipeline is too long | ✅ **One-Click Processing** — Fully automated pipeline, single command |

### 🔥 Use Cases

> **Douyin/TikTok Viral Shorts** → **Game Highlight Moments** → **Vlog Highlights** → **Sports Event Reels**

---

## 🚀 Quick Start

### Basic Usage (Local BGM)

```bash
python main.py your_video.mp4
```

### Using Tunee AI (Professional Grade)

```bash
python main.py your_video.mp4 \
  --bgm-source tunee \
  --api-key YOUR_API_KEY \
  --style epic
```

### Parameter Reference

| Parameter | Description | Default |
|:----------|:------------|:-------:|
| `--bgm-source` | BGM source: `local` / `tunee` | `local` |
| `--style` | Music style | `epic` |
| `--preset` | Mix preset | `social` |
| `--duration` | Target video duration (seconds) | `30` |
| `--analyze-only` | Analyze only, do not generate | — |

---

## ⚡ Core Features

| Feature | Description |
|:--------|:------------|
| 🎬 **Auto Clipping** | Intelligently detect scene changes, extract the best moments |
| 🎵 **Dual-Source BGM** | Tunee AI professional quality + local fast generation, choose as needed |
| 🎨 **5 Styles** | epic / chill / electronic / cinematic / sports |
| 🔊 **4 Presets** | social / cinematic / vlog / action (smart BGM volume adaptation) |
| ⚡ **One-Click Pipeline** | Analysis → Editing → Scoring → Mixing fully automated |
| 🔍 **Analyze-Only Mode** | `--analyze-only` for quick preview of clip results |
| 🛡️ **Audio Protection** | 100% original audio preserved by default, BGM as background |
