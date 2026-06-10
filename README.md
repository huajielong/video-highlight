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

---

## 🎵 Music Styles

| Style | Description | Best For |
|:------|:------------|:---------|
| `epic` | 🎺 High-energy action, cinematic feel | Gaming, sports, competitions |
| `chill` | 🌊 Relaxed vibe, lo-fi | Vlogs, daily life |
| `electronic` | ⚡ Electronic music, energetic | Tech, modern, trendy |
| `cinematic` | 🎻 Film score, dramatic | Trailers, promos |
| `sports` | 🏃 Sports,激昂 | Athletics, fitness |

---

## 🔊 Mix Presets

| Preset | BGM Volume | Use Case | Description |
|:-------|:----------:|:---------|:------------|
| `social` | 50% | 📱 Social Media | Standard mode, preserves dialogue clarity |
| `cinematic` | 70% | 🎬 Cinematic | Dramatic effect, BGM leads the atmosphere |
| `vlog` | 30% | 🎤 Vlog | Dialogue-focused, light BGM background |
| `action` | 80% | 🔥 High-Energy Action | BGM-driven, ideal for music-focused videos |

---

## 📦 Installation

### Install as a Claude Code Skill

```bash
# Option 1: Git Clone (Recommended)
git clone https://github.com/huajielong/video-highlight.git ~/.claude/skills/video-highlight-skill --depth 1

# Option 2: Curl Download
curl -L https://github.com/huajielong/video-highlight/archive/refs/heads/main.tar.gz | tar -xz

# Option 3: Windows PowerShell
git clone https://github.com/huajielong/video-highlight.git $env:USERPROFILE\.claude\skills\video-highlight-skill --depth 1
```

### Dependencies

```bash
# 1. Install FFmpeg (Required)
# macOS
brew install ffmpeg
# Ubuntu/Debian
sudo apt install ffmpeg
# Windows
choco install ffmpeg

# 2. Install Python Dependencies
pip install -r requirements.txt

# 3. Configure Tunee API (Optional)
export TUNEE_API_KEY=your-api-key
```

---

## 📖 Usage Examples

| Scenario | Command |
|:---------|:--------|
| 📱 **Social Media** | `python main.py video.mp4 --preset social` |
| 🎮 **Gaming Moments** | `python main.py video.mp4 --preset action --style epic` |
| 🎤 **Vlog** | `python main.py video.mp4 --preset vlog --style chill` |
| 🎬 **Promo / Trailer** | `python main.py video.mp4 --preset cinematic --duration 60` |

---

## 🔧 Script Tools

```bash
# Check Tunee AI Credits
python scripts/tunee_music.py --api-key YOUR_KEY --check-credits

# List Available Models
python scripts/tunee_music.py --api-key YOUR_KEY --list-models

# Generate Custom BGM
python scripts/tunee_music.py --api-key YOUR_KEY --style epic --output bgm.mp3
```

---

## 📁 Project Structure

```
video-highlight-skill/
├── SKILL.md              # Claude Code skill definition
├── main.py               # Main workflow script
├── scripts/
│   ├── tunee_music.py    # Tunee AI music generation
│   ├── generate_bgm.py   # Local BGM generation
│   ├── analyze_scenes_v2.py # Scene analysis
│   ├── mix_audio_v2.py   # Audio mixing tool
│   └── utils/
│       └── tunee_api.py  # Tunee API wrapper
├── evals/                # Test cases
├── requirements.txt      # Python dependencies
├── OPTIMIZATION.md       # Optimization notes
├── LICENSE               # MIT License
└── README.md             # 💡 You are here
```

---

## ❓ FAQ

<details>
<summary><b>Where do I get a Tunee AI API Key?</b></summary>
Visit <a href="https://www.tunee.ai">https://www.tunee.ai</a> to register an account. First registration usually comes with free credits for testing.
</details>

<details>
<summary><b>Will BGM overwrite the original video audio?</b></summary>
No. By default, 100% of the original audio is preserved, with BGM layered as background. Different mix presets adjust the BGM-to-original ratio: social (50%), vlog (30%), cinematic (70%), action (80%).
</details>

<details>
<summary><b>What video formats are supported?</b></summary>
All formats supported by FFmpeg: MP4, MOV, AVI, MKV, FLV, WMV, etc. All inputs are processed into a standard MP4 output.
</details>

<details>
<summary><b>Is the processing fast?</b></summary>
It depends on video length and hardware. A 10-minute video typically completes the full analysis → editing → scoring → mixing pipeline in 2-5 minutes. GPU acceleration can significantly improve speed.
</details>

<details>
<summary><b>What's the difference between local BGM and Tunee AI?</b></summary>
Local BGM uses algorithmic synthesis (free, fast, no network required), suitable for quick previews. Tunee AI uses professional AI music models (requires API Key and credits), offering higher quality and more variety, ideal for final release.
</details>

---

## 🤝 Contributing

Contributions of any kind are welcome — submit an Issue, Pull Request, or improve the documentation.

<a href="https://github.com/huajielong/video-highlight/graphs/contributors">
  <img src="https://img.shields.io/badge/contributions-welcome-brightgreen" alt="Contributions Welcome"/>
</a>

## 📄 License

MIT © [huajielong](https://github.com/huajielong)

---

<p align="center">
  <i>v2.1 — Professional Music Generation, One-Click Smart Editing!</i><br>
  ⭐ If this helps you, please give it a Star!
</p>

> [中文说明](README.zh.md)
