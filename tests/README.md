# Test Suite Documentation

**Purpose**: Comprehensive test suite for discord-guildmaster-mcp that validates all documented functionality.

**Philosophy**: Every documented feature is a promise. Every test validates that promise is kept.

**Phase**: DDD Phase 2 - Test Suite Implementation  
**Generated**: 2025-12-23  
**Status**: Infrastructure Complete, Implementation In Progress

---

## Quick Start

### Run All Tests

```bash
pytest
```

### Run With Coverage

```bash
pytest --cov=discord_guildmaster_mcp --cov-report=html
open htmlcov/index.html
```

### Run Specific Categories

```bash
# Unit tests only (fast)
pytest -m unit

# Integration tests
pytest -m integration

# Specific tool category
pytest -m messages
pytest -m members
pytest -m channels

# Exclude integration tests
pytest -m "not integration"
```

### Run Specific Test File

```bash
pytest tests/tools/test_messages.py -v
pytest tests/test_config.py -v
```

### Run In Parallel (Faster)

```bash
# Install pytest-xdist first: pip install pytest-xdist
pytest -n auto
```

---

## Test Organization

```
tests/
├── conftest.py                    # Shared fixtures (Discord mocks, ComfyUI mocks)
├── pytest.ini                     # Pytest configuration
├── TEST_MATRIX.md                 # Maps all 33 tools to test requirements
├── COVERAGE_TARGETS.md            # Quality standards and coverage goals
├── README.md                      # This file
│
├── tools/                         # Tool-specific tests (33 tools)
│   ├── test_guild.py             # Guild information tools (2)
│   ├── test_members.py           # Member management tools (4)
│   ├── test_roles.py             # Role operation tools (3)
│   ├── test_channels.py          # Channel management tools (4)
│   ├── test_messages.py          # Messaging tools (5) ← REFERENCE IMPLEMENTATION
│   ├── test_webhooks.py          # Webhook management tools (3)
│   ├── test_forums.py            # Forum support tools (3)
│   ├── test_threads.py           # Thread management tools (2)
│   ├── test_comfyui.py           # ComfyUI integration tools (4)
│   └── test_utility.py           # Utility tools (3)
│
├── test_config.py                 # Configuration validation tests
├── test_theming.py                # Theming system tests
│
├── integration/                   # Integration tests
│   ├── test_multi_agent_workflows.py
│   └── test_chronicler_integration.py
│
└── utils/                         # Test utilities
    ├── assertions.py              # Custom assertion helpers
    └── factories.py               # Object factories for test data
```

---

## Test Categories & Markers

### Execution Speed Markers

- `@pytest.mark.unit` - Fast unit tests (< 1 second each), heavily mocked
- `@pytest.mark.integration` - Slower integration tests, may require external services
- `@pytest.mark.slow` - Known slow tests (> 5 seconds)

### Tool Category Markers

- `@pytest.mark.guild` - Guild information tools
- `@pytest.mark.members` - Member management tools
- `@pytest.mark.roles` - Role operation tools
- `@pytest.mark.channels` - Channel management tools
- `@pytest.mark.messages` - Messaging tools
- `@pytest.mark.webhooks` - Webhook management tools
- `@pytest.mark.forums` - Forum support tools
- `@pytest.mark.threads` - Thread management tools
- `@pytest.mark.utility` - Utility tools

### System Markers

- `@pytest.mark.config` - Configuration tests
- `@pytest.mark.theming` - Theming system tests
- `@pytest.mark.workflows` - Multi-agent workflow tests
- `@pytest.mark.chronicler` - The Chronicler integration tests
- `@pytest.mark.comfyui` - Tests requiring ComfyUI server

### Usage Examples

```bash
# Run only fast unit tests
pytest -m unit

# Run all message tool tests
pytest -m messages

# Run everything except slow tests
pytest -m "not slow"

# Run config and theming tests
pytest -m "config or theming"

# Run integration tests only
pytest -m integration
```

---

## Coverage Requirements

**Minimum Thresholds** (enforced in CI):

```
Overall Project                    ≥80%
discord_guildmaster_mcp/tools/     ≥90%  (Critical user-facing functionality)
discord_guildmaster_mcp/config.py  ≥95%  (Configuration must be bulletproof)
discord_guildmaster_mcp/theming/   ≥85%  (Theme switching thoroughly tested)
discord_guildmaster_mcp/server.py  ≥80%  (MCP server logic)
```

### Check Coverage

```bash
# Generate coverage report
pytest --cov=discord_guildmaster_mcp --cov-report=term-missing

# Generate HTML report (more detailed)
pytest --cov=discord_guildmaster_mcp --cov-report=html
open htmlcov/index.html

# Fail if coverage below 80%
pytest --cov=discord_guildmaster_mcp --cov-fail-under=80
```

