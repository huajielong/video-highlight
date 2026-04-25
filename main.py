#!/usr/bin/env python3
"""
Video Highlight主工作流脚本 v2.1
一键完成：分析→剪辑→BGM→混音
支持Tunee AI和本地BGM生成
"""

import subprocess
import argparse
import sys
from pathlib import Path
from typing import Optional, Literal
import json
import shutil


class VideoHighlightProcessor:
    """高燃视频处理器"""

    def __init__(self, video_file: str, output_dir: str = "."):
        self.video_file = Path(video_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # 文件路径
        self.highlight_file = None
        self.bgm_file = None
        self.final_file = None

        # 参数
        self.duration = 30
        self.threshold = 0.4
        self.min_scenes = 3
        self.bgm_source: Literal["local", "tunee"] = "local"
        self.mix_preset = "social"
        self.api_key: Optional[str] = None
        self.music_style = "epic"  # Tunee音乐风格

        # 结果
        self.analysis_result = {}

        # 验证视频文件
        self._validate_video()

    def _validate_video(self):
        """验证视频文件"""
        if not self.video_file.exists():
            raise FileNotFoundError(f"视频文件不存在: {self.video_file}")

        # 检查FFmpeg
        try:
            subprocess.run(['ffmpeg', '-version'],
                          capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError("FFmpeg未安装或不在PATH中")

    def analyze(self) -> dict:
        """分析视频"""
        print(f"\n{'='*50}")
        print(f"分析视频: {self.video_file.name}")
        print(f"{'='*50}")

        cmd = [
            'python', 'scripts/analyze_scenes_v2.py',
            str(self.video_file),
            '--find-best',
            '--duration', str(self.duration),
            '--min-scenes', str(self.min_scenes),
            '--json'
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self.analysis_result = json.loads(result.stdout)
            return self.analysis_result

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"视频分析失败: {e.stderr}")
        except json.JSONDecodeError:
            raise RuntimeError(f"分析结果解析失败: {result.stdout}")

    def extract_clip(self, start: float, end: float) -> Path:
        """提取片段"""
        print(f"\n{'='*50}")
        print(f"提取片段: {start:.1f}s - {end:.1f}s")
        print(f"{'='*50}")

        output_name = f"{self.video_file.stem}_highlight_{self.duration}s.mp4"
        self.highlight_file = self.output_dir / output_name

        cmd = [
            'ffmpeg',
            '-i', str(self.video_file),
            '-ss', str(start),
            '-to', str(end),
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '22',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-y',
            str(self.highlight_file)
        ]

        try:
            subprocess.run(cmd, capture_output=True, check=True)
            size_mb = self.highlight_file.stat().st_size / (1024 * 1024)
            print(f"✓ 片段提取完成: {self.highlight_file.name} ({size_mb:.1f}MB)")
            return self.highlight_file

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"片段提取失败: {e.stderr}")

    def generate_bgm(self) -> Path:
        """生成BGM"""
        print(f"\n{'='*50}")
        print(f"生成背景音乐 (源: {self.bgm_source})")
        print(f"{'='*50}")

        if self.bgm_source == "local":
            return self._generate_local_bgm()
        elif self.bgm_source == "tunee":
            return self._generate_tunee_bgm()
        else:
            raise ValueError(f"未知的BGM源: {self.bgm_source}")

    def _generate_local_bgm(self) -> Path:
        """生成本地BGM"""
        output_name = f"{self.video_file.stem}_bgm_{self.duration}s.wav"
        self.bgm_file = self.output_dir / output_name

        cmd = [
            'python', 'scripts/generate_bgm.py',
            str(self.bgm_file),
            '--duration', str(self.duration)
        ]

        try:
            subprocess.run(cmd, capture_output=True, check=True)
            size_kb = self.bgm_file.stat().st_size / 1024
            print(f"✓ 本地BGM生成完成: {self.bgm_file.name} ({size_kb:.1f}KB)")
            return self.bgm_file

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"BGM生成失败: {e.stderr}")

    def _generate_tunee_bgm(self) -> Path:
        """使用Tunee AI生成BGM"""
        # 检查tunee_music.py脚本
        tunee_script = Path("scripts/tunee_music.py")
        if not tunee_script.exists():
            raise RuntimeError("tunee_music.py脚本不存在")

        output_name = f"{self.video_file.stem}_bgm_{self.duration}s.mp3"
        self.bgm_file = self.output_dir / output_name

        # 构建命令
        cmd = ['python', str(tunee_script)]

        if self.api_key:
            cmd.extend(['--api-key', self.api_key])

        cmd.extend([
            '--style', self.music_style,
            '--output', str(self.bgm_file)
        ])

        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            size_mb = self.bgm_file.stat().st_size / (1024 * 1024)
            print(f"✓ Tunee AI BGM生成完成: {self.bgm_file.name} ({size_mb:.1f}MB)")
            return self.bgm_file

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr or e.stdout or str(e)
            raise RuntimeError(f"Tunee AI BGM生成失败: {error_msg}")
        except Exception as e:
            raise RuntimeError(f"Tunee AI BGM生成失败: {str(e)}")

    def mix_audio(self) -> Path:
        """混音"""
        print(f"\n{'='*50}")
        print(f"智能混音 (预设: {self.mix_preset})")
        print(f"{'='*50}")

        output_name = f"{self.video_file.stem}_final.mp4"
        self.final_file = self.output_dir / output_name

        # 检查混音脚本
        mix_script = Path("scripts/mix_audio_v2.py")
        if mix_script.exists():
            # 使用v2脚本
            cmd = [
                'python', str(mix_script),
                str(self.highlight_file),
                str(self.bgm_file),
                str(self.final_file),
                '--preset', self.mix_preset
            ]
        else:
            # 使用v1脚本作为后备
            cmd = [
                'ffmpeg',
                '-i', str(self.highlight_file),
                '-i', str(self.bgm_file),
                '-filter_complex',
                '[1:a]volume=0.5[bgm];[0:a][bgm]amix=inputs=2:weights=1 0.5',
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-y',
                str(self.final_file)
            ]

        try:
            subprocess.run(cmd, capture_output=True, check=True)
            size_mb = self.final_file.stat().st_size / (1024 * 1024)
            print(f"✓ 混音完成: {self.final_file.name} ({size_mb:.1f}MB)")
            return self.final_file

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"混音失败: {e.stderr}")

    def process(self) -> dict:
        """执行完整流程"""
        print(f"\n{'='*60}")
        print(f"Video Highlight v2.1")
        print(f"{'='*60}")
        print(f"输入视频: {self.video_file}")
        print(f"输出目录: {self.output_dir}")
        print(f"目标时长: {self.duration}秒")
        print(f"BGM来源: {self.bgm_source}")
        if self.bgm_source == "tunee":
            print(f"音乐风格: {self.music_style}")
        print(f"{'='*60}")

        try:
            # 1. 分析
            analysis = self.analyze()
            rec = analysis.get("recommendation", {})
            start = rec.get("start", 0)
            end = rec.get("end", self.duration)

            # 2. 提取片段
            self.extract_clip(start, end)

            # 3. 生成BGM
            self.generate_bgm()

            # 4. 混音
            self.mix_audio()

            # 输出结果摘要
            print(f"\n{'='*60}")
            print(f"处理完成！")
            print(f"{'='*60}")
            print(f"\n输出文件:")
            if self.highlight_file:
                print(f"  1. {self.highlight_file}")
            if self.bgm_file:
                print(f"  2. {self.bgm_file}")
            if self.final_file:
                print(f"  3. {self.final_file} ← 最终版本")

            print(f"\n推荐使用: {self.final_file}")
            print(f"{'='*60}")

            return {
                "success": True,
                "files": {
                    "highlight": str(self.highlight_file) if self.highlight_file else None,
                    "bgm": str(self.bgm_file) if self.bgm_file else None,
                    "final": str(self.final_file) if self.final_file else None
                },
                "analysis": analysis
            }

        except Exception as e:
            print(f"\n✗ 处理失败: {e}", file=sys.stderr)
            return {
                "success": False,
                "error": str(e)
            }

    def set_params(self, **kwargs):
        """设置参数"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


def main():
    parser = argparse.ArgumentParser(
        description="Video Highlight v2.1 - 一键剪辑高燃视频片段",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础用法（本地BGM）
  python main.py video.mp4

  # 使用Tunee AI生成BGM
  python main.py video.mp4 --bgm-source tunee --api-key YOUR_KEY

  # 自定义Tunee音乐风格
  python main.py video.mp4 --bgm-source tunee --style cinematic

  # 完整自定义
  python main.py video.mp4 \
    --duration 60 \
    --bgm-source tunee \
    --style epic \
    --preset action \
    --api-key YOUR_KEY \
    --output ./output

  # 只分析不处理
  python main.py video.mp4 --analyze-only

BGM来源:
  local   - 本地快速生成（无需API，质量⭐⭐⭐）
  tunee   - Tunee AI生成（需API Key，质量⭐⭐⭐⭐⭐）

混音预设:
  social    - 社交媒体标准（保留对白）
  cinematic - 电影感（BGM突出）
  vlog      - Vlog（对白为主）
  action    - 高燃动作（BGM主导）

Tunee音乐风格:
  epic       - 高燃动作，电影感
  chill      - 轻松氛围，lo-fi
  electronic - 电子音乐，能量感
  cinematic  - 电影配乐，戏剧化
  sports     - 体育运动，激昂
        """
    )

    parser.add_argument("video", help="视频文件")
    parser.add_argument("--output", "-o", default=".",
                        help="输出目录 (默认: 当前目录)")
    parser.add_argument("--duration", "-d", type=int, default=30,
                        help="目标时长 (秒, 默认: 30)")
    parser.add_argument("--threshold", "-t", type=float, default=0.4,
                        help="场景检测阈值 (默认: 0.4)")
    parser.add_argument("--min-scenes", "-m", type=int, default=3,
                        help="最小场景变化数 (默认: 3)")
    parser.add_argument("--bgm-source", choices=["local", "tunee"],
                        default="local", help="BGM来源 (默认: local)")
    parser.add_argument("--style", "-s", choices=["epic", "chill", "electronic", "cinematic", "sports"],
                        default="epic", help="Tunee音乐风格 (默认: epic)")
    parser.add_argument("--api-key", help="Tunee API Key")
    parser.add_argument("--preset", "-p", choices=["social", "cinematic", "vlog", "action"],
                        default="social", help="混音预设")
    parser.add_argument("--analyze-only", action="store_true",
                        help="只分析，不处理")

    args = parser.parse_args()

    try:
        processor = VideoHighlightProcessor(args.video, args.output)
        processor.set_params(
            duration=args.duration,
            threshold=args.threshold,
            min_scenes=args.min_scenes,
            bgm_source=args.bgm_source,
            api_key=args.api_key,
            music_style=args.style,
            mix_preset=args.preset
        )

        if args.analyze_only:
            # 只分析
            result = processor.analyze()
            print(f"\n分析结果:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            # 完整处理
            result = processor.process()

            # 保存结果
            result_file = processor.output_dir / "result.json"
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"\n结果已保存: {result_file}")

        sys.exit(0 if result.get("success") else 1)

    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
