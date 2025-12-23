<!-- Generated: 2025-12-23 | DDD Phase 1: Documentation Genesis -->

# ComfyUI Integration Guide

Transform your Discord community with AI-generated visual content. This guide covers the 4 curated workflow presets and the BYOW (Bring Your Own Workflow) infrastructure for custom image generation.

---

## Table of Contents

1. [Overview](#overview)
2. [Installation & Setup](#installation--setup)
3. [Preset Workflows](#preset-workflows)
4. [BYOW (Bring Your Own Workflow)](#byow-bring-your-own-workflow)
5. [Image Delivery Modes](#image-delivery-modes)
6. [Advanced Configuration](#advanced-configuration)
7. [Troubleshooting](#troubleshooting)

---

## Overview

### Philosophy: Curated Presets + BYOW Infrastructure

Discord Guildmaster MCP ships with **4 production-ready workflow presets** optimized for common guild use cases, plus robust infrastructure for loading **custom workflows** from your ComfyUI installation.

**Preset workflows solve 80% of use cases:**
- Character portraits for member spotlights
- Event banners for announcements
- Recruitment posters for growth campaigns
- Guild emblems for branding

**BYOW infrastructure handles the remaining 20%:**
- Custom art styles
- Specialized aspect ratios
- Advanced ComfyUI node configurations
- Community-specific visual themes

### Why ComfyUI?

- **Local execution**  No API keys, no usage limits, no cloud dependencies
- **Full control**  Customize models, LoRAs, controlnets, workflows
- **Privacy**  Your guild's visual content stays on your hardware
- **Cost-effective**  One-time GPU investment vs ongoing API costs

---

## Installation & Setup

### Prerequisites

1. **ComfyUI Server** running and accessible
   - Install from [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI)
   - Recommended: NVIDIA GPU with 8GB+ VRAM
   - Minimum: CPU-only (slow but functional)

2. **Base Models** downloaded to ComfyUI's `models/checkpoints/`:
   - **SD 1.5** (512×512, fast): `v1-5-pruned-emaonly.safetensors`
   - **SDXL** (1024×1024, high quality): `sd_xl_base_1.0.safetensors`

3. **Discord Guildmaster MCP** installed (see [INSTALLATION.md](./INSTALLATION.md))

### Quick Setup

#### 1. Start ComfyUI Server

```bash
# Navigate to ComfyUI installation
cd /path/to/ComfyUI

# Start server
python main.py

# Server will start at http://localhost:8188
```

#### 2. Configure Guildmaster MCP

Edit `.env` file:

```bash
# Enable ComfyUI integration
COMFYUI_ENABLED=true

# ComfyUI server connection
COMFYUI_HOST=localhost
COMFYUI_PORT=8188

# Workflow directory (default: ./workflows in project root)
COMFYUI_WORKFLOW_DIR=./workflows

# Image return mode (base64 works with localhost)
COMFYUI_RETURN_MODE=base64
```

#### 3. Verify Connection

```bash
# Run connection test
guildmaster test-comfyui

# Expected output:
#  ComfyUI server reachable at http://localhost:8188
#  Queue: 0 pending, 0 running
#  Device: cuda (24GB VRAM)
```

---

## Preset Workflows

The Guildmaster MCP ships with 4 curated workflows optimized for Discord communities.

### 1. Portrait (512×768)

**Use Case:** Character portraits, member spotlights, profile images

**Aspect Ratio:** 2:3 (portrait orientation)
**Resolution:** 512×768 pixels
**Model:** SD 1.5 (fast generation, ~30-60 seconds)
**Optimized For:** Face/character detail, close-ups

**Example Usage:**

```python
# Generate character portrait
portrait = generate_image(
    workflow="portrait",
    prompt="Female night elf druid, silver hair, wise expression, forest background, detailed face",
    negative_prompt="low quality, blurry, distorted, multiple heads"
)
```

**Recommended Prompts:**
- "Male orc warrior, green skin, battle scars, determined expression"
- "Human paladin, blonde hair, holy aura, plate armor, castle background"
- "Undead rogue, glowing eyes, shadowy cloak, mysterious atmosphere"

**Workflow Details:**
- **Sampler:** DPM++ 2M Karras (quality/speed balance)
- **Steps:** 25 (configurable)
- **CFG Scale:** 7.0
- **VAE:** Standard SD 1.5 VAE

---

### 2. Banner (1200×400)

**Use Case:** Event announcements, server headers, channel banners

**Aspect Ratio:** 3:1 (wide banner)
**Resolution:** 1200×400 pixels
**Model:** SD 1.5 or SDXL
**Optimized For:** Horizontal composition, text overlays, event branding

**Example Usage:**

```python
# Generate event banner
banner = generate_image(
    workflow="banner",
    prompt="Epic fantasy raid banner, Molten Core, fiery lava background, dramatic lighting",
    negative_prompt="text, watermark, low quality, portrait orientation"
)
```

**Recommended Prompts:**
- "Guild recruitment banner, heroic fantasy, epic composition, vibrant colors"
- "Weekly raid night announcement, dark portal, mystical energy, dramatic"
- "PvP tournament header, battleground, intense action, cinematic"

**Workflow Details:**
- **Sampler:** DPM++ SDE Karras (better for landscapes)
- **Steps:** 30
- **CFG Scale:** 7.5
- **Special:** Horizontal composition bias in prompts

---

### 3. Recruitment (800×1000)

**Use Case:** Recruitment posters, call-to-action graphics, guild promotions

**Aspect Ratio:** 4:5 (tall poster)
**Resolution:** 800×1000 pixels
**Model:** SDXL (higher quality for marketing materials)
**Optimized For:** Vertical posters, promotional content, high detail

**Example Usage:**

```python
# Generate recruitment poster
recruitment = generate_image(
    workflow="recruitment",
    prompt="Fantasy guild recruitment poster, heroic adventurers, epic battlefield, 'Join Us' energy",
    negative_prompt="text, logo, low quality, blurry"
)
```

**Recommended Prompts:**
- "WoW Classic guild recruitment, diverse races, united heroes, epic landscape"
- "Raid team recruiting poster, coordinated group, legendary weapons, powerful"
- "PvP guild poster, intense combat, Alliance vs Horde, dynamic action"

**Workflow Details:**
- **Sampler:** DPM++ 2M SDE Karras
- **Steps:** 40 (higher quality)
- **CFG Scale:** 8.0
- **Model:** SDXL recommended (fallback to SD 1.5 if VRAM limited)

---

### 4. Emblem (512×512)

**Use Case:** Guild crests, role icons, reaction images, logos

**Aspect Ratio:** 1:1 (square)
**Resolution:** 512×512 pixels
**Model:** SD 1.5 (fast, suitable for icons)
**Optimized For:** Centered subjects, icons, emblems, logos

**Example Usage:**

```python
# Generate guild emblem
emblem = generate_image(
    workflow="emblem",
    prompt="Phoenix guild emblem, fiery wings, circular design, heraldic style, symmetrical",
    negative_prompt="text, asymmetrical, complex background, low quality"
)
```

**Recommended Prompts:**
- "Dragon crest emblem, golden scales, circular frame, heraldic design"
- "Sword and shield icon, metallic, clean design, guild symbol"
- "Arcane magic symbol, glowing runes, mystical, centered composition"

**Workflow Details:**
- **Sampler:** Euler A (good for symmetrical designs)
- **Steps:** 20 (fast generation for iteration)
- **CFG Scale:** 7.0
- **Special:** Symmetry bias in workflow configuration

---

## BYOW (Bring Your Own Workflow)

For advanced users and custom use cases, load your own ComfyUI workflows.

### Exporting Workflows from ComfyUI

#### 1. Design Workflow in ComfyUI

1. Open ComfyUI web interface (`http://localhost:8188`)
2. Create your workflow using nodes
3. Test generation to ensure it works

#### 2. Enable API Format

1. Click **"Settings"** (gear icon, top-right)
2. Enable **"Enable Dev mode Options"**
3. Close settings

#### 3. Export Workflow

1. Click **"Save (API Format)"** button
2. Save as `my-workflow.json`

#### 4. Add to Workflows Directory

```bash
# Copy workflow to configured directory
cp ~/Downloads/my-workflow.json ./workflows/my-custom.json
```

### Workflow Requirements

Your workflow JSON must include:

1. **Text Input Nodes**  For prompt injection
   - Node type: `CLIPTextEncode`
   - The system automatically finds and injects your prompts

2. **Checkpoint Loader**  For model selection
   - Node type: `CheckpointLoaderSimple`
   - Ensure model exists in ComfyUI `models/checkpoints/`

3. **KSampler**  For generation
   - Node type: `KSampler` or `KSamplerAdvanced`
   - Seed randomization handled automatically (if `COMFYUI_RANDOMIZE_SEEDS=true`)

4. **VAE Decode + Save**  For output
   - Node types: `VAEDecode` ’ `SaveImage`

**Minimal workflow structure:**

```json
{
  "1": {
    "class_type": "CheckpointLoaderSimple",
    "inputs": {"ckpt_name": "v1-5-pruned-emaonly.safetensors"}
  },
  "2": {
    "class_type": "CLIPTextEncode",
    "inputs": {"text": "PROMPT_PLACEHOLDER", "clip": ["1", 1]}
  },
  "3": {
    "class_type": "CLIPTextEncode",
    "inputs": {"text": "NEGATIVE_PROMPT_PLACEHOLDER", "clip": ["1", 1]}
  },
  "4": {
    "class_type": "KSampler",
    "inputs": {
      "seed": 42,
      "steps": 20,
      "cfg": 7.0,
      "sampler_name": "euler",
      "scheduler": "normal",
      "denoise": 1.0,
      "model": ["1", 0],
      "positive": ["2", 0],
      "negative": ["3", 0],
      "latent_image": ["5", 0]
    }
  },
  "5": {
    "class_type": "EmptyLatentImage",
    "inputs": {"width": 512, "height": 512, "batch_size": 1}
  },
  "6": {
    "class_type": "VAEDecode",
    "inputs": {"samples": ["4", 0], "vae": ["1", 2]}
  },
  "7": {
    "class_type": "SaveImage",
    "inputs": {"filename_prefix": "guildmaster", "images": ["6", 0]}
  }
}
```

### Parameter Injection

The Guildmaster MCP automatically injects parameters into your workflow:

| Parameter | Injected Into | Node Type |
|-----------|---------------|-----------|
| `prompt` | `text` field | `CLIPTextEncode` (first instance) |
| `negative_prompt` | `text` field | `CLIPTextEncode` (second instance) |
| `seed` | `seed` field | `KSampler` (all instances) |
| `steps` | `steps` field | `KSampler` (all instances) |

**You don't need placeholders**  the system intelligently finds appropriate nodes.

### Using Custom Workflows

```python
# Use custom workflow by filename
result = generate_image(
    workflow="my-custom.json",
    prompt="Your custom prompt here",
    negative_prompt="low quality",
    steps=30,
    seed=42
)

# Or just the name (without .json extension)
result = generate_image(
    workflow="my-custom",
    prompt="..."
)
```

### Workflow Organization

Recommended directory structure:

```
workflows/
   portrait.json          # Preset
   banner.json            # Preset
   recruitment.json       # Preset
   emblem.json            # Preset
   custom-fantasy.json    # Your BYOW
   cyberpunk-style.json   # Your BYOW
   guild-specific.json    # Your BYOW
```

**Naming conventions:**
- Use lowercase with hyphens
- Descriptive names (not `workflow1.json`)
- Group by style or use case

---

## Image Delivery Modes

Choose how generated images are returned based on your infrastructure.

### Mode 1: base64 (Default)

**Best for:** Localhost ComfyUI, simple setups

**Configuration:**
```bash
COMFYUI_RETURN_MODE=base64
```

**Behavior:**
- Image encoded as base64 string
- Returned directly in API response
- Ready for Discord embedding

**Pros:**
-  Works with localhost ComfyUI (no public URL needed)
-  Simple configuration
-  Immediate availability

**Cons:**
- L Increases token usage (~30% overhead for base64 encoding)
- L Not suitable for very large images (>2MB)

**Example Response:**

```json
{
  "image": {
    "format": "base64",
    "data": "/9j/4AAQSkZJRgABAQAA...",
    "content_type": "image/png"
  }
}
```

**Discord Usage:**

```python
import base64
import io

# Get generated image
img = get_image(generation_id="...")

# Decode base64
img_data = base64.b64decode(img['image']['data'])
img_file = io.BytesIO(img_data)

# Send to Discord
send_message(
    channel_id="...",
    content="Check out this character portrait!",
    file=("portrait.png", img_file)
)
```

---

### Mode 2: url

**Best for:** Publicly accessible ComfyUI server

**Configuration:**
```bash
COMFYUI_RETURN_MODE=url
COMFYUI_HOST=comfyui.example.com  # Must be publicly reachable
```

**Behavior:**
- Returns direct URL to image on ComfyUI server
- Discord fetches and embeds image from URL

**Pros:**
-  Minimal token usage
-  Fast response (no encoding/decoding)
-  Discord handles embedding automatically

**Cons:**
- L Requires publicly accessible ComfyUI server
- L Discord cannot embed localhost URLs
- L Images may be deleted when ComfyUI clears output directory

**Example Response:**

```json
{
  "image": {
    "format": "url",
    "url": "http://comfyui.example.com/view?filename=guildmaster_00123.png"
  }
}
```

**Discord Usage:**

```python
# Get image URL
img = get_image(generation_id="...")

# Embed in Discord message
send_message(
    channel_id="...",
    embed={
        "title": "Character Portrait",
        "image": {"url": img['image']['url']}
    }
)
```

---

### Mode 3: cdn

**Best for:** Production deployments, persistence

**Configuration:**
```bash
COMFYUI_RETURN_MODE=cdn
COMFYUI_CDN_PROVIDER=s3  # Options: s3, r2, discord
COMFYUI_CDN_BUCKET=my-guild-images
COMFYUI_CDN_REGION=us-east-1
COMFYUI_CDN_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE
COMFYUI_CDN_SECRET_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

**Behavior:**
- Generated image uploaded to CDN (S3, Cloudflare R2, etc.)
- Returns public CDN URL
- Persistent storage (images not deleted)

**Pros:**
-  Works with localhost ComfyUI
-  Minimal token usage (just URL)
-  Persistent image hosting
-  CDN performance for Discord embedding
-  Archive of all generated images

**Cons:**
- L Requires CDN setup and credentials
- L Storage costs (usually minimal: ~$0.02/GB/month)
- L Additional configuration complexity

**Supported CDN Providers:**

| Provider | Setup Guide |
|----------|-------------|
| **AWS S3** | Create bucket, IAM user with S3 write permissions |
| **Cloudflare R2** | Create bucket, generate API token |
| **Discord CDN** | Upload as Discord attachment, use attachment URL |

**Example Response:**

```json
{
  "image": {
    "format": "cdn",
    "url": "https://my-guild-images.s3.amazonaws.com/portraits/abc123.png",
    "cdn_provider": "s3"
  }
}
```

**Discord Usage:**

```python
# Get CDN URL
img = get_image(generation_id="...")

# Embed in Discord (URL is persistent)
send_message(
    channel_id="...",
    embed={
        "title": "Character Portrait",
        "image": {"url": img['image']['url']},
        "footer": {"text": "Generated with ComfyUI"}
    }
)
```

---

## Advanced Configuration

### Seed Randomization

Control whether each generation uses a random seed or fixed seed.

```bash
# Random seeds (default) - each generation is unique
COMFYUI_RANDOMIZE_SEEDS=true

# Fixed seeds - reproducible generations
COMFYUI_RANDOMIZE_SEEDS=false
```

**When to use random:**
- Batch generation of character portraits
- Exploring variations of a prompt
- General use cases

**When to use fixed:**
- Iterating on a specific composition
- Debugging workflow issues
- Reproducible results for testing

### Generation Timeout

Set maximum time to wait for generation before failing.

```bash
# 5 minutes (good for SD 1.5)
COMFYUI_TIMEOUT=300

# 10 minutes (good for SDXL)
COMFYUI_TIMEOUT=600

# 15 minutes (for very complex workflows)
COMFYUI_TIMEOUT=900
```

**Tuning guidance:**
- SD 1.5 (20-30 steps): 1-2 minutes on GPU, 10-15 minutes on CPU
- SDXL (30-40 steps): 3-5 minutes on GPU, 30-60 minutes on CPU
- Complex workflows (ControlNet, multiple passes): Add 2-5 minutes

### Custom Models and LoRAs

To use custom models or LoRAs in your workflows:

1. **Download models** to ComfyUI directories:
   - Checkpoints: `ComfyUI/models/checkpoints/`
   - LoRAs: `ComfyUI/models/loras/`
   - VAEs: `ComfyUI/models/vae/`

2. **Reference in workflow JSON:**

```json
{
  "1": {
    "class_type": "CheckpointLoaderSimple",
    "inputs": {
      "ckpt_name": "my-custom-model.safetensors"
    }
  },
  "2": {
    "class_type": "LoraLoader",
    "inputs": {
      "lora_name": "fantasy-style-lora.safetensors",
      "strength_model": 0.8,
      "strength_clip": 0.8,
      "model": ["1", 0],
      "clip": ["1", 1]
    }
  }
}
```

3. **Use in generation:**

```python
result = generate_image(
    workflow="custom-with-lora.json",
    prompt="...",
    negative_prompt="..."
)
```

---

## Troubleshooting

### "Cannot connect to ComfyUI server"

**Symptoms:** `test_comfyui()` fails with connection error

**Solutions:**

1. **Verify ComfyUI is running:**
   ```bash
   curl http://localhost:8188
   # Should return ComfyUI web interface HTML
   ```

2. **Check host/port configuration:**
   ```bash
   # In .env
   COMFYUI_HOST=localhost
   COMFYUI_PORT=8188
   ```

3. **Firewall rules:**
   ```bash
   # Allow port 8188 (Linux)
   sudo ufw allow 8188
   ```

---

### "Workflow not found"

**Symptoms:** `generate_image()` fails with "Workflow 'X' not found"

**Solutions:**

1. **Verify file exists:**
   ```bash
   ls -la ./workflows/
   # Should show your workflow JSON files
   ```

2. **Check filename:**
   ```python
   # These are equivalent:
   generate_image(workflow="portrait")
   generate_image(workflow="portrait.json")
   ```

3. **Verify COMFYUI_WORKFLOW_DIR:**
   ```bash
   echo $COMFYUI_WORKFLOW_DIR
   # Should print ./workflows or your custom path
   ```

---

### "Generation timeout"

**Symptoms:** Generation exceeds configured timeout, fails

**Solutions:**

1. **Increase timeout:**
   ```bash
   COMFYUI_TIMEOUT=900  # 15 minutes
   ```

2. **Reduce workflow complexity:**
   - Lower `steps` parameter
   - Use faster sampler (Euler vs DPM++)
   - Reduce resolution
   - Remove expensive nodes (ControlNet, upscaling)

3. **Check GPU usage:**
   ```bash
   nvidia-smi
   # Should show ComfyUI process using GPU
   ```

---

### "Discord cannot embed image URL"

**Symptoms:** `url` mode returns URL, but Discord shows broken image

**Solutions:**

1. **Verify URL is publicly accessible:**
   ```bash
   curl -I http://comfyui.example.com/view?filename=...
   # Should return 200 OK
   ```

2. **Switch to base64 mode:**
   ```bash
   COMFYUI_RETURN_MODE=base64
   ```

3. **Use CDN mode for persistence:**
   ```bash
   COMFYUI_RETURN_MODE=cdn
   # Configure S3/R2 credentials
   ```

---

### "Out of VRAM"

**Symptoms:** ComfyUI crashes with CUDA out of memory error

**Solutions:**

1. **Use smaller models:**
   - SD 1.5 (~4GB VRAM) instead of SDXL (~8GB VRAM)

2. **Reduce resolution:**
   - 512×512 instead of 1024×1024
   - Modify workflow's `EmptyLatentImage` node

3. **Enable model offloading:**
   - ComfyUI settings ’ Enable "CPU Offload"
   - Slower but uses less VRAM

4. **Close other applications:**
   - Free up GPU memory

---

## Best Practices

### Prompt Engineering

**Good prompts for guild images:**

 **Specific, descriptive:**
```
"Female night elf druid, silver hair, wise expression,
detailed face, forest background, moonlight, fantasy art"
```

L **Vague, generic:**
```
"elf character"
```

 **Include style keywords:**
```
"..., digital painting, high detail, professional, 4k"
```

 **Use negative prompts:**
```
negative_prompt="low quality, blurry, distorted, watermark, text"
```

### Workflow Iteration

1. **Start with presets**  Validate use case before custom workflows
2. **Test in ComfyUI first**  Ensure workflow generates correctly
3. **Export and integrate**  Save API format, add to workflows/
4. **Iterate parameters**  Adjust steps, CFG, samplers for quality/speed

### Resource Management

- **Batch during off-hours**  Queue multiple generations when server idle
- **Monitor queue**  Check `test_comfyui()` for pending jobs
- **Clean output directory**  ComfyUI's `output/` fills up over time

---

<div align="center">

**ComfyUI integration complete. Transform your guild with AI-generated visuals. <¨**

</div>
