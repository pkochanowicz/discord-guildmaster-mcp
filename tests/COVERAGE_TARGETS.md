# Coverage Targets & Quality Standards

**Purpose**: Define quality standards, coverage requirements, and success criteria for the test suite.

**Phase**: DDD Phase 2 - Test Suite Implementation  
**Generated**: 2025-12-23  
**Standards**: Based on docs/CONTRIBUTING.md and industry best practices

---

## Coverage Requirements

### Minimum Coverage Thresholds

**Overall Project**: ≥80% line coverage  
**Critical Modules**: Higher standards apply

```
discord_guildmaster_mcp/tools/      ≥90%  (Critical path - user-facing tools)
discord_guildmaster_mcp/config.py   ≥95%  (Configuration must be bulletproof)
discord_guildmaster_mcp/theming/    ≥85%  (Theme switching tested thoroughly)
discord_guildmaster_mcp/server.py   ≥80%  (MCP server logic)
discord_guildmaster_mcp/discord_client.py ≥85%  (Connection management)
```

### Coverage Enforcement

**CI/CD Pipeline**:
```bash
pytest --cov=discord_guildmaster_mcp \
       --cov-report=html \
       --cov-report=term-missing \
       --cov-fail-under=80
```

**Fails if**:
- Overall coverage < 80%
- Any critical module below its threshold
- New code contributions < 85% coverage

---

## Module-Specific Targets

### Tools Module (discord_guildmaster_mcp/tools/)

**Target**: 90%+ coverage  
**Rationale**: Core user-facing functionality, high-risk if broken

**Files**:
```
tools/guild.py          90%  (2 tools: get_guild_info, get_audit_log)
tools/members.py        90%  (4 tools: list_members, get_member, search_members, get_user_id_by_name)
tools/roles.py          90%  (3 tools: list_roles, assign_role, remove_role)
tools/channels.py       90%  (4 tools: list_channels, create_channel, delete_channel, create_category)
tools/messages.py       90%  (5 tools: send_message, read_messages, delete_message, add_reaction, send_dm)
tools/webhooks.py       90%  (3 tools: create_webhook, send_webhook_message, delete_webhook)
tools/forums.py         90%  (3 tools: create_forum_post, reply_to_forum, get_forum_post)
tools/threads.py        90%  (2 tools: create_thread, archive_thread)
tools/comfyui.py        85%  (4 tools: generate_image, list_workflows, get_generation_status, get_image)
tools/utility.py        85%  (3 tools: test_connection, test_comfyui, list_available_tools)
```

**Test Coverage Requirements**:
- ✅ Every function has happy path tests
- ⚠️ Every error case documented has test
- 🔍 Boundary values tested (max/min limits)
- 🔗 Integration with Discord API mocked and tested

---

### Configuration Module (discord_guildmaster_mcp/config.py)

**Target**: 95%+ coverage  
**Rationale**: Misconfiguration leads to runtime failures, must be rock-solid

**What Must Be Tested**:
```python
✅ Settings class initialization
✅ All environment variable loading
✅ Default value application
✅ Pydantic validation rules
✅ Required field enforcement (DISCORD_TOKEN)
✅ Optional field handling (DISCORD_DEFAULT_GUILD_ID, etc.)
✅ Type coercion (string to int, string to bool)
✅ Invalid value rejection (invalid theme, invalid transport)
✅ ComfyUI configuration validation
✅ MCP transport configuration
```

**Test File**: tests/test_config.py  
**Test Count**: 30+ test cases

---

### Theming Module (discord_guildmaster_mcp/theming/)

**Target**: 85%+ coverage  
**Rationale**: Theme switching must not break tool functionality

**Files**:
```
theming/base.py         85%  (ThemeBase abstract class)
theming/generic.py      90%  (GenericTheme implementation)
theming/wow.py          90%  (WoWTheme implementation)
theming/loader.py       90%  (ThemeLoader, theme discovery)
```

**What Must Be Tested**:
```python
✅ Generic theme tool name mapping (1:1, no changes)
✅ WoW theme tool name mapping (immersive terminology)
✅ Custom theme loading from YAML
✅ Theme switching without restart
✅ Invalid theme rejection
✅ Tool description formatting per theme
✅ Message content formatting per theme
```

