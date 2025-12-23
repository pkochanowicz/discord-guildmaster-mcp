<!-- Generated: 2025-12-23 | DDD Phase 1: Documentation Genesis -->

# Discord Guildmaster MCP

> Command your Discord realm through AI agents. Built for guild leaders, raid organizers, and community architects who value craft over convenience.

[![MCP](https://img.shields.io/badge/MCP-Server-5865F2?style=for-the-badge)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com)
[![License](https://img.shields.io/badge/License-AGPL%20v3-blue?style=for-the-badge)](./LICENSE)

**Discord Guildmaster MCP** is a production-ready Model Context Protocol (MCP) server that enables AI agents to manage Discord communities with precision and craft. Born from [The Chronicler](https://github.com/pkochanowicz/the_chronicler)—a WoW Classic+ guild bot—this standalone server brings sophisticated multi-agent orchestration to any Discord community.

---

## ⚔️ Quick Start (30 Seconds)

### Docker (Recommended)

```bash
docker run -d \
  --name guildmaster-mcp \
  -e DISCORD_TOKEN=your_bot_token \
  -e DISCORD_DEFAULT_GUILD_ID=your_guild_id \
  -p 8080:8080 \
  discord/guildmaster-mcp:latest
```

### Using `uv` (10-100x faster than pip)

```bash
uv pip install discord-guildmaster-mcp
export DISCORD_TOKEN=your_bot_token
guildmaster
```

**See [docs/INSTALLATION.md](./docs/INSTALLATION.md) for detailed setup instructions.**

---

## 🏰 Features

### 🎯 33 Precision-Crafted Tools

Organized into logical categories for efficient agent orchestration:

- **Guild Management** — Server info, audit logs, member operations
- **Role & Permission Control** — Assign, remove, query role hierarchies
- **Channel Operations** — Create, delete, organize channels and categories
- **Messaging & Communication** — Send, read, delete messages with embed support
- **Webhook Automation** — Custom identity messaging for advanced workflows
- **Forum & Thread Management** — Full support for modern Discord features
- **ComfyUI Integration** — Local AI image generation with curated presets
- **Utility & Diagnostics** — Connection testing, tool discovery

### 🤖 Agent-First Architecture

Designed for multi-agent workflows, not just single LLM interaction:

- **Token-efficient responses** — Pre-filtered data, paginated results
- **Tool annotations** — `readOnlyHint` and `destructiveHint` for agent safety
- **Default guild/channel IDs** — Reduce parameter overhead via environment config
- **Structured outputs** — JSON schemas optimized for LLM comprehension

### 🎨 Optional ComfyUI Integration

Transform your community with AI-generated visuals:

- **4 Curated Workflow Presets**:
  - `portrait.json` (512×768) — Character portraits, member spotlights
  - `banner.json` (1200×400) — Event announcements, server headers
  - `recruitment.json` (800×1000) — Recruitment posters, call-to-action graphics
  - `emblem.json` (512×512) — Guild crests, role icons, reaction images

- **BYOW (Bring Your Own Workflow)** — Drop custom ComfyUI workflows into `./workflows/` directory

See [docs/COMFYUI_INTEGRATION.md](./docs/COMFYUI_INTEGRATION.md) for setup and workflow documentation.

### 🎭 Themeable Architecture

Switch between personality modes without touching code:

- **Generic Mode** — Universal "gaming community" terminology (`send_message`, `list_members`)
- **WoW Mode** — Immersive World of Warcraft theming (`summon_herald`, `muster_roster`)
- **Custom Mode** — Fork-friendly theme layer for your own terminology

Configure via `.env`:
```bash
GUILDMASTER_THEME=generic  # Options: generic, wow, custom
```

See [docs/CONFIGURATION.md](./docs/CONFIGURATION.md) for theming options.

---

## 📦 Installation

### Prerequisites

- **Python 3.11+** (recommended: 3.12)
- **Discord Bot** with proper intents enabled (see [docs/INSTALLATION.md](./docs/INSTALLATION.md#discord-bot-setup))
- **Optional:** Docker, ComfyUI server for image generation

### Installation Methods

| Method | Speed | Use Case |
|--------|-------|----------|
| **`uv`** | ⚡️ Fastest | Development, local testing |
| **pip + venv** | ⚙️ Standard | Traditional Python workflow |
| **Docker** | 🐳 Containerized | Production, multi-service deployment |

**Complete installation guide:** [docs/INSTALLATION.md](./docs/INSTALLATION.md)

---

## 🛠️ Tool Categories

| Category | Tools | Description |
|----------|-------|-------------|
| **Guild Information** | 2 | Server metadata, audit logs |
| **Member Management** | 4 | List, search, get member details, ID lookup |
| **Role Operations** | 3 | List, assign, remove roles |
| **Channel Management** | 4 | Create/delete channels, categories |
| **Messaging** | 5 | Send, read, delete, react, DM |
| **Webhook Management** | 3 | Create, send, delete webhooks |
| **Forum Support** | 3 | Create posts, reply, retrieve threads |
| **Thread Management** | 2 | Create, archive threads |
| **ComfyUI Integration** | 4 | Generate images, list workflows, check status |
| **Utility** | 3 | Test connections, discover tools |

**Total: 33 tools** — See [docs/TOOLS_REFERENCE.md](./docs/TOOLS_REFERENCE.md) for complete documentation with parameter schemas and examples.

---

## 🤖 Agent Integration

### Claude Desktop Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "discord-guildmaster": {
      "command": "guildmaster",
      "env": {
        "DISCORD_TOKEN": "your_bot_token",
        "DISCORD_DEFAULT_GUILD_ID": "your_guild_id"
      }
    }
  }
}
```

### Cursor Configuration

Add to `.cursor/mcp-config.json`:

```json
{
  "discord-guildmaster": {
    "command": "uv",
    "args": ["run", "guildmaster"],
    "env": {
      "DISCORD_TOKEN": "your_bot_token",
      "DISCORD_DEFAULT_GUILD_ID": "your_guild_id"
    }
  }
}
```

### Multi-Agent Orchestration

Example workflow with specialized agents:

```yaml
# multi-agent-guild-manager.yaml
agents:
  - name: guild_manager
    tools: [get_guild_info, list_members, list_roles]
    role: "Guild operations and membership queries"

  - name: content_publisher
    tools: [send_message, create_webhook, send_webhook_message]
    role: "Content creation and announcement distribution"

  - name: visual_designer
    tools: [generate_image, get_generation_status, get_image]
    role: "ComfyUI image generation for events and recruitment"

  orchestrator:
    coordination: "Route tasks based on agent specialization"
    context_sharing: "Share guild_id and channel_id across agents"
```

**See [docs/MULTI_AGENT_WORKFLOWS.md](./docs/MULTI_AGENT_WORKFLOWS.md) for orchestration patterns and integration with The Chronicler.**

**Complete configuration examples:** [examples/](./examples/)

---

## 📚 Documentation

### User Documentation

- **[docs/INSTALLATION.md](./docs/INSTALLATION.md)** — Detailed setup for `uv`, pip, Docker
- **[docs/CONFIGURATION.md](./docs/CONFIGURATION.md)** — Environment variables, theming, ComfyUI setup
- **[docs/TOOLS_REFERENCE.md](./docs/TOOLS_REFERENCE.md)** — Complete tool inventory with schemas
- **[docs/COMFYUI_INTEGRATION.md](./docs/COMFYUI_INTEGRATION.md)** — Workflow presets and BYOW guide
- **[docs/MULTI_AGENT_WORKFLOWS.md](./docs/MULTI_AGENT_WORKFLOWS.md)** — Agent orchestration patterns
- **[docs/TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)** — Common issues and solutions

### Developer Documentation

- **[docs/architecture.md](./docs/architecture.md)** — System design and data flow
- **[docs/api-internals.md](./docs/api-internals.md)** — Internal API and extension points
- **[docs/theming-guide.md](./docs/theming-guide.md)** — Creating custom themes
- **[docs/CONTRIBUTING.md](./docs/CONTRIBUTING.md)** — Development setup and PR process
- **[docs/CHANGELOG.md](./docs/CHANGELOG.md)** — Version history

---

## 📜 From The Chronicler

Discord Guildmaster MCP is a strategic spinoff from **[The Chronicler](https://github.com/pkochanowicz/the_chronicler)**, the arcane heart of the *Azeroth Bound* World of Warcraft Classic+ guild. The Chronicler handles character registration, guild banking, talent validation, and ceremonial workflows—powered by PostgreSQL and FastAPI webhooks.

### Integration with The Chronicler

The Guildmaster MCP serves as **The Chronicler's Discord interface layer**, enabling:

- **Agent-driven character registration** — Multi-step flows coordinated by specialized agents
- **Guild bank operations** — Query deposits, check balances, automation triggers
- **Cemetery notifications** — Post burial rites to memorial channels
- **Talent validation workflows** — Audit builds against Classic+ rules

**Integration guide:** [docs/MULTI_AGENT_WORKFLOWS.md](./docs/MULTI_AGENT_WORKFLOWS.md#the-chronicler-integration)

---

## 🔧 Development

### Quick Development Setup

```bash
# Clone repository
git clone https://github.com/your-org/discord-guildmaster-mcp.git
cd discord-guildmaster-mcp

# Install with dev dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Start server
guildmaster
```

### Technology Stack

- **Python 3.11+** — Modern async/await patterns
- **discord.py 2.3+** — Official Discord API library
- **MCP SDK** — Model Context Protocol implementation
- **httpx** — Async HTTP client for ComfyUI integration
- **Pydantic** — Data validation and settings management
- **pytest** — Comprehensive test suite

**See [docs/CONTRIBUTING.md](./docs/CONTRIBUTING.md) for development guidelines.**

---

## 🛡️ License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

**What this means:**
- ✅ Free to use, modify, and distribute
- ✅ Commercial use allowed
- ⚠️ **If you modify and deploy as a network service, you must share your modifications**
- ⚠️ Derivative works must also be AGPL-3.0

This license prevents corporate extraction while encouraging genuine community contribution. Build on this, but share what you build.

**Full license:** [LICENSE](./LICENSE)

---

## 🤝 Community

- **Issues & Bug Reports:** [GitHub Issues](https://github.com/your-org/discord-guildmaster-mcp/issues)
- **Feature Requests:** [GitHub Discussions](https://github.com/your-org/discord-guildmaster-mcp/discussions)
- **The Chronicler Discord:** [Azeroth Bound](https://discord.gg/fJDzq5rfAK)

---

## 🏆 Success Metrics

A guild leader should be able to:

1. ✅ **Install and configure** the server in < 10 minutes
2. ✅ **Understand all 33 tools** without reading source code
3. ✅ **Set up ComfyUI integration** with presets or BYOW workflows
4. ✅ **Configure multi-agent workflows** for orchestration
5. ✅ **Customize theming** for their community
6. ✅ **Troubleshoot independently** using comprehensive documentation
7. ✅ **Contribute confidently** with clear development guidelines

---

<div align="center">

*Built with craft for communities that value quality over convenience.*

**For the guilds. For the communities. For the craft. ⚔️**

</div>
