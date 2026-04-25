# Video Highlight Skill v2.1

智能视频剪辑工具 - 自动剪辑高燃片段并配卡点BGM

[![Version](https://img.shields.io/badge/version-2.1-blue.svg)](https://github.com/huajielong/skills-hub/tree/main/video-highlight-skill)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tunee](https://img.shields.io/badge/Tunee_AI-integrated-purple.svg)](https://www.tunee.ai)

---

## 功能特点

- 🎬 **自动剪辑** - 智能检测场景变化，提取最精彩片段
- 🎵 **双源BGM** - Tunee AI专业质量 + 本地快速生成
- 🎨 **5种风格** - epic, chill, electronic, cinematic, sports
- 🔊 **4种预设** - social, cinematic, vlog, action混音
- ⚡ **一键处理** - 分析→剪辑→配乐→混音全自动

---

## 快速开始

### 基础用法（本地BGM）

```bash
python main.py your_video.mp4
```

### 使用Tunee AI

```bash
python main.py your_video.mp4 \
  --bgm-source tunee \
  --api-key YOUR_API_KEY \
  --style epic
```

### 只分析视频

```bash
python main.py your_video.mp4 --analyze-only
```

---

## 音乐风格选择

| 风格 | 描述 | 适用场景 |
|------|------|----------|
| `epic` | 高燃动作，电影感 | 游戏、运动 |
| `chill` | 轻松氛围，lo-fi | Vlog、生活 |
| `electronic` | 电子音乐，能量感 | 科技、现代 |
| `cinematic` | 电影配乐，戏剧化 | 宣传片、预告 |
| `sports` | 体育运动，激昂 | 体育、竞技 |

---

## 混音预设

| 预设 | BGM音量 | 适用场景 |
|------|---------|----------|
| `social` | 50% | 社交媒体标准（保留对白） |
| `cinematic` | 70% | 电影感，戏剧化 |
| `vlog` | 30% | Vlog（对白为主） |
| `action` | 80% | 高燃动作（BGM主导） |

---

## 安装

### 一键安装

```bash
# 方式1: Git Clone（推荐）
git clone https://github.com/huajielong/skills-hub.git ~/.claude/skills/video-highlight-skill --depth 1 --single-branch --branch main

# 方式2: Curl 下载
curl -L https://github.com/huajielong/skills-hub/archive/refs/heads/main.tar.gz | tar -xz -C ~/.claude/skills/ --strip-components=1 skills-hub-main/video-highlight-skill

# 方式3: Wget 下载
wget -O- https://github.com/huajielong/skills-hub/archive/refs/heads/main.tar.gz | tar -xz -C ~/.claude/skills/ --strip-components=1 skills-hub-main/video-highlight-skill

# Windows PowerShell
git clone https://github.com/huajielong/skills-hub.git $env:USERPROFILE\.claude\skills\video-highlight-skill --depth 1 --single-branch --branch main
```

### 手动安装

```bash
# 1. 安装FFmpeg

# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
choco install ffmpeg

# 2. 安装Python依赖
pip install -r requirements.txt

# 3. 配置Tunee API（可选）
export TUNEE_API_KEY=your-api-key

# 4. 复制技能目录
cp -r video-highlight-skill ~/.claude/skills/
```

---

## 使用示例

### 示例1：社交媒体短视频

```bash
python main.py video.mp4 --preset social
```

### 示例2：游戏精彩时刻

```bash
python main.py video.mp4 --preset action --style epic
```

### 示例3：Vlog片段

```bash
python main.py video.mp4 --preset vlog --style chill
```

### 示例4：自定义时长

```bash
python main.py video.mp4 --duration 60 --preset cinematic
```

---

## Tunee API工具

```bash
# 检查积分
python scripts/tunee_music.py --api-key YOUR_KEY --check-credits

# 列出模型
python scripts/tunee_music.py --api-key YOUR_KEY --list-models

# 生成音乐
python scripts/tunee_music.py --api-key YOUR_KEY --style epic --output bgm.mp3
```

---

## 项目结构

```
video-highlight-skill/
├── SKILL.md              # 技能说明（Claude使用）
├── main.py              # 主工作流脚本
├── scripts/
│   ├── tunee_music.py       # Tunee AI音乐生成
│   ├── generate_bgm.py      # 本地BGM生成
│   ├── analyze_scenes_v2.py # 场景分析
│   ├── mix_audio_v2.py      # 混音工具
│   ├── progress.py         # 进度跟踪
│   └── utils/
│       └── tunee_api.py     # Tunee API工具
│   └── README.md            # 脚本文档
└── README.md               # 本文件
```

---

## 依赖

| 工具 | 版本 | 必需 |
|------|------|------|
| FFmpeg | 7.0+ | ✓ |
| Python | 3.7+ | ✓ |
| NumPy | - | 本地BGM |
| requests | - | Tunee AI |

---

## 版本历史

### v2.1 (2026-04-25)
- ✨ Tunee AI完整集成
- ✨ 5种音乐风格
- ✨ 积分查询和模型列表
- ✨ 完善错误处理

### v2.0 (2026-04-25)
- ✨ 进度反馈系统
- ✨ 4种混音预设
- ✨ 增强的场景分析
- ✨ 一键处理工作流

### v1.0 (2026-04-25)
- 🎉 初始版本

---

## 常见问题

**Q: Tunee AI API Key从哪里获取？**
A: 访问 https://www.tunee.ai 注册账号获取

**Q: 如何检查剩余积分？**
```bash
python scripts/tunee_music.py --api-key YOUR_KEY --check-credits
```

**Q: BGM会覆盖原声吗？**
A: 不会。默认保留100%原声，BGM作为背景。可通过预设调整。

**Q: 支持哪些视频格式？**
A: 支持FFmpeg支持的所有格式：MP4, MOV, AVI, MKV, FLV等

---

## 技能包信息

- **版本**: v2.1
- **仓库**: https://github.com/huajielong/skills-hub/tree/main/video-highlight-skill

---

*v2.1 - 专业音乐生成，一键智能剪辑！* 🎬🎵✨
