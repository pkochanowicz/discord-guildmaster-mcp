<!-- Generated: 2025-12-23 | DDD Phase 1: Documentation Genesis -->

# System Architecture

Technical design and data flow for Discord Guildmaster MCP.

---

## Overview

Discord Guildmaster MCP is a **stateless MCP server** providing Discord API operations through 33 specialized tools optimized for multi-agent workflows.

```
┌──────────────────────────────────────┐
│     AI Agents (Claude, etc.)         │
│  - Guild Manager                     │
│  - Content Publisher                 │
│  - Visual Designer                   │
│  - Moderation Agent                  │
└─────────────┬────────────────────────┘
              │ MCP Protocol
              ↓
┌──────────────────────────────────────┐
│   Discord Guildmaster MCP Server     │
│  ┌────────────────────────────────┐  │
│  │  Tool Registry (33 tools)      │  │
│  ├────────────────────────────────┤  │
│  │  Theming Layer                 │  │
│  │  (generic/wow/custom)          │  │
│  ├────────────────────────────────┤  │
│  │  Discord Client (discord.py)   │  │
│  ├────────────────────────────────┤  │
│  │  ComfyUI Client (httpx)        │  │
│  └────────────────────────────────┘  │
└─────────────┬────────────────────────┘
              │
       ┌──────┴──────┐
       ↓             ↓
┌─────────────┐  ┌──────────────┐
│   Discord   │  │   ComfyUI    │
│     API     │  │    Server    │
└─────────────┘  └──────────────┘
```

---

## Module Structure

```
discord_guildmaster_mcp/
├── server.py              # MCP server entry point
├── tools/                 # Tool implementations
│   ├── guild.py          # Guild information tools
│   ├── members.py        # Member management
│   ├── roles.py          # Role operations
│   ├── channels.py       # Channel management
│   ├── messages.py       # Messaging tools
│   ├── webhooks.py       # Webhook operations
│   ├── forums.py         # Forum support
│   ├── threads.py        # Thread management
│   ├── comfyui.py        # ComfyUI integration
│   └── utility.py        # Diagnostic tools
├── theming/              # Theme layer
│   ├── base.py           # Theme interface
│   ├── generic.py        # Generic theme
│   ├── wow.py            # WoW theme
│   └── loader.py         # Custom theme loader
├── config.py             # Configuration (Pydantic)
└── discord_client.py     # Discord connection manager
```

---

## Data Flow: send_message

Example tool execution flow:

```
Agent Request
    │
    ↓
┌─────────────────────────────────────────┐
│ 1. MCP Server receives tool call        │
│    {                                     │
│      "tool": "send_message",             │
│      "params": {                         │
│        "channel_id": "123",              │
│        "content": "Hello guild!"         │
│      }                                   │
│    }                                     │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 2. Theming Layer (optional transform)   │
│    generic: send_message                 │
│    wow: summon_herald                    │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 3. Tool Implementation                   │
│    - Validate parameters (Pydantic)      │
│    - Apply defaults (DISCORD_DEFAULT_*)  │
│    - Check permissions                   │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 4. Discord Client                        │
│    await channel.send(content=...)       │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 5. Discord API                           │
│    POST /channels/123/messages           │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 6. Response Processing                   │
│    - Extract essential fields            │
│    - Apply truncation (if enabled)       │
│    - Format for LLM context              │
└──────────────┬──────────────────────────┘
               ↓
     Return to Agent
     {
       "success": true,
       "message": {
         "id": "456",
         "channel_id": "123",
         "content": "Hello guild!",
         "timestamp": "2025-12-23T10:00:00Z"
       }
     }
```

---

## Design Decisions

### 1. Stateless Architecture

**Decision:** No persistent state stored in MCP server

**Rationale:**
- Simplifies deployment (no database required)
- Enables horizontal scaling
- Reduces failure modes
- Agent context is authoritative source

**Trade-off:** Cannot cache guild/member data (acceptable - Discord API is fast)

---

### 2. Token Efficiency by Default

**Decision:** All list operations return pre-filtered, paginated results

