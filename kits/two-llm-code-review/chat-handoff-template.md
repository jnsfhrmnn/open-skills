# Chat-Handoff-Template

Kopiere diesen Text in den Chat des Implementierer-LLMs, nachdem das Reviewer-LLM Audit und Plan-Dateien erstellt hat.

```text
Du bist jetzt das Implementierer-LLM.

Wichtiges Rollenmodell:
- Du implementierst.
- Das zweite LLM hat unabhängig reviewt.
- Du sollst den Review-Plan nicht blind 1:1 umsetzen.

Lies zuerst diese Dateien:
1. <Pfad zum Audit-Log>
2. <Pfad zur Plan-Datei>
3. <Optional: Done-Liste oder Inventar>

Deine Aufgabe:
1. Lies den Audit vollständig.
2. Erstelle einen eigenen unabhängigen Umsetzungsplan.
3. Vergleiche deinen Plan mit dem Review-Plan.
4. Suche aktiv Widersprüche, fehlende Tests, Sicherheitslücken und Architektur-Risiken.
5. Schreibe einen Fusionsplan aus beiden Plänen.
6. Setze erst den Fusionsplan um.
7. Verifiziere mit Tests, Lint, Build oder anderen Projekt-Gates.
8. Schreibe am Ende kurz:
   - was umgesetzt wurde,
   - welche Dateien geändert wurden,
   - welche Tests liefen,
   - welche Risiken offen bleiben.

Nicht erlaubt:
- Den Review-Plan ungeprüft kopieren.
- Kritische Findings ohne Begründung ignorieren.
- Produktcode außerhalb des vereinbarten Scopes anfassen.
- Secrets, Tokens oder private Daten in Logs oder Commit-Nachrichten schreiben.
```

## Platzhalter

- `<Pfad zum Audit-Log>`: zum Beispiel `_audit/codex-review-loop/2026-06-30-audit.md`
- `<Pfad zur Plan-Datei>`: zum Beispiel `plans/01-fix-policy-bypass.md`
- `<Optional: Done-Liste oder Inventar>`: zum Beispiel `_audit/codex-review-loop/done-list.jsonl`
