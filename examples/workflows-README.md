# ComfyUI Workflow Presets

This directory contains 4 curated workflow presets optimized for Discord guild use cases.

---

## Preset Workflows

### 1. portrait.json (512×768)
**Use Case:** Character portraits, member spotlights, profile images  
**Model:** SD 1.5  
**Generation Time:** ~30-60 seconds

**Recommended Prompts:**
- "Female night elf druid, silver hair, wise expression, forest background"
- "Male orc warrior, green skin, battle scars, determined look"

---

### 2. banner.json (1200×400)
**Use Case:** Event announcements, server headers, channel banners  
**Model:** SD 1.5 or SDXL  
**Generation Time:** ~45-90 seconds

**Recommended Prompts:**
- "Epic fantasy raid banner, Molten Core, fiery background"
- "Guild recruitment banner, heroic composition, vibrant"

---

### 3. recruitment.json (800×1000)
**Use Case:** Recruitment posters, call-to-action graphics  
**Model:** SDXL (higher quality)  
**Generation Time:** ~2-5 minutes

**Recommended Prompts:**
- "WoW guild recruitment poster, diverse heroes, epic landscape"
- "PvP tournament poster, intense combat, dynamic action"

---

### 4. emblem.json (512×512)
**Use Case:** Guild crests, role icons, reaction images, logos  
**Model:** SD 1.5  
**Generation Time:** ~20-30 seconds

**Recommended Prompts:**
- "Phoenix guild emblem, fiery wings, circular design, symmetrical"
- "Dragon crest, golden scales, heraldic style"

---

## Bring Your Own Workflow (BYOW)

1. Design workflow in ComfyUI web interface
2. Save in API format: Settings → Enable Dev mode → Save (API Format)
3. Place JSON file in this directory
4. Use via `generate_image(workflow="your-custom.json", prompt="...")`

**See [docs/COMFYUI_INTEGRATION.md](../docs/COMFYUI_INTEGRATION.md) for detailed BYOW guide.**

---

**Transform your community with AI-generated visuals.** 🎨
