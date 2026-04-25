---
name: video-highlight
description: 自动剪辑高燃视频片段并配卡点BGM。当用户提到剪辑视频、制作短视频、剪精彩片段、配BGM、高燃、卡点、30秒、抖音、TikTok、精彩时刻、游戏高光、运动视频、vlog片段、宣传片剪辑等任务时使用此技能。一键完成分析→剪辑→配乐→混音全流程。
---

# Video Highlight v2.1

智能视频剪辑工具，自动将长视频剪辑为30秒高燃片段并配卡点背景音乐。

## 快速使用

```bash
# 一键剪辑
python main.py video.mp4

# Tunee AI音乐
python main.py video.mp4 --bgm-source tunee --api-key YOUR_KEY --style epic

# 只分析
python main.py video.mp4 --analyze-only
```

## 功能

- **场景分析** - 自动检测场景变化，推荐最活跃片段
- **视频剪辑** - 提取30秒高质量片段
- **BGM生成** - Tunee AI（5种风格）或本地快速生成
- **智能混音** - 4种预设，保留原声对白

## Tunee音乐风格

| 风格 | 用途 |
|------|------|
| epic | 游戏、运动、高燃 |
| chill | Vlog、生活 |
| electronic | 科技、现代 |
| cinematic | 宣传、预告 |
| sports | 体育、竞技 |

## 混音预设

| 预设 | BGM音量 | 用途 |
|------|---------|------|
| social | 50% | 社交媒体 |
| cinematic | 70% | 电影感 |
| vlog | 30% | 保留对白 |
| action | 80% | 高燃主导 |

## 参数

| 参数 | 默认 | 说明 |
|------|------|------|
| --duration | 30 | 时长（秒）|
| --preset | social | 混音预设 |
| --bgm-source | local | BGM来源 |
| --style | epic | Tunee风格 |

## 输出规格

- 时长: 可自定义（默认30秒）
- 视频: H.264 @ CRF 22
- 音频: AAC @ 192kbps

## 依赖

- FFmpeg（必需）
- Python 3.7+（可选）
- NumPy, requests（可选）

## Tunee API

```bash
# 检查积分
python scripts/tunee_music.py --api-key KEY --check-credits

# 列出模型
python scripts/tunee_music.py --api-key KEY --list-models

# 生成音乐
python scripts/tunee_music.py --api-key KEY --style epic --output bgm.mp3
```

## 版本

- **v2.1** - Tunee AI集成，5种风格
- **v2.0** - 进度反馈，4种预设
- **v1.0** - 初始版本