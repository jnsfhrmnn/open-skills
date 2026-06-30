# Contributing to open-skills

Thanks for wanting to make this better. This repo is a free collection of small,
self-contained Claude Code skills. The bar is simple: a skill should be useful,
generic, and safe to share publicly.

## Ground rules

- **Generic only.** No references to private projects, internal infrastructure,
  company names, client data, or anything that only makes sense inside one org.
- **No secrets.** Never commit API keys, tokens, passwords, or `.env` files.
  Skills that need credentials should read them from the environment.
- **Self-contained.** A skill lives in its own folder under `skills/` and works
  after a plain copy into `~/.claude/skills/` — no extra install steps.
- **One job per skill.** If it does two unrelated things, make it two skills.

## Adding a skill

1. Create `skills/<your-skill-name>/SKILL.md`.
2. Add frontmatter with a `name` and a clear, trigger-friendly `description`.
3. Write focused, step-by-step instructions (see `skills/_example/SKILL.md`).
4. Add a row to the **Catalog** table in `README.md`.
5. Open a pull request.

## License

By contributing, you agree your contribution is licensed under the
[GPL-3.0](LICENSE), the same license as the rest of this repository.
