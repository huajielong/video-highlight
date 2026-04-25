#!/usr/bin/env python3
"""
改进的场景分析工具 v2.0
增强功能：
- 更多的分析维度
- 完善的错误处理
- 进度反馈
- 更智能的片段推荐
"""

import subprocess
import re
import argparse
import json
from pathlib import Path
from typing import List, Tuple, Dict, Optional
import sys
import time


class VideoAnalyzer:
    """视频分析器"""

    def __init__(self, video_file: str):
        self.video_file = Path(video_file)
        self.duration = 0.0
        self.scenes = []
        self.fps = 24.0
        self.resolution = (0, 0)

        # 验证文件
        self._validate_file()
        # 获取视频信息
        self._get_video_info()

    def _validate_file(self):
        """验证视频文件"""
        if not self.video_file.exists():
            raise FileNotFoundError(f"视频文件不存在: {self.video_file}")

        if self.video_file.suffix.lower() not in ['.mp4', '.mov', '.avi', '.mkv', '.flv']:
            print(f"警告: 不常见的视频格式 {self.video_file.suffix}")

    def _get_video_info(self):
        """获取视频信息"""
        try:
            # 时长
            result = subprocess.run([
                'ffprobe', '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                str(self.video_file)
            ], capture_output=True, text=True, check=True)

            self.duration = float(result.stdout.strip())

            # 分辨率
            result = subprocess.run([
                'ffprobe', '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height,r_frame_rate',
                '-of', 'csv=s=x:p=0',
                str(self.video_file)
            ], capture_output=True, text=True, check=True)

            parts = result.stdout.strip().split(',')
            if len(parts) >= 3:
                self.resolution = (int(parts[0]), int(parts[1]))
                fps_str = parts[2]
                if '/' in fps_str:
                    num, den = fps_str.split('/')
                    self.fps = float(num) / float(den)
                else:
                    self.fps = float(fps_str)

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"获取视频信息失败: {e.stderr}")
        except Exception as e:
            raise RuntimeError(f"解析视频信息失败: {e}")

    def detect_scenes(self, threshold: float = 0.4) -> List[float]:
        """检测场景变化"""
        print(f"正在分析场景变化 (阈值: {threshold})...")

        cmd = [
            'ffmpeg',
            '-i', str(self.video_file),
            '-vf', f"select='gt(scene,{threshold})',showinfo",
            '-vsync', 'vfr',
            '-f', 'null',
            '-'
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            timestamps = []

            for line in result.stderr.split('\n'):
                match = re.search(r"pts_time:(\d+\.\d+)", line)
                if match:
                    timestamps.append(float(match.group(1)))

            self.scenes = sorted(timestamps)
            print(f"✓ 检测到 {len(self.scenes)} 个场景变化")

            return self.scenes

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"场景检测失败: {e.stderr}")

    def find_best_segment(self, target_duration: float = 30,
                         min_scenes: int = 3) -> Tuple[float, float, int]:
        """找到最佳片段

        Args:
            target_duration: 目标时长（秒）
            min_scenes: 最小场景变化数

        Returns:
            (开始时间, 结束时间, 场景数量)
        """
        print(f"\n正在寻找最佳片段 (目标: {target_duration}秒)...")

        if not self.scenes:
            # 没有场景变化，返回中间片段
            start = max(0, (self.duration - target_duration) / 2)
            end = min(self.duration, start + target_duration)
            print("未检测到场景变化，返回中间片段")
            return (start, end, 0)

        # 滑动窗口分析
        best_start = 0
        best_end = target_duration
        best_count = 0
        best_score = 0

        window_size = target_duration
        step = 1.0  # 1秒步长

        for start in [i * step for i in range(int((self.duration - window_size) / step) + 1)]:
            end = start + window_size

            # 统计场景数
            count = sum(1 for t in self.scenes if start <= t <= end)

            # 计算分数（考虑位置和场景数）
            position_score = 1.0 - abs((start + end/2) - self.duration/2) / self.duration
            score = count * 2 + position_score

            if count >= min_scenes and score > best_score:
                best_score = score
                best_count = count
                best_start = start
                best_end = end

        # 如果没找到满足条件的，返回场景最多的
        if best_count == 0:
            best_start, best_end, best_count = self.find_most_active_segment(window_size)

        print(f"✓ 推荐片段: {best_start:.1f}s - {best_end:.1f}s")
        print(f"  包含 {best_count} 个场景变化")

        return (best_start, best_end, best_count)

    def find_most_active_segment(self, duration: float) -> Tuple[float, float, int]:
        """找到场景最活跃的片段"""
        best_start = 0
        best_count = 0

        for i, scene_time in enumerate(self.scenes):
            start = max(0, scene_time - duration / 2)
            end = min(self.duration, start + duration)

            count = sum(1 for t in self.scenes if start <= t <= end)

            if count > best_count:
                best_count = count
                best_start = start

        return (best_start, best_start + duration, best_count)

    def get_recommendations(self, target_duration: float = 30) -> Dict:
        """获取推荐信息"""
        return {
            "video_info": {
                "file": str(self.video_file),
                "duration": self.duration,
                "resolution": self.resolution,
                "fps": self.fps
            },
            "scene_analysis": {
                "total_scenes": len(self.scenes),
                "scenes_per_minute": len(self.scenes) / (self.duration / 60),
                "avg_interval": self.duration / (len(self.scenes) + 1) if self.scenes else 0
            },
            "recommendation": {
                "start": 0,
                "end": 0,
                "scene_count": 0,
                "duration": target_duration
            }
        }

    def print_summary(self):
        """打印分析摘要"""
        print("\n" + "="*50)
        print("视频分析摘要")
        print("="*50)
        print(f"文件: {self.video_file.name}")
        print(f"时长: {self.duration:.1f}秒 ({self.duration/60:.1f}分钟)")
        print(f"分辨率: {self.resolution[0]}x{self.resolution[1]}")
        print(f"帧率: {self.fps:.1f}fps")
        print(f"场景变化: {len(self.scenes)} 个")

        if self.scenes:
            avg_interval = self.duration / (len(self.scenes) + 1)
            print(f"平均间隔: {avg_interval:.1f}秒")

            # 显示前10个场景
            print(f"\n前10个场景变化:")
            for i, t in enumerate(self.scenes[:10]):
                print(f"  {i+1}. {t:.2f}s")

            if len(self.scenes) > 10:
                print(f"  ... 还有 {len(self.scenes)-10} 个")
        else:
            print("\n未检测到场景变化")