**Test File**: tests/test_theming.py  
**Test Count**: 25+ test cases

---

### Server Module (discord_guildmaster_mcp/server.py)

**Target**: 80%+ coverage  
**Rationale**: MCP server protocol handling

**What Must Be Tested**:
```python
✅ Server initialization (stdio transport)
✅ Server initialization (HTTP transport)
✅ Tool registration (all 33 tools)
✅ Tool invocation (parameter passing)
✅ Tool result serialization
✅ Error handling (tool errors, protocol errors)
✅ Discord client connection lifecycle
✅ Graceful shutdown
```

**Test File**: tests/test_server.py  
**Test Count**: 20+ test cases

---

### Discord Client Module (discord_guildmaster_mcp/discord_client.py)

**Target**: 85%+ coverage  
**Rationale**: Connection management critical for all tools

**What Must Be Tested**:
```python
✅ Client initialization
✅ Bot login with token
✅ Connection ready event
✅ Guild caching
✅ Permission checking
✅ Rate limit handling
✅ Reconnection logic
✅ Graceful disconnection
```

**Test File**: tests/test_discord_client.py  
**Test Count**: 20+ test cases

---

## Test Quality Standards

### Code Quality

**All test code must**:
- ✅ Pass ruff linting (no warnings)
- ✅ Pass mypy type checking
- ✅ Follow AAA pattern (Arrange-Act-Assert)
- ✅ Have descriptive docstrings
- ✅ Use existing fixtures (no duplicate mocking)
- ✅ Be isolated (no shared state between tests)
- ✅ Be deterministic (no flaky tests)

### Test Organization

```
tests/
├── conftest.py                    # Shared fixtures
├── TEST_MATRIX.md                 # This document's companion
├── COVERAGE_TARGETS.md            # This document
├── README.md                      # Test suite documentation
├── tools/                         # Tool-specific tests
│   ├── test_guild.py
│   ├── test_members.py
│   ├── test_roles.py
│   ├── test_channels.py
│   ├── test_messages.py
│   ├── test_webhooks.py
│   ├── test_forums.py
│   ├── test_threads.py
│   ├── test_comfyui.py
│   └── test_utility.py
├── test_config.py                 # Configuration tests
├── test_theming.py                # Theming system tests
├── test_server.py                 # MCP server tests
├── test_discord_client.py         # Discord client tests
├── integration/                   # Integration tests
│   ├── test_chronicler_integration.py
│   ├── test_multi_agent_workflows.py
│   └── test_end_to_end.py
└── utils/                         # Test utilities
    ├── assertions.py
    └── factories.py
```

---

## Test Performance Standards

### Execution Time

**Unit tests**: < 30 seconds total  
**Integration tests**: < 2 minutes total  
**Full suite**: < 3 minutes total

**If tests are slow**:
1. Profile: `pytest --durations=10`
2. Parallelize: `pytest -n auto` (use pytest-xdist)
3. Mock expensive operations (HTTP calls, database, file I/O)
4. Split fast/slow tests with markers

### Test Markers

```python
@pytest.mark.unit            # Fast unit tests (default)
@pytest.mark.integration     # Slow integration tests
@pytest.mark.comfyui         # Requires ComfyUI server
@pytest.mark.slow            # Known slow tests

# Run fast tests only
pytest -m "not integration and not slow"

# Run all tests including integration
pytest
```

---

## Error Handling Standards

### Every Tool Must Test

**Happy Path** (Success Cases):
```python
✅ Minimal valid parameters
✅ All parameters provided
✅ Optional parameters work
✅ Default values applied correctly
✅ Return value schema matches docs
```

**Error Path** (Failure Cases):
```python
⚠️ Missing required parameters → ValueError
⚠️ Invalid parameter types → TypeError/ValueError
⚠️ Invalid IDs (format) → ValueError
⚠️ Resources not found → discord.NotFound → ValueError
⚠️ Insufficient permissions → discord.Forbidden → PermissionError
⚠️ Rate limits → discord.HTTPException (handled gracefully)
⚠️ Connection errors → ConnectionError
⚠️ Timeout errors → TimeoutError
```