**Rationale:**
- LLM context windows are precious
- Agents should receive only relevant data
- Pagination prevents context overflow

**Implementation:**
- `DEFAULT_PAGE_SIZE=50`
- `RESPONSE_TRUNCATION=true`
- Agents can override limits when needed

---

### 3. Dual Transport Support

**Decision:** stdio (default) and HTTP modes

**Rationale:**
- stdio: Best for local agent integration (Claude Desktop, Cursor)
- HTTP: Enables remote agent connections, multi-server deployments

**Implementation:**
```python
if MCP_TRANSPORT == "stdio":
    server.run(transport=StdioTransport())
else:
    server.run(transport=HttpTransport(port=MCP_HTTP_PORT))
```

---

### 4. Theming as Optional Layer

**Decision:** Theming wraps tools without modifying core logic

**Rationale:**
- Clean separation of concerns
- Easy to add new themes
- Generic mode ensures broad compatibility
- WoW mode adds personality without coupling

**Implementation:**
```python
class ThemeLayer:
    def transform_tool_name(self, tool: str) -> str:
        if self.theme == "wow":
            return WOW_MAPPINGS.get(tool, tool)
        return tool
```

---

## ComfyUI Integration Architecture

```
Agent requests image
       ↓
generate_image(workflow="portrait", prompt="...")
       ↓
┌──────────────────────────────────────┐
│ 1. Workflow Loading                  │
│    - Load JSON from COMFYUI_WORKFLOW_DIR
│    - Parse node graph                │
└────────────┬─────────────────────────┘
             ↓
┌──────────────────────────────────────┐
│ 2. Parameter Injection                │
│    - Find CLIPTextEncode nodes       │
│    - Inject prompt/negative_prompt   │
│    - Randomize KSampler seeds        │
└────────────┬─────────────────────────┘
             ↓
┌──────────────────────────────────────┐
│ 3. Queue Submission                   │
│    POST http://comfyui:8188/prompt   │
│    Returns: prompt_id                │
└────────────┬─────────────────────────┘
             ↓
Return generation_id to agent
             ↓
Agent polls get_generation_status()
             ↓
┌──────────────────────────────────────┐
│ 4. Status Polling                     │
│    GET /history/{prompt_id}          │
│    Status: queued → processing →     │
│            completed                 │
└────────────┬─────────────────────────┘
             ↓
Agent calls get_image(generation_id)
             ↓
┌──────────────────────────────────────┐
│ 5. Image Retrieval                    │
│    Mode: base64 → Encode image       │
│    Mode: url → Return ComfyUI URL    │
│    Mode: cdn → Upload to S3/R2       │
└────────────┬─────────────────────────┘
             ↓
Return image to agent
```

---

## Security Model

### Authentication
- Bot token stored in environment (never in code)
- Token validated on startup via `test_connection()`
- Invalid tokens fail fast with clear error

### Authorization
- Bot permissions checked before operations
- Tools annotated with required permissions
- Graceful failure with actionable error messages

### Rate Limiting
- Discord API rate limits respected (handled by discord.py)
- No artificial throttling (trust Discord's limits)
- Agents should implement retry logic for 429 errors

### Input Validation
- All parameters validated via Pydantic models
- SQL injection impossible (no SQL)
- Command injection impossible (no shell execution)
- Discord IDs validated as numeric strings

---

## Error Handling Strategy

1. **Validation Errors** → Return clear parameter error to agent
2. **Permission Errors** → Return actionable permission name
3. **Not Found Errors** → Return entity type and ID
4. **Rate Limit Errors** → Return retry-after duration
5. **Network Errors** → Return connectivity diagnostic info

---

## Future Scalability

### Horizontal Scaling
- Stateless design enables load balancing
- Multiple MCP server instances per guild
- Shared Discord bot connection (singleton pattern)

### Tool Extensibility
- New tools: Add to tools/ directory
- Register in server.py
- Auto-discovered by agents via `list_available_tools()`

### Theme Extensibility
- New themes: Implement ThemeBase interface
- No core code changes required
- Community themes via YAML files

---

**Technical design complete. Ready for implementation.** ⚔️

