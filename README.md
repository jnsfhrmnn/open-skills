# open-skills

Free, ready-to-use **skills & kits for AI coding agents** ([Claude Code](https://docs.claude.com/en/docs/claude-code), [Codex](https://openai.com/codex/) & co.) — given away for fellow vibe coders.

Each item is small and self-contained: drop it into your agent and use it immediately. No setup, no accounts, no strings attached. Take what's useful, remix it, ship faster.

- **Skills** (`skills/`) — single-folder agent skills (one `SKILL.md`).
- **Kits** (`kits/`) — small ready-to-copy packages that wire several pieces together (agent rules, a skill, plan templates, a workflow).

## What is a "skill"?

A Claude Code skill is a folder with a `SKILL.md` file. The file has a bit of frontmatter (a `name` and a `description`) and then instructions that tell Claude how to do one specific job well. When the job matches, Claude loads the skill and follows it.

```
skills/
  my-skill/
    SKILL.md          <- required: the skill itself
    (optional helper files, scripts, templates, ...)
```

See [`skills/_example/SKILL.md`](skills/_example/SKILL.md) for a minimal template.

## How to install a skill

Pick a skill folder and copy it into one of these locations:

| Scope | Path | Use when |
|---|---|---|
| **Personal** (all your projects) | `~/.claude/skills/<skill-name>/` | You want it everywhere |
| **Project** (one repo, shareable with a team) | `<your-project>/.claude/skills/<skill-name>/` | It belongs to a specific project |

On Windows, `~` is `C:\Users\<you>`.

Example (personal install of the example skill):

```bash
# macOS / Linux
cp -r skills/_example ~/.claude/skills/example

# Windows (PowerShell)
Copy-Item -Recurse skills\_example $env:USERPROFILE\.claude\skills\example
```

Restart Claude Code (or start a new session) and the skill is available.

## Catalog

### Kits

| Kit | What it does |
|---|---|
| [`two-llm-code-review`](kits/two-llm-code-review/) | Have a **second LLM review your code**. One model implements, a second model reviews independently — writing audit logs and plan files instead of silently rewriting. Four-eyes principle for AI-assisted development. Works with plain files + chat handoff, no special infrastructure. |

### Skills

| Skill | What it does |
|---|---|
| [`_example`](skills/_example/SKILL.md) | Template showing the skill format — copy it to start your own |

_More skills and kits are added over time. Suggestions and pull requests welcome._

## Contributing

Found a bug, want to improve a skill, or have one to add? See [CONTRIBUTING.md](CONTRIBUTING.md). Keep skills generic, self-contained, and free of any private/project-specific details.

## License

[GNU General Public License v3.0](LICENSE) © Jens Fehrmann

You are free to use, study, share, and modify these skills. If you distribute modified versions, they must stay under the GPL-3.0 as well.
