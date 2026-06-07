# 🎨 Agnes Image 2.1 Flash 命令行工具

一个使用 Agnes Image 2.1 Flash API 生成图片的命令行工具，支持文生图和图生图两种功能。

## 功能特性

- **文生图 (Text-to-Image)**：根据文字描述生成图片
- **图生图 (Image-to-Image)**：根据文字提示修改现有图片
- **自动分类输出**：图片自动保存到分类目录
- **可自定义参数**：模型、尺寸、质量等

## 快速开始

### 1. 安装依赖

```bash
pip install openai requests
```

### 2. 设置 API Key

在这里获取你的 API Key：https://platform.agnes-ai.com

```bash
# 方式 A：设置环境变量
export AGNES_API_KEY='your-api-key-here'

# 方式 B：复制 .env.example 文件并编辑
cp .env.example .env
# 然后编辑 .env 文件填入你的 API Key
```

### 3. 生成图片

```bash
# 文生图（自动保存到 output/image/text-to-image/）
python agnes_image.py "一只坐在月球上的小猫，超现实主义风格"

# 图生图（自动保存到 output/image/image-to-image/）
python agnes_image.py "把图片变成日落风格" -i input.jpg

# 自定义输出路径（覆盖默认目录）
python agnes_image.py "一只可爱的小猫" -o custom/cat.png

# 自定义模型和尺寸
python agnes_image.py "山脉风景" --size 1024x512 --quality hd

# 直接提供 API Key
python agnes_image.py "一幅机器人的画" --key sk-your-key
```

## 输出目录结构

```
output/
└── image/
    ├── text-to-image/          # 文生图输出目录
    │   ├── t2i_20260607_155007.png
    │   └── ...
    └── image-to-image/         # 图生图输出目录
        ├── i2i_20260607_155204.png
        └── ...
```

- **文生图**图片自动保存到 `output/image/text-to-image/`
- **图生图**图片自动保存到 `output/image/image-to-image/`
- 文件名使用时间戳命名（例如 `t2i_YYYYMMDD_HHMMSS.png`
- 你可以使用 `-o` 或 `--output` 参数指定自定义输出路径

## 命令参数参考

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `prompt` | 文本提示（位置参数） | 必填 |
| `-i, --image` | 图生图的输入图片路径 | 无 |
| `-o, --output` | 输出文件路径 | 分类目录中的自动生成文件名 |
| `-k, --key` | API Key | AGNES_API_KEY 环境变量 |
| `--base-url` | 自定义 API 基础地址 | https://apihub.agnes-ai.com/v1 |
| `--model` | 模型名称 | agnes-image-2.1-flash |
| `-s, --size` | 图片尺寸 | 1024x1024 |
| `-q, --quality` | 图片质量：standard/hd | standard |
| `-f, --format` | 响应格式：url/b64 | url |
| `--info` | 显示 API 信息 | - |
| `-h, --help` | 显示帮助信息 | - |

## API 详情

- **基础地址**：`https://apihub.agnes-ai.com/v1`
- **接口**：`POST /v1/images/generations`
- **模型**：`agnes-image-2.1-flash`
- **认证**：通过 `Authorization: Bearer $AGNES_API_KEY`
- **格式**：兼容 OpenAI API 格式

## 支持的图片尺寸

- 1024x1024（正方形）
- 512x512（小正方形）
- 1024x512（横向）
- 512x1024（纵向）

## 系统要求

- Python 3.8+
- openai >= 1.0.0
- requests

## 文件说明

- `agnes_image.py` - 图片生成主程序
- `agnes_image_requirements.txt` - Python 依赖包列表
- `.env.example` - 环境配置示例文件
- `output/image/text-to-image/` - 文生图默认输出目录
- `output/image/image-to-image/` - 图生图默认输出目录

## 使用示例

### 示例 1：生成一只可爱的小狗

```bash
python agnes_image.py "一只可爱的小狗，坐在公园里" --key sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

输出：
```
🎨 Generating image: '一只可爱的小狗，坐在公园里...'
   Model: agnes-image-2.1-flash
   Size: 1024x1024
   Quality: standard
✅ Saved to: output/image/text-to-image/t2i_20260607_155007.png
```

### 示例 2：在小狗图片中添加一只小猫

```bash
python agnes_image.py "在小狗旁边加一只可爱的小猫" --image output/image/text-to-image/t2i_20260607_155007.png --key sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

输出：
```
🎨 Image-to-Image: '在小狗旁边加一只可爱的小猫...'
   Input: output/image/text-to-image/t2i_20260607_155007.png
   Model: agnes-image-2.1-flash
✅ Saved to: output/image/image-to-image/i2i_20260607_155204.png
```

## 许可证

MIT
