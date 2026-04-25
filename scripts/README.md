# Video Highlight Scripts

这个目录包含用于高燃视频剪辑的辅助脚本。

## 脚本列表

### 1. `generate_bgm.py` - 生成本地BGM

快速生成高燃背景音乐，无需API。

```bash
python generate_bgm.py output.wav --duration 30 --drops 5 10 15 20 25
```

**参数**：
- `output.wav` - 输出文件
- `--duration 30` - 时长（秒），默认30秒
- `--drops 5 10 15 20 25` - 音量增强时间点

### 2. `analyze_scenes.py` - 分析场景变化

检测视频中的场景变化，找到最活跃的片段。

```bash
python analyze_scenes.py video.mp4 --duration 30
```

**参数**：
- `video.mp4` - 视频文件
- `--threshold 0.4` - 检测阈值（0.0-1.0）
- `--duration 30` - 目标片段时长
- `--json` - 输出JSON格式

### 3. `mix_audio.py` - 智能音频混音

将BGM与视频混合，保留原声对白。

```bash
python mix_audio.py video.mp4 bgm.m4a output.mp4 --mode smooth
```

**混音模式**：
- `smooth` - 平滑过渡（推荐）
- `sidechain` - 侧链压缩（原声大时自动降低BGM）
- `simple` - 简单音量混合

**参数**：
- `--bgm-volume 0.5` - BGM音量（0.0-1.0）
- `--fade-duration 2` - 淡入淡出时长（秒）

## 完整工作流示例

```bash
# 1. 分析视频，找到最佳片段
python analyze_scenes.py input.mp4 --duration 30

# 2. 剪辑视频（输出推荐：start 35s, end 65s）
ffmpeg -i input.mp4 -ss 35 -to 65 -c:v libx264 -preset fast -crf 22 highlight_30s.mp4

# 3. 生成BGM
python generate_bgm.py bgm.wav --duration 30

# 4. 混音
python mix_audio.py highlight_30s.mp4 bgm.wav final_video.mp4 --mode smooth
```

## 依赖

- Python 3.7+
- NumPy: `pip install numpy`
- FFmpeg

## 快速开始

```bash
pip install numpy
```

确保FFmpeg已安装并在PATH中。
