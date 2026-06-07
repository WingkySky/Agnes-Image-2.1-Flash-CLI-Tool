
# 🎨 Agnes Media Create 媒体生成工具

[![Stars](https://img.shields.io/github/stars/your-org/agnes-media-create?style=flat)](https://github.com/)
[![Forks](https://img.shields.io/github/forks/your-org/agnes-media-create?style=flat)](https://github.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white)
![Shell](https://img.shields.io/badge/-Shell-4EAA25?logo=gnu-bash&logoColor=white)
![Markdown](https://img.shields.io/badge/-Markdown-000000?logo=markdown&logoColor=white)

> **4 种生成模式** | **2 种 API 集成** | **7 个独立模块** | **自动轮询** | **跨平台**

---

<div align="center">

**🌐 Language / 语言**

[English](README.md) | [**中文**](README_zh.md)

</div>

---

**一个使用 Agnes Image 2.1 Flash 与 Agnes Video V2.0 API 生成媒体内容的模块化命令行工具包。**

这不仅仅是一个脚本。它是一个完整的系统，采用三层架构设计：通用工具（`.env` 自动加载、HTTP 请求、文件下载、参数校验）、API 专属封装（图片与视频接口及响应解析）、独立功能脚本（文生图、图生图、文生视频，以及支持多图/关键帧动画的图生视频）。

专为追求简洁、生产级脚本的开发者而设计 —— 零配置摩擦，无 OpenAI SDK 依赖，开箱即用。

---

## ✨ 功能特性

### 当前支持

| 模式                                  | 说明                                                     | 脚本                        |
| ------------------------------------- | -------------------------------------------------------- | --------------------------- |
| 🖼️**文生图 (Text-to-Image)**  | 根据文本提示词生成图片                                   | `agnes_text_to_image.py`  |
| 🖼️**图生图 (Image-to-Image)** | 根据输入图片与提示词修改现有图片                         | `agnes_image_to_image.py` |
| 🎬**文生视频 (Text-to-Video)**  | 根据文本提示词生成视频（异步任务 + 自动轮询）            | `agnes_text_to_video.py`  |
| 🎬**图生视频 (Image-to-Video)** | 根据输入图片生成视频 —— 支持单图、多图与关键帧动画模式 | `agnes_image_to_video.py` |

### 架构亮点

- **三层模块化设计** —— 通用基础层 → API 封装层 → 独立功能脚本
- **`.env` 自动检测** —— 无需手动 export，可在任意子目录中运行
- **统一的 API Key 管理** —— 命令行参数 > 环境变量 > `.env` 文件
- **异步视频轮询** —— 可配置轮询间隔与超时时间的智能等待
- **校验优先** —— 视频帧数（`8n+1` 规则）、帧率、URL 格式均在发送前校验
- **零重度依赖** —— 仅需 `requests`，不绑定 OpenAI SDK

---

## 📦 项目结构

```
agnes-media-create/
├── SKILL.md                              # Skill 定义（frontmatter + 使用指南）
├── README.md                             # 项目文档（英文）
├── README_zh.md                          # 项目文档（中文）— 本文件
├── requirements.txt                      # Python 依赖
├── .env.example                          # 环境变量示例
├── .env                                  # 可选：本地 API Key 配置（自动加载）
├── scripts/
│   ├── agnes_common.py                   # 通用工具 —— .env / HTTP / 下载 / 路径
│   ├── agnes_image_common.py             # 图片 API 封装
│   ├── agnes_video_common.py             # 视频 API 封装（异步 + 轮询）
│   ├── agnes_text_to_image.py            # 文生图独立脚本
│   ├── agnes_image_to_image.py           # 图生图独立脚本
│   ├── agnes_text_to_video.py            # 文生视频独立脚本
│   └── agnes_image_to_video.py           # 图生视频独立脚本（多图 / 关键帧）
└── output/
    ├── image/text-to-image/              # 文生图输出目录
    ├── image/image-to-image/             # 图生图输出目录
    ├── video/text-to-video/              # 文生视频输出目录
    └── video/image-to-video/             # 图生视频输出目录
```

---

## 🚀 快速开始

2 分钟内启动并运行：

### 步骤 1：安装依赖

```bash
cd /path/to/Agnes-Media-Create
pip install -r requirements.txt
# 或最小安装：
# pip install requests
```

### 步骤 2：配置 API Key

在 https://platform.agnes-ai.com 获取你的 Key，然后：

```bash
# 选项 A —— 使用 .env（推荐 —— 自动检测，无需 export）
cp .env.example .env
# 编辑 .env，设置 AGNES_API_KEY=sk-your-key-here

# 选项 B —— 环境变量
export AGNES_API_KEY='your-api-key'

# 选项 C —— 命令行参数传入
python scripts/agnes_text_to_image.py "提示词" --key 'your-api-key'
```

### 步骤 3：开始生成内容

```bash
# 🖼️ 文生图
python scripts/agnes_text_to_image.py "日落时分的未来都市，电影级光线"

# 🖼️ 图生图（自动将本地文件转为 base64）
python scripts/agnes_image_to_image.py "改成日落风格" -i input.jpg

# 🎬 文生视频（自动轮询直至完成）
python scripts/agnes_text_to_video.py "一位剑客在霓虹摩天大楼间穿梭" \
    --num-frames 121 --frame-rate 24

# 🎬 图生视频（单图 / 多图 / 关键帧动画模式）
python scripts/agnes_image_to_video.py "角色缓慢转身回望" \
    --image https://example.com/portrait.png
```

✨ **完成！** 输出结果将以时间戳命名，保存在 `output/` 目录下。

---

## 📖 完整使用参考

### 文生图 (Text-to-Image)

```bash
python scripts/agnes_text_to_image.py "提示词" [选项]
```

| 参数              | 说明                                      | 默认值                     |
| ----------------- | ----------------------------------------- | -------------------------- |
| `--output, -o`  | 自定义输出文件路径                        | 分类目录中的自动生成文件名 |
| `--model`       | 模型名称                                  | `agnes-image-2.1-flash`  |
| `--size, -s`    | 图片尺寸（如 `1024x1024`、`512x512`） | `1024x1024`              |
| `--quality, -q` | 质量：`standard` 或 `hd`              | `standard`               |
| `--format, -f`  | 响应格式：`url` 或 `b64`              | `url`                    |
| `--key, -k`     | API Key（覆盖环境变量与 .env）            | 来自环境变量或 `.env`    |

### 图生图 (Image-to-Image)

```bash
python scripts/agnes_image_to_image.py "提示词" -i input.jpg [选项]
```

| 参数              | 说明                                                    | 默认值                    |
| ----------------- | ------------------------------------------------------- | ------------------------- |
| `--image, -i`   | 输入图片 —— 本地文件路径（自动转为 base64）或公开 URL | **必填**            |
| `--model`       | 模型名称                                                | `agnes-image-2.1-flash` |
| `--size, -s`    | 输出图片尺寸                                            | `1024x1024`             |
| `--quality, -q` | 质量：`standard` 或 `hd`                            | `standard`              |

### 文生视频 (Text-to-Video)

```bash
python scripts/agnes_text_to_video.py "提示词" [选项]
```

| 参数                | 说明                                                          | 默认值   |
| ------------------- | ------------------------------------------------------------- | -------- |
| `--num-frames`    | 总帧数 —— 必须满足 `8n+1`（如 33、49、81、121、241、441） | `121`  |
| `--frame-rate`    | 帧率（1–60）                                                 | `30`   |
| `--width`         | 视频宽度（像素）                                              | `1152` |
| `--height`        | 视频高度（像素）                                              | `768`  |
| `--seed`          | 随机种子（用于可重复性）                                      | 随机     |
| `--poll-interval` | 轮询请求间隔秒数                                              | `5`    |
| `--max-wait`      | 超时前的最大等待秒数                                          | `600`  |

**按帧数估算时长**（24 fps 下）：

| num_frames | 大致时长 |
| ---------- | -------- |
| 33         | ~1.4 秒  |
| 81         | ~3.4 秒  |
| 121        | ~5.0 秒  |
| 241        | ~10.0 秒 |
| 441        | ~18.4 秒 |

### 图生视频 (Image-to-Video)

```bash
python scripts/agnes_image_to_video.py "提示词" --image URL [选项]
```

支持三种输入模式：

1. **单图** —— `--image https://example.com/portrait.png`
2. **多图** —— `--image URL1 --image URL2`
3. **关键帧动画** —— `--image URL1 --image URL2 --keyframes`

| 参数                       | 说明                                         | 默认值         |
| -------------------------- | -------------------------------------------- | -------------- |
| `--image, -i`            | 公开可访问的图片 URL —— 多图模式可重复使用 | **必填** |
| `--keyframes`            | 启用关键帧动画模式                           | 关闭           |
| `--num-frames`           | 总帧数（`8n+1` 规则）                      | `121`        |
| `--frame-rate`           | 帧率（1–60）                                | `30`         |
| `--width` / `--height` | 视频分辨率                                   | `1152 / 768` |

> ⚠️ **注意：** Agnes Video API 的图生视频需要图片为**公网可访问的 URL**。不支持本地文件路径。

---

## 📋 API 详情

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
  1. `POST /v1/videos/generations` → 创建异步任务，返回 `task_id` / `video_id`
  2. `GET /v1/videos/{video_id}` → 轮询完成状态
  3. 状态变化：`in_progress` → `completed`
  4. 从返回的 URL 下载视频
- **认证**：通过 `Authorization: Bearer $AGNES_API_KEY` 传递 Bearer token

---

## 🛠️ 架构概览

```
agnes_text_to_image.py
agnes_image_to_image.py  }  独立功能脚本（CLI 层）
agnes_text_to_video.py
agnes_image_to_video.py

         │
         ▼

agnes_image_common.py    }  API 专属封装（业务逻辑层）
agnes_video_common.py

         │
         ▼

agnes_common.py          }  通用工具（底层基础层）
```

- **底层（`agnes_common.py`）** —— `.env` 自动加载、API Key 解析、HTTP 请求、文件下载、路径管理、参数校验。所有脚本共享。
- **业务逻辑层（`agnes_image_common.py` / `agnes_video_common.py`）** —— 分别封装图片与视频的 API 调用流程、响应解析，以及参数校验（如视频 `8n+1` 帧数规则）。
- **CLI 层（4 个独立脚本）** —— 每个脚本只负责解析命令行参数并调用对应业务逻辑 —— 一个脚本，一件事。

---

## 📝 实际输出示例

### 文生视频

```
🎬 Text-to-Video task
   Prompt: a young swordsman in flowing robes running through neon-lit skyscrapers, cinematic
   Expected duration: ~5.04 seconds (121 frames / 24 fps)
   Output file: output/video/text-to-video/t2v_20260607_161011.mp4

🎬 Creating video task...
   Model: agnes-video-v2.0  Resolution: 1152x768  Frames/fps: 121/24
✅ Task created
   task_id:  task_mTtvzZl6qaHTJQg7ifoWDysd6Jqa73gj
   video_id: video_bGl0ZWxsbTpjdXN0b21fbGxt...

⏳ Polling video results (interval 5s, max 600s)...
   [   0s] status=in_progress progress=30%
   [ 119s] status=completed   progress=100%

✅ Video generation complete

📥 Downloading video to output/video/text-to-video/t2v_20260607_161011.mp4...
✅ Saved to: output/video/text-to-video/t2v_20260607_161011.mp4  (2.19 MB)
```

### 文生图

```
🎨 Creating image...
   Model: agnes-image-2.1-flash  Size: 1024x1024  Quality: standard
✅ Saved to: output/image/text-to-image/t2i_20260607_155007.png
```

---

## 📦 支持的图片尺寸

| 尺寸          | 方向     |
| ------------- | -------- |
| `1024x1024` | 正方形   |
| `512x512`   | 小正方形 |
| `1024x512`  | 横向     |
| `512x1024`  | 纵向     |

---

## 💡 注意事项

- **项目根目录**：`/Users/skywing/Documents/Agnes-Media-Create`
- **视频生成**为异步任务 —— 脚本自动轮询等待，通常 1–3 分钟
- **图生视频**的输入图片必须是**公网可访问的 URL** —— API 不支持本地上传
- 建议将 API Key 存入 `.env` 文件，避免在命令历史中泄漏

---

## 📜 许可证

MIT
