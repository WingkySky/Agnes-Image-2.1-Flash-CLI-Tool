#!/usr/bin/env python3
"""
Agnes Video - 文生视频（Text-to-Video）
===========================================
用文本提示词生成视频。

用法：
    python agnes_text_to_video.py "一位身穿飘逸长袍的年轻剑客"
    python agnes_text_to_video.py "prompt" --num-frames 241 --frame-rate 30 --output my.mp4
"""

import argparse
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import agnes_common as ac  # noqa: E402
import agnes_video_common as vc  # noqa: E402


def _add_optional_payload_args(p):
    """向 argparse 中添加视频可选高级参数。"""
    p.add_argument("--seed", type=int, default=None, help="随机种子（可选）")
    p.add_argument("--num-inference-steps", type=int, default=None, help="推理步数（可选）")
    p.add_argument("--negative-prompt", default=None, help="负面提示词（可选）")
    p.add_argument("--poll-interval", type=int, default=5, help="轮询间隔秒数（默认 5）")
    p.add_argument("--max-wait", type=int, default=600, help="最长等待秒数（默认 600）")


def main():
    parser = argparse.ArgumentParser(
        description="🎬 Agnes Video - 文生视频（Text-to-Video）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""示例：
  # 基本使用
  python %(prog)s "一位身穿飘逸长袍的年轻剑客在雨夜都市中穿行"

  # 调参控制时长
  python %(prog)s "prompt" --width 1152 --height 768 --num-frames 241 --frame-rate 30

  # 自定义输出
  python %(prog)s "prompt" --output custom/my.mp4

默认输出目录：{vc.OUTPUT_DIR_T2V}/
""")

    parser.add_argument("prompt", help="文本提示词")
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

    _add_optional_payload_args(parser)

    args = parser.parse_args()

    # 参数校验
    vc.validate_num_frames(args.num_frames)
    vc.validate_frame_rate(args.frame_rate)

    # 获取 API Key 和输出路径
    api_key = ac.get_api_key(args.key)
    output_path = ac.make_output_path(args.output, vc.OUTPUT_DIR_T2V, file_suffix=".mp4")

    # 构造 payload，可选字段仅在显式传入时添加
    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "width": args.width,
        "height": args.height,
        "num_frames": args.num_frames,
        "frame_rate": args.frame_rate,
    }
    for key, val in (("seed", args.seed),
                     ("num_inference_steps", args.num_inference_steps),
                     ("negative_prompt", args.negative_prompt)):
        if val is not None and val != "":
            payload[key] = val

    # 打印任务摘要
    duration_secs = args.num_frames / args.frame_rate
    print(f"🎬 文生视频任务")
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
