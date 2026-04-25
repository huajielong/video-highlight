#!/usr/bin/env python3
"""
Tunee AI Music Generation for video-highlight skill
Adapted from free-music-generator
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Literal

from utils.tunee_api import (
    API_GENERATE,
    check_credits,
    format_tunee_error,
    fetch_models,
    parse_tunee_error,
    request_tunee_api,
    resolve_access_key,
    TuneeAPIError,
    TuneeResponse,
)


# 预设的音乐风格
MUSIC_PRESETS = {
    "epic": {
        "prompt": "High-energy epic action music with strong rhythmic beats, intense drops every 5 seconds, powerful bass, cinematic orchestral elements, perfect for video highlight editing",
        "title": "Epic Action",
        "model": "tempolor_v4.5"
    },
    "chill": {
        "prompt": "Relaxing lo-fi background music, smooth beats, ambient pads, gentle melodies, perfect for vlog and lifestyle videos",
        "title": "Chill Vibes",
        "model": "tempolor_v4.5"
    },
    "electronic": {
        "prompt": "Upbeat electronic music, synthwave vibes, driving beat, energetic drops, modern production, perfect for gaming and sports",
        "title": "Electronic Energy",
        "model": "tempolor_v4.5"
    },
    "cinematic": {
        "prompt": "Epic cinematic orchestral music, dramatic strings, powerful brass section, building tension, emotional crescendo, perfect for trailers and highlights",
        "title": "Cinematic Epic",
        "model": "lyria_3"
    },
    "sports": {
        "prompt": "High-energy sports music, driving rock beats, electric guitar riffs, powerful drums, motivating anthem style, perfect for sports highlights",
        "title": "Sports Champion",
        "model": "mureka_v9"
    }
}


def get_audio_url_from_response(data: dict) -> str | None:
    """Extract audio URL from Tunee API response."""
    item_list = data.get("itemList")
    if not item_list or not isinstance(item_list, list):
        return None

    for item in item_list:
        if isinstance(item, dict):
            # 检查各种可能的音频URL字段
            for url_key in ["audioUrl", "audio_url", "url", "shareUrl"]:
                url = item.get(url_key)
                if url and isinstance(url, str):
                    return url

            # 检查嵌套的media对象
            media = item.get("media")
            if media and isinstance(media, dict):
                for url_key in ["audioUrl", "audio_url", "url"]:
                    url = media.get(url_key)
                    if url and isinstance(url, str):
                        return url

    return None


def generate_music(
    api_key: str,
    style: str = "epic",
    duration: int = 30,
    custom_prompt: str | None = None,
    custom_title: str | None = None,
    model: str | None = None
) -> dict:
    """
    Generate music using Tunee AI

    Args:
        api_key: Tunee API key
        style: Music style preset (epic, chill, electronic, cinematic, sports)
        duration: Target duration in seconds
        custom_prompt: Custom prompt (overrides style)
        custom_title: Custom title (overrides style)
        model: Specific model to use

    Returns:
        dict with keys: success, url, title, item_id, error
    """
    try:
        # 使用预设或自定义
        if custom_prompt:
            prompt = custom_prompt
            title = custom_title or "Custom Track"
            if not model:
                model = "tempolor_v4.5"
        else:
            preset = MUSIC_PRESETS.get(style, MUSIC_PRESETS["epic"])
            prompt = preset["prompt"]
            title = preset["title"]
            model = model or preset["model"]

        # 构建请求
        payload = {
            "prompt": "",
            "style": prompt,
            "title": title,
            "instrumental": True,
            "lyric": "",
            "action": "generate",
            "model": model,
            "modelKey": model,
            "callback_url": "https://example.com/callback",
            "source": "tunee",
            "custom": True,
            "needCover": True,
            "coverPrompt": title,
        }

        print(f"正在生成音乐...")
        print(f"  风格: {style}")
        print(f"  模型: {model}")
        print(f"  标题: {title}")

        # 发送请求
        resp = request_tunee_api(API_GENERATE, api_key, payload, timeout=120)

        # 提取音频URL
        audio_url = get_audio_url_from_response(resp.data)

        if audio_url:
            # 提取item_id
            item_id = None
            item_list = resp.data.get("itemList", [])
            if item_list and isinstance(item_list, list) and len(item_list) > 0:
                item_id = item_list[0].get("itemId") or item_list[0].get("item_id")

            return {
                "success": True,
                "url": audio_url,
                "title": title,
                "item_id": item_id,
                "share_url": f"https://www.tunee.ai/music/{item_id}" if item_id else None
            }
        else:
            return {
                "success": False,
                "error": "无法从响应中提取音频URL",
                "response": resp.raw
            }

    except TuneeAPIError as e:
        return {
            "success": False,
            "error": format_tunee_error(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"生成失败: {str(e)}"
        }


def download_audio(url: str, output_file: str) -> bool:
    """
    Download audio from Tunee URL

    Args:
        url: Audio URL
        output_file: Output file path

    Returns:
        bool: Success status
    """
    try:
        import requests

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        print(f"正在下载音乐...")
        print(f"  URL: {url[:80]}...")

        resp = requests.get(url, headers=headers, timeout=60, stream=True)
        resp.raise_for_status()

        # 保存文件
        with open(output_file, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)

        size_mb = Path(output_file).stat().st_size / (1024 * 1024)
        print(f"✓ 下载完成: {output_file.name} ({size_mb:.1f}MB)")

        return True

    except Exception as e:
        print(f"✗ 下载失败: {e}", file=sys.stderr)
        return False


def generate_and_download(
    api_key: str,
    output_file: str,
    style: str = "epic",
    duration: int = 30,
    custom_prompt: str | None = None,
    custom_title: str | None = None,
    model: str | None = None
) -> dict:
    """
    Generate and download music in one step

    Returns:
        dict with generation and download results
    """
    # 生成音乐
    result = generate_music(
        api_key=api_key,
        style=style,
        duration=duration,
        custom_prompt=custom_prompt,
        custom_title=custom_title,
        model=model
    )

    if not result.get("success"):
        return result

    # 下载音频
    audio_url = result["url"]
    success = download_audio(audio_url, output_file)

    return {
        "success": success,
        "file": output_file if success else None,
        "title": result.get("title"),
        "share_url": result.get("share_url"),
        "item_id": result.get("item_id")
    }


def list_models(api_key: str) -> list[dict]:
    """
    List available Tunee models

    Returns:
        List of model info dicts
    """
    try:
        resp = fetch_models(api_key)
        models = resp.get("models", [])

        result = []
        for m in models:
            caps = m.get("capabilities", [])
            instrumental_caps = [c for c in caps if c.get("music_type") == "Instrumental"]

            if instrumental_caps:
                for cap in instrumental_caps:
                    result.append({
                        "id": m.get("id"),
                        "name": m.get("name"),
                        "description": cap.get("description"),
                        "credits": cap.get("creditsShow"),
                    })

        return result

    except TuneeAPIError as e:
        print(f"获取模型列表失败: {format_tunee_error(e)}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"获取模型列表失败: {e}", file=sys.stderr)
        return []


def check_api_status(api_key: str) -> dict:
    """
    Check API key status and remaining credits

    Returns:
        dict with credits info
    """
    try:
        credits_data = check_credits(api_key)

        return {
            "success": True,
            "credits": credits_data.get("credits", 0),
            "raw": credits_data
        }

    except TuneeAPIError as e:
        return {
            "success": False,
            "error": format_tunee_error(e)
        }


def main():
    parser = argparse.ArgumentParser(
        description="Tunee AI Music Generation for video-highlight",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
音乐风格预设:
  epic       - 高燃动作，电影感
  chill      - 轻松氛围，lo-fi
  electronic - 电子音乐，能量感
  cinematic  - 电影配乐，戏剧化
  sports     - 体育运动，激昂

示例:
  # 使用预设生成
  python tunee_music.py --api-key YOUR_KEY --style epic --output bgm.mp3

  # 自定义生成
  python tunee_music.py --api-key YOUR_KEY --prompt "epic action music" --title "My Track" --output bgm.mp3

  # 检查积分
  python tunee_music.py --api-key YOUR_KEY --check-credits

  # 列出模型
  python tunee_music.py --api-key YOUR_KEY --list-models
        """
    )

    parser.add_argument("--api-key", help="Tunee API Key (或设置TUNEE_API_KEY环境变量)")
    parser.add_argument("--style", choices=list(MUSIC_PRESETS.keys()),
                        default="epic", help="音乐风格预设")
    parser.add_argument("--prompt", help="自定义音乐描述（覆盖style）")
    parser.add_argument("--title", help="自定义标题（覆盖style）")
    parser.add_argument("--model", help="指定模型ID")
    parser.add_argument("--duration", type=int, default=30, help="目标时长（秒）")
    parser.add_argument("--output", "-o", help="输出音频文件路径")
    parser.add_argument("--list-models", action="store_true", help="列出可用模型")
    parser.add_argument("--check-credits", action="store_true", help="检查剩余积分")

    args = parser.parse_args()

    try:
        # 解析API Key
        api_key = resolve_access_key(args.api_key)

        # 检查积分
        if args.check_credits:
            status = check_api_status(api_key)
            if status["success"]:
                print(f"剩余积分: {status['credits']}")
            else:
                print(f"错误: {status['error']}", file=sys.stderr)
            sys.exit(0 if status["success"] else 1)

        # 列出模型
        if args.list_models:
            models = list_models(api_key)
            if models:
                print("可用模型:")
                for m in models:
                    print(f"  {m['id']} - {m['name']} ({m['credits']}积分)")
                    print(f"    {m['description']}")
            sys.exit(0 if models else 1)

        # 生成和下载音乐
        if not args.output:
            output_file = "tunee_bgm.mp3"
        else:
            output_file = args.output

        result = generate_and_download(
            api_key=api_key,
            output_file=output_file,
            style=args.style,
            duration=args.duration,
            custom_prompt=args.prompt,
            custom_title=args.title,
            model=args.model
        )

        if result["success"]:
            print(f"\n✓ 完成！")
            print(f"  文件: {result['file']}")
            print(f"  标题: {result['title']}")
            if result.get("share_url"):
                print(f"  在线: {result['share_url']}")
            sys.exit(0)
        else:
            print(f"\n✗ 失败: {result.get('error', '未知错误')}", file=sys.stderr)
            sys.exit(1)

    except ValueError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"未知错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
