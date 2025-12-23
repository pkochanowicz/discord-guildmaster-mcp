# Changelog

All notable changes to Discord Guildmaster MCP will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- Additional workflow presets for ComfyUI
- Webhook event listeners for The Chronicler integration
- Advanced moderation tools
- Metrics and analytics aggregation
- Multi-language support for tool descriptions

---

## [1.0.0] - 2025-12-23 (DDD Phase 1 Complete)

### Added
- **33 Discord management tools** organized into 10 categories
- **ComfyUI integration** with 4 curated workflow presets
- **Multi-agent orchestration** support with token-efficient design
- **Theming layer** (generic, WoW, custom modes)
- **Comprehensive documentation** (17 files, 6000+ lines)
- **Dual transport support** (stdio for local, HTTP for remote)
- **Tool annotations** (readOnlyHint, destructiveHint, idempotentHint)
- **Default guild/channel IDs** for reduced parameter overhead
- **Pagination** on all list operations
- **Response truncation** for token efficiency

#### Tool Categories
- Guild Information (2 tools)
- Member Management (4 tools)
- Role Operations (3 tools)
- Channel Management (4 tools)
- Messaging (5 tools)
- Webhook Management (3 tools)
- Forum Support (3 tools)
- Thread Management (2 tools)
- ComfyUI Integration (4 tools)
- Utility (3 tools)

### Documentation
- Installation guide (uv, pip, Docker)
- Configuration reference (all environment variables)
- Complete tools reference with schemas and examples
- ComfyUI integration guide with BYOW infrastructure
- Multi-agent workflow patterns
- Troubleshooting guide
- System architecture documentation
- Contributing guidelines
- Example configurations for Claude Desktop, Cursor, orchestrators

### Dependencies
- Python ≥3.11
- discord.py ≥2.3.0
- mcp ≥1.0.0
- httpx ≥0.27.0 (for ComfyUI)
- pydantic ≥2.0
- pydantic-settings ≥2.0

---

## Release Guidelines

### Version Numbers
- **Major (X.0.0)**: Breaking API changes, tool removals/renames
- **Minor (1.X.0)**: New tools, new features, backward-compatible
- **Patch (1.0.X)**: Bug fixes, documentation, no API changes

### Release Process
1. Update CHANGELOG.md with version and date
2. Update version in pyproject.toml
3. Tag release: `git tag -a v1.0.0 -m "Release v1.0.0"`
4. Push tag: `git push origin v1.0.0`
5. Build and publish: `uv build && uv publish`
6. Create GitHub release with CHANGELOG excerpt

---

**For the craft. For the community. For the guilds.** ⚔️