def main():
    parser = argparse.ArgumentParser(
        description="改进的场景分析工具 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本分析
  python analyze_scenes_v2.py video.mp4

  # 查找最佳片段
  python analyze_scenes_v2.py video.mp4 --find-best --duration 30

  # 调整检测阈值
  python analyze_scenes_v2.py video.mp4 --threshold 0.3

  # 输出JSON
  python analyze_scenes_v2.py video.mp4 --json
        """
    )

    parser.add_argument("video", help="视频文件")
    parser.add_argument("--threshold", type=float, default=0.4,
                        help="场景检测阈值 (0.0-1.0)")
    parser.add_argument("--duration", type=float, default=30,
                        help="目标片段时长 (秒)")
    parser.add_argument("--find-best", action="store_true",
                        help="查找最佳片段")
    parser.add_argument("--min-scenes", type=int, default=3,
                        help="最小场景变化数")
    parser.add_argument("--json", action="store_true",
                        help="输出JSON格式")
    parser.add_argument("--output", type=str,
                        help="保存分析结果到文件")

    args = parser.parse_args()

    try:
        analyzer = VideoAnalyzer(args.video)
        analyzer.detect_scenes(args.threshold)

        if args.find_best:
            start, end, count = analyzer.find_best_segment(
                args.duration, args.min-scenes
            )

            if args.json:
                result = analyzer.get_recommendations(args.duration)
                result["recommendation"] = {
                    "start": start,
                    "end": end,
                    "scene_count": count,
                    "duration": args.duration
                }
                print(json.dumps(result, indent=2))

                if args.output:
                    with open(args.output, 'w', encoding='utf-8') as f:
                        json.dump(result, f, indent=2, ensure_ascii=False)
            else:
                analyzer.print_summary()
                print(f"\n推荐剪辑: {start:.1f}s - {end:.1f}s")
                print(f"FFmpeg命令:")
                print(f"  ffmpeg -i {args.video} -ss {start} -to {end} highlight.mp4")

        else:
            if args.json:
                result = analyzer.get_recommendations()
                print(json.dumps(result, indent=2))

                if args.output:
                    with open(args.output, 'w', encoding='utf-8') as f:
                        json.dump(result, f, indent=2, ensure_ascii=False)
            else:
                analyzer.print_summary()

    except FileNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"未知错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
