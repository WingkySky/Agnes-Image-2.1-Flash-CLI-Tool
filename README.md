<div align="right">

  [**English**](README.md) · [中文](README_zh.md)

</div>

# 🎨 Agnes Media Create

**Skill Name**: `agnes-media-create`

A modular CLI toolkit for generating media content using the **Agnes Image 2.1 Flash** and **Agnes Video V2.0** APIs. Supports text-to-image, image-to-image, text-to-video, and image-to-video (including multi-image and keyframe animation modes).

**The entire folder functions as a standalone Skill that can be invoked by intelligent agents.**

## Project Structure (Standard Skill Layout)

```
Skill Root/ (The entire folder is invoked as a Skill)
├── SKILL.md                      # Skill definition file (with frontmatter and usage guide)
├── README.md                     # Project documentation (English) — this file
├── README_zh.md                  # Project documentation (Chinese)
├── requirements.txt              # Python dependencies
├── .env.example                  # Example environment variables
├── .env                          # Optional: local API Key config (auto-loaded, no export needed)
├── src/
│   ├── agnes_common.py           # Common module: .env loading / HTTP / download / path
│   ├── agnes_image_common.py     # Image API encapsulation
│   ├── agnes_video_common.py     # Video API encapsulation (async task + polling)
│   ├── agnes_text_to_image.py    # Standalone Text-to-Image script
│   ├── agnes_image_to_image.py   # Standalone Image-to-Image script
│   ├── agnes_text_to_video.py    # Standalone Text-to-Video script
│   └── agnes_image_to_video.py   # Standalone Image-to-Video script (multi-image / keyframes)
└── output/
    ├── image/text-to-image/      # Text-to-Image output directory
    ├── image/image-to-image/     # Image-to-Image output directory
    ├── video/text-to-video/      # Text-to-Video output directory
    └── video/image-to-video/     # Image-to-Video output directory
```

## How It Works

1. Intelligent agents read the frontmatter (`name`, `description`) in `SKILL.md` to identify this Skill
2. Based on the usage instructions in `SKILL.md`, agents invoke the appropriate standalone script for content generation
3. The project uses a three-layer modular design: common utilities → API-specific encapsulation → CLI scripts

## Features

### Currently Supported
- **Text-to-Image**: Generate images from text descriptions
- **Image-to-Image**: Modify existing images based on text prompts + input image
- **Text-to-Video**: Generate videos from text descriptions (async task with auto-polling)
- **Image-to-Video**: Generate videos from input images + text prompts, supporting:
  - Single-image mode
  - Multi-image mode
  - Keyframe animation mode

## Architecture Design

```
agnes_text_to_image.py
agnes_image_to_image.py  }  Standalone function scripts (CLI layer)
agnes_text_to_video.py
agnes_image_to_video.py

         │
         ▼

agnes_image_common.py    }  API-specific encapsulation (Business logic layer)
agnes_video_common.py

         │
         ▼

agnes_common.py          }  Common utilities (Foundation layer)
```

- **Foundation layer (`agnes_common.py`)**: `.env` auto-loading, API Key retrieval, HTTP requests, file downloading, path management, parameter validation — shared by all scripts.
- **Business logic layer (`agnes_image_common.py` / `agnes_video_common.py`)**: Encapsulates image/video API flows, response parsing, and parameter validation (such as the video `8n+1` rule).
- **CLI layer (four standalone scripts)**: Each script only parses command-line arguments and calls the corresponding business logic — one script does one thing.

## Quick Start

### 1. Install Dependencies

Only Python 3.8+ and `requests` are needed:

```bash
cd /path/to/Agnes-Media-Create
pip install requests
# Or use the provided requirements file
pip install -r requirements.txt
```

### 2. Set API Key

Get your API key from: https://platform.agnes-ai.com

There are three ways to configure it — priority order: CLI argument > environment variable > `.env` file.

**Option A: Use a `.env` file (Recommended)**

```bash
cp .env.example .env
# Edit .env and add:
# AGNES_API_KEY=sk-your-key-here
```

Scripts automatically search the project directory for a `.env` file and load it — no manual `export` needed.

**Option B: Environment variable**

