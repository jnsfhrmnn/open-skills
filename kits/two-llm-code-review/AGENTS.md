# AGENTS.md - Beispiel für Zwei-LLM-Code-Review

Diese Datei ist ein minimales Muster für ein Repository, in dem ein LLM implementiert und ein zweites LLM reviewt.

## Rollenmodell

- Implementierer-LLM coded.
- Reviewer-LLM reviewt.
- Das Reviewer-LLM ist für Code-Review, Sicherheits-/Architektur-Audit, Audit-Logs, Done-Listen und Review-Pläne zuständig.
- Das Reviewer-LLM ändert Produktcode nicht direkt, außer der Nutzer gibt dafür ausdrücklich einen konkreten Implementierungsauftrag.
- Review-Pläne sind keine 1:1-Implementierungsanweisung. Das Implementierer-LLM muss den Audit selbst lesen, selbst planen, Review-Plan und eigenen Plan gegenseitig verbessern, einen Fusionsplan schreiben und erst diese Fusion umsetzen.

## Projektregeln lesen

- Lies die vorhandene Projektanweisung deines Repositories, zum Beispiel `CLAUDE.md`, `AGENTS.md`, `README.md`, Architektur-Dokumente oder Contributing-Guides.
- Klone lange Projektanweisungen nicht in diese Datei. Referenziere sie direkt.
- Wenn eine bestehende Projektanweisung schreibgeschützt bleiben soll, schreibe Ergänzungen additiv in diese Datei oder in eine separate Reviewer-Datei.

## Review-Workflow

- Nutze den global installierten Skill `~/.codex/skills/codex-claude-review-loop/SKILL.md` bzw. unter Windows `C:\Users\<dein-name>\.codex\skills\codex-claude-review-loop\SKILL.md`.
- Schreibe Audit-Logs und Plan-Dateien als normale Markdown-Dateien.
- Übergib Audit und Plan im Chat an das Implementierer-LLM.
- Halte fest, welche Dateien bereits mit welchem Commit oder Hash geprüft wurden.
