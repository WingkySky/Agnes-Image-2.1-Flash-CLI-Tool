# 🎨 Agnes Image 2.1 Flash CLI Tool

A CLI tool for generating images using the Agnes Image 2.1 Flash API, supporting both text-to-image and image-to-image operations.

## Features

- **Text-to-Image**: Generate images from text descriptions
- **Image-to-Image**: Modify existing images based on text prompts
- **Auto-organized output**: Images are automatically saved to categorized directories
- **Customizable parameters**: Model, size, quality, and more

## Quick Start

### 1. Install Dependencies

```bash
pip install openai requests
```

### 2. Set API Key

Get your API key from: https://platform.agnes-ai.com

```bash
# Option A: Environment variable
export AGNES_API_KEY='your-api-key-here'

# Option B: Copy .env.example and edit
cp .env.example .env
# Edit .env with your key
```

### 3. Generate Images

```bash
# Text-to-Image (auto-saves to output/image/text-to-image/)
python agnes_image.py "a cat sitting on the moon, surreal art"

# Image-to-Image (auto-saves to output/image/image-to-image/)
python agnes_image.py "make it sunset style" -i input.jpg

# Custom output path (overrides default directory)
python agnes_image.py "a cute cat" -o custom/cat.png

# Custom model and size
python agnes_image.py "mountain landscape" --size 1024x512 --quality hd

# Provide API key inline
python agnes_image.py "a robot painting" --key sk-your-key
```

## Output Directory Structure

```
output/
└── image/
    ├── text-to-image/          # Text-to-Image outputs
    │   ├── t2i_20260607_155007.png
    │   └── ...
    └── image-to-image/         # Image-to-Image outputs
        ├── i2i_20260607_155204.png
        └── ...
```

- **Text-to-Image** images are automatically saved to `output/image/text-to-image/`
- **Image-to-Image** images are automatically saved to `output/image/image-to-image/`
- Files are named using timestamps (e.g., `t2i_YYYYMMDD_HHMMSS.png`)
- You can always use `-o` or `--output` to specify a custom output path

## Command Reference

| Flag | Description | Default |
|------|-------------|---------|
| `prompt` | Text prompt (positional) | required |
| `-i, --image` | Input image for image-to-image | none |
| `-o, --output` | Output file path | auto-generated in category dir |
| `-k, --key` | API key | AGNES_API_KEY env |
| `--base-url` | Custom API base URL | https://apihub.agnes-ai.com/v1 |
| `--model` | Model name | agnes-image-2.1-flash |
| `-s, --size` | Image size | 1024x1024 |
| `-q, --quality` | Quality: standard/hd | standard |
| `-f, --format` | Response: url/b64 | url |
| `--info` | Show API info | - |
| `-h, --help` | Show help | - |

## API Details

- **Base URL**: `https://apihub.agnes-ai.com/v1`
- **Endpoint**: `POST /v1/images/generations`
- **Model**: `agnes-image-2.1-flash`
- **Auth**: Bearer token via `Authorization: Bearer $AGNES_API_KEY`
- **Format**: OpenAI-compatible API

## Supported Image Sizes

- 1024x1024 (square)
- 512x512 (small square)
- 1024x512 (landscape)
- 512x1024 (portrait)

## Requirements

- Python 3.8+
- openai >= 1.0.0
- requests

## File Overview

- `agnes_image.py` - Main CLI script for image generation
- `agnes_image_requirements.txt` - Python dependencies
- `.env.example` - Example environment configuration
- `output/image/text-to-image/` - Default text-to-image output directory
- `output/image/image-to-image/` - Default image-to-image output directory

## License

MIT
