<div align="right">

  [English](README.md) · [**中文**](README_zh.md)

</div>

# 🎨 Agnes Media Create 媒体生成工具

**Skill 名称**: `agnes-media-create`

一个使用 **Agnes Image 2.1 Flash** 和 **Agnes Video V2.0** API 的模块化命令行工具包，用于生成媒体内容。支持文生图、图生图、文生视频以及图生视频（包括多图和关键帧动画模式）。

**整个文件夹作为一个独立的 Skill 被智能体调用。**

## 项目结构（Skill 标准结构）

```
Skill 根目录/（整个文件夹作为 Skill 被调用）
├── SKILL.md                      # Skill 定义文件（frontmatter + 使用说明）
├── README.md                     # 项目文档（英文）
├── README_zh.md                  # 项目文档（中文）— 本文件
├── requirements.txt              # Python 依赖
├── .env.example                  # 环境变量示例
├── .env                          # 可选：本地 API Key 配置文件（无需 export 自动加载）
├── src/
│   ├── agnes_common.py           # 通用模块（.env 加载 / HTTP 请求 / 文件下载 / 路径管理）
│   ├── agnes_image_common.py     # 图片 API 封装
│   ├── agnes_video_common.py     # 视频 API 封装（异步任务 + 轮询）
│   ├── agnes_text_to_image.py    # 文生图独立脚本
│   ├── agnes_image_to_image.py   # 图生图独立脚本
│   ├── agnes_text_to_video.py    # 文生视频独立脚本
│   └── agnes_image_to_video.py   # 图生视频独立脚本（支持多图/关键帧）
└── output/
    ├── image/text-to-image/      # 文生图输出目录
    ├── image/image-to-image/     # 图生图输出目录
    ├── video/text-to-video/      # 文生视频输出目录
    └── video/image-to-video/     # 图生视频输出目录
```

## Skill 工作原理

1. 智能体读取 `SKILL.md` 中的 frontmatter（`name`、`description`）来识别此 Skill
2. 根据 `SKILL.md` 中的使用说明，调用对应的独立脚本进行内容生成
3. 项目采用三层模块化设计：通用工具 → API 封装 → CLI 脚本

## 功能特性

### 当前支持
- **文生图（Text-to-Image）**：根据文本描述生成图片
- **图生图（Image-to-Image）**：根据输入图片和文本提示词修改现有图片
- **文生视频（Text-to-Video）**：根据文本描述生成视频（异步任务 + 自动轮询）
- **图生视频（Image-to-Video）**：根据输入图片与文本提示词生成视频，支持：
  - 单图模式
  - 多图模式
  - 关键帧动画模式

## 架构设计

```
agnes_text_to_image.py
agnes_image_to_image.py  }  独立功能脚本（CLI 层）
agnes_text_to_video.py
agnes_image_to_video.py

         │
         ▼

agnes_image_common.py    }  专用 API 封装（业务逻辑层）
agnes_video_common.py

         │
         ▼

agnes_common.py          }  通用工具（底层基础层）
```

- **底层（`agnes_common.py`）**：`.env` 自动加载、API Key 获取、HTTP 请求、文件下载、路径管理、参数校验 — 所有脚本共享的基础功能。
- **业务逻辑层（`agnes_image_common.py` / `agnes_video_common.py`）**：分别封装图片和视频的 API 调用流程、响应解析、参数校验（如视频 `8n+1` 规则）。
- **CLI 层（四个独立脚本）**：仅负责解析命令行参数并调用对应业务逻辑 — 一个脚本只做一件事。

## 快速开始

### 1. 安装依赖

仅需原生 Python 3.8+ 和 `requests` 包：

```bash
cd /Users/skywing/Documents/Agnes-Media-Create
pip install requests
# 或使用项目提供的依赖文件
pip install -r requirements.txt
```

### 2. 设置 API Key

在这里获取你的 API Key：https://platform.agnes-ai.com

有三种配置方式 — 优先级：命令行参数 > 环境变量 > `.env` 文件。

**方式 A：使用 `.env` 文件（推荐）**

```bash
cp .env.example .env
# 编辑 .env，填入：
# AGNES_API_KEY=sk-your-key-here
```

脚本会自动从项目目录查找 `.env` 文件并加载，无需手动 `export`。

**方式 B：环境变量**

```bash
export AGNES_API_KEY='your-api-key'
```

**方式 C：命令行参数**

```bash
python src/agnes_text_to_image.py "提示词" --key 'your-api-key'
```

### 3. 生成媒体内容

#### 文生图（Text-to-Image）

