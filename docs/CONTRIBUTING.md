<!-- Generated: 2025-12-23 | DDD Phase 1: Documentation Genesis -->

# Contributing to Discord Guildmaster MCP

Thank you for your interest in contributing! This project values **craft over convenience** and follows strict Documentation-Driven Development (DDD) principles.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Development Setup](#development-setup)
3. [Project Structure](#project-structure)
4. [Coding Standards](#coding-standards)
5. [Testing Requirements](#testing-requirements)
6. [Pull Request Process](#pull-request-process)
7. [Documentation Standards](#documentation-standards)

---

## Code of Conduct

Be excellent to each other. This project is for **community benefit** under AGPL v3.0. Contributions should:

- Respect the craft
- Value quality over speed
- Maintain thorough documentation
- Include comprehensive tests

---

## Development Setup

### Prerequisites

- Python 3.11+ (recommended: 3.12)
- `uv` package manager (10-100x faster than pip)
- Git
- Discord bot for testing

### Initial Setup

```bash
# Clone repository
git clone https://github.com/your-org/discord-guildmaster-mcp.git
cd discord-guildmaster-mcp

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies with dev tools
uv pip install -e ".[dev,comfyui]"

# Copy environment template
cp .env.example .env

# Edit .env with your Discord bot token
nano .env
```

### Run Tests

```bash
# Run full test suite
pytest

# Run with coverage
pytest --cov=discord_guildmaster_mcp

# Run specific test file
pytest tests/test_tools.py
```

### Start Development Server

```bash
# With debug logging
LOG_LEVEL=DEBUG uv run guildmaster

# Run in HTTP mode for testing
MCP_TRANSPORT=http MCP_HTTP_PORT=8080 uv run guildmaster
```

---

## Project Structure

```
discord-guildmaster-mcp/
├── discord_guildmaster_mcp/     # Source code
│   ├── server.py                # MCP server entry point
│   ├── config.py                # Pydantic configuration
│   ├── discord_client.py        # Discord connection manager
│   ├── tools/                   # Tool implementations
│   │   ├── guild.py
│   │   ├── members.py
│   │   ├── roles.py
│   │   ├── channels.py
│   │   ├── messages.py
│   │   ├── webhooks.py
│   │   ├── forums.py
│   │   ├── threads.py
│   │   ├── comfyui.py
│   │   └── utility.py
│   └── theming/                 # Theme layer
│       ├── base.py
│       ├── generic.py
│       ├── wow.py
│       └── loader.py
├── tests/                       # Test suite
│   ├── test_tools.py
│   ├── test_theming.py
│   ├── test_config.py
│   └── fixtures/
├── docs/                        # Documentation
├── examples/                    # Configuration examples
├── workflows/                   # ComfyUI workflow presets
├── .env.example                 # Environment template
├── pyproject.toml               # Package configuration
└── README.md                    # Entry point
```

---

## Coding Standards

### Python Style

**We use `ruff` for linting and formatting:**

```bash
# Check code
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .
```

### Configuration (pyproject.toml)

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]
ignore = ["E501"]  # Line too long (handled by formatter)
```

### Code Conventions

1. **Type Hints Required**

    ```python
    def get_member(guild_id: str, user_id: str) -> dict:
        """Get member details."""
        ...
    ```

2. **Pydantic for Validation**

    ```python
    from pydantic import BaseModel

    class MemberParams(BaseModel):
        guild_id: str | None = None
        user_id: str
    ```

3. **Async/Await Pattern**

    ```python
    async def send_message(channel_id: str, content: str) -> dict:
        channel = await bot.fetch_channel(channel_id)
        message = await channel.send(content)
        return {"id": str(message.id), ...}
    ```

4. **Error Handling**

    ```python
    try:
        member = await guild.fetch_member(user_id)
    except discord.NotFound:
        raise ValueError(f"Member {user_id} not found in guild")
    except discord.Forbidden:
        raise PermissionError("Bot lacks permission to fetch member")
    ```

5. **Docstrings** (Google style)

    ```python
    def list_members(guild_id: str, limit: int = 50) -> dict:
        """List guild members with pagination.

        Args:
            guild_id: Discord guild ID
            limit: Maximum members to return (1-1000)

        Returns:
            Dict with members list and pagination info

        Raises:
            ValueError: If guild_id invalid
            PermissionError: If bot lacks Members Intent
        """
    ```

---

## Testing Requirements

### Test Coverage

**Minimum 80% code coverage required for PR approval.**

```bash
pytest --cov=discord_guildmaster_mcp --cov-report=html
open htmlcov/index.html
```

### Test Structure

```python
# tests/test_tools.py
import pytest
from discord_guildmaster_mcp.tools import members

@pytest.mark.asyncio
async def test_list_members_pagination(mock_discord_client):
    """Test member list pagination."""
    result = await members.list_members(guild_id="123", limit=50)

    assert "members" in result
    assert len(result["members"]) <= 50
    assert "has_more" in result

@pytest.mark.asyncio
async def test_list_members_invalid_guild(mock_discord_client):
    """Test handling of invalid guild ID."""
    with pytest.raises(ValueError, match="Guild .* not found"):
        await members.list_members(guild_id="invalid")
```

### Fixtures

```python
# tests/conftest.py
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
def mock_discord_client():
    """Mock Discord client for testing."""
    client = AsyncMock()
    client.get_guild.return_value = create_mock_guild()
    return client
```

---

## Pull Request Process

### Before Submitting

1. **Tests pass:** `pytest`
2. **Linting clean:** `ruff check .`
3. **Type checking:** `mypy discord_guildmaster_mcp`
4. **Documentation updated:** If adding features
5. **CHANGELOG updated:** Add entry under `[Unreleased]`

### PR Template

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix (non-breaking)
- [ ] New feature (non-breaking)
- [ ] Breaking change
- [ ] Documentation update

## Testing

- [ ] Added tests for new functionality
- [ ] All tests pass
- [ ] Coverage ≥80%

## Documentation

- [ ] Updated relevant docs
- [ ] Added examples if applicable
- [ ] Updated CHANGELOG.md

## Checklist

- [ ] Code follows project style
- [ ] Self-reviewed code
- [ ] Commented complex logic
- [ ] No new warnings
```

### Review Process

1. **Automated checks** must pass (CI/CD)
2. **Code review** by maintainer
3. **Documentation review** (if applicable)
4. **Approval** → Merge to main

---

## Documentation Standards

### Adding New Tools

When adding a new tool, update:

1. **Tool implementation** in `tools/`
2. **docs/TOOLS_REFERENCE.md** — Add complete tool documentation
3. **README.md** — Update tool count in categories table
4. **Tests** — Add test coverage for new tool

### Documentation Template

````markdown
### XX. tool_name

**Purpose:** Brief description optimized for LLM comprehension

**Hints:** 🔒 Read-only | 💡 Token-efficient

**Parameters:**

```json
{
    "param_name": {
        "type": "string",
        "required": true,
        "description": "What this parameter does"
    }
}
```

**Returns:**

```json
{
    "field": "value",
    "description": "Return structure"
}
```

**Usage Example:**

```python
result = tool_name(param="value")
```

**Agent Considerations:**

- Token efficiency notes
- Safety considerations
- Best practices
````

---

## Adding Custom Themes

1. Create theme file in `theming/`:

    ```python
    # theming/custom.py
    from .base import ThemeBase

    class CustomTheme(ThemeBase):
        def get_tool_mapping(self) -> dict:
            return {
                "send_message": "custom_send",
                "list_members": "custom_list",
                # ...
            }
    ```

2. Register in `theming/__init__.py`
3. Add documentation to `docs/theming-guide.md`
4. Add tests to `tests/test_theming.py`

---

## Release Process (Maintainers Only)

1. **Update version** in `pyproject.toml`
2. **Update CHANGELOG.md** with release date
3. **Tag release:** `git tag -a v1.1.0 -m "Release v1.1.0"`
4. **Push tag:** `git push origin v1.1.0`
5. **Build package:** `uv build`
6. **Publish to PyPI:** `uv publish`
7. **Create GitHub release** with CHANGELOG excerpt

---

## Getting Help

- **Questions:** [GitHub Discussions](https://github.com/your-org/discord-guildmaster-mcp/discussions)
- **Bugs:** [GitHub Issues](https://github.com/your-org/discord-guildmaster-mcp/issues)
- **Discord:** [Azeroth Bound](https://discord.gg/rM8EevEq)

---

**Thank you for contributing to the craft.** ⚔️
