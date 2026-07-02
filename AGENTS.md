# AGENTS.md

> **Project:** Teaching repository for the "Working Critically with AI Coding Tools" workshop.
> **Core constraint:** Learners experiment with AI coding tools; code should not be changed except as a deliberate workshop exercise.

## Toolchain

| Action | Command |
|---|---|
| Run notebook | `jupyter nbconvert --to notebook --execute text_analysis_notebook.ipynb` |
| AI config | `opencode.json` |

## Judgment Boundaries

**ASK**
- Before modifying any existing code or fixing any issue

## AI Use Policy

AI assistance is expected and encouraged. When committing AI-assisted work, the precise model used **must** be named in the commit message body.

### Example Commit Message

```
feat: add lemmatization pipeline to notebook

AI: DeepSeek V4 Flash (opencode/deepseek-v4-flash-free)
```

The model identifier should match the exact model string used (e.g., `openrouter/free`, `claude-sonnet-4-20250514`, `gpt-4o-2025-01-20`).
