---
name: "agnes-media-create"
description: "通过 Agnes Image 2.1 Flash API 进行文生图和图生图；通过 Agnes Video V2.0 API 进行文生视频和图生视频。当用户要求生成图片、视频，或根据描述创作/修改媒体内容时调用。"
---

# Agnes Media Create 媒体生成技能

本 Skill 基于 `Agnes Image 2.1 Flash` 与 `Agnes Video V2.0` API 提供以下功能：

- **文生图（Text-to-Image）**：根据文本描述生成图片
- **图生图（Image-to-Image）**：根据输入图片与文本提示词修改现有图片
- **文生视频（Text-to-Video）**：根据文本描述生成视频
- **图生视频（Image-to-Video）**：根据输入图片与文本提示词生成视频，支持多图/关键帧动画模式

**整个文件夹作为一个独立的 Skill 被智能体调用。**

## 项目结构（Skill 标准结构）

```
Skill 根目录/（整个文件夹作为 Skill 被调用）
├── SKILL.md                      # 本文件，Skill 定义（frontmatter + 使用说明）
├── README.md                     # 项目文档（英文）
├── README_zh.md                  # 项目文档（中文）
├── requirements.txt              # Python 依赖
├── .env.example                  # 环境变量示例
├── .env                          # 可选：本地 API Key 配置文件（无需 export 自动加载）
├── scripts/
│   ├── agnes_common.py           # 通用模块（.env 加载 / HTTP / 下载 / 路径）
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

## 前置条件

### 1. 依赖安装

只需原生 Python 3.8+ 和 `requests` 包：

```bash
cd /Users/skywing/Documents/Agnes-Media-Create
pip install requests
# 或使用项目提供的依赖文件
pip install -r requirements.txt
```

### 2. API Key 配置

API Key 可在 https://platform.agnes-ai.com 获取。有三种方式配置：

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
python scripts/agnes_text_to_image.py "提示词" --key 'your-api-key'
```

优先级：命令行参数 > 环境变量 > `.env` 文件。

## 功能模块说明

每个功能都是一个独立的 Python 脚本，各自专注一件事。

### 1. 文生图（Text-to-Image）

根据文本提示词生成图片。

**调用方式**：

```bash
python scripts/agnes_text_to_image.py "文本提示词"
```

**示例**：

```bash
# 基础用法
python scripts/agnes_text_to_image.py "一只坐在月球上的小猫，超现实主义风格"

# 指定输出路径
python scripts/agnes_text_to_image.py "可爱的小狗" -o custom/dog.png

# 自定义模型与尺寸
python scripts/agnes_text_to_image.py "山脉风景" --size 1024x512 --quality hd
```

### 2. 图生图（Image-to-Image）

根据输入图片和文本提示词修改现有图片。

**调用方式**：

```bash
python scripts/agnes_image_to_image.py "文本提示词" -i 输入图片路径
```

**示例**：

```bash
# 传入本地图片（自动转为 base64）
python scripts/agnes_image_to_image.py "改成日落风格" -i input.jpg

# 传入公开 URL
python scripts/agnes_image_to_image.py "把画变成油画风格" -i https://example.com/img.jpg
```

### 3. 文生视频（Text-to-Video）

根据文本提示词生成视频（异步任务，脚本自动轮询结果）。

**调用方式**：

```bash
python scripts/agnes_text_to_video.py "文本提示词"
```

**视频参数**：

- `--num-frames`：总帧数，必须满足 `8n+1`（例如 33、49、65、81、97、121、241、441），默认 121
- `--frame-rate`：帧率（1–60），默认 30
- `--width` / `--height`：视频分辨率，默认 1152x768

**示例**：

```bash
# 基础用法（约 5 秒短视频，121 帧 / 24 fps）
python scripts/agnes_text_to_video.py "一位身穿飘逸长袍的年轻剑客，在雨夜都市中穿行" \
    --num-frames 121 --frame-rate 24

# 约 10 秒视频，更高分辨率
python scripts/agnes_text_to_video.py "一只独角兽奔跑在彩虹山脉上" \
    --width 1280 --height 720 --num-frames 241 --frame-rate 24
```

### 4. 图生视频 / 多图视频 / 关键帧动画（Image-to-Video）

根据输入图片与文本提示词生成视频，支持三种输入模式：

- **单图**：`--image URL`
- **多图**：`--image URL1 --image URL2`
- **关键帧动画**：`--image URL1 --image URL2 --keyframes`

**调用方式**：

```bash
python scripts/agnes_image_to_video.py "文本提示词" --image 图片URL
```

**示例**：

```bash
# 单图 → 视频（图生视频）
python scripts/agnes_image_to_video.py "人物缓慢转身回望镜头" \
    --image https://example.com/portrait.png

# 多图 → 视频
python scripts/agnes_image_to_video.py "平滑变换" \
    --image https://example.com/a.png --image https://example.com/b.png

# 关键帧动画
python scripts/agnes_image_to_video.py "平滑过渡" \
    --image https://example.com/kf1.png --image https://example.com/kf2.png \
    --keyframes
```