```bash
export AGNES_API_KEY='your-api-key'
```

**Option C: Command-line argument**

```bash
python src/agnes_text_to_image.py "a prompt" --key 'your-api-key'
```

### 3. Generate Media Content

#### Text-to-Image

```bash
# Basic usage (auto-saves to output/image/text-to-image/)
python src/agnes_text_to_image.py "a cat sitting on the moon, surreal art"

# Custom output path
python src/agnes_text_to_image.py "a cute puppy" -o custom/puppy.png

# Custom model and size
python src/agnes_text_to_image.py "mountain landscape" --size 1024x512 --quality hd

# Inline API key
python src/agnes_text_to_image.py "a robot painting" --key sk-your-key
```

#### Image-to-Image

```bash
# With a local file (auto-converted to base64)
python src/agnes_image_to_image.py "make it sunset style" -i input.jpg

# With a public URL
python src/agnes_image_to_image.py "turn this into an oil painting" -i https://example.com/img.jpg
```

#### Text-to-Video

Video generation is an **async task** — scripts automatically poll and wait (usually 1–3 minutes).

```bash
# Basic: ~5s short video, 121 frames / 24 fps
python src/agnes_text_to_video.py "A young swordsman in flowing ancient robes running through a neon-lit modern city" \
    --num-frames 121 --frame-rate 24

# ~10s video with higher resolution
python src/agnes_text_to_video.py "A unicorn running across rainbow mountains" \
    --width 1280 --height 720 --num-frames 241 --frame-rate 24
```

#### Image-to-Video

Supports three input modes:
- **Single image**: `--image URL`
- **Multiple images**: `--image URL1 --image URL2`
- **Keyframe animation**: `--image URL1 --image URL2 --keyframes`

```bash
# Single image → video
python src/agnes_image_to_video.py "character slowly turning to look back" \
    --image https://example.com/portrait.png

# Multiple images → video
python src/agnes_image_to_video.py "smooth transition" \
    --image https://example.com/a.png --image https://example.com/b.png

# Keyframe animation
python src/agnes_image_to_video.py "smooth morph" \
    --image https://example.com/kf1.png --image https://example.com/kf2.png \
    --keyframes
```

> **Note**: Agnes Video API's image-to-video requires **publicly accessible image URLs**. Local file paths are not supported.

## Output Directory Structure

```
output/
├── image/
│   ├── text-to-image/          # Text-to-Image outputs
│   │   ├── t2i_20260607_155007.png
│   │   └── ...
│   └── image-to-image/         # Image-to-Image outputs
│       ├── i2i_20260607_155204.png
│       └── ...
└── video/
    ├── text-to-video/          # Text-to-Video outputs
    │   ├── t2v_20260607_161011.mp4
    │   └── ...
    └── image-to-video/         # Image-to-Video outputs
        ├── i2v_20260607_161203.mp4
        └── ...
```

- Files are named using timestamps
- Use `-o` or `--output` to specify a custom output path (skips the category directory)

## Complete Parameter Reference

| Flag | Scope | Description | Default |
|------|-------|-------------|---------|
| `prompt` | All | Text prompt (positional argument) | required |
| `-o, --output` | All | Output file path | auto-generated in category dir |
| `-k, --key` | All | API Key | `AGNES_API_KEY` env var / `.env` |
| `--model` | All | Model name | Image: `agnes-image-2.1-flash` / Video: `agnes-video-v2.0` |
| `-s, --size` | Image scripts | Image size, e.g. `1024x1024` | `1024x1024` |
| `-q, --quality` | Image scripts | Quality: `standard` / `hd` | `standard` |
| `-f, --format` | Image scripts | Response format: `url` / `b64` | `url` |
| `-i, --image` | Image-to-Image / Image-to-Video | Input image (path or URL — video scripts require URL) | none |
| `--num-frames` | Video scripts | Total frames (must satisfy `8n+1`) | `121` |
| `--frame-rate` | Video scripts | Frame rate 1–60 | `30` |
| `--width / --height` | Video scripts | Video resolution | `1152 / 768` |
| `--seed` | Video scripts | Random seed (optional) | none |
| `--keyframes` | Image-to-Video | Enable keyframe animation mode | off |
| `--poll-interval` | Video scripts | Polling interval in seconds | `5` |
| `--max-wait` | Video scripts | Maximum wait time in seconds | `600` |

