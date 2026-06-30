# 01 - Installation

## Ziel

Dieses Paket in einem bestehenden Repository verwenden, ohne spezielle Infrastruktur.

## Schritte

1. Kopiere `AGENTS.md` in dein Repository oder übertrage die Rollenregel in deine bestehende Agent-Datei.
2. Installiere den Skill global, damit er in allen Repositories nutzbar ist:
   - Windows: `C:\Users\<dein-name>\.codex\skills\codex-claude-review-loop\`
   - macOS/Linux: `~/.codex/skills/codex-claude-review-loop/`
3. Kopiere dazu den Paketordner `codex-skills/codex-claude-review-loop/` an diese Stelle.
4. Prüfe in einer neuen Codex-Session, ob `$codex-claude-review-loop` bekannt ist.
5. Optional: Passe `AGENTS.md` an deine bestehenden Projektregeln an.

## Erwartete Struktur im Ziel-Repo

```text
my-project/
  AGENTS.md

~/.codex/
  skills/
    codex-claude-review-loop/
      SKILL.md
      agents/openai.yaml
      references/output-templates.md
      scripts/review_inventory.py
```

## Test

```powershell
python "$env:USERPROFILE\.codex\skills\codex-claude-review-loop\scripts\review_inventory.py" --repo . --scope changed
```

Der Befehl sollte ein Inventar ausgeben. Er bewertet keinen Code, sondern sammelt nur Dateien, Hashes und Cluster.
