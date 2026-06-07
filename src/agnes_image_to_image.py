#!/usr/bin/env python3
"""
Agnes Image - 图生图（Image-to-Image）
==========================================
传入一张图片与文本提示词，生成新图片。

用法：
    python agnes_image_to_image.py "让它变成日落风格" --image input.png
    python agnes_image_to_image.py "prompt" -i https://example.com/img.png --output out.png
"""

import argparse
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import agnes_common as ac  # noqa: E402
import agnes_image_common as imgc  # noqa: E402


def _is_url(value):
    return isinstance(value, str) and value.startswith(("http://", "https://"))


def main():
    parser = argparse.ArgumentParser(
        description="🎨 Agnes Image - 图生图（Image-to-Image）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""示例：
  # 传入本地图片（自动转为 base64 data URL）
  python %(prog)s "让它变成日落风格" --image input.png

  # 传入公开可访问的图片 URL
  python %(prog)s "prompt" --image https://example.com/img.png

  # 自定义输出路径
  python %(prog)s "prompt" --image input.png --output custom/output.png

默认输出目录：{imgc.OUTPUT_DIR_I2I}/
""")

    parser.add_argument("prompt", help="文本提示词")
    parser.add_argument("--image", "-i", required=True, help="输入图片：本地文件路径或公开 URL")
    parser.add_argument("--output", "-o", help="输出图片路径")
    parser.add_argument("--key", "-k", help="API Key（或设置 AGNES_API_KEY 环境变量）")
    parser.add_argument("--model", default=imgc.DEFAULT_IMAGE_MODEL,
                        help=f"模型名称（默认：{imgc.DEFAULT_IMAGE_MODEL}）")
    parser.add_argument("--size", "-s", default=imgc.DEFAULT_IMAGE_SIZE,
                        help=f"图片尺寸（默认：{imgc.DEFAULT_IMAGE_SIZE}）")
    parser.add_argument("--quality", "-q", default=imgc.DEFAULT_IMAGE_QUALITY,
                        choices=["standard", "hd"],
                        help=f"生成质量（默认：{imgc.DEFAULT_IMAGE_QUALITY}）")
    parser.add_argument("--format", "-f", default="url", choices=["url", "b64"],
                        help="响应格式：url（默认）或 b64（base64）")

    args = parser.parse_args()

    api_key = ac.get_api_key(args.key)
    output_path = ac.make_output_path(args.output, imgc.OUTPUT_DIR_I2I, file_suffix=".png")
    response_format = args.format if args.format != "url" else None

    # 处理 image 输入：本地文件 → base64；URL → 直接传入
    if _is_url(args.image):
        image_data = args.image
    else:
        image_data = imgc.encode_image_to_base64(args.image)

    imgc.run_image_to_image(
        api_key=api_key,
        model=args.model,
        prompt=args.prompt,
        image_data=image_data,
        size=args.size,
        quality=args.quality,
        response_format=response_format,
        output_path=output_path,
    )


if __name__ == "__main__":
    main()
