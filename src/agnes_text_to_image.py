#!/usr/bin/env python3
"""
Agnes Image - 文生图（Text-to-Image）
==========================================
用文本提示词生成图片的 CLI 工具。

用法：
    python agnes_text_to_image.py "一只猫坐在月亮上"
    python agnes_text_to_image.py "prompt" --size 512x512 --quality hd --output my.png
    python agnes_text_to_image.py "prompt" --format b64
"""

import argparse
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import agnes_common as ac  # noqa: E402
import agnes_image_common as imgc  # noqa: E402


def main():
    parser = argparse.ArgumentParser(
        description="🎨 Agnes Image - 文生图（Text-to-Image）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""示例：
  # 基本使用
  python %(prog)s "A cat sitting on the moon"

  # 指定尺寸 / 质量
  python %(prog)s "prompt" --size 1024x1024 --quality hd

  # 指定输出
  python %(prog)s "prompt" --output custom/output.png

默认输出目录：{imgc.OUTPUT_DIR_T2I}/
""")

    parser.add_argument("prompt", help="文本提示词")
    parser.add_argument("--output", "-o", help="输出图片路径（默认使用时间戳命名）")
    parser.add_argument("--key", "-k", help="API Key（或设置 AGNES_API_KEY 环境变量）")
    parser.add_argument("--model", default=imgc.DEFAULT_IMAGE_MODEL,
                        help=f"模型名称（默认：{imgc.DEFAULT_IMAGE_MODEL}）")
    parser.add_argument("--size", "-s", default=imgc.DEFAULT_IMAGE_SIZE,
                        help=f"图片尺寸，例如 1024x1024 / 512x512（默认：{imgc.DEFAULT_IMAGE_SIZE}）")
    parser.add_argument("--quality", "-q", default=imgc.DEFAULT_IMAGE_QUALITY,
                        choices=["standard", "hd"],
                        help=f"生成质量（默认：{imgc.DEFAULT_IMAGE_QUALITY}）")
    parser.add_argument("--format", "-f", default="url", choices=["url", "b64"],
                        help="响应格式：url（默认）或 b64（base64）")

    args = parser.parse_args()

    api_key = ac.get_api_key(args.key)
    output_path = ac.make_output_path(args.output, imgc.OUTPUT_DIR_T2I, file_suffix=".png")
    response_format = args.format if args.format != "url" else None

    imgc.run_text_to_image(
        api_key=api_key,
        model=args.model,
        prompt=args.prompt,
        size=args.size,
        quality=args.quality,
        response_format=response_format,
        output_path=output_path,
    )


if __name__ == "__main__":
    main()
