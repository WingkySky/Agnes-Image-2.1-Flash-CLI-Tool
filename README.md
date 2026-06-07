# 🎨 Agnes Media Create Skill

**Skill Name**: `agnes-media-create`

A CLI tool for generating media content using the Agnes Image 2.1 Flash API. Currently supports text-to-image and image-to-image operations, with future support planned for video generation.
**The entire folder functions as a standalone Skill that can be invoked by intelligent agents.**

## Project Structure (Standard Skill Layout)

```
Skill Root/ (The entire folder is invoked as a Skill)
├── SKILL.md                      # Skill definition file (with frontmatter and usage guide)
├── src/
│   └── agnes_image.py            # Main image generation script
├── requirements.txt              # Python dependencies
├── .env.example                  # Example environment variables
├── README.md                     # Project documentation (English)
└── README_zh.md                  # Project documentation (Chinese)
```

## How the Skill Works

1. Intelligent agents read the frontmatter (`name`, `description`) in `SKILL.md` to identify this Skill
2. Based on the usage instructions in `SKILL.md`, agents invoke `src/agnes_image.py` for content generation
3. Supports both text-to-image and image-to-image modes

## Features

### Currently Supported
- **Text-to-Image**: Generate images from text descriptions
- **Image-to-Image**: Modify existing images based on text prompts
- **Auto-organized output**: Images are automatically saved to categorized directories
- **Customizable parameters**: Model, size, quality, and more

### Future Extensions
- **Text-to-Video**: Generate videos from text descriptions
- **Video-to-Video**: Modify existing videos based on text prompts

## Quick Start

### 1. Install Dependencies

```bash
pip install openai requests
# Or use the provided dependencies file
pip install -r requirements.txt
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

### 3. Generate Media Content

```bash
# Text-to-Image (auto-saves to output/image/text-to-image/)
python src/agnes_image.py "a cat sitting on the moon, surreal art"

# Image-to-Image (auto-saves to output/image/image-to-image/)
python src/agnes_image.py "make it sunset style" -i input.jpg

# Custom output path (overrides default directory)
python src/agnes_image.py "a cute cat" -o custom/cat.png

# Custom model and size
python src/agnes_image.py "mountain landscape" --size 1024x512 --quality hd

# Provide API key inline
python src/agnes_image.py "a robot painting" --key sk-your-key
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

- `SKILL.md` - Skill definition file (includes frontmatter name/description and detailed usage guide)
- `src/agnes_image.py` - Main CLI script for image generation
- `requirements.txt` - Python dependencies
- `.env.example` - Example environment configuration
- `output/image/text-to-image/` - Default text-to-image output directory
- `output/image/image-to-image/` - Default image-to-image output directory

## License

MIT
