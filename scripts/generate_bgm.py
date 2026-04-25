#!/usr/bin/env python3
"""
生成本地高燃背景音乐
无需API，快速生成带节奏点的BGM
"""

import numpy as np
import wave
import argparse


def generate_high_energy_bgm(output_file, duration=30, drop_times=None):
    """
    生成高燃背景音乐

    Args:
        output_file: 输出WAV文件路径
        duration: 时长（秒）
        drop_times: 音量增强时间点列表（秒），默认每5秒
    """
    if drop_times is None:
        drop_times = [5, 10, 15, 20, 25]

    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration))

    # 1. 底层低音（Kick drum）
    kick_pattern = np.zeros_like(t)
    for i in range(0, len(t), int(sample_rate * 0.5)):  # 每0.5秒
        if i + 200 < len(t):
            kick_freq = 60 * np.exp(-np.linspace(0, 1, 200))
            kick_wave = np.sin(2 * np.pi * kick_freq * np.arange(200) / sample_rate)
            kick_wave = kick_wave * np.exp(-np.linspace(0, 3, 200))
            kick_pattern[i:i+200] += kick_wave * 0.8

    # 2. 中频节奏（Synth bass）
    bass_freq = 80 + 40 * np.sin(2 * np.pi * 0.5 * t)
    bass_wave = np.sin(2 * np.pi * bass_freq * t) * 0.3

    # 3. 高频冲击（Hi-hats）
    hihat_pattern = np.zeros_like(t)
    for i in range(0, len(t), int(sample_rate * 0.25)):  # 每0.25秒
        if i + 100 < len(t):
            hihat_wave = np.random.normal(0, 0.1, 100)
            hihat_wave = hihat_wave * np.exp(-np.linspace(0, 5, 100))
            hihat_pattern[i:i+100] += hihat_wave

    # 4. 渐进增强的旋律
    melody_freq = 220 + 110 * np.sin(2 * np.pi * 0.33 * t)
    melody_wave = np.sin(2 * np.pi * melody_freq * t) * 0.15 * (t / duration)

    # 5. 添加Drops（节奏突变点）
    for drop_time in drop_times:
        drop_idx = int(drop_time * sample_rate)
        if drop_idx + sample_rate < len(t):
            bass_wave[drop_idx:drop_idx+sample_rate] *= 2
            melody_wave[drop_idx:drop_idx+sample_rate] *= 1.5

    # 合成
    audio = kick_pattern + bass_wave + hihat_pattern + melody_wave

    # 归一化
    audio = audio / np.max(np.abs(audio)) * 0.95

    # 保存为WAV
    with wave.open(output_file, 'w') as wav_file:
        wav_file.setnchannels(1)  # 单声道
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        audio_int16 = (audio * 32767).astype(np.int16)
        wav_file.writeframes(audio_int16.tobytes())

    print(f"Generated: {output_file}")
    print(f"Duration: {duration}s")
    print(f"Drop points: {drop_times}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate high-energy background music")
    parser.add_argument("output", help="Output WAV file path")
    parser.add_argument("--duration", type=int, default=30, help="Duration in seconds")
    parser.add_argument("--drops", nargs="+", type=float, default=[5, 10, 15, 20, 25],
                        help="Drop time points in seconds")

    args = parser.parse_args()
    generate_high_energy_bgm(args.output, args.duration, args.drops)