**Edge Cases**:
```python
🔍 Boundary values (0, 1, max, max+1)
🔍 Empty collections
🔍 Null/None values
🔍 Special characters
🔍 Unicode/emoji
🔍 Very long strings
🔍 Very large numbers
```

---

## Documentation-Test Alignment

### Contract Validation

**Every documented feature = test requirement**

**Verification Process**:
1. Read tool documentation (docs/TOOLS_REFERENCE.md)
2. Extract all promises (parameters, returns, behavior)
3. Create test for each promise
4. Verify test validates exactly what docs claim

**Example**:
```python
# Documentation says: "Default limit=50"
def test_list_members_default_limit():
    """Verify default limit is 50 as documented."""
    result = list_members()
    assert len(result["members"]) <= 50

# Documentation says: "Excludes bot users automatically"
def test_list_members_excludes_bots():
    """Verify bot users excluded as documented."""
    result = list_members()
    for member in result["members"]:
        assert not member.get("bot", False)
```

---

## Current Baseline (Pre-Implementation)

**Run baseline coverage check**:
```bash
pytest --cov=discord_guildmaster_mcp \
       --cov-report=term-missing \
       --cov-report=html

# Expected: Low coverage (implementation may not exist yet)
# Target: 80%+ after Phase 2 complete
```

**Baseline Results** (to be filled after first run):
```
Name                                          Stmts   Miss  Cover   Missing
---------------------------------------------------------------------------
discord_guildmaster_mcp/__init__.py               0      0   100%
discord_guildmaster_mcp/server.py               ???    ???   ???%
discord_guildmaster_mcp/config.py               ???    ???   ???%
discord_guildmaster_mcp/discord_client.py       ???    ???   ???%
discord_guildmaster_mcp/tools/guild.py          ???    ???   ???%
discord_guildmaster_mcp/tools/members.py        ???    ???   ???%
discord_guildmaster_mcp/tools/roles.py          ???    ???   ???%
discord_guildmaster_mcp/tools/channels.py       ???    ???   ???%
discord_guildmaster_mcp/tools/messages.py       ???    ???   ???%
discord_guildmaster_mcp/tools/webhooks.py       ???    ???   ???%
discord_guildmaster_mcp/tools/forums.py         ???    ???   ???%
discord_guildmaster_mcp/tools/threads.py        ???    ???   ???%
discord_guildmaster_mcp/tools/comfyui.py        ???    ???   ???%
discord_guildmaster_mcp/tools/utility.py        ???    ???   ???%
discord_guildmaster_mcp/theming/base.py         ???    ???   ???%
discord_guildmaster_mcp/theming/generic.py      ???    ???   ???%
discord_guildmaster_mcp/theming/wow.py          ???    ???   ???%
discord_guildmaster_mcp/theming/loader.py       ???    ???   ???%
---------------------------------------------------------------------------
TOTAL                                           ???    ???   ???%
```

---

## Gap Analysis Process

### Identifying Coverage Gaps

**After each test implementation batch**:
```bash
# Generate coverage report
pytest --cov=discord_guildmaster_mcp --cov-report=html

# Open report
open htmlcov/index.html

# Identify gaps
# - Red/yellow lines = not covered
# - Focus on high-risk areas first (tools, config)
# - Add tests for uncovered lines
```

### Priority for Gap Filling

**P0 - Critical** (must reach 90%):
- Tools module (all tool functions)
- Config validation
- Error handling paths

**P1 - Important** (must reach 85%):
- Theming system
- Discord client
- Server initialization

**P2 - Nice to have** (must reach 80%):
- Utility functions
- Helper methods
- Edge case branches

---

## CI/CD Pipeline Requirements

### GitHub Actions Workflow

**File**: `.github/workflows/test.yml`

**Jobs**:
1. **Lint** (ruff check, ruff format --check)
2. **Type Check** (mypy)
3. **Test** (pytest with coverage)
4. **Coverage Report** (upload to Codecov)

**Matrix**:
- Python 3.11
- Python 3.12

**Triggers**:
- Every push to main
- Every pull request
- Manual workflow dispatch

### Quality Gates

