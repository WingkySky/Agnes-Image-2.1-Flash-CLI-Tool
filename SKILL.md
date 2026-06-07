---
name: "agnes-media-create"
description: "通过 Agnes Image 2.1 Flash API 进行文生图和图生图，未来支持视频生成。当用户要求生成图片、视频，或根据描述创作/修改媒体内容时调用。"
---

# Agnes Media Create 媒体生成技能

本技能基于 [src/agnes_image.py](file:///Users/skywing/Documents/Agnes-Image-2.1-Flash-CLI-Tool/src/agnes_image.py) 提供文生图（Text-to-Image）和图生图（Image-to-Image）功能，未来将扩展支持视频生成。
**整个文件夹作为一个独立的 Skill 被智能体调用。**

## 项目结构（Skill 标准结构）

```
Skill 根目录/（整个文件夹作为 Skill 被调用）
├── SKILL.md                      # 本文件，Skill 定义（包含 frontmatter 和使用说明）
├── src/
│   └── agnes_image.py            # 图片生成主程序
├── requirements.txt              # Python 依赖
├── .env.example                  # 环境变量示例
├── README.md                     # 项目文档（英文）
└── README_zh.md                  # 项目文档（中文）
```

## 前置条件

### 1. 依赖安装

需要安装 `openai` 和 `requests` Python 包：

```bash
cd /Users/skywing/Documents/Agnes-Image-2.1-Flash-CLI-Tool
pip install openai requests
# 或使用项目提供的依赖文件
pip install -r requirements.txt
```

### 2. API Key 配置

需要设置 `AGNES_API_KEY` 环境变量，或通过 `--key` 参数传入。API Key 可在 https://platform.agnes-ai.com 获取。

```bash
export AGNES_API_KEY='your-api-key'
```

或通过命令行参数传入：

```bash
python src/agnes_image.py "提示词" --key 'your-api-key'
```

## 功能模块

### 1. 文生图（Text-to-Image）

根据文本提示词生成图片。

**调用方式**：

```bash
cd /Users/skywing/Documents/Agnes-Image-2.1-Flash-CLI-Tool
python src/agnes_image.py "文本提示词"
```

**示例**：

```bash
# 基础用法（默认输出到 output/image/text-to-image/ 目录）
python src/agnes_image.py "一只坐在月球上的小猫，超现实主义风格"

# 指定输出路径
python src/agnes_image.py "可爱的小狗" -o custom/dog.png

# 自定义模型与尺寸
python src/agnes_image.py "山脉风景" --size 1024x512 --quality hd
```

### 2. 图生图（Image-to-Image）

根据输入图片和文本提示词修改现有图片。

**调用方式**：

```bash
cd /Users/skywing/Documents/Agnes-Image-2.1-Flash-CLI-Tool
python src/agnes_image.py "文本提示词" -i 输入图片路径
```

**示例**：

```bash
# 图生图（输出到 output/image/image-to-image/ 目录）
python src/agnes_image.py "把图片变成日落风格" -i input.jpg

# 自定义输出路径
python src/agnes_image.py "添加一只小猫" -i input.jpg -o output/modified.png
```

## 常用参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `prompt` | 位置参数，文本提示词 | 必填 |
| `-i, --image` | 图生图的输入图片路径 | 无 |
| `-o, --output` | 输出文件路径 | 自动生成文件名 |
| `-k, --key` | API Key | `AGNES_API_KEY` 环境变量 |
| `--base-url` | 自定义 API 基础地址 | `https://apihub.agnes-ai.com/v1` |
| `--model` | 模型名称 | `agnes-image-2.1-flash` |
| `-s, --size` | 图片尺寸 | `1024x1024` |
| `-q, --quality` | 图片质量：`standard` / `hd` | `standard` |
| `-f, --format` | 响应格式：`url` / `b64` | `url` |
| `--info` | 显示 API 信息 | - |

## 支持的图片尺寸

- `1024x1024`（正方形）
- `512x512`（小正方形）
- `1024x512`（横向）
- `512x1024`（纵向）

## 输出目录

- **文生图**默认输出到 `output/image/text-to-image/`
- **图生图**默认输出到 `output/image/image-to-image/`
- 文件命名使用时间戳，如 `t2i_20260607_155007.png`
- 使用 `-o` 或 `--output` 可自定义输出路径

## 完整调用示例

### 文生图场景

当用户说「帮我生成一张风景图」或「根据这个描述画一张图」，使用：

```bash
cd /Users/skywing/Documents/Agnes-Image-2.1-Flash-CLI-Tool
python src/agnes_image.py "雄伟的雪山风景，早晨阳光，油画风格"
```

### 图生图场景

当用户说「把这张图片改成日落风格」或「在这张图中添加一只小狗」，使用：

```bash
cd /Users/skywing/Documents/Agnes-Image-2.1-Flash-CLI-Tool
python src/agnes_image.py "改成日落风格" -i /path/to/input.jpg
```

## 未来扩展

本 Skill 设计为可扩展的媒体生成平台，未来计划支持：

- **文生视频 (Text-to-Video)**：根据文字描述生成视频
- **视频编辑 (Video-to-Video)**：根据文字提示修改现有视频

## 注意事项

- 文生图和图生图的主程序位于 [src/agnes_image.py](file:///Users/skywing/Documents/Agnes-Image-2.1-Flash-CLI-Tool/src/agnes_image.py)
- 项目根目录：`/Users/skywing/Documents/Agnes-Image-2.1-Flash-CLI-Tool`
- 调用前请确保已安装依赖并配置 API Key
