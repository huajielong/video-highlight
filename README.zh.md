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

---

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
<p align="center"><b>智能视频剪辑工具 — 自动剪辑高燃片段并配卡点 BGM</b></p>
<p align="center">
  ⚡ 一键生成 · 🎵 双源 BGM · 🎨 5 种风格 · 🔊 4 种预设
</p>

<p align="center">
  <a href="#-快速开始">🚀 快速开始</a> •
  <a href="#-核心功能">⚡ 核心功能</a> •
  <a href="#-音乐风格">🎵 音乐风格</a> •
  <a href="#-混音预设">🔊 混音预设</a> •
  <a href="#-安装">📦 安装</a> •
  <a href="#-常见问题">❓ 常见问题</a>
</p>

---

## 🤔 剪个高燃视频要多久？

想做一个带卡点 BGM 的精彩视频合集，传统剪辑软件步骤繁琐、耗时巨大：

| 你可能遇到的问题 | Video Highlight 帮你解决 |
|:-----------------|:------------------------|
| ❓ 手动找高燃片段，一帧帧看太累 | ✅ **智能场景检测** — 自动识别精彩片段，秒级完成分析 |
| ❓ 配乐要找合适的 BGM，还要手动卡点 | ✅ **双源 BGM** — Tunee AI 专业生成或本地快速合成，自动卡点 |
| ❓ 不懂混音，音量比例调不好 | ✅ **4 种混音预设** — social/cinematic/vlog/action，一键应用 |
| ❓ 想做不同风格的视频但无从下手 | ✅ **5 种音乐风格** — epic/chill/electronic/cinematic/sports |
| ❓ 分析→剪辑→配乐→导出流程太长 | ✅ **一键处理** — 全自动管道，一条命令完成 |

### 🔥 适用场景

> **抖音/TikTok 爆款短视频** → **游戏精彩时刻剪辑** → **Vlog 高光片段** → **运动赛事集锦**

---

## 🚀 快速开始

### 基础用法（本地 BGM）

```bash
python main.py your_video.mp4
```

### 使用 Tunee AI（专业级）

```bash
python main.py your_video.mp4 \
  --bgm-source tunee \
  --api-key YOUR_API_KEY \
  --style epic
```

### 参数速览

| 参数 | 说明 | 默认值 |
|:-----|:------|:------:|
| `--bgm-source` | BGM 来源：`local` / `tunee` | `local` |
| `--style` | 音乐风格 | `epic` |
| `--preset` | 混音预设 | `social` |
| `--duration` | 目标视频时长（秒） | `30` |
| `--analyze-only` | 仅分析，不生成 | — |

---

## ⚡ 核心功能

| 功能 | 说明 |
|:-----|:------|
| 🎬 **自动剪辑** | 智能检测场景变化，提取最精彩片段 |
| 🎵 **双源 BGM** | Tunee AI 专业质量 + 本地快速生成，按需选择 |
| 🎨 **5 种风格** | epic / chill / electronic / cinematic / sports |
| 🔊 **4 种预设** | social / cinematic / vlog / action（BGM 音量智能适配） |
| ⚡ **一键处理** | 分析 → 剪辑 → 配乐 → 混音全自动管道 |
| 🔍 **仅分析模式** | `--analyze-only` 快速预览剪辑效果 |
| 🛡️ **原声保护** | 默认 100% 保留原声，BGM 作为背景音 |

---

## 🎵 音乐风格选择

| 风格 | 描述 | 适用场景 |
|:-----|:------|:---------|
| `epic` | 🎺 高燃动作，电影感 | 游戏、运动、竞赛 |
| `chill` | 🌊 轻松氛围，lo-fi | Vlog、生活记录 |
| `electronic` | ⚡ 电子音乐，能量感 | 科技、现代、潮流 |
| `cinematic` | 🎻 电影配乐，戏剧化 | 宣传片、预告片 |
| `sports` | 🏃 体育运动，激昂 | 体育、竞技、健身 |

---

## 🔊 混音预设

| 预设 | BGM 音量 | 适用场景 | 说明 |
|:-----|:--------:|:---------|:-----|
| `social` | 50% | 📱 社交媒体 | 标准模式，保留对白清晰度 |
| `cinematic` | 70% | 🎬 电影感 | 戏剧化效果，BGM 主导氛围 |
| `vlog` | 30% | 🎤 Vlog | 对白为主，BGM 轻背景 |
| `action` | 80% | 🔥 高燃动作 | BGM 主导，适合纯音乐视频 |