### Coverage Reports

- **Terminal**: Quick summary with missing line numbers
- **HTML** (`htmlcov/`): Interactive, per-file detailed view
- **XML** (`coverage.xml`): For CI/CD integration (Codecov)

---

## Test Infrastructure

### Fixtures (conftest.py)

**Discord Object Fixtures:**
- `mock_discord_client` - Mocked Discord.py client
- `mock_guild` - Standard test guild
- `mock_text_channel`, `mock_voice_channel`, `mock_category_channel`, `mock_forum_channel`
- `mock_member`, `mock_member_officer` - Standard and elevated members
- `mock_role`, `mock_role_admin` - Standard and admin roles
- `mock_message` - Test message
- `mock_webhook` - Test webhook
- `mock_thread` - Test thread

**Configuration Fixtures:**
- `mock_settings` - Standard test configuration
- `mock_settings_with_comfyui` - Config with ComfyUI enabled
- `mock_settings_wow_theme` - Config with WoW theme

**ComfyUI Fixtures:**
- `mock_comfyui_client` - Mocked ComfyUI HTTP client
- `mock_comfyui_workflow` - Test workflow structure

**Error Fixtures:**
- `mock_discord_errors(error_type)` - Factory for Discord API errors

**Theming Fixtures:**
- `generic_theme` - Generic theme instance
- `wow_theme` - WoW theme instance

### Utilities (tests/utils/)

**assertions.py** - Custom assertions:
- `assert_valid_discord_id()` - Validate Discord snowflake format
- `assert_message_sent()` - Verify message sent to channel
- `assert_role_assigned()` - Verify role assigned to member
- `assert_response_has_keys()` - Verify response schema
- `assert_pagination_response()` - Verify paginated response structure
- `assert_success_response()` - Verify success=true response
- `assert_valid_image_response()` - Verify image generation response

**factories.py** - Object factories:
- `DiscordFactory` - Create Discord objects with defaults
  - `.create_guild()`, `.create_member()`, `.create_role()`
  - `.create_text_channel()`, `.create_message()`, etc.
- `BatchFactory` - Create collections
  - `.create_members(count)`, `.create_roles(count)`, etc.
- `ComfyUIFactory` - Create ComfyUI test data
  - `.create_workflow()`, `.create_generation_response()`
- `ErrorFactory` - Create error responses
  - `.create_not_found_error()`, `.create_forbidden_error()`

---

## Writing New Tests

### Test Structure (AAA Pattern)

```python
@pytest.mark.asyncio
@pytest.mark.unit
@pytest.mark.messages
async def test_send_message_success(self, mock_text_channel):
    """Verify basic message sending works as documented."""
    # Arrange: Set up test data
    channel_id = str(mock_text_channel.id)
    content = "Hello guild!"
    mock_text_channel.send.return_value = mock_message
    
    # Act: Execute the behavior
    result = await messages.send_message(
        channel_id=channel_id,
        content=content
    )
    
    # Assert: Verify the outcome
    assert_response_has_keys(result, ["message_id", "channel_id"])
    assert result["content"] == content
```

### Test Coverage Checklist (Per Tool)

For each tool, implement tests for:

**✅ Happy Path:**
- [ ] Minimal valid parameters
- [ ] All optional parameters used
- [ ] Return value schema matches docs
- [ ] Default values applied correctly

**⚠️ Error Handling:**
- [ ] Missing required parameters → ValueError
- [ ] Invalid parameter types → TypeError/ValueError
- [ ] Invalid IDs → ValueError
- [ ] Resources not found → NotFound → ValueError
- [ ] Insufficient permissions → Forbidden → PermissionError
- [ ] Rate limits handled gracefully

**🔍 Edge Cases:**
- [ ] Boundary values (0, 1, max, max+1)
- [ ] Empty collections/strings
- [ ] Null/None values
- [ ] Special characters, Unicode, emoji
- [ ] Very long strings
- [ ] Maximum limits reached

**🔗 Integration:**
- [ ] Uses configuration correctly (default guild ID, etc.)
- [ ] Respects theme settings
- [ ] Works with mocked Discord API

### Best Practices

1. **Use Existing Fixtures** - Don't recreate mocks, use conftest.py fixtures
2. **Use Utility Functions** - Use assertions.py and factories.py helpers
3. **Clear Docstrings** - Explain what promise the test validates
4. **Descriptive Names** - `test_send_message_too_long_raises_error` not `test_error1`
5. **One Assert Per Concept** - Test one behavior, multiple assertions OK if related
6. **Isolate Tests** - No shared state between tests
7. **Fast Tests** - Mock expensive operations (HTTP, database, file I/O)
8. **Deterministic** - No randomness, no time dependencies (use fixtures)