```bash
# 基础用法（自动保存到 output/image/text-to-image/）
python src/agnes_text_to_image.py "一只坐在月球上的小猫，超现实主义风格"

# 自定义输出路径
python src/agnes_text_to_image.py "一只可爱的小狗" -o custom/dog.png

# 自定义模型和尺寸
python src/agnes_text_to_image.py "山脉风景" --size 1024x512 --quality hd

# 直接提供 API Key
python src/agnes_text_to_image.py "一幅机器人的画" --key sk-your-key
```

#### 图生图（Image-to-Image）

```bash
# 使用本地图片（自动转为 base64）
python src/agnes_image_to_image.py "改成日落风格" -i input.jpg

# 使用公开可访问的 URL
python src/agnes_image_to_image.py "把这幅画变成油画风格" -i https://example.com/img.jpg
```

#### 文生视频（Text-to-Video）

视频生成是 **异步任务** — 脚本自动轮询等待（通常需要 1–3 分钟）。

```bash
# 基础：约 5 秒短视频，121 帧 / 24 fps
python src/agnes_text_to_video.py "一位身穿飘逸古风长袍的年轻剑客，在霓虹闪烁的现代都市摩天大楼之间奔跑穿梭" \
    --num-frames 121 --frame-rate 24

# 约 10 秒视频，更高分辨率
python src/agnes_text_to_video.py "一只独角兽奔跑在彩虹山脉上" \
    --width 1280 --height 720 --num-frames 241 --frame-rate 24
```

#### 图生视频（Image-to-Video）

支持三种输入模式：
- **单图**：`--image URL`
- **多图**：`--image URL1 --image URL2`
- **关键帧动画**：`--image URL1 --image URL2 --keyframes`

```bash
# 单图 → 视频
python src/agnes_image_to_video.py "人物缓慢转身回望镜头" \
    --image https://example.com/portrait.png

# 多图 → 视频
python src/agnes_image_to_video.py "平滑变换" \
    --image https://example.com/a.png --image https://example.com/b.png

# 关键帧动画
python src/agnes_image_to_video.py "平滑过渡" \
    --image https://example.com/kf1.png --image https://example.com/kf2.png \
    --keyframes
```

> **注意**：Agnes Video API 的图生视频需要图片为 **公网可访问的 URL**，不支持本地文件直接上传。

## 输出目录结构

```
output/
├── image/
│   ├── text-to-image/          # 文生图输出
│   │   ├── t2i_20260607_155007.png
│   │   └── ...
│   └── image-to-image/         # 图生图输出
│       ├── i2i_20260607_155204.png
│       └── ...
└── video/
    ├── text-to-video/          # 文生视频输出
    │   ├── t2v_20260607_161011.mp4
    │   └── ...
    └── image-to-video/         # 图生视频输出
        ├── i2v_20260607_161203.mp4
        └── ...
```

- 文件命名使用时间戳
- 使用 `-o` 或 `--output` 可指定自定义输出路径（跳过分类目录）

## 完整参数参考

| 参数 | 适用范围 | 说明 | 默认值 |
|------|---------|------|--------|
| `prompt` | 全部 | 文本提示（位置参数） | 必填 |
| `-o, --output` | 全部 | 输出文件路径 | 分类目录中的自动生成文件名 |
| `-k, --key` | 全部 | API Key | `AGNES_API_KEY` 环境变量 / `.env` |
| `--model` | 全部 | 模型名称 | 图片：`agnes-image-2.1-flash` / 视频：`agnes-video-v2.0` |
| `-s, --size` | 图片脚本 | 图片尺寸，例如 `1024x1024` | `1024x1024` |
| `-q, --quality` | 图片脚本 | 生成质量：`standard` / `hd` | `standard` |
| `-f, --format` | 图片脚本 | 响应格式：`url` / `b64` | `url` |
| `-i, --image` | 图生图/图生视频 | 输入图片（路径或 URL — 视频脚本要求 URL） | 无 |
| `--num-frames` | 视频脚本 | 视频总帧数（需满足 `8n+1`） | `121` |
| `--frame-rate` | 视频脚本 | 帧率 1–60 | `30` |
| `--width / --height` | 视频脚本 | 视频分辨率 | `1152 / 768` |
| `--seed` | 视频脚本 | 随机种子（可选） | 无 |
| `--keyframes` | 图生视频 | 启用关键帧动画模式 | 关闭 |
| `--poll-interval` | 视频脚本 | 轮询间隔秒数 | `5` |
| `--max-wait` | 视频脚本 | 最长等待秒数 | `600` |

## API 详情

### 图片 API
- **基础地址**：`https://apihub.agnes-ai.com/v1`
- **接口**：`POST /v1/images/generations`
- **模型**：`agnes-image-2.1-flash`
- **认证**：通过 `Authorization: Bearer $AGNES_API_KEY` 传递 Bearer token
- **格式**：兼容 OpenAI API 格式