**Pull Request Requirements**:
```
✅ All tests pass
✅ Coverage ≥80% overall
✅ Coverage ≥85% for new code
✅ No linting errors
✅ No type checking errors
✅ Test execution time < 3 minutes
```

**Automated Checks**:
- Pre-commit hooks (optional but recommended)
- Branch protection rules
- Required review from maintainer

---

## Success Criteria

### Phase 2 Complete When

**Coverage**:
- ✅ Overall coverage ≥80%
- ✅ Tools coverage ≥90%
- ✅ Config coverage ≥95%
- ✅ Theming coverage ≥85%

**Test Quality**:
- ✅ All tests passing
- ✅ No flaky tests
- ✅ Execution time < 3 minutes
- ✅ All documented features have tests

**Documentation**:
- ✅ TEST_MATRIX.md complete
- ✅ COVERAGE_TARGETS.md (this file) complete
- ✅ tests/README.md complete
- ✅ Coverage report accessible

**Infrastructure**:
- ✅ conftest.py with comprehensive fixtures
- ✅ Test utilities (assertions, factories)
- ✅ CI/CD pipeline configured
- ✅ Coverage badges in README.md

**Validation**:
- ✅ Every tool in TEST_MATRIX has tests
- ✅ Every config variable validated
- ✅ Every error case tested
- ✅ Integration tests for workflows

---

## Maintenance Standards

### Adding New Tests

**When adding a new tool**:
1. Add to docs/TOOLS_REFERENCE.md (documentation first!)
2. Add to tests/TEST_MATRIX.md
3. Create tests following existing patterns
4. Verify coverage threshold met
5. Update tests/README.md if needed

**When fixing a bug**:
1. Create failing test that reproduces bug
2. Fix the bug
3. Verify test now passes
4. Verify coverage not decreased

### Refactoring Tests

**Allowed**:
- ✅ Extract common fixtures
- ✅ Improve test clarity
- ✅ Fix flaky tests
- ✅ Optimize slow tests

**Not Allowed**:
- ❌ Removing tests without replacement
- ❌ Lowering coverage thresholds
- ❌ Skipping tests permanently
- ❌ Masking test failures

---

## Monitoring & Reporting

### Coverage Tracking

**Tools**:
- pytest-cov (local development)
- Codecov (CI/CD, PR comments)
- Coverage badges (README.md)

**Reports**:
- HTML report (htmlcov/index.html) - detailed per-file
- Terminal report (pytest --cov) - quick summary
- Codecov dashboard - trends over time

### Metrics to Track

```
Total Coverage %         (target: ≥80%)
Tools Coverage %         (target: ≥90%)
Config Coverage %        (target: ≥95%)
Test Count               (growing with features)
Test Execution Time      (target: <3 min)
Flaky Test Count         (target: 0)
```

---

## Emergency Protocols

### Coverage Drop Below Threshold

**If CI fails due to low coverage**:
1. Identify which module dropped
2. Check recent changes (git diff)
3. Add tests for new code paths
4. Verify coverage restored
5. Document any legitimate exemptions

### Flaky Tests Detected

**If tests pass/fail intermittently**:
1. Isolate the flaky test
2. Run 100 times: `pytest --count=100 path/to/test.py::test_name`
3. Identify cause (timing, randomness, shared state)
4. Fix root cause
5. Verify determinism restored

### Test Suite Too Slow

**If tests take >5 minutes**:
1. Profile: `pytest --durations=20`
2. Identify slowest tests
3. Mock expensive operations
4. Use fixtures efficiently
5. Consider parallelization
6. Split integration tests to separate suite

---

## Quality Philosophy

**Every test is a promise validator.**

- Documentation makes promises to users
- Tests verify those promises are kept
- Failing tests = broken promises
- High coverage = high confidence

**We aim for**:
- 100% of documented features tested
- 0 flaky tests (deterministic only)
- Fast feedback (< 3 minute test runs)
- Clear failures (descriptive error messages)

---

**For the craft. For quality. For bulletproof code.** ⚔️

**Last Updated**: 2025-12-23  
**Phase**: 2 - Test Suite Implementation  
**Status**: Standards Defined - Implementation In Progress