---

## 📦 安装

### 作为 Claude Code Skill 安装

```bash
# 方式 1: Git Clone（推荐）
git clone https://github.com/huajielong/video-highlight.git ~/.claude/skills/video-highlight-skill --depth 1

# 方式 2: Curl 下载
curl -L https://github.com/huajielong/video-highlight/archive/refs/heads/main.tar.gz | tar -xz

# 方式 3: Windows PowerShell
git clone https://github.com/huajielong/video-highlight.git $env:USERPROFILE\.claude\skills\video-highlight-skill --depth 1
```

### 环境依赖

```bash
# 1. 安装 FFmpeg（必需）
# macOS
brew install ffmpeg
# Ubuntu/Debian
sudo apt install ffmpeg
# Windows
choco install ffmpeg

# 2. 安装 Python 依赖
pip install -r requirements.txt

# 3. 配置 Tunee API（可选）
export TUNEE_API_KEY=your-api-key
```

---

## 📖 使用示例

| 场景 | 命令 |
|:-----|:------|
| 📱 **社交媒体** | `python main.py video.mp4 --preset social` |
| 🎮 **游戏时刻** | `python main.py video.mp4 --preset action --style epic` |
| 🎤 **Vlog** | `python main.py video.mp4 --preset vlog --style chill` |
| 🎬 **宣传片** | `python main.py video.mp4 --preset cinematic --duration 60` |

---

## 🔧 脚本工具

```bash
# 检查 Tunee AI 积分
python scripts/tunee_music.py --api-key YOUR_KEY --check-credits

# 列出可用模型
python scripts/tunee_music.py --api-key YOUR_KEY --list-models

# 生成自定义 BGM
python scripts/tunee_music.py --api-key YOUR_KEY --style epic --output bgm.mp3
```

---

## 📁 项目结构

```
video-highlight-skill/
├── SKILL.md              # Claude Code 技能定义
├── main.py               # 主工作流脚本
├── scripts/
│   ├── tunee_music.py    # Tunee AI 音乐生成
│   ├── generate_bgm.py   # 本地 BGM 生成
│   ├── analyze_scenes_v2.py # 场景分析
│   ├── mix_audio_v2.py   # 混音工具
│   └── utils/
│       └── tunee_api.py  # Tunee API 封装
├── evals/                # 测试用例
├── requirements.txt      # Python 依赖
├── OPTIMIZATION.md       # 优化说明
├── LICENSE               # MIT 许可证
└── README.md             # 💡 你在这里
```

---

## ❓ 常见问题

<details>
<summary><b>Tunee AI API Key 从哪里获取？</b></summary>
访问 <a href="https://www.tunee.ai">https://www.tunee.ai</a> 注册账号获取。首次注册通常赠送免费积分用于测试。
</details>

<details>
<summary><b>BGM 会覆盖视频原声吗？</b></summary>
不会。默认保留 100% 原声，BGM 作为背景音叠加。通过不同混音预设可以调整 BGM 与原声的比例：social（50%）、vlog（30%）、cinematic（70%）、action（80%）。
</details>

<details>
<summary><b>支持哪些视频格式？</b></summary>
支持 FFmpeg 支持的所有格式：MP4、MOV、AVI、MKV、FLV、WMV 等。输入后统一处理为标准 MP4 输出。
</details>

<details>
<summary><b>处理速度快吗？</b></summary>
取决于视频长度和硬件配置。一个 10 分钟的视频通常 2-5 分钟完成分析→剪辑→配乐→混音全流程。使用 GPU 加速可显著提升速度。
</details>

<details>
<summary><b>本地 BGM 和 Tunee AI 有什么区别？</b></summary>
本地 BGM 使用算法合成（免费、快速、不需要网络），适合快速预览。Tunee AI 使用专业 AI 音乐模型（需 API Key 和积分），质量更高、更丰富，适合正式发布。
</details>

---

## 🤝 贡献

欢迎任何形式的贡献——提交 Issue、Pull Request 或改进文档。

<a href="https://github.com/huajielong/video-highlight/graphs/contributors">
  <img src="https://img.shields.io/badge/contributions-welcome-brightgreen" alt="Contributions Welcome"/>
</a>

## 📄 License

MIT © [huajielong](https://github.com/huajielong)

---

<p align="center">
  <i>v2.1 — 专业音乐生成，一键智能剪辑！</i><br>
  ⭐ 如果对你有帮助，请点个 Star 支持一下！
</p>