> **注意**：Agnes Video API 的图生视频需要图片为**公网可访问的 URL**。如果传入本地路径，脚本会提示并退出。

## 常用参数总览

| 参数 | 适用范围 | 说明 | 默认值 |
|------|---------|------|--------|
| `prompt` | 全部 | 位置参数，文本提示词 | 必填 |
| `-o, --output` | 全部 | 输出文件路径 | 自动生成文件名（在对应分类目录） |
| `-k, --key` | 全部 | API Key | `AGNES_API_KEY` 环境变量 / `.env` |
| `--model` | 全部 | 模型名称 | 图片：`agnes-image-2.1-flash` / 视频：`agnes-video-v2.0` |
| `-s, --size` | 图片类 | 图片尺寸，例如 `1024x1024` | `1024x1024` |
| `-q, --quality` | 图片类 | 生成质量：`standard` / `hd` | `standard` |
| `-f, --format` | 图片类 | 响应格式：`url` / `b64` | `url` |
| `-i, --image` | 图生图/图生视频 | 输入图片（路径或 URL，视频脚本要求 URL） | 无 |
| `--num-frames` | 视频类 | 视频总帧数（需满足 `8n+1`） | `121` |
| `--frame-rate` | 视频类 | 帧率 1–60 | `30` |
| `--width / --height` | 视频类 | 视频分辨率 | `1152 / 768` |
| `--seed` | 视频类 | 随机种子（可选） | 无 |
| `--keyframes` | 图生视频 | 启用关键帧动画模式 | 关闭 |
| `--poll-interval` | 视频类 | 轮询间隔秒数 | `5` |
| `--max-wait` | 视频类 | 最长等待秒数 | `600` |

## 支持的图片尺寸

- `1024x1024`（正方形）
- `512x512`（小正方形）
- `1024x512`（横向）
- `512x1024`（纵向）

## 视频帧数约束

视频 `num_frames` 必须满足 `8n + 1` 且 `≤ 441`。例如：

| n | num_frames | 大致时长 (24fps) |
|---|------------|------------------|
| 1 | 9 | 0.375s |
| 4 | 33 | 1.375s |
| 6 | 49 | 2.0s |
| 10 | 81 | 3.375s |
| 15 | 121 | 5.0s |
| 30 | 241 | 10.0s |
| 55 | 441 | 18.375s |

脚本会自动校验，不满足规则时会直接报错并给出推荐值。

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
- 使用 `-o` 或 `--output` 可自定义输出路径（跳过分类目录）

## 完整调用示例

### 场景 1：文生图

当用户说「帮我生成一张风景图」：

```bash
python scripts/agnes_text_to_image.py "雄伟的雪山风景，早晨阳光，油画风格"
```

### 场景 2：图生图

当用户说「把这张图片改成日落风格」：

```bash
python scripts/agnes_image_to_image.py "改成日落风格" -i /path/to/input.jpg
```

### 场景 3：文生视频

当用户说「生成一个剑侠在都市中穿行的视频」：

```bash
python scripts/agnes_text_to_video.py "一位身穿飘逸古风长袍的年轻剑客，在霓虹闪烁的现代都市摩天大楼之间奔跑穿梭，电影级宽银幕镜头" \
    --num-frames 121 --frame-rate 24 --width 1152 --height 768
```

### 场景 4：图生视频

当用户说「根据这张图片生成一段视频」：

```bash
python scripts/agnes_image_to_video.py "人物缓慢转身回望镜头" \
    --image https://your-storage.example.com/portrait.png
```

## 模块设计说明（供参考）

项目采用三层模块化设计，便于扩展与维护：

```
agnes_text_to_image.py
agnes_image_to_image.py  } 独立功能脚本（CLI 层）
agnes_text_to_video.py
agnes_image_to_video.py

         │
         ▼

agnes_image_common.py    } 专用 API 封装（业务逻辑层）
agnes_video_common.py

         │
         ▼

agnes_common.py          } 通用工具（底层基础层）
```

- **底层（`agnes_common.py`）**：`.env` 自动加载、API Key 获取、HTTP 请求、文件下载、路径管理、参数校验等所有脚本共享的基础功能。
- **业务逻辑层（`agnes_image_common.py` / `agnes_video_common.py`）**：分别封装图片和视频的 API 调用流程、响应解析、参数校验（如视频 `8n+1` 规则）。
- **CLI 层（四个独立脚本）**：仅负责解析命令行参数并调用对应业务逻辑，每个脚本只做一件事。

## 注意事项

- 项目根目录：`/Users/skywing/Documents/Agnes-Media-Create`
- 视频生成是**异步任务**，脚本会自动轮询等待，通常需要 1–3 分钟
- 图生视频（`image-to-video`）的输入图片必须是公网可访问的 URL，不支持本地文件直接上传
- 建议将 API Key 写入 `.env` 文件，避免在命令行中泄漏
