<!-- Generated: 2025-12-23 | DDD Phase 1: Documentation Genesis -->

# API Internals

Technical reference for contributors implementing tools, themes, and extensions.

---

## Tool Implementation

### Adding a New Tool

1. **Create tool module** in `tools/`:

```python
# tools/custom_tool.py
from typing import Optional
from pydantic import BaseModel

class CustomToolParams(BaseModel):
    """Parameters for custom_tool."""
    param1: str
    param2: Optional[int] = None

async def custom_tool(params: CustomToolParams) -> dict:
    """
    Brief description for LLM comprehension.
    
    Args:
        params: Validated parameters
        
    Returns:
        Structured response dict
    """
    # Implementation
    return {"success": True, "data": {...}}
```

2. **Register in server.py**:

```python
from tools import custom_tool

server.add_tool(
    name="custom_tool",
    description="Brief LLM-optimized description",
    input_schema=CustomToolParams.model_json_schema(),
    handler=custom_tool.custom_tool,
    hints=["readOnlyHint"]  # or "destructiveHint"
)
```

3. **Add tests** in `tests/test_custom_tool.py`
4. **Update docs/TOOLS_REFERENCE.md**

### Tool Response Format

All tools should return structured dicts:

```python
{
    "success": bool,           # Operation succeeded
    "data": {...},             # Core response data
    "metadata": {...},         # Optional: pagination, timing
    "errors": [...]            # Optional: warnings/errors
}
```

---

## Theming System

### Theme Interface

```python
# theming/base.py
from abc import ABC, abstractmethod

class ThemeBase(ABC):
    @abstractmethod
    def get_tool_mapping(self) -> dict[str, str]:
        """Map generic tool names to themed names."""
        pass
        
    @abstractmethod
    def transform_description(self, tool: str, desc: str) -> str:
        """Transform tool descriptions."""
        pass
```

### Implementing a Theme

```python
# theming/cyberpunk.py
from .base import ThemeBase

class CyberpunkTheme(ThemeBase):
    def get_tool_mapping(self) -> dict[str, str]:
        return {
            "send_message": "transmit_signal",
            "list_members": "scan_netrunners",
            "create_channel": "establish_node",
            # Map all 33 tools
        }
        
    def transform_description(self, tool: str, desc: str) -> str:
        # Add cyberpunk flavor to descriptions
        return desc.replace("guild", "subnet").replace("member", "netrunner")
```

### Register Theme

```python
# theming/__init__.py
from .cyberpunk import CyberpunkTheme

THEMES = {
    "generic": GenericTheme,
    "wow": WoWTheme,
    "cyberpunk": CyberpunkTheme,
}
```

---

## Configuration System

### Using Pydantic Settings

```python
# config.py
from pydantic_settings import BaseSettings

class GuildmasterConfig(BaseSettings):
    discord_token: str
    discord_default_guild_id: str | None = None
    comfyui_enabled: bool = False
    comfyui_host: str = "localhost"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

config = GuildmasterConfig()
```

---

## Extension Points

1. **Custom Tools** — Add to `tools/` directory
2. **Custom Themes** — Implement `ThemeBase`
3. **Custom Workflows** — Add JSON to workflows/ directory
4. **Event Handlers** — Hook into Discord events
5. **Middleware** — Pre/post processing for tools

---

**For contributors building on the foundation.** ⚔️
