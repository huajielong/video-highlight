#!/usr/bin/env python3
"""
改进的音频混音工具 v2.0
增强功能：
- 更多混音模式
- 可调节参数
- 完善的错误处理
- 进度反馈
"""

import subprocess
import argparse
from pathlib import Path
from typing import Optional, Literal
import sys


class AudioMixer:
    """音频混音器"""

    # 预设配置
    PRESETS = {
        "social": {
            "bgm_volume": 0.5,
            "fade_duration": 2.0,
            "transition": 2.0,
            "description": "社交媒体标准（保留对白）"
        },
        "cinematic": {
            "bgm_volume": 0.7,
            "fade_duration": 3.0,
            "transition": 3.0,
            "description": "电影感（BGM较突出）"
        },
        "vlog": {
            "bgm_volume": 0.3,
            "fade_duration": 1.5,
            "transition": 1.0,
            "description": "Vlog（对白为主）"
        },
        "action": {
            "bgm_volume": 0.8,
            "fade_duration": 0.5,
            "transition": 1.0,
            "description": "高燃动作（BGM主导）"
        }
    }

    def __init__(self, video_file: str, bgm_file: str, output_file: str):
        self.video_file = Path(video_file)
        self.bgm_file = Path(bgm_file)
        self.output_file = Path(output_file)

        # 参数
        self.bgm_volume = 0.5
        self.fade_duration = 2.0
        self.transition_duration = 2.0
        self.mode: Literal["smooth", "sidechain", "simple"] = "smooth"

        # 验证文件
        self._validate_files()

    def _validate_files(self):
        """验证输入文件"""
        if not self.video_file.exists():
            raise FileNotFoundError(f"视频文件不存在: {self.video_file}")
        if not self.bgm_file.exists():
            raise FileNotFoundError(f"BGM文件不存在: {self.bgm_file}")

    def load_preset(self, preset_name: str):
        """加载预设配置"""
        if preset_name not in self.PRESETS:
            raise ValueError(f"未知预设: {preset_name}. 可用预设: {list(self.PRESETS.keys())}")

        preset = self.PRESETS[preset_name]
        self.bgm_volume = preset["bgm_volume"]
        self.fade_duration = preset["fade_duration"]
        self.transition_duration = preset["transition"]

        print(f"应用预设: {preset_name}")
        print(f"  {preset['description']}")

    def mix_smooth(self) -> bool:
        """平滑过渡混音"""
        print(f"使用平滑过渡模式...")
        print(f"  BGM音量: {self.bgm_volume*100:.0f}%")
        print(f"  淡入/淡出: {self.fade_duration}秒")

        filter_complex = (
            f"[1:a]volume={self.bgm_volume}[bgm];"
            f"[bgm]afade=t=in:st=0:d={self.fade_duration},"
            f"afade=t=out:st=28:d={self.fade_duration}[bgm_fade];"
            f"[0:a][bgm_fade]amix=inputs=2:duration=first:dropout_transition={self.transition_duration}"
        )

        return self._execute_ffmpeg(filter_complex)

    def mix_sidechain(self,
                      threshold: int = -20,
                      ratio: int = 4,
                      attack: int = 50,
                      release: int = 200) -> bool:
        """侧链压缩混音"""
        print(f"使用侧链压缩模式...")
        print(f"  阈值: {threshold}dB")
        print(f"  压缩比: {ratio}:1")
        print(f"  起音: {attack}ms, 释音: {release}ms")

        filter_complex = (
            f"[1:a]volume={self.bgm_volume}[bgm];"
            f"[bgm][0:a]sidechaincompress="
            f"threshold={threshold}dB:ratio={ratio}:"
            f"attack={attack}:release={release}[compressed];"
            f"[0:a][compressed]amix=inputs=2:weights=1 0.6"
        )

        return self._execute_ffmpeg(filter_complex)

    def mix_simple(self, original_volume: float = 1.0) -> bool:
        """简单音量混音"""
        print(f"使用简单混音模式...")
        print(f"  原声音量: {original_volume*100:.0f}%")
        print(f"  BGM音量: {self.bgm_volume*100:.0f}%")

        filter_complex = (
            f"[0:a]volume={original_volume}[orig];"
            f"[1:a]volume={self.bgm_volume}[bgm];"
            f"[orig][bgm]amix=inputs=2:weights=1 1"
        )

        return self._execute_ffmpeg(filter_complex)

    def _execute_ffmpeg(self, filter_complex: str) -> bool:
        """执行FFmpeg命令"""
        cmd = [
            'ffmpeg',
            '-i', str(self.video_file),
            '-i', str(self.bgm_file),
            '-filter_complex', filter_complex,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-y',
            str(self.output_file)
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )

            if self.output_file.exists():
                size_mb = self.output_file.stat().st_size / (1024 * 1024)
                print(f"✓ 混音完成: {self.output_file.name} ({size_mb:.1f}MB)")
                return True
            else:
                print("✗ 输出文件未生成", file=sys.stderr)
                return False

        except subprocess.CalledProcessError as e:
            print(f"✗ FFmpeg错误: {e.stderr}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"✗ 未知错误: {e}", file=sys.stderr)
            return False

    def mix(self, mode: Optional[str] = None, **kwargs) -> bool:
        """执行混音"""
        if mode is None:
            mode = self.mode

        if mode == "smooth":
            return self.mix_smooth()
        elif mode == "sidechain":
            return self.mix_sidechain(
                threshold=kwargs.get("threshold", -20),
                ratio=kwargs.get("ratio", 4),
                attack=kwargs.get("attack", 50),
                release=kwargs.get("release", 200)
            )
        elif mode == "simple":
            return self.mix_simple(kwargs.get("original_volume", 1.0))
        else:
            raise ValueError(f"未知混音模式: {mode}")


def main():
    parser = argparse.ArgumentParser(
        description="改进的音频混音工具 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
预设配置:
  social    - 社交媒体标准（保留对白，BGM 50%）
  cinematic - 电影感（BGM较突出，BGM 70%）
  vlog      - Vlog（对白为主，BGM 30%）
  action    - 高燃动作（BGM主导，BGM 80%）

混音模式:
  smooth    - 平滑过渡（推荐）
  sidechain - 侧链压缩（原声大时自动降低BGM）
  simple    - 简单音量混合

示例:
  # 使用预设
  python mix_audio_v2.py video.mp4 bgm.m4a output.mp4 --preset social

  # 自定义参数
  python mix_audio_v2.py video.mp4 bgm.m4a output.mp4 --mode smooth --bgm-volume 0.6

  # 使用侧链压缩
  python mix_audio_v2.py video.mp4 bgm.m4a output.mp4 --mode sidechain --threshold -25
        """
    )

    parser.add_argument("video", help="视频文件")
    parser.add_argument("bgm", help="BGM文件")
    parser.add_argument("output", help="输出文件")

    # 预设
    parser.add_argument("--preset", choices=list(AudioMixer.PRESETS.keys()),
                        help="使用预设配置")

    # 模式
    parser.add_argument("--mode", choices=["smooth", "sidechain", "simple"],
                        default="smooth", help="混音模式")

    # 参数
    parser.add_argument("--bgm-volume", type=float, default=0.5,
                        help="BGM音量 (0.0-1.0)")
    parser.add_argument("--fade-duration", type=float, default=2.0,
                        help="淡入淡出时长 (秒, smooth模式)")
    parser.add_argument("--transition", type=float, default=2.0,
                        help="过渡时长 (秒, smooth模式)")
    parser.add_argument("--threshold", type=int, default=-20,
                        help="压缩阈值 (dB, sidechain模式)")
    parser.add_argument("--ratio", type=int, default=4,
                        help="压缩比 (sidechain模式)")
    parser.add_argument("--attack", type=int, default=50,
                        help="起音时间 (ms, sidechain模式)")
    parser.add_argument("--release", type=int, default=200,
                        help="释音时间 (ms, sidechain模式)")

    args = parser.parse_args()

    # 创建混音器
    mixer = AudioMixer(args.video, args.bgm, args.output)

    # 应用预设
    if args.preset:
        mixer.load_preset(args.preset)
    else:
        # 应用命令行参数
        mixer.bgm_volume = args.bgm_volume
        mixer.fade_duration = args.fade_duration
        mixer.transition_duration = args.transition

    # 执行混音
    success = mixer.mix(args.mode, threshold=args.threshold, ratio=args.ratio,
                       attack=args.attack, release=args.release)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
