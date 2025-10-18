# Claude Code Project Template

**Purpose:** Bootstrap new projects with proven Claude Code organizational patterns from the Offboarding Knowledge Capture System.

**When to Use:** Starting a new software project where you want systematic AI-assisted development with context preservation, quality gates, and structured workflows.

---

## What This Template Provides

This template extracts the **organizational patterns** (not domain logic) from a production project:

✅ **CLAUDE.md** - Project guidance for Claude Code
✅ **PRPs/** - Product Requirements Process for systematic feature development
✅ **/.claude/commands/** - Custom slash commands for common workflows
✅ **\*_TASKS.md** - Task tracking that survives context loss
✅ **docs/** - Methodology documentation
✅ **Quality gates** - Type checking, linting, testing standards

**NOT Included:** Domain-specific code, business logic, or tech stack choices (you pick those).

---

## Quick Start (5 Minutes)

### 1. Copy Template Structure

```bash
# In your new project root
mkdir -p .claude/commands PRPs docs

# Copy these files from template project:
cp path/to/template/CLAUDE.md ./CLAUDE.md
cp -r path/to/template/.claude/commands/* ./.claude/commands/
cp -r path/to/template/docs/* ./docs/
```

### 2. Customize CLAUDE.md

Open `CLAUDE.md` and update these sections:

```markdown
## Project Overview
**[Your Project Name]** - [One sentence description]
**Status:** Phase 1 - [Current phase]
**Tech Stack:** [Your technologies]

## Repository Structure
[Your actual directory structure]

## Architecture
[Your specific patterns and technologies]

## Essential Commands
[Your development commands]
```

**Keep these sections as-is:**
- Service Management
- Custom Commands
- Task Tracking Files
- Validation Gates
- Sub-Agent Usage
- Context Recovery

### 3. Adapt Custom Commands

In `.claude/commands/`, update these files:

**generate-prp.md** - Change to your tech stack:
```markdown
# Before:
Research React/TypeScript patterns...

# After:
Research [YOUR_STACK] patterns...
```

**execute-prp.md** - Update task file name:
```markdown
# Before:
FRONTEND_TASKS.md

# After:
[YOUR_MODULE]_TASKS.md
```

**recover-context.md** - Update paths:
```markdown
# Before:
- onboarding-frontend/CLAUDE.md
- FRONTEND_TASKS.md

# After:
- [your-paths]/CLAUDE.md
- [YOUR]_TASKS.md
```

### 4. Initialize Task Tracking

```bash
# Create your first task file
echo "# Project Tasks\n\n**Status:** Not Started\n**Last Updated:** $(date +%Y-%m-%d)\n\n## Setup\n- [ ] Initialize project\n" > PROJECT_TASKS.md
```

### 5. Start Using It

```bash
# Generate your first PRP
/generate-prp.md "Setup project foundation"

# Execute the PRP
/execute-prp.md PRPs/project-foundation-prp.md

# If you lose context
/recover-context.md
```

---

## Directory Structure

### Minimal Setup

```
your-project/
├── CLAUDE.md                    # Main guidance for Claude Code
├── .claude/
│   └── commands/
│       ├── generate-prp.md      # Create feature PRPs
│       ├── execute-prp.md       # Execute PRPs with validation
│       └── recover-context.md   # Restore context after /clear
├── PRPs/                        # Product Requirements Process
│   └── README.md               # PRP organization guide
├── docs/                        # Methodology documentation
│   ├── prp-methodology.md      # How PRPs work
│   ├── quality-standards.md    # Validation framework
│   ├── sub-agent-patterns.md   # When to use sub-agents
│   └── context-management.md   # Context preservation
└── PROJECT_TASKS.md            # Current progress tracking
```

### Monorepo Setup

```
your-monorepo/
├── CLAUDE.md                    # Root guidance
├── .claude/commands/            # Shared commands
├── PRPs/
│   ├── README.md
│   ├── frontend/               # Frontend PRPs
│   ├── backend/                # Backend PRPs
│   └── fullstack/              # Cross-cutting PRPs
├── docs/                        # Shared methodology
├── frontend/
│   ├── CLAUDE.md               # Frontend-specific guidance
│   └── docs/                   # Frontend docs
├── backend/
│   ├── CLAUDE.md               # Backend-specific guidance
│   └── docs/                   # Backend docs
├── FRONTEND_TASKS.md           # Frontend progress
└── BACKEND_TASKS.md            # Backend progress
```

---

## CLAUDE.md Template

### Required Sections

**1. Project Overview**
- Project name and one-sentence description
- Current phase/status
- Tech stack summary

**2. Repository Structure**
- Directory tree with explanations
- Module organization

**3. Architecture**
- Key patterns and conventions
- Non-obvious design decisions
- Technology choices

**4. Essential Commands**
- Development setup
- Common operations
- Testing commands

**5. Service Management**
- When to restart services
- When NOT to restart
- Hot reload capabilities

**6. Custom Commands**
- Available slash commands
- When to use each
- Example workflows

**7. Task Tracking Files**
- Active task files
- Archive location
- Purpose and usage

**8. Critical Constraints**
- DO ✅ patterns
- DON'T ❌ anti-patterns

**9. Validation Gates**
- Type checking (Level 1)
- Linting (Level 2)
- Unit tests (Level 3)
- Integration tests (Level 4)
- E2E tests (Level 5)

**10. Sub-Agent Usage**
- When to use sub-agents
- When to avoid
- Example patterns

**11. Context Recovery**
- Quick recovery command
- Manual recovery steps

**12. Documentation**
- Essential reading list
- Project-specific docs

### Optional Sections (Add as needed)

- Environment Variables
- Quick Start Guide
- Example Workflows
- Troubleshooting
- API Patterns
- Database Patterns

---

## PRP Methodology

### What is a PRP?

**Product Requirements Process** - A structured document that:
1. Analyzes requirements
2. Researches codebase patterns
3. Defines implementation steps
4. Sets validation checkpoints
5. Provides success criteria

### PRP Structure

```markdown
# [Feature Name] PRP

## 1. Requirements Analysis
- User story
- Acceptance criteria
- Technical constraints

## 2. Codebase Research
- Existing patterns
- Relevant files
- Dependencies

## 3. Implementation Plan
### Epic 1: [Name]
- Task 1.1: [Description]
- Task 1.2: [Description]
**Validation:** [How to verify]

### Epic 2: [Name]
...

## 4. Validation Gates
- [ ] Type checking passes
- [ ] Linting passes
- [ ] Unit tests ≥70% coverage
- [ ] Integration tests pass

## 5. Success Criteria
- [ ] Feature works as specified
- [ ] No regressions
- [ ] Documentation updated
```

### PRPs Organization

**Single Module:**
```
PRPs/
├── README.md
├── feature-1-prp.md
├── feature-2-prp.md
└── refactor-1-prp.md
```

**Monorepo:**
```
PRPs/
├── README.md
├── frontend/
│   ├── ui-component-prp.md
│   └── state-management-prp.md
├── backend/
│   ├── api-endpoint-prp.md
│   └── database-schema-prp.md
└── fullstack/
    └── authentication-prp.md
```

---

## Custom Commands

### Core Commands to Include

**1. /generate-prp.md** - Generate PRP for a feature

**Template:**
```markdown
# Generate PRP Command

You are generating a Product Requirements Process (PRP) document.

## Steps:
1. Research codebase patterns using Task tool with subagent_type=Explore
2. Analyze requirements and constraints
3. Create implementation plan with epics and tasks
4. Define validation checkpoints
5. Write PRP to PRPs/{feature-name}-prp.md

## PRP Structure:
[Include your PRP template here]

## Validation:
- Must include all required sections
- Must define clear success criteria
- Must specify validation gates

Output: PRPs/{feature-name}-prp.md
```

**2. /execute-prp.md** - Execute a PRP with validation

**Template:**
```markdown
# Execute PRP Command

You are executing a PRP with systematic validation.

## Steps:
1. Read the PRP file: {prp-file}
2. Create/update PROJECT_TASKS.md with epics from PRP
3. For each epic:
   a. Mark tasks as in_progress
   b. Implement tasks
   c. Run validation checkpoint
   d. Mark tasks as completed
4. Run final validation gates
5. Update PROJECT_TASKS.md with results

## Validation Gates:
- Type checking: [your command]
- Linting: [your command]
- Unit tests: [your command]
- Integration tests: [your command]

## Critical Rules:
- MUST validate after each epic
- MUST update task file after each epic
- MUST run all validation gates before completion
```

**3. /recover-context.md** - Restore context after /clear

**Template:**
```markdown
# Recover Context Command

You are recovering context after /clear or context loss.

## Steps:
1. Read CLAUDE.md files:
   - Root: CLAUDE.md
   - [Module 1]: [path]/CLAUDE.md
   - [Module 2]: [path]/CLAUDE.md

2. Read active task files:
   - PROJECT_TASKS.md
   - [OTHER]_TASKS.md

3. Check recent commits:
   - git log -10 --oneline

4. Summarize:
   - Current phase
   - Last completed work
   - Next actions
   - Active blockers

Output: Context summary with next recommended action
```

### Optional Commands

- `/check-dependencies.md` - Verify dependencies
- `/verify-setup.md` - Verify project setup
- `/run-tests.md` - Run test suite with reporting

---

## Task Tracking Pattern

### File Naming Convention

**Single module:** `PROJECT_TASKS.md`
**Multiple modules:** `[MODULE]_TASKS.md` (e.g., `FRONTEND_TASKS.md`, `BACKEND_TASKS.md`)

### Task File Structure

```markdown
# [Module] Tasks

**Status:** [In Progress | Blocked | Complete]
**Last Updated:** YYYY-MM-DD
**Current Epic:** [Epic name or N/A]

---

## Epic 1: [Name]

**Status:** ✅ Complete | 🔄 In Progress | ⏸️ Blocked | ⏳ Pending

### Tasks
- [x] Task 1.1: [Description]
- [x] Task 1.2: [Description]
- [ ] Task 1.3: [Description]

### Validation
- [x] Type checking passes
- [x] Unit tests ≥70%
- [ ] Integration tests pass

### Notes
- Completed: 2025-10-15
- Blocker: [If any]

---

## Epic 2: [Name]

**Status:** 🔄 In Progress

### Tasks
- [x] Task 2.1: [Description]
- [ ] Task 2.2: [Description] ← CURRENT

### Validation
- [ ] Type checking
- [ ] Tests

### Notes
- Started: 2025-10-16

---

## Backlog

- [ ] Future Epic 1
- [ ] Future Epic 2

---

## Archive

Move completed sections here with completion date.
```

### Update Frequency

**During PRP Execution:**
- After completing each epic
- After validation checkpoint
- When blocked
- At end of epic

**Between Sessions:**
- Before `/clear`
- When switching focus
- At end of work session

---

## Quality Standards

### Validation Gates

**Level 1: Type Checking** ❌ BLOCKING
```bash
# Must pass before proceeding
[Your type check command]
```

**Level 2: Linting** ❌ BLOCKING
```bash
# Must pass before proceeding
[Your lint command]
```

**Level 3: Unit Tests** ❌ BLOCKING
```bash
# Must pass with coverage thresholds
[Your test command]
# Coverage: ≥70% overall, ≥90% critical paths
```

**Level 4: Integration Tests** ⚠️ STRONGLY RECOMMENDED
```bash
[Your integration test command]
```

**Level 5: E2E Tests** ⚠️ RECOMMENDED
```bash
[Your e2e test command]
```

### Coverage Thresholds

**Minimum (Level 3):**
- Overall: ≥70%
- Critical paths: ≥90%

**Recommended (Level 4):**
- Overall: ≥80%
- Critical paths: ≥95%

**Excellent (Level 5):**
- Overall: ≥90%
- Critical paths: 100%

---

## Sub-Agent Patterns

### When to Use Sub-Agents

**✅ EXCELLENT Use Cases:**
- Comprehensive testing & validation
- Code review & security audits
- Documentation generation
- Research & pattern analysis
- Repetitive bulk operations (10+ files)
- Task list management (updating *_TASKS.md)

**❌ AVOID For:**
- Simple file reads (use Read tool)
- Single searches (use Glob/Grep)
- Quick 2-3 file analysis
- Trivial edits

### Sub-Agent Invocation Pattern

```markdown
Launch [general-purpose] sub-agent to [task description]:

1. [Specific step 1]
2. [Specific step 2]
3. [Specific step 3]

Return:
- [Expected output 1]
- [Expected output 2]
- Confidence score (1-10)
```

---

## Context Management

### Preservation Strategies

**1. CLAUDE.md Files**
- Root CLAUDE.md for project overview
- Module-specific CLAUDE.md for subsystems
- Update when patterns change

**2. Task Files**
- Update after each epic
- Mark current task clearly
- Note blockers immediately

**3. Documentation**
- Keep methodology in docs/
- Archive completed work
- Link related documents

**4. Git Commits**
- Commit after each epic
- Use descriptive messages
- Reference PRPs in commits

### Recovery Protocol

**After `/clear`:**
```bash
/recover-context.md
```

**After Internet Loss:**
```bash
cat CLAUDE.md
cat PROJECT_TASKS.md
git log -5 --oneline
```

**Manual Recovery:**
1. Read CLAUDE.md
2. Read active task files
3. Check git history
4. Review recent PRPs

---

## Customization Guide

### For Different Tech Stacks

**Backend (Python/FastAPI):**
- Update commands: `pytest`, `mypy`, `ruff`
- Validation: pytest coverage, type hints
- Patterns: FastAPI routes, Pydantic models

**Backend (Node/Express):**
- Update commands: `jest`, `tsc`, `eslint`
- Validation: Jest coverage, TypeScript
- Patterns: Express middleware, Zod schemas

**Frontend (React):**
- Update commands: `vitest`, `tsc`, `eslint`
- Validation: Vitest coverage, TypeScript
- Patterns: React hooks, component structure

**Frontend (Vue):**
- Update commands: `vitest`, `vue-tsc`, `eslint`
- Validation: Vitest coverage, TypeScript
- Patterns: Vue composition API, composables

### For Different Project Types

**Library/Package:**
- Focus on API design PRPs
- Emphasize documentation
- Include publishing workflow

**CLI Tool:**
- Focus on command structure
- Include usage examples
- Test with real scenarios

**Web Application:**
- Focus on user flows
- Include E2E tests
- Document deployment

**Microservices:**
- Separate CLAUDE.md per service
- PRPs/ organized by service
- Service-specific task files

---

## Example Workflow

### Starting a New Feature

```bash
# 1. Generate PRP
/generate-prp.md "User authentication with JWT"

# 2. Review generated PRP
cat PRPs/user-authentication-prp.md

# 3. Execute PRP (creates/updates PROJECT_TASKS.md)
/execute-prp.md PRPs/user-authentication-prp.md

# Claude will:
# - Create PROJECT_TASKS.md with epics
# - Implement each epic
# - Validate after each epic
# - Update task file after each epic
# - Run final validation gates

# 4. Check progress anytime
cat PROJECT_TASKS.md

# 5. If context lost
/recover-context.md
```

### Continuing After Context Loss

```bash
# Option 1: Use recover command
/recover-context.md

# Option 2: Manual recovery
cat CLAUDE.md
cat PROJECT_TASKS.md
git log -10 --oneline

# Then continue where you left off
cat PRPs/[current-prp].md  # If mid-PRP
# Resume implementation
```

---

## Getting Started Checklist

- [ ] Copy directory structure
- [ ] Customize CLAUDE.md with your project details
- [ ] Update .claude/commands/ with your tech stack
- [ ] Create initial PROJECT_TASKS.md
- [ ] Test /recover-context.md command
- [ ] Generate first PRP with /generate-prp.md
- [ ] Execute first PRP with /execute-prp.md
- [ ] Commit structure to git

---

## Files to Copy from Template

**Essential (copy these):**
```
CLAUDE.md                       # Customize for your project
.claude/commands/
  ├── generate-prp.md          # Update tech stack references
  ├── execute-prp.md           # Update validation commands
  └── recover-context.md       # Update file paths
docs/
  ├── prp-methodology.md       # Keep as-is
  ├── quality-standards.md     # Update validation commands
  ├── sub-agent-patterns.md    # Keep as-is
  └── context-management.md    # Keep as-is
PRPs/
  └── README.md                # Customize examples
```

**Optional (adapt as needed):**
```
.claude/commands/
  ├── check-dependencies.md
  ├── verify-setup.md
  └── run-tests.md
```

---

## Tips for Success

**1. Start Small**
- Use minimal structure first
- Add complexity as needed
- Don't over-engineer initially

**2. Update CLAUDE.md Early**
- Add patterns as you discover them
- Document non-obvious decisions
- Keep it current

**3. Use PRPs Consistently**
- Don't skip for "small" features
- They catch edge cases early
- Build better mental models

**4. Trust Task Files**
- Update them religiously
- They're your safety net
- Mark current task clearly

**5. Validate Often**
- Run validation after each epic
- Don't batch validations
- Fix issues immediately

**6. Leverage Sub-Agents**
- Use for repetitive work
- Use for comprehensive validation
- Don't use for simple tasks

---

## Support

**Lost context?**
→ `/recover-context.md`

**PRP unclear?**
→ `docs/prp-methodology.md`

**Validation failing?**
→ `docs/quality-standards.md`

**Sub-agent confusion?**
→ `docs/sub-agent-patterns.md`

**Context management?**
→ `docs/context-management.md`

---

## Version History

**1.0.0** (2025-10-18)
- Initial template extracted from Offboarding Knowledge Capture System
- Includes CLAUDE.md, PRPs, custom commands, task tracking
- Supports monorepo and single-module projects

---

## License

Adapt freely for your projects. Attribution appreciated but not required.

---

**Last Updated:** 2025-10-18
**Source Project:** Offboarding Knowledge Capture System
**Template Version:** 1.0.0
