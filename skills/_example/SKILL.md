---
name: example
description: A minimal template skill. Copy this folder, rename it, and replace the body with instructions for the one job you want Claude to do well. Use this as the starting point when authoring a new Claude Code skill.
---

# Example skill (template)

This is a starting point. Delete everything below and write your own instructions.

## When to use

Describe, in one or two sentences, the situation in which this skill should fire.
The `description` in the frontmatter above is what Claude reads to decide whether
to load the skill — make it specific and trigger-friendly.

## Instructions

Write the actual procedure here. Good skills are:

- **Focused** — one job, done well. Split unrelated jobs into separate skills.
- **Self-contained** — no references to private repos, internal tools, or secrets.
- **Concrete** — prefer step-by-step instructions over vague advice.
- **Safe** — never hardcode credentials; read them from the environment if needed.

## Example structure for a real skill

1. State the goal in one line.
2. List the steps Claude should take, in order.
3. Note any edge cases or things to avoid.
4. (Optional) Reference helper files you ship alongside `SKILL.md` in this folder.