## API Details

### Image API
- **Base URL**: `https://apihub.agnes-ai.com/v1`
- **Endpoint**: `POST /v1/images/generations`
- **Model**: `agnes-image-2.1-flash`
- **Auth**: Bearer token via `Authorization: Bearer $AGNES_API_KEY`
- **Format**: OpenAI-compatible API

### Video API
- **Base URL**: `https://api.agnes-ai.com/v1/videos`
- **Model**: `agnes-video-v2.0`
- **Flow**:
  1. `POST /v1/videos/generations` to create an async task, returns `task_id` / `video_id`
  2. `GET /v1/videos/{video_id}` to poll the result
  3. Status progresses: `in_progress` → `completed`
  4. Download the video from the returned URL
- **Auth**: Bearer token via `Authorization: Bearer $AGNES_API_KEY`

## Supported Image Sizes

- 1024x1024 (square)
- 512x512 (small square)
- 1024x512 (landscape)
- 512x1024 (portrait)

## Video Frame Count Constraint

Video `num_frames` must satisfy `8n + 1` and `≤ 441`. Examples:

| n | num_frames | Approx. duration (24fps) |
|---|------------|-------------------------|
| 1 | 9 | 0.375s |
| 4 | 33 | 1.375s |
| 6 | 49 | 2.0s |
| 10 | 81 | 3.375s |
| 15 | 121 | 5.0s |
| 30 | 241 | 10.0s |
| 55 | 441 | 18.375s |

Scripts automatically validate this — if violated, the script exits with a clear error message and suggested values.

## Requirements

- Python 3.8+
- requests

## File Overview

- `SKILL.md` — Skill definition file (frontmatter name/description + detailed usage guide)
- `src/agnes_common.py` — Foundation utilities shared by all scripts
- `src/agnes_image_common.py` — Image API encapsulation
- `src/agnes_video_common.py` — Video API encapsulation
- `src/agnes_text_to_image.py` — Text-to-Image standalone script
- `src/agnes_image_to_image.py` — Image-to-Image standalone script
- `src/agnes_text_to_video.py` — Text-to-Video standalone script
- `src/agnes_image_to_video.py` — Image-to-Video standalone script (supports multi-image / keyframes)
- `requirements.txt` — Python dependencies
- `.env.example` — Example environment configuration

## Usage Examples

### Example 1: Text-to-Image

```bash
python src/agnes_text_to_image.py "A majestic snow mountain at sunrise, oil painting style"
```

Output:
```
🎨 Creating image...
   Model: agnes-image-2.1-flash  Size: 1024x1024  Quality: standard
✅ Saved to: output/image/text-to-image/t2i_20260607_155007.png
```

### Example 2: Image-to-Image

```bash
python src/agnes_image_to_image.py "Add a cute kitten next to the puppy" -i output/image/text-to-image/t2i_20260607_155007.png
```

Output:
```
🎨 Creating image-to-image...
   Model: agnes-image-2.1-flash  Size: 1024x1024  Quality: standard
   Input image: output/image/text-to-image/t2i_20260607_155007.png
✅ Saved to: output/image/image-to-image/i2i_20260607_155204.png
```

### Example 3: Text-to-Video

```bash
python src/agnes_text_to_video.py "A young swordsman in flowing robes running through a neon-lit modern city skyscrapers, cinematic widescreen, 24fps" \
    --num-frames 121 --frame-rate 24 --width 1152 --height 768
```

Output:
```
🎬 Text-to-Video task
   Prompt: A young swordsman in flowing robes running through a neon-lit modern city...
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

## Notes

- Project root directory: `/Users/skywing/Documents/Agnes-Media-Create`
- Video generation is an **async task**; scripts automatically poll and wait, typically taking 1–3 minutes
- Image-to-Video input images must be **publicly accessible URLs** — local file uploads are not supported by the API
- It's recommended to store your API Key in a `.env` file to avoid leaking it in command history

## License

MIT
