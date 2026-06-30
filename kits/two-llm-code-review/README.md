# Code mit einem zweiten LLM reviewen

Dieses Paket zeigt ein einfaches Prinzip:

**Ein LLM schreibt Code. Ein zweites LLM reviewt.**

So entsteht ein Vier-Augen-Prinzip für KI-gestützte Entwicklung. Das erste Modell arbeitet als Implementierer, das zweite Modell arbeitet als unabhängiger Reviewer. Der Reviewer ändert den Produktcode nicht direkt, sondern erzeugt Audit-Logs, Done-Listen und konkrete Plan-Dateien. Danach liest der Implementierer den Audit, erstellt einen eigenen Plan, vergleicht beide Pläne und setzt erst eine verbesserte Fusion um.

## Inhalt

```text
two-llm-code-review/
  README.md
  AGENTS.md
  chat-handoff-template.md
  codex-skills/
    codex-claude-review-loop/
      SKILL.md
      agents/openai.yaml
      references/output-templates.md
      scripts/review_inventory.py
  plans/
    01-installation.md
    02-review-workflow.md
```

## Schnellstart

1. Kopiere `AGENTS.md` in dein Repository oder übertrage die Rollenregel in deine bestehende Agent-Datei. Diese Projekt-Härtung bleibt lokal im jeweiligen Repo.
2. Installiere den Skill global, nicht doppelt im Repo:
   - Windows: kopiere `codex-skills/codex-claude-review-loop/` nach `C:\Users\<dein-name>\.codex\skills\codex-claude-review-loop\`
   - macOS/Linux: kopiere `codex-skills/codex-claude-review-loop/` nach `~/.codex/skills/codex-claude-review-loop/`
3. Lass ein LLM implementieren.
4. Lass Codex mit `$codex-claude-review-loop` reviewen.
5. Gib dem Implementierer anschließend `chat-handoff-template.md`, den Audit und die Plan-Datei.
6. Der Implementierer setzt nicht blind um, sondern schreibt einen Fusionsplan aus eigenem Plan und Review-Plan.

## Warum das funktioniert

- Das Review-Modell hat ein anderes Fehlerprofil.
- Die Rollen sind getrennt: Implementierung ist nicht Review.
- Die Done-Liste verhindert doppelte Arbeit über viele Dateien.
- Die Plan-Dateien machen aus Kritik umsetzbare Arbeit.
- Das Muster funktioniert auch ohne spezielle Infrastruktur: Chat + Dateien reichen.

## Sicherheitsregel

Dieses Paket ist ein Muster. Entferne vor öffentlicher Nutzung alle privaten Pfade, Projektnamen, Screenshots, Secrets und Kundendaten.

## Warum global installieren?

Der Skill ist wiederverwendbar und sollte nur einmal in deinem persönlichen Codex-Skill-Ordner liegen. Die Rollenregel in `AGENTS.md` bleibt dagegen pro Repository lokal, weil jedes Projekt eigene Regeln, Schutzbereiche und Dokumentationspfade hat.
