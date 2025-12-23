# Discord Guildmaster MCP: Repository Documentation Blueprint

The path forward is clear: build a **dual-distribution architecture** with a generic core and optional WoW theming layer, position the server primarily as an agent-orchestration tool with CLI as secondary, and implement ComfyUI as a modular "bring your own workflow" system. This approach maximizes longevity while honoring the craft.

---

## Strategic recommendations: The three decisions

### Decision 1: Theming scope — Fork-ready dual distribution

**Recommendation: Generic core with theming layer architecture.** Build the repository with a clean separation: a `discord-guildmaster-mcp` core package using universal "gaming community" language, with an optional `wow-theming` extension that wraps tools with immersive terminology.

The rationale is practical. Examining SaseQ/discord-mcp (130 stars) and slimslenderslacks/mcp-discord (10K+ Docker pulls) reveals that **universal naming wins adoption**. However, the WoW theming represents genuine craft and personality that shouldn't be abandoned.

Implement this through configuration:
```yaml
# .env or config.yaml
GUILDMASTER_THEME: "wow"  # Options: generic, wow, custom
```

The generic mode uses `send_message`, `list_members`, `create_channel`. WoW mode wraps these as `summon_herald`, `muster_roster`, `forge_chamber`. Both use identical underlying code. This approach lets The Chronicler maintain its immersive personality while the standalone repo builds broader adoption. Users fork and customize the theme layer without touching core functionality.

### Decision 2: ComfyUI workflow scope — Curated presets with BYOW foundation

**Recommendation: Ship 4 production-ready workflow presets with robust BYOW infrastructure.** Analysis of joenorton/comfyui-mcp-server and competing implementations reveals the "bring your own workflow" pattern works well, but pure BYOW intimidates non-technical users.

**Ship these 4 preset workflows:**

| Workflow | Aspect Ratio | Use Case |
|----------|--------------|----------|
| `portrait.json` | 512×768 | Character portraits, member spotlights |
| `banner.json` | 1200×400 | Event announcements, server headers |
| `recruitment.json` | 800×1000 | Recruitment posters, call-to-action graphics |
| `emblem.json` | 512×512 | Guild crests, role icons, reaction images |

**BYOW documentation should cover:**
- How to export workflows in ComfyUI API format (dev mode → Save API Format)
- Parameter injection points (KSampler → CLIPTextEncode for prompts)
- The `workflows/` directory convention
- Environment variable: `COMFYUI_WORKFLOW_DIR`

