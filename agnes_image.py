#!/usr/bin/env python3
"""
Agnes Image 2.1 Flash API Client
=================================
A simple CLI tool for generating images using the Agnes Image 2.1 Flash model.

Usage:
    # Text-to-Image (output to output/image/text-to-image/)
    python agnes_image.py "a cat sitting on a moon, surreal art"

    # Image-to-Image (output to output/image/image-to-image/)
    python agnes_image.py "make it sunset style" --image input.jpg

    # Custom output path (overrides default directory)
    python agnes_image.py "a cat" --output custom/path/cat.png

API Key: Set AGNES_API_KEY env var, or provide via --key flag.
Docs: https://agnes-ai.com/doc/agnes-image-21-flash
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("Error: 'openai' package is required. Install with: pip install openai")
    sys.exit(1)

# ─── Configuration ───────────────────────────────────────────────

DEFAULT_BASE_URL = "https://apihub.agnes-ai.com/v1"
DEFAULT_MODEL = "agnes-image-2.1-flash"
DEFAULT_API_KEY_ENV = "AGNES_API_KEY"
PLATFORM_URL = "https://platform.agnes-ai.com"

# 输出目录配置
OUTPUT_BASE_DIR = "output/image"
OUTPUT_DIR_T2I = f"{OUTPUT_BASE_DIR}/text-to-image"  # 文生图输出目录
OUTPUT_DIR_I2I = f"{OUTPUT_BASE_DIR}/image-to-image"  # 图生图输出目录


def get_api_key(args):
    """Get API key from args, env var, or prompt."""
    if args.key:
        return args.key
    key = os.environ.get(DEFAULT_API_KEY_ENV)
    if key:
        return key
    print(f"Error: API key not found.")
    print(f"  1. Set env var: export {DEFAULT_API_KEY_ENV}='your-key'")
    print(f"  2. Use --key flag: python agnes_image.py 'prompt' --key your-key")
    print(f"  3. Get a key from: {PLATFORM_URL}")
    sys.exit(1)


def create_client(api_key, base_url=None):
    """Create OpenAI-compatible client."""
    return OpenAI(
        api_key=api_key,
        base_url=base_url or DEFAULT_BASE_URL,
        max_retries=2,
    )


def text_to_image(client, prompt, args):
    """Generate image from text prompt."""
    print(f"🎨 Generating image: '{prompt[:60]}...'")
    print(f"   Model: {args.model}")
    print(f"   Size: {args.size}")
    print(f"   Quality: {args.quality}")

    # 只有在用户明确指定时才添加 response_format
    extra_body = {}
    if args.format and args.format != "url":
        extra_body["response_format"] = args.format

    try:
        response = client.images.generate(
            model=args.model,
            prompt=prompt,
            size=args.size,
            quality=args.quality,
            n=1,
            **({"extra_body": extra_body} if extra_body else {}),
        )

        if response.data and len(response.data) > 0:
            img_data = response.data[0]
            handle_response(img_data, args, output_type="t2i")
        else:
            print("❌ No image data in response")
            sys.exit(1)

    except Exception as e:
        error_detail = str(e)
        print(f"❌ API Error: {error_detail}")
        # Try to extract detailed error
        if hasattr(e, 'body'):
            try:
                error_json = json.loads(e.body)
                print(f"   Details: {json.dumps(error_json, indent=2, ensure_ascii=False)}")
            except:
                pass
        sys.exit(1)


def image_to_image(client, prompt, image_path, args, api_key=None):
    """Generate modified image from existing image (image-to-image)."""
    img_path = Path(image_path)
    if not img_path.exists():
        print(f"❌ Image not found: {image_path}")
        sys.exit(1)

    # Read image as base64
    with open(img_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    ext = img_path.suffix.lstrip(".")
    mime_type = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "webp": "image/webp",
    }.get(ext, "image/png")

    print(f"🎨 Image-to-Image: '{prompt[:60]}...'")
    print(f"   Input: {image_path}")
    print(f"   Model: {args.model}")

    # 构建请求参数
    payload = {
        "model": args.model,
        "prompt": prompt,
        "image": f"data:{mime_type};base64,{img_b64}",
        "size": args.size,
        "quality": args.quality,
        "n": 1,
    }

    # 只有在用户明确指定时才添加 response_format
    if args.format and args.format != "url":
        payload["response_format"] = args.format

    try:
        # 使用 requests 直接调用 API，避免 OpenAI SDK 的参数限制
        import requests
        
        api_url = f"{DEFAULT_BASE_URL}/images/generations"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(api_url, headers=headers, json=payload, timeout=120)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("data") and len(data["data"]) > 0:
                img_data = data["data"][0]
                # 将 dict 转为对象以便与 handle_response 的通用逻辑兼容
                class ImgData:
                    def __init__(self, data):
                        self.url = data.get("url")
                        self.b64_json = data.get("b64_json")
                    def get(self, key, default=None):
                        return getattr(self, key, default)
                handle_response(ImgData(img_data), args, output_type="i2i")
            else:
                print("❌ No image data in response")
                sys.exit(1)
        else:
            print(f"❌ API Error: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            sys.exit(1)

    except Exception as e:
        print(f"❌ API Error: {e}")
        sys.exit(1)


def handle_response(img_data, args, output_type="t2i"):
    """Handle the image generation response.
    
    Args:
        img_data: API 返回的图像数据
        args: 命令行参数
        output_type: 输出类型，"t2i" 表示文生图，"i2i" 表示图生图
    """
    format_type = args.format or "url"

    # 根据类型确定输出目录
    if output_type == "i2i":
        default_dir = OUTPUT_DIR_I2I
    else:
        default_dir = OUTPUT_DIR_T2I

    # 生成默认文件名（使用时间戳）
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    default_filename = f"{output_type}_{timestamp}.png"

    # 确定最终输出路径：用户指定优先，否则使用默认目录 + 默认文件名
    if args.output:
        output = args.output
    else:
        output = f"{default_dir}/{default_filename}"
    
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if format_type == "b64_json":
        # Base64 response
        b64_data = getattr(img_data, 'b64_json', None) or img_data.get('b64_json', None)
        if b64_data:
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(b64_data))
            print(f"✅ Saved to: {output_path}")
        else:
            print("❌ No b64_json in response")
            print(f"   Response: {img_data}")
            sys.exit(1)
    else:
        # URL response (default)
        img_url = getattr(img_data, 'url', None) or img_data.get('url', None)
        if img_url:
            download_image(img_url, str(output_path))
        else:
            print("❌ No URL in response")
            print(f"   Response: {img_data}")
            sys.exit(1)


def download_image(url, output_path):
    """Download image from URL."""
    import urllib.request

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    # Try direct download first
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as response:
            data = response.read()
        with open(output, "wb") as f:
            f.write(data)
        print(f"✅ Saved to: {output}")
    except Exception as e:
        print(f"⚠️  Direct download failed ({e}), trying with requests...")
        try:
            import requests
            resp = requests.get(url, timeout=60, headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            with open(output, "wb") as f:
                f.write(resp.content)
            print(f"✅ Saved to: {output}")
        except Exception as e2:
            print(f"❌ Download failed: {e2}")
            print(f"   Please manually download from: {url}")
            print(f"   Output would be: {output}")


def main():
    parser = argparse.ArgumentParser(
        description="🎨 Agnes Image 2.1 Flash - AI Image Generation CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text to image (output to output/image/text-to-image/)
  python %(prog)s "a cat on the moon"

  # Image to image (output to output/image/image-to-image/)
  python %(prog)s "make it sunset" --image input.jpg

  # Custom output path (overrides default directory)
  python %(prog)s "a cat" --output custom/cat.png

  # Using API key flag
  python %(prog)s "futuristic city" --key sk-xxx

  # Custom model & size
  python %(prog)s "a forest" --model agnes-image-2.1-flash --size 1024x1024

Output Directories:
  Text-to-Image: output/image/text-to-image/
  Image-to-Image: output/image/image-to-image/

API Key: Set AGNES_API_KEY env var or use --key
Get API Key: https://platform.agnes-ai.com
Docs: https://agnes-ai.com/doc/agnes-image-21-flash
        """,
    )

    parser.add_argument("prompt", nargs="?", help="Text prompt for image generation")
    parser.add_argument("--image", "-i", help="Input image path for image-to-image")
    parser.add_argument("--output", "-o", help="Output file path (default: output.png)")
    parser.add_argument("--key", "-k", help="API key (or set AGNES_API_KEY env var)")
    parser.add_argument("--base-url", help=f"API base URL (default: {DEFAULT_BASE_URL})")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model name (default: {DEFAULT_MODEL})")
    parser.add_argument(
        "--size",
        "-s",
        default="1024x1024",
        help="Image size (default: 1024x1024, e.g., 1024x1024, 512x512)",
    )
    parser.add_argument(
        "--quality",
        "-q",
        default="standard",
        choices=["standard", "hd"],
        help="Image quality (default: standard)",
    )
    parser.add_argument(
        "--format",
        "-f",
        default="url",
        choices=["url", "b64"],
        help="Response format: url (default) or b64 (base64)",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--info", action="store_true", help="Show API info and exit")

    args = parser.parse_args()

    if args.info:
        show_info()
        return

    if not args.prompt and not args.image:
        parser.print_help()
        sys.exit(1)

    api_key = get_api_key(args)
    client = create_client(api_key, args.base_url)

    if args.image:
        image_to_image(client, args.prompt or "", args.image, args, api_key=api_key)
    else:
        text_to_image(client, args.prompt, args)


def show_info():
    """Display API information."""
    print("🎨 Agnes Image 2.1 Flash - API Information")
    print("=" * 50)
    print()
    print("Base URL:  ", DEFAULT_BASE_URL)
    print("Model:     ", DEFAULT_MODEL)
    print("Platform:  ", PLATFORM_URL)
    print("Docs:      ", "https://agnes-ai.com/doc/agnes-image-21-flash")
    print()
    print("Environment Variable:")
    print(f"  {DEFAULT_API_KEY_ENV}='your-api-key'")
    print()
    print("Supported Sizes:")
    print("  1024x1024, 512x512, 1024x512, 512x1024")
    print()
    print("Supported Quality:")
    print("  standard, hd")
    print()
    print("Response Format:")
    print("  url    - Returns image URL (default)")
    print("  b64    - Returns base64 encoded image")
    print()
    print("Output Directories:")
    print(f"  Text-to-Image:  {OUTPUT_DIR_T2I}/")
    print(f"  Image-to-Image: {OUTPUT_DIR_I2I}/")
    print()
    print("Endpoints:")
    print("  POST /v1/images/generations  (OpenAI-compatible)")


if __name__ == "__main__":
    main()
