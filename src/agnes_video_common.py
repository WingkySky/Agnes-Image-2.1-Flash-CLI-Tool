#!/usr/bin/env python3
"""
Agnes Video V2.0 - 视频生成公共模块
===========================================
提供视频生成的专用逻辑：
  - POST /v1/videos  创建视频任务
  - GET  agnesapi?video_id=xxx  轮询结果（推荐）
  - GET  /v1/videos/{task_id}   轮询结果（兼容旧版）
  - 提取 video_url 并下载
  - num_frames / frame_rate 的专用校验
  - 文生视频 / 图生视频 的统一流程封装

依赖：agnes_common（提供统一的 HTTP / 下载 / 路径 / API Key）
"""

import sys
import time

import agnes_common as ac  # noqa: E402

# ─── 视频 API 配置 ───────────────────────────────────────────────────

CREATE_VIDEO_ENDPOINT = f"{ac.DEFAULT_BASE_URL}/videos"
QUERY_BY_VIDEO_ID_ENDPOINT = "https://apihub.agnes-ai.com/agnesapi"

# 兼容旧版（基于 task_id）
QUERY_BY_TASK_ID_TEMPLATE = f"{ac.DEFAULT_BASE_URL}/videos/{{task_id}}"

DEFAULT_VIDEO_MODEL = "agnes-video-v2.0"
DEFAULT_VIDEO_WIDTH = 1152
DEFAULT_VIDEO_HEIGHT = 768
DEFAULT_NUM_FRAMES = 121
DEFAULT_FRAME_RATE = 24

# 支持的 num_frames 列表（仅用于建议提示；实际规则是 8n+1 且 ≤ 441）
SUPPORTED_NUM_FRAMES = [81, 121, 161, 241, 441]

# 输出目录
OUTPUT_BASE_VIDEO = "output/video"
OUTPUT_DIR_T2V = f"{OUTPUT_BASE_VIDEO}/text-to-video"
OUTPUT_DIR_I2V = f"{OUTPUT_BASE_VIDEO}/image-to-video"


# ─── 视频参数专用校验 ─────────────────────────────────────────────

def validate_num_frames(num_frames):
    """校验 num_frames 是否满足 8n+1 且 ≤ 441。"""
    if num_frames < 1 or num_frames > 441:
        print(f"❌ num_frames ({num_frames}) 必须 ≤ 441 且 ≥ 1")
        sys.exit(1)
    if (num_frames - 1) % 8 != 0:
        suggestion = min(
            [n for n in SUPPORTED_NUM_FRAMES if n >= num_frames]
            or [SUPPORTED_NUM_FRAMES[-1]]
        )
        print(f"❌ num_frames ({num_frames}) 必须满足 8n+1 形式")
        print(f"   常用值: {SUPPORTED_NUM_FRAMES}")
        print(f"   最接近的较大值: {suggestion}")
        sys.exit(1)
    return num_frames


def validate_frame_rate(frame_rate):
    """校验 frame_rate 是否在 1-60 范围内。"""
    return ac.validate_in_range("frame_rate", frame_rate, 1, 60)


# ─── 创建视频任务 ─────────────────────────────────────────────────

def create_video_task(api_key, payload):
    """POST /v1/videos 创建视频生成任务。

    Returns:
        dict: 响应 JSON（至少包含 task_id / video_id）
    """
    print(f"🎬 创建视频任务 ...")
    print(f"   模型: {payload.get('model')}  分辨率: {payload.get('width')}x{payload.get('height')}  "
          f"帧数/帧率: {payload.get('num_frames')}/{payload.get('frame_rate')}")

    data = ac.http_post_json(api_key, CREATE_VIDEO_ENDPOINT, payload, timeout=120)
    task_id = data.get("task_id") or data.get("id")
    video_id = data.get("video_id")
    print(f"✅ 任务已创建")
    print(f"   task_id:  {task_id}")
    print(f"   video_id: {video_id}")
    return data


# ─── 轮询视频结果 ─────────────────────────────────────────────────

def poll_video_result(api_key, video_id=None, task_id=None, model_name=None,
                      poll_interval=5, max_wait_seconds=600):
    """轮询直到任务完成，返回最终 JSON。"""
    if video_id:
        url, params = QUERY_BY_VIDEO_ID_ENDPOINT, {"video_id": video_id}
        if model_name:
            params["model_name"] = model_name
    elif task_id:
        url, params = QUERY_BY_TASK_ID_TEMPLATE.format(task_id=task_id), None
    else:
        print("❌ 需要提供 video_id 或 task_id 中的一个")
        sys.exit(1)

    print(f"\n⏳ 轮询视频结果（间隔 {poll_interval}s，最长 {max_wait_seconds}s）...")
    start = time.time()
    last_status = None
    while True:
        elapsed = int(time.time() - start)
        if elapsed > max_wait_seconds:
            print(f"❌ 等待超时（> {max_wait_seconds}s），请稍后手动查询")
            sys.exit(1)

        data = ac.http_get_json(api_key, url, params=params, timeout=60)
        if not data:
            time.sleep(poll_interval)
            continue

        status = data.get("status", "unknown")
        progress = data.get("progress", 0)

        if status != last_status:
            last_status = status
            print(f"   [{elapsed:>4}s] status={status:<11} progress={progress}%")
        else:
            print(f"   [{elapsed:>4}s] status={status:<11} progress={progress}%", end="\r")

        if status == "completed":
            print()
            print(f"✅ 视频生成完成")
            return data
        if status == "failed":
            print()
            print(f"❌ 视频生成失败")
            err = data.get("error") or data.get("error_message") or "未知错误"
            print(f"   Error: {err}")
            sys.exit(1)

        time.sleep(poll_interval)


# ─── 提取 video URL ───────────────────────────────────────────────

def extract_video_url(result_data):
    """从响应中按优先级提取视频 URL。"""
    for key in ("video_url", "remixed_from_video_id", "url"):
        val = result_data.get(key) if isinstance(result_data, dict) else getattr(
            result_data, key, None)
        if val and isinstance(val, str) and val.startswith("http"):
            return val
    print(f"❌ 响应中未找到可访问的视频 URL")
    print(f"   响应: {result_data}")
    sys.exit(1)


# ─── 统一流程入口 ───────────────────────────────────────────────────

def run_video_generation(api_key, payload, output_path, poll_interval=5, max_wait_seconds=600):
    """创建任务 → 轮询 → 下载。"""
    created = create_video_task(api_key, payload)
    video_id = created.get("video_id")
    task_id = created.get("task_id") or created.get("id")

    result = poll_video_result(
        api_key,
        video_id=video_id,
        task_id=task_id,
        model_name=payload.get("model"),
        poll_interval=poll_interval,
        max_wait_seconds=max_wait_seconds,
    )

    video_url = extract_video_url(result)
    ac.download_file(video_url, output_path, label="视频")
    return result