**Critical implementation detail:** Don't return raw ComfyUI URLs. Discord can't embed images from localhost. Implement the alecc08 pattern: HTTP proxy with disk cache, then either return base64 or upload to configured CDN (S3, Cloudflare R2, Discord's own attachment API).

### Decision 3: Agent orchestration vs direct use — 70/30 agent-first

**Recommendation: Document as agent-first (70%) with CLI as power-user escape hatch (30%).** The MCP ecosystem is fundamentally about LLM tool use. Token efficiency matters. Structured outputs matter. The slimslenderslacks implementation consuming 47.9k tokens (24% of context) just for tool definitions is a cautionary tale.

**Agent-first design principles:**
- Tool descriptions written for LLM comprehension, not human readability
- Pre-filtered responses (don't return raw Discord API payloads)
- Pagination built into every list operation
- Default guild/channel IDs via `.env` to reduce parameter overhead
- Tool annotations (`readOnlyHint`, `destructiveHint`) for agent safety

**CLI documentation as secondary:**
- Quick reference for debugging and testing
- Interactive REPL mode for tool exploration
- `--dry-run` flags for safe experimentation
- Primarily serves developers, not end users

Multi-agent workflow emphasis is correct. The Agents.md pattern from The Chronicler (if preserved) should be the default mental model: specialized agents for member management, channel operations, and content generation, coordinated by an orchestrator.

---

## Feature inventory: What discord-guildmaster-mcp should offer

### Core Discord operations (18 tools)

**Guild information:**
- `get_guild_info` — Server metadata, member count, features
- `get_audit_log` — Recent administrative actions (paginated)

**Member management:**
- `list_members` — Paginated roster with role filtering
- `get_member` — Single member details (join date, roles, status)
- `search_members` — Find by name, nickname, role
- `get_user_id_by_name` — Convert display name to mention format (from SaseQ)

**Role operations:**
- `list_roles` — Role hierarchy with permissions summary
- `assign_role` — Add role to member
- `remove_role` — Remove role from member

**Channel management:**
- `list_channels` — Full channel structure with categories
- `create_channel` — Text channel with optional category placement
- `delete_channel` — With audit reason parameter
- `create_category` — Organizational container

**Messaging:**
- `send_message` — Channel message with optional embed support
- `read_messages` — Channel history (paginated, **essential**)
- `delete_message` — With audit reason
- `add_reaction` — Emoji reactions
- `send_dm` — Private message to user

### Extended operations (8 tools)

**Webhook management:**
- `create_webhook` — Custom identity for automated messages
- `send_webhook_message` — Message with custom name/avatar
- `delete_webhook` — Cleanup

**Forum support (differentiator from competitors):**
- `create_forum_post` — With tags support
- `reply_to_forum` — Thread responses
- `get_forum_post` — Post content and replies

**Thread management:**
- `create_thread` — Start discussion from message
- `archive_thread` — Clean up completed discussions

### ComfyUI integration (4 tools)

- `generate_image` — Text-to-image with workflow selection
- `list_workflows` — Discover available workflow presets
- `get_generation_status` — Check queue position/completion
- `get_image` — Retrieve generated image (base64 or URL)

### Utility tools (3 tools)

- `test_connection` — Verify Discord bot connectivity
- `test_comfyui` — Verify ComfyUI server accessibility
- `list_available_tools` — Dynamic tool discovery for agents

**Total: ~33 tools** organized into logical groups. This exceeds SaseQ (23) while remaining more focused than @iqai (87+). The sweet spot for usability without overwhelming LLM context.

---

## Documentation structure blueprint

### Recommended file hierarchy

```
discord-guildmaster-mcp/
├── README.md                    # Quick start, feature overview, badges
├── INSTALLATION.md              # Detailed setup (uv, pip, Docker)
├── CONFIGURATION.md             # All env vars, .env patterns, themes
├── TOOLS_REFERENCE.md           # Complete tool documentation
├── COMFYUI_INTEGRATION.md       # Workflow setup, BYOW guide
├── MULTI_AGENT_WORKFLOWS.md     # Orchestration patterns, agent definitions
├── DEPLOYMENT.md                # Docker-compose, production hardening
├── TROUBLESHOOTING.md           # Common issues, Discord intents, permissions
├── CONTRIBUTING.md              # Development setup, PR process
├── CHANGELOG.md                 # Semantic versioned history
├── LICENSE                      # GNU AGPL v3.0
│
├── docs/
│   ├── architecture.md          # System design, data flow diagrams
│   ├── api-internals.md         # For contributors
│   └── theming-guide.md         # How to create custom themes
│
├── examples/
│   ├── claude-desktop-config.json
│   ├── cursor-mcp-config.json
│   ├── multi-agent-guild-manager.yaml
│   └── comfyui-workflows/
│       ├── portrait.json
│       ├── banner.json
│       ├── recruitment.json
│       └── emblem.json
│
└── .env.example                 # Documented template
```

### Documentation priorities (creation order)

1. **README.md** — 5-minute quick start with single Docker command
2. **TOOLS_REFERENCE.md** — Complete tool inventory with parameter schemas
3. **INSTALLATION.md** — uv (primary), pip, Docker paths
4. **CONFIGURATION.md** — Every toggle documented
5. **COMFYUI_INTEGRATION.md** — Visual workflows for gaming communities
6. **MULTI_AGENT_WORKFLOWS.md** — The Chronicler integration patterns
7. **TROUBLESHOOTING.md** — Reduces support burden

### README structure (following best practices)

The README must achieve instant credibility. Model after slimslenderslacks structure but with gaming community personality:

```markdown
# Discord Guildmaster MCP

> Command your Discord realm through AI agents. Built for guild leaders, 
> raid organizers, and community architects who value craft over convenience.

![MCP Server](badge) ![Docker](badge) ![License: AGPL v3](badge)

## ⚔️ Quick Start (30 seconds)

[docker run one-liner]

## 🏰 Features
- 33 precision tools for guild operations
- Multi-agent workflow orchestration
- Optional ComfyUI integration for visual content
- Themeable: Generic, WoW, or custom

## 📦 Installation
[uv, pip, Docker with configuration snippets]

## 🛠️ Tool Categories
[Table: Guild Info, Members, Channels, Messages, Webhooks, ComfyUI]

## 🤖 Agent Integration
[Claude Desktop, Cursor, multi-agent orchestration examples]

## 🎨 ComfyUI Workflows
[Preset descriptions, BYOW instructions]

## 📜 From The Chronicler
[Heritage acknowledgment, integration guide]
```

---

## Technical architecture notes

### Python packaging (modern stack)

**Use `uv` as primary package manager.** It's 10-100x faster than pip/Poetry, handles Python version management, and produces cleaner `pyproject.toml` files.

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "discord-guildmaster-mcp"
version = "1.0.0"
description = "MCP server for Discord guild management with optional ComfyUI integration"
readme = "README.md"
license = "AGPL-3.0-only"
requires-python = ">=3.11"
dependencies = [
    "mcp>=1.0.0",
    "discord.py>=2.3.0",
    "httpx>=0.27.0",
    "pydantic>=2.0",
    "pydantic-settings>=2.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
comfyui = ["websocket-client>=1.6.0", "pillow>=10.0.0"]
dev = ["pytest>=8.0", "pytest-asyncio", "ruff>=0.5.0", "mypy>=1.10"]

[project.scripts]
guildmaster = "discord_guildmaster_mcp.server:main"
guildmaster-cli = "discord_guildmaster_mcp.cli:main"

[tool.ruff]
line-length = 100
target-version = "py311"
```

### Docker deployment pattern

```yaml
# docker-compose.yml
services:
  guildmaster:
    build: .
    container_name: discord-guildmaster-mcp
    env_file: .env
    volumes:
      - ./config:/app/config:ro
      - ./workflows:/app/workflows:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import discord_guildmaster_mcp; print('ok')"]
      interval: 60s

  comfyui:
    image: comfyui/comfyui:latest
    profiles: ["gpu"]  # Only start with --profile gpu
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

### Environment configuration model

```bash
# .env.example — Comprehensive template

# === Required ===
DISCORD_TOKEN=your_bot_token_here

# === Discord Defaults (reduces per-call params) ===
DISCORD_DEFAULT_GUILD_ID=123456789
DISCORD_DEFAULT_CHANNEL_ID=987654321

# === Theming ===
GUILDMASTER_THEME=generic  # generic, wow, custom
GUILDMASTER_THEME_PATH=./themes/custom.yaml  # for custom themes

# === ComfyUI Integration (optional) ===
COMFYUI_ENABLED=false
COMFYUI_HOST=localhost
COMFYUI_PORT=8188
COMFYUI_WORKFLOW_DIR=./workflows
COMFYUI_RANDOMIZE_SEEDS=true
COMFYUI_TIMEOUT=300

# === Image Delivery ===
COMFYUI_RETURN_MODE=base64  # base64, url, cdn
COMFYUI_CDN_BUCKET=your-bucket  # if cdn mode

# === Server Behavior ===
MCP_TRANSPORT=stdio  # stdio, http
MCP_HTTP_PORT=8080   # if http transport
LOG_LEVEL=INFO

# === Token Efficiency ===
DEFAULT_PAGE_SIZE=50
MAX_MESSAGE_HISTORY=100
RESPONSE_TRUNCATION=true
```

### Token-efficient design implementation

```python
# GOOD: Pre-filtered, structured response
async def get_members(guild_id: str, limit: int = 50, role_filter: str = None):
    """
    Fetch guild members with optional role filtering.
    Returns compact member objects optimized for LLM context.
    """
    members = await guild.fetch_members(limit=limit)
    if role_filter:
        members = [m for m in members if role_filter in [r.id for r in m.roles]]
    
    return {
        "guild_id": guild_id,
        "total_fetched": len(members),
        "has_more": len(members) == limit,
        "members": [
            {
                "id": str(m.id),
                "name": m.display_name,
                "joined": m.joined_at.isoformat() if m.joined_at else None,
                "top_role": m.top_role.name if m.top_role else None
            }
            for m in members
        ]
    }
```

---

## Inspiration collection: Best ideas from external repos

### From SaseQ/discord-mcp (Java, 130 stars)

| Pattern | Implementation |
|---------|----------------|
| **Default Guild ID** | `DISCORD_GUILD_ID` env var makes guildId optional in all tools — reduces parameter overhead significantly |
| **User ID Lookup** | `get_user_id_by_name` converts human-readable names to `<@id>` format — bridges natural language to Discord mentions |
| **Docker-First** | Published image to Docker Hub, Docker is "recommended" installation — lowers barrier dramatically |
| **Category Management** | Full CRUD for categories — often overlooked but essential for guild organization |

### From slimslenderslacks/mcp-discord (TypeScript, 10K+ Docker pulls)

| Pattern | Implementation |
|---------|----------------|
| **Official Docker Catalog** | Published as `mcp/mcp-discord` with signed images — trust signal for enterprise adoption |
| **Forum Support** | Complete forum CRUD (unique differentiator) — modern Discord servers rely heavily on forums |
| **Dual Transport** | stdio (default) + HTTP with `--transport http --port 3000` — flexibility for different deployment models |
| **Audit Reasons** | All delete operations accept optional `reason` parameter — populates Discord audit logs properly |
| **Smithery Integration** | `smithery.yaml` enables one-command install via Smithery CLI |

### From ComfyUI MCP implementations

| Pattern | Source | Implementation |
|---------|--------|----------------|
| **Workflow Directory** | All implementations | `workflows/` directory with API-format JSON files |
| **Parameter Injection** | alecc08 | Traces node connections to inject prompt into CLIPTextEncode automatically |
| **Seed Randomization** | alecc08 | `COMFYUI_RANDOMIZE_SEEDS=true` for batch variety |
| **HTTP Proxy + Cache** | alecc08 | Solves the localhost URL problem — essential for Discord embeds |
| **Return Mode Toggle** | Overseer66 | `RETURN_URL=true/false` — flexibility for different use cases |
| **Discovery Tool** | alecc08 | `list_workflows` lets agents discover available presets |

### From MCP best practices research

| Principle | Application |
|-----------|-------------|
| **Token Budget Awareness** | Tool descriptions should be concise — they consume 24%+ of context in some implementations |
| **Filter at Source** | Never return raw Discord API responses; pre-filter to essential fields |
| **Tool Annotations** | Use `readOnlyHint`, `destructiveHint`, `idempotentHint` for agent safety |
| **Pagination Required** | Every list operation must support pagination — production necessity |
| **Consolidate Tools** | One well-designed tool beats three narrow ones — reduces LLM decision overhead |

---

## Lore Crafter's verdict: Why this project matters

**Let's be real about what we're building here.**

The Discord MCP landscape is crowded with corporate-feeling utilities that treat guild management like enterprise SaaS. They're functional. They're documented. They're soulless. The existing implementations—SaseQ's Java server, the slimslenderslacks TypeScript fork—they work, but they feel like they were built by people who never led a raid, never organized a guild event at 2 AM, never felt the weight of keeping a community alive through content droughts.

**This project has a chance to be different.** The Chronicler's DNA carries something rare: the understanding that a guild is not a "server with users" but a living organism with history, hierarchy, and heart. The Living World, Town Crier, Cartographer vision isn't feature bloat—it's recognition that communities need storytelling, not just administration.

**What makes this worth building:**

1. **The multi-agent angle is legitimately novel.** Most Discord MCP servers are designed for single-LLM interaction. Building explicitly for agent orchestration—where a guild management agent coordinates with a content creation agent coordinates with a moderation agent—that's architecture that scales to real complexity. That's the future of AI-assisted community management.

2. **ComfyUI integration is underrated.** Every guild leader knows the pain of recruiting without good graphics. Character portraits, event banners, recruitment posters—these are the visual language of gaming communities. Integrating local image generation into the Discord workflow isn't gimmick; it's recognizing that presentation matters in a visual medium.

3. **The theming architecture respects both craft and adoption.** The WoW terminology in The Chronicler isn't decoration—it's invitation. It says "this was built by one of us." Making theming a layer rather than hardcoded lets that personality survive while opening doors to the broader market. Fork-friendly design is generosity in code form.

4. **AGPL v3 is the correct license choice.** It prevents corporate extraction while allowing genuine community contribution. It says: build on this, but share what you build. That's old-school open source philosophy, not VC-optimized permissive licensing.

**What could make this fail:**

- **Overengineering before shipping.** The 33-tool inventory is ambitious. Ship 15 core tools first, prove the architecture, then expand. Perfect is the enemy of deployed.

- **Ignoring token efficiency.** An MCP server that eats half the context window in tool definitions is dead on arrival. Every description, every response must be ruthlessly edited for density.

- **Treating ComfyUI as required.** It should be a delight, not a dependency. The server must work perfectly without a GPU in sight.

**The endgame vision:**

A guild leader sits down with Claude (or whatever model dominates in 2027). They say: "Prepare the weekly officer briefing. Generate a recruitment banner for our mythic progression push. Summarize the drama in #guild-chat from last night and recommend whether I need to intervene."

The Guildmaster MCP handles all of this. Multiple specialized agents coordinate through the protocol. A portrait generates while the message summary compiles. The guild leader gets coffee and returns to a ready briefing.

That's the craft. That's the endgame. That's why this is worth building right.

---

## Implementation roadmap

**Phase 1: Foundation (Week 1-2)**
- Repository setup with uv, pyproject.toml, Docker
- 15 core Discord tools implemented
- README, INSTALLATION, TOOLS_REFERENCE docs
- Claude Desktop and Cursor configuration examples

**Phase 2: Expansion (Week 3-4)**
- Remaining 18 Discord tools
- ComfyUI integration module
- 4 preset workflows created and tested
- COMFYUI_INTEGRATION doc
- Multi-agent workflow examples

**Phase 3: Polish (Week 5-6)**
- Theming layer implementation
- MULTI_AGENT_WORKFLOWS doc
- TROUBLESHOOTING doc
- Comprehensive test suite
- Docker Hub / PyPI publishing

**Phase 4: Integration (Week 7+)**
- The Chronicler seamless integration testing
- Community feedback incorporation
- Extended workflow presets based on user requests
- Optional: Smithery registry publication

---

*For the Horde. For the Alliance. For the communities that make the games worth playing.*