### 视频 API
- **基础地址**：`https://api.agnes-ai.com/v1/videos`
- **模型**：`agnes-video-v2.0`
- **流程**：
  1. `POST /v1/videos/generations` 创建异步任务，返回 `task_id` / `video_id`
  2. `GET /v1/videos/{video_id}` 轮询结果
  3. 状态变化：`in_progress` → `completed`
  4. 从返回的 URL 下载视频
- **认证**：通过 `Authorization: Bearer $AGNES_API_KEY` 传递 Bearer token

## 支持的图片尺寸

- 1024x1024（正方形）
- 512x512（小正方形）
- 1024x512（横向）
- 512x1024（纵向）

## 视频帧数约束

视频 `num_frames` 必须满足 `8n + 1` 且 `≤ 441`。例如：

| n | num_frames | 大致时长（24fps） |
|---|------------|------------------|
| 1 | 9 | 0.375s |
| 4 | 33 | 1.375s |
| 6 | 49 | 2.0s |
| 10 | 81 | 3.375s |
| 15 | 121 | 5.0s |
| 30 | 241 | 10.0s |
| 55 | 441 | 18.375s |

脚本会自动校验 — 如果不满足规则，脚本会退出并给出清晰的错误信息和推荐值。

## 系统要求

- Python 3.8+
- requests

## 文件说明

- `SKILL.md` — Skill 定义文件（frontmatter 名称/描述 + 详细使用指南）
- `src/agnes_common.py` — 所有脚本共享的底层工具
- `src/agnes_image_common.py` — 图片 API 封装
- `src/agnes_video_common.py` — 视频 API 封装
- `src/agnes_text_to_image.py` — 文生图独立脚本
- `src/agnes_image_to_image.py` — 图生图独立脚本
- `src/agnes_text_to_video.py` — 文生视频独立脚本
- `src/agnes_image_to_video.py` — 图生视频独立脚本（支持多图 / 关键帧）
- `requirements.txt` — Python 依赖包列表
- `.env.example` — 环境配置示例文件

## 使用示例

### 示例 1：文生图

```bash
python src/agnes_text_to_image.py "雄伟的雪山风景，早晨阳光，油画风格"
```

输出：
```
🎨 Creating image...
   Model: agnes-image-2.1-flash  Size: 1024x1024  Quality: standard
✅ Saved to: output/image/text-to-image/t2i_20260607_155007.png
```

### 示例 2：图生图

```bash
python src/agnes_image_to_image.py "在小狗旁边加一只可爱的小猫" -i output/image/text-to-image/t2i_20260607_155007.png
```

输出：
```
🎨 Creating image-to-image...
   Model: agnes-image-2.1-flash  Size: 1024x1024  Quality: standard
   Input image: output/image/text-to-image/t2i_20260607_155007.png
✅ Saved to: output/image/image-to-image/i2i_20260607_155204.png
```

### 示例 3：文生视频

```bash
python src/agnes_text_to_video.py "一位身穿飘逸长袍的年轻剑客，在霓虹闪烁的现代都市摩天大楼之间奔跑穿梭，电影级宽银幕镜头，24fps" \
    --num-frames 121 --frame-rate 24 --width 1152 --height 768
```

输出：
```
🎬 Text-to-Video task
   Prompt: 一位身穿飘逸长袍的年轻剑客，在霓虹闪烁的现代都市摩天大楼之间奔跑穿梭...
   Expected duration: ~5.04 seconds (121 frames / 24 fps)
   Output file: output/video/text-to-video/t2v_20260607_161011.mp4

🎬 Creating video task...
   Model: agnes-video-v2.0  Resolution: 1152x768  Frames/fps: 121/24
✅ Task created
   task_id: task_mTtvzZl6qaHTJQg7ifoWDysd6Jqa73gj
   video_id: video_...

⏳ Polling video results (interval 5s, max 600s)...
   [   0s] status=in_progress progress=30%
   [ 119s] status=completed   progress=100%

✅ Video generation complete

📥 Downloading video to output/video/text-to-video/t2v_20260607_161011.mp4...
✅ Saved to: output/video/text-to-video/t2v_20260607_161011.mp4
```

## 注意事项

- 项目根目录：`/Users/skywing/Documents/Agnes-Media-Create`
- 视频生成是 **异步任务**，脚本会自动轮询等待，通常需要 1–3 分钟
- 图生视频的输入图片必须是 **公网可访问的 URL** — API 不支持本地文件上传
- 建议将 API Key 存储在 `.env` 文件中，避免在命令历史中泄漏

## 许可证

MIT