---

## CI/CD Integration

### GitHub Actions Workflow

**File**: `.github/workflows/test.yml`

**Runs on**:
- Every push to `main`
- Every pull request
- Manual workflow dispatch

**Matrix**: Python 3.11, 3.12

**Steps**:
1. **Lint** - `ruff check .`
2. **Format Check** - `ruff format --check .`
3. **Type Check** - `mypy discord_guildmaster_mcp tests`
4. **Unit Tests** - `pytest -m "not integration"`
5. **Integration Tests** - `pytest -m integration` (main branch only)
6. **Coverage Report** - Upload to Codecov

**Quality Gates** (PR must pass):
- ✅ All tests passing
- ✅ Coverage ≥80%
- ✅ Linting clean
- ✅ Type checking clean (warning only for now)

### Running Tests Like CI Locally

```bash
# Full CI simulation
ruff check . && \
ruff format --check . && \
mypy discord_guildmaster_mcp tests --ignore-missing-imports && \
pytest --cov=discord_guildmaster_mcp --cov-fail-under=80 -m "not integration"
```

---

## Troubleshooting

### Tests Fail Unexpectedly

1. **Check mocks**: Verify mock configuration matches actual Discord.py API
2. **Run single test**: `pytest tests/path/to/test.py::TestClass::test_name -v`
3. **Check dependencies**: `pip list | grep discord`
4. **Clear cache**: `pytest --cache-clear`

### Coverage Below Threshold

1. **Identify gaps**: `pytest --cov --cov-report=term-missing`
2. **Check report**: `open htmlcov/index.html`
3. **Add tests**: Focus on red/yellow lines in report
4. **Re-measure**: `pytest --cov`

### Tests Too Slow

1. **Profile**: `pytest --durations=20`
2. **Parallelize**: `pytest -n auto` (requires pytest-xdist)
3. **Mock expensive calls**: Network, file I/O
4. **Split suites**: Run unit tests separately from integration

### Flaky Tests

1. **Run 100 times**: `pytest tests/path/to/test.py --count=100`
2. **Fix timing issues**: Add proper `await`, remove `sleep()`
3. **Fix randomness**: Seed RNG, use fixed datetime fixtures
4. **Fix isolation**: Ensure proper cleanup, no shared state

---

## Test Development Workflow

### Adding a New Tool

1. **Document first**: Add to docs/TOOLS_REFERENCE.md
2. **Map tests**: Add to tests/TEST_MATRIX.md
3. **Create tests**: Follow pattern in test_messages.py
4. **Implement tool**: Make tests pass
5. **Verify coverage**: `pytest --cov` should show ≥90% for new tool
6. **Update CHANGELOG**: Add to [Unreleased]

### Fixing a Bug

1. **Write failing test**: Reproduces the bug
2. **Run test**: Verify it fails
3. **Fix bug**: In source code
4. **Run test**: Verify it passes
5. **Check coverage**: Ensure no coverage decrease
6. **Commit**: Include test + fix together

---

## Current Test Status

**Phase 2 Progress**:

✅ **Completed:**
- Test infrastructure (conftest.py, utilities)
- TEST_MATRIX.md (all 33 tools mapped)
- COVERAGE_TARGETS.md (quality standards defined)
- CI/CD configuration (.github/workflows/test.yml)
- Pytest configuration (pytest.ini)
- Reference implementation (test_messages.py)
- Test skeletons for all tool groups
- Configuration tests (test_config.py)
- Theming tests (test_theming.py)
- Integration test skeletons

🚧 **In Progress:**
- Complete implementation of all tool tests (33 tools)
- Achieve 80%+ overall coverage
- Achieve 90%+ tools coverage

📋 **Next Steps:**
1. Implement remaining tool tests (use test_messages.py as template)
2. Run full test suite and measure baseline coverage
3. Fill coverage gaps to reach 80%+ threshold
4. Run CI/CD pipeline and verify all quality gates pass
5. Update badges in README.md with coverage status

---

## Resources

- **Pytest Docs**: https://docs.pytest.org
- **Discord.py Docs**: https://discordpy.readthedocs.io
- **Coverage.py Docs**: https://coverage.readthedocs.io
- **Ruff Docs**: https://docs.astral.sh/ruff
- **Mypy Docs**: https://mypy.readthedocs.io

---

**For the craft. For quality. For bulletproof code.** ⚔️

**Every test is a promise validator. Every passing test is a kept promise.**

