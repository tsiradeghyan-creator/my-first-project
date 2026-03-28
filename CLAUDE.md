# CLAUDE.md

This file provides guidance for AI assistants (Claude and others) working in this repository.

## Project Overview

**my-first-project** is a newly initialized repository with no source code yet. It currently contains only a README.md. Development conventions below should be followed as the project grows.

## Repository Structure

```
my-first-project/
├── CLAUDE.md       # This file — AI assistant guidance
└── README.md       # Project introduction
```

## Git Workflow

- The default branch is `main`.
- Feature and task branches follow the pattern: `<prefix>/<short-description>-<id>` (e.g., `claude/add-claude-documentation-DMirb`).
- Commit messages should be short, imperative, and descriptive (e.g., `Add login page`, `Fix null pointer in auth handler`).
- Never push directly to `main` without explicit permission.
- Always use `git push -u origin <branch-name>` when pushing a new branch.

## Development Conventions

Since no language or framework has been chosen yet, apply these general rules and update this file once a stack is selected:

- Keep commits small and focused on a single concern.
- Do not commit secrets, credentials, or `.env` files.
- Add a `.gitignore` appropriate for the chosen language/framework before adding source files.
- Write tests alongside new features, not as an afterthought.

## Adding a Stack

When a language or framework is introduced, update this file to include:

1. **Language & runtime version** (e.g., `Node.js 20`, `Python 3.12`)
2. **Package manager** (e.g., `npm`, `pip`, `cargo`)
3. **How to install dependencies** (e.g., `npm install`)
4. **How to run the project** (e.g., `npm start`)
5. **How to run tests** (e.g., `npm test`)
6. **Linting / formatting tools and commands**
7. **Build steps** if applicable

## AI Assistant Notes

- This is an early-stage project. Prefer simple solutions over complex abstractions.
- Do not add frameworks, dependencies, or boilerplate unless explicitly asked.
- When introducing new files, update this CLAUDE.md to reflect the new structure.
- Follow the git workflow described above: develop on the designated branch, commit with clear messages, then push.
