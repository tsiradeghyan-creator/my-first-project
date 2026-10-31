---
description: Read and answer the VS Code ⇄ Cloud mailbox in BRIDGE.md, or post a new message to the other side.
argument-hint: "[optional: a new question to send to the other side]"
---

You are one side of a shared workspace. Work out which side you are: if the environment is a cloud container (for example the path starts with /home/user/ and CLAUDE_CODE_REMOTE or a similar remote marker is set, or there is no macOS `sw_vers`), you are **Cloud**; on Tigran's laptop you are **VS Code**.

1. Run `git pull origin main`.
2. Read `BRIDGE.md` and `NOTES.md` (newest first).
3. Answer every message marked OPEN that is addressed to your side, following the rules at the top of BRIDGE.md. Do the real work the question needs (run the commands, read the files) and never paste secret values.
4. If `$ARGUMENTS` is not empty, add it as a new message from your side to the other side, at the top of the current thread (or a new thread if it starts a new topic), with the next id.
5. Add a short NOTES.md entry if anything was decided or changed.
6. Commit with a message like "Bridge: <side> answered C1-C3" and push to main.
7. Tell Tigran in Armenian, in a few lines: what you answered, what you asked, and that the other side needs `/bridge` to see it.
