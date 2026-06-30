# 02 - Review-Workflow

## Ziel

Ein LLM implementiert, ein zweites LLM reviewt unabhängig.

## Ablauf

1. Implementierer-LLM schreibt Code oder ändert Dateien.
2. Reviewer-LLM startet `$codex-claude-review-loop`.
3. Reviewer-LLM erstellt ein Inventar der geänderten Dateien.
4. Reviewer-LLM bildet Cluster: Security, Architektur, Tests, Doku, Release.
5. Reviewer-LLM schreibt Audit-Log und Done-Ledger.
6. Reviewer-LLM schreibt Plan-Datei(en) mit konkreten Umsetzungsschritten.
7. Nutzer kopiert `chat-handoff-template.md` in den Chat des Implementierer-LLMs und ergänzt Audit-/Plan-Pfade.
8. Implementierer-LLM schreibt einen eigenen Plan, vergleicht ihn mit dem Review-Plan und setzt eine Fusion um.

## Wichtig

- Der Reviewer ändert keinen Produktcode.
- Der Implementierer übernimmt den Review-Plan nicht blind.
- Jede kritische Schwachstelle braucht Evidenz und Verifikation.
- Die Done-Liste verhindert, dass bei langen Reviews dieselben Dateien wieder und wieder geprüft werden.

## Ergebnisartefakte

```text
_audit/codex-review-loop/
  <run-id>-inventory.json
  <run-id>-audit.md
  done-list.jsonl

plans/
  <number>-<topic>.md
```
