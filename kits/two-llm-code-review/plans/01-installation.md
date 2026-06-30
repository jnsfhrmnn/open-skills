# 01 - Installation

## Ziel

Dieses Paket in einem bestehenden Repository verwenden, ohne spezielle Infrastruktur.

## Schritte

1. Kopiere `AGENTS.md` in dein Repository oder übertrage die Rollenregel in deine bestehende Agent-Datei.
2. Kopiere `.codex/skills/codex-claude-review-loop/` in dein Repository oder in dein Codex-Skill-Verzeichnis.
3. Prüfe, ob dein Codex die Skill-Datei erkennt.
4. Optional: Passe `AGENTS.md` an deine bestehenden Projektregeln an.

## Erwartete Struktur im Ziel-Repo

```text
my-project/
  AGENTS.md
  .codex/
    skills/
      codex-claude-review-loop/
        SKILL.md
        agents/openai.yaml
        references/output-templates.md
        scripts/review_inventory.py
```

## Test

```powershell
python .codex/skills/codex-claude-review-loop/scripts/review_inventory.py --repo . --scope changed
```

Der Befehl sollte ein Inventar ausgeben. Er bewertet keinen Code, sondern sammelt nur Dateien, Hashes und Cluster.
