#!/usr/bin/env python3
"""
Agnes Video - 图生视频 / 多图视频 / 关键帧动画
================================================
输入一张或多张图片 + 文本提示词生成视频。

用法：
    python agnes_image_to_video.py "人物缓慢转身回望镜头" \
        --image https://example.com/portrait.png

    python agnes_image_to_video.py "平滑变换" \
        --image https://example.com/a.png \
        --image https://example.com/b.png

    python agnes_image_to_video.py "关键帧过渡" \
        --image kf1.png --image kf2.png --keyframes
"""

import argparse
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import agnes_common as ac  # noqa: E402
import agnes_video_common as vc  # noqa: E402


def _is_url(value):
    return isinstance(value, str) and value.startswith(("http://", "https://"))


def main():
    parser = argparse.ArgumentParser(
        description="🎬 Agnes Video - 图生视频（Image-to-Video / 多图 / 关键帧）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""示例：
  # 单图视频：传入图片 URL
  python %(prog)s "人物缓慢转身回望" --image https://example.com/portrait.png

  # 多图视频：传入多张图片 URL
  python %(prog)s "平滑变换" \
      --image https://example.com/a.png \
      --image https://example.com/b.png

  # 关键帧动画：传入多张图片并启用 --keyframes
  python %(prog)s "平滑过渡" \
      --image https://example.com/kf1.png \
      --image https://example.com/kf2.png \
      --keyframes

默认输出目录：{vc.OUTPUT_DIR_I2V}/
""")

    parser.add_argument("prompt", help="文本提示词")
    parser.add_argument("--image", "-i", action="append", required=True,
                        help="输入图片 URL（可重复），若 Agnes API 支持本地路径则可传本地文件")
    parser.add_argument("--output", "-o", help="输出视频路径")
    parser.add_argument("--key", "-k", help="API Key（或设置 AGNES_API_KEY 环境变量）")
    parser.add_argument("--model", default=vc.DEFAULT_VIDEO_MODEL,
                        help=f"模型名称（默认：{vc.DEFAULT_VIDEO_MODEL}）")
    parser.add_argument("--width", type=int, default=vc.DEFAULT_VIDEO_WIDTH,
                        help=f"视频宽度（默认：{vc.DEFAULT_VIDEO_WIDTH}）")
    parser.add_argument("--height", type=int, default=vc.DEFAULT_VIDEO_HEIGHT,
                        help=f"视频高度（默认：{vc.DEFAULT_VIDEO_HEIGHT}）")
    parser.add_argument("--num-frames", type=int, default=vc.DEFAULT_NUM_FRAMES,
                        help=f"总帧数，必须满足 8n+1 且 ≤ 441（默认：{vc.DEFAULT_NUM_FRAMES}）")
    parser.add_argument("--frame-rate", type=int, default=vc.DEFAULT_FRAME_RATE,
                        help=f"帧率 1-60（默认：{vc.DEFAULT_FRAME_RATE}）")

    parser.add_argument("--seed", type=int, default=None, help="随机种子（可选）")
    parser.add_argument("--num-inference-steps", type=int, default=None, help="推理步数（可选）")
    parser.add_argument("--negative-prompt", default=None, help="负面提示词（可选）")
    parser.add_argument("--keyframes", action="store_true",
                        help="启用关键帧动画模式（传入多张图片时使用）")

    parser.add_argument("--poll-interval", type=int, default=5, help="轮询间隔秒数（默认 5）")
    parser.add_argument("--max-wait", type=int, default=600, help="最长等待秒数（默认 600）")

    args = parser.parse_args()

    # 参数校验
    vc.validate_num_frames(args.num_frames)
    vc.validate_frame_rate(args.frame_rate)

    # 获取 API Key
    api_key = ac.get_api_key(args.key)

    # 处理图片：按规则，多图时走 extra_body.image，单图时顶层字段 image
    images = args.image
    for idx, url in enumerate(images, 1):
        if not _is_url(url):
            print(f"⚠️ 第 {idx} 个图片不是 http(s) URL ({url[:80]})")
            print("   Agnes Video API 需要公网可访问的图片 URL，请将图片上传到对象存储。")
            sys.exit(1)

    # 构造 payload
    if len(images) == 1 and not args.keyframes:
        payload = {
            "model": args.model,
            "prompt": args.prompt,
            "image": images[0],
            "num_frames": args.num_frames,
            "frame_rate": args.frame_rate,
            "width": args.width,
            "height": args.height,
        }
        mode_label = "图生视频（单图）"
    else:
        extra_body = {"image": images}
        if args.keyframes or len(images) > 1:
            if args.keyframes:
                extra_body["mode"] = "keyframes"
                mode_label = "关键帧动画"
            else:
                mode_label = "多图视频"
        payload = {
            "model": args.model,
            "prompt": args.prompt,
            "extra_body": extra_body,
            "num_frames": args.num_frames,
            "frame_rate": args.frame_rate,
            "width": args.width,
            "height": args.height,
        }

    # 可选参数
    for key, val in (("seed", args.seed),
                     ("num_inference_steps", args.num_inference_steps),
                     ("negative_prompt", args.negative_prompt)):
        if val is not None and val != "":
            payload[key] = val

    # 输出路径 + 任务摘要
    output_path = ac.make_output_path(args.output, vc.OUTPUT_DIR_I2V, file_suffix=".mp4")
    duration_secs = args.num_frames / args.frame_rate

    print(f"🎬 图生视频任务（{mode_label}）")
    print(f"   图片数量: {len(images)}")
    for i, url in enumerate(images, 1):
        print(f"     [{i}] {url if len(url) < 80 else url[:77] + '...'}")
    print(f"   提示词: {args.prompt[:80]}{'...' if len(args.prompt) > 80 else ''}")
    print(f"   预计时长: 约 {duration_secs:.2f} 秒 ({args.num_frames} 帧 / {args.frame_rate} fps)")
    print(f"   输出文件: {output_path}")
    print()

    vc.run_video_generation(
        api_key=api_key,
        payload=payload,
        output_path=output_path,
        poll_interval=args.poll_interval,
        max_wait_seconds=args.max_wait,
    )


if __name__ == "__main__":
    main()
