# Recover Context - 10-K AI Intelligence Pipeline

**Use after /clear or context loss**

---

## Detect Work Area

Check which module you're working on:

```bash
# Check current directory
pwd

# If in backend/ → Backend context
# If in frontend/ → Frontend context
# If in root → Check recent git changes
```

---

## Load Context

### For Backend Work

```bash
# Read guides
cat backend/CLAUDE.md

# Read current tasks
cat BACKEND_TASKS.md

# Check recent commits
git log --oneline -5 backend/
```

**Loaded:**
- Backend-specific patterns (FastAPI, Browser-Use, Daytona)
- Current PRD progress
- Recent work

### For Frontend Work

```bash
# Read guides
cat frontend/CLAUDE.md

# Read current tasks
cat FRONTEND_TASKS.md

# Check recent commits
git log --oneline -5 frontend/
```

**Loaded:**
- Frontend-specific patterns (React, TypeScript, TailwindCSS)
- Current component progress
- Recent work

---

## Summary Format

```
🔍 CONTEXT RECOVERED

📂 Project: 10-K AI Intelligence Pipeline
🎯 Module: [BACKEND | FRONTEND]

📚 Context Loaded:
✅ Module CLAUDE.md
✅ TASKS.md file
✅ Recent git history

📍 CURRENT STATUS:
[From TASKS.md - current epic/task]

🔧 IN PROGRESS:
[Current work]

📋 NEXT ACTIONS:
[Next 3-5 tasks]

⚠️ BLOCKERS:
[Any blockers or "None"]

🚀 Ready to continue!
```

---

**Last Updated:** 2025-10-18
