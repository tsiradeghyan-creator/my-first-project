# CLAUDE.md

## Project Overview

This is a starter project repository ("My First Project"). It is currently in its initial state with no application code, build system, or dependencies yet configured.

## Repository Structure

```
.
├── README.md        # Project description
└── CLAUDE.md        # This file — guidance for AI assistants
```

## Development Guidelines

### Git Workflow

- **Default branch**: `master`
- Write clear, descriptive commit messages that explain the "why" behind changes.
- Keep commits focused — one logical change per commit.
- Do not force-push to `master`.

### Adding Code

When adding new code to this project:

1. **Choose a language/framework** and set up the appropriate tooling (e.g., `package.json` for Node.js, `requirements.txt` for Python, `Cargo.toml` for Rust).
2. **Add a `.gitignore`** appropriate for the chosen language before committing generated or dependency files.
3. **Prefer standard project layouts** for the chosen ecosystem (e.g., `src/` for source code, `tests/` for tests).

### Code Style & Conventions

- Follow the standard conventions of whatever language/framework is adopted.
- Keep files small and focused on a single responsibility.
- Write tests alongside new features.

### What to Avoid

- Do not commit secrets, credentials, or `.env` files.
- Do not commit large binary files or build artifacts.
- Do not add unnecessary dependencies.

## Notes for AI Assistants

- This project is in its earliest stage. There are no build commands, test commands, or lint commands yet.
- When the user starts adding code, update this file to reflect the actual tech stack, build steps, and project conventions.
- Always read existing files before modifying them.
- Prefer editing over creating new files when possible.
