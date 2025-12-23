<!-- Generated: 2025-12-23 | DDD Phase 1: Documentation Genesis -->

# Installation Guide

This guide walks you through installing **Discord Guildmaster MCP** using your preferred method. Choose the path that best fits your workflow.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Discord Bot Setup](#discord-bot-setup)
3. [Installation Methods](#installation-methods)
   - [Method 1: uv (Recommended)](#method-1-uv-recommended)
   - [Method 2: pip + Virtual Environment](#method-2-pip--virtual-environment)
   - [Method 3: Docker](#method-3-docker)
4. [Configuration](#configuration)
5. [Verification](#verification)
6. [Next Steps](#next-steps)

---

## Prerequisites

### System Requirements

- **Python 3.11 or higher** (recommended: Python 3.12)
  - Check version: `python3 --version`
  - Install from [python.org](https://www.python.org/downloads/) if needed

- **Git** (for cloning repository)
  - Check version: `git --version`

- **Discord Account** with permissions to:
  - Create applications at [Discord Developer Portal](https://discord.com/developers/applications)
  - Add bots to servers with proper intents

### Optional Requirements

- **Docker** (for containerized deployment)
  - Install from [docker.com](https://www.docker.com/get-started)

- **ComfyUI Server** (for AI image generation)
  - See [COMFYUI_INTEGRATION.md](./COMFYUI_INTEGRATION.md) for setup

---

## Discord Bot Setup

### Step 1: Create Discord Application

1. Visit [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"**
3. Name your application (e.g., "Guildmaster MCP")
4. Click **"Create"**

### Step 2: Create Bot User

1. Navigate to **"Bot"** tab in left sidebar
2. Click **"Add Bot"**
3. Confirm by clicking **"Yes, do it!"**
4. Under **"Token"**, click **"Reset Token"** and copy it
   - **  IMPORTANT:** Save this token securely. You'll need it for configuration.
   - Never share your token publicly or commit it to version control

### Step 3: Enable Privileged Intents

The bot requires these intents to function properly:

1. Scroll down to **"Privileged Gateway Intents"**
2. Enable the following:
   -  **Presence Intent** (for member status)
   -  **Server Members Intent** (for member list, search)
   -  **Message Content Intent** (for reading message history)

### Step 4: Configure Bot Permissions

1. Navigate to **"OAuth2"** ’ **"URL Generator"**
2. Under **"Scopes"**, select:
   -  `bot`
   -  `applications.commands`

3. Under **"Bot Permissions"**, select:
   -  **Manage Channels** (create/delete channels)
   -  **Manage Roles** (assign/remove roles)
   -  **Manage Webhooks** (create/send webhooks)
   -  **Read Messages/View Channels**
   -  **Send Messages**
   -  **Manage Messages** (delete, pin)
   -  **Embed Links**
   -  **Attach Files**
   -  **Read Message History**
   -  **Add Reactions**
   -  **Manage Threads** (create/archive)

4. Copy the generated URL at the bottom
5. Open URL in browser and add bot to your server

### Step 5: Get Guild ID (Server ID)

1. Open Discord desktop/web app
2. Enable **Developer Mode**:
   - Settings ’ Advanced ’ Developer Mode (toggle on)
3. Right-click your server icon ’ **"Copy Server ID"**
4. Save this ID for configuration

---

## Installation Methods

### Method 1: uv (Recommended)

**Why `uv`?** It's 10-100x faster than pip, handles Python version management, and produces cleaner dependency resolution.

#### Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

#### Install Discord Guildmaster MCP

```bash
# Install from PyPI (when published)
uv pip install discord-guildmaster-mcp

# OR: Install from source (development)
git clone https://github.com/your-org/discord-guildmaster-mcp.git
cd discord-guildmaster-mcp
uv pip install -e .

# For development with optional dependencies
uv pip install -e ".[dev,comfyui]"
```

#### Verify Installation

```bash
guildmaster --version
```

---

### Method 2: pip + Virtual Environment

Traditional Python workflow using pip and virtual environments.

#### Create Virtual Environment

```bash
# Clone repository
git clone https://github.com/your-org/discord-guildmaster-mcp.git
cd discord-guildmaster-mcp

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate

# Verify activation (should show path to venv)
which python  # macOS/Linux
where python  # Windows
```

#### Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install package
pip install .

# OR: Install from PyPI (when published)
pip install discord-guildmaster-mcp

# For development with optional dependencies
pip install -e ".[dev,comfyui]"
```

#### Verify Installation

```bash
guildmaster --version
```

---

### Method 3: Docker

Containerized deployment for production environments.

#### Quick Start (Docker Run)

```bash
# Pull image (when published)
docker pull discord/guildmaster-mcp:latest

# Run server
docker run -d \
  --name guildmaster-mcp \
  -e DISCORD_TOKEN=your_bot_token_here \
  -e DISCORD_DEFAULT_GUILD_ID=your_guild_id_here \
  -p 8080:8080 \
  --restart unless-stopped \
  discord/guildmaster-mcp:latest
```

#### Docker Compose (Recommended for Production)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  guildmaster:
    image: discord/guildmaster-mcp:latest
    container_name: guildmaster-mcp
    env_file:
      - .env
    volumes:
      - ./config:/app/config:ro
      - ./workflows:/app/workflows:ro
    ports:
      - "8080:8080"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import discord; print('ok')"]
      interval: 60s
      timeout: 10s
      retries: 3

  # Optional: ComfyUI service
  comfyui:
    image: comfyui/comfyui:latest
    profiles: ["gpu"]
    ports:
      - "8188:8188"
    volumes:
      - ./models:/app/models
      - ./outputs:/app/outputs
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

#### Start Services

```bash
# Start Guildmaster only
docker-compose up -d

# Start with ComfyUI (requires GPU)
docker-compose --profile gpu up -d

# View logs
docker-compose logs -f guildmaster

# Stop services
docker-compose down
```

#### Build from Source

```bash
# Clone repository
git clone https://github.com/your-org/discord-guildmaster-mcp.git
cd discord-guildmaster-mcp

# Build image
docker build -t discord-guildmaster-mcp:local .

# Run local image
docker run -d \
  --name guildmaster-mcp \
  --env-file .env \
  -p 8080:8080 \
  discord-guildmaster-mcp:local
```

---

## Configuration

### Create Environment File

Copy the example configuration and customize it:

```bash
# Copy template
cp .env.example .env

# Edit with your favorite editor
nano .env  # or vim, code, etc.
```

### Minimal Configuration

At minimum, set these variables in `.env`:

```bash
# Required: Discord bot token from Developer Portal
DISCORD_TOKEN=your_bot_token_here

# Recommended: Default guild ID to reduce per-call parameters
DISCORD_DEFAULT_GUILD_ID=your_guild_id_here
```

### Complete Configuration Options

See [CONFIGURATION.md](./CONFIGURATION.md) for comprehensive environment variable documentation, including:

- Theming options (generic, WoW, custom)
- ComfyUI integration settings
- Transport configuration (stdio vs HTTP)
- Token efficiency settings
- Logging and debugging

---

## Verification

### Test Discord Connection

```bash
# Run connection test tool
guildmaster test-connection

# Expected output:
#  Connected to Discord
#  Bot username: YourBotName#1234
#  Default guild: YourGuildName (ID: 123456789)
#  Bot has required permissions
```

### Test Tool Discovery

```bash
# List available tools
guildmaster list-tools

# Expected output: List of 33 tools organized by category
```

### Interactive REPL Mode (Development)

```bash
# Start interactive REPL for tool exploration
guildmaster-cli

# Try a test command
>>> get_guild_info(guild_id="your_guild_id")
```

---

## Next Steps

### For Users

1. **Configure environment variables**  [CONFIGURATION.md](./CONFIGURATION.md)
2. **Explore tools**  [TOOLS_REFERENCE.md](./TOOLS_REFERENCE.md)
3. **Set up agent integration**  [README.md#agent-integration](./README.md#agent-integration)
4. **Optional: ComfyUI setup**  [COMFYUI_INTEGRATION.md](./COMFYUI_INTEGRATION.md)

### For Developers

1. **Read architecture docs**  [docs/architecture.md](./docs/architecture.md)
2. **Study internal APIs**  [docs/api-internals.md](./docs/api-internals.md)
3. **Set up development environment**  [CONTRIBUTING.md](./CONTRIBUTING.md)
4. **Run test suite**  `pytest tests/`

---

## Troubleshooting

### Common Installation Issues

#### "Python 3.11+ required"

```bash
# Check current version
python3 --version

# Install Python 3.12 via uv
uv python install 3.12

# Use uv to run with specific version
uv run --python 3.12 guildmaster
```

#### "ModuleNotFoundError: No module named 'discord'"

This usually means the virtual environment isn't activated or dependencies weren't installed:

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate   # Windows

# Reinstall dependencies
pip install -e .
```

#### "Permission denied" errors

```bash
# Use --user flag (if not using virtual environment)
pip install --user discord-guildmaster-mcp

# OR: Fix permissions on Linux/macOS
sudo chown -R $USER ~/.local
```

#### Docker: "Cannot connect to Discord"

Check that your `.env` file is being loaded:

```bash
# Verify environment variables inside container
docker exec guildmaster-mcp env | grep DISCORD

# If empty, ensure docker-compose.yml has env_file configured
# OR: Pass variables explicitly via -e flags
```

### Getting Help

- **Troubleshooting Guide:** [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
- **GitHub Issues:** [Report a bug](https://github.com/your-org/discord-guildmaster-mcp/issues)
- **Discord Community:** [Azeroth Bound](https://discord.gg/fJDzq5rfAK)

---

<div align="center">

**Installation complete! Ready to command your Discord realm. ”**

</div>
