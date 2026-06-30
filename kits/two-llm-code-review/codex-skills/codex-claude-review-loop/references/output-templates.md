# Output Templates

Use these templates for durable artifacts created by `codex-claude-review-loop`.

## Audit Log

```markdown
# Codex Review Audit - <run_id>

**Repo:** <repo>
**Branch:** <branch>
**Baseline commit:** <commit>
**Worktree dirty:** <yes/no>
**Codex model:** <model or not available>
**Scope:** <paths/range>
**Inventory:** <path to inventory json>
**Done ledger:** <path to done-list.jsonl>

## Coverage

| Cluster | Files scanned | Files skipped unchanged | Remaining | Notes |
|---|---:|---:|---:|---|

## Findings

| ID | Severity | File:line | Cluster | Problem | Attack/failure path | Evidence | Plan ref | Status |
|---|---|---|---|---|---|---|---|---|

## Cross-Cluster Architecture Findings

| ID | Severity | Interfaces | Problem | Evidence | Plan ref | Status |
|---|---|---|---|---|---|---|

## Verification Commands Run

| Command | Result | Notes |
|---|---|---|

## Limits

- <Anything not read, not executable, or not verifiable>
```

## Done Ledger JSONL Entry

One JSON object per scanned file:

```json
{
  "run_id": "20260630-120000-codex-review",
  "timestamp_utc": "2026-06-30T10:00:00Z",
  "repo": "my-project",
  "branch": "main",
  "commit": "abc123",
  "content_ref": "commit",
  "worktree_dirty": true,
  "path": "src/example.py",
  "blob_sha256": "<sha256>",
  "size_bytes": 1234,
  "line_count": 42,
  "cluster": "security-boundary",
  "audit_status": "scanned-findings",
  "finding_ids": ["SEC-001"],
  "plan_refs": ["plans/01-fix-policy-bypass.md"],
  "auditor": "Codex",
  "auditor_model": "GPT-5",
  "notes": "No product-code edits by Codex."
}
```

Valid `audit_status` values: `scanned`, `scanned-no-findings`, `scanned-findings`, `skipped-unchanged`, `blocked`, `out-of-scope`.

## Plan File

```markdown
# <number> - <short title>

**Source:** Codex review audit <run_id>
**Audit:** <path to audit log>
**Codex model:** <model>
**Baseline commit:** <commit>

## Handoff Rule

The coding agent must not implement this Codex plan 1:1. It must read the audit, create an independent plan, compare both plans, improve them against each other, write a fusion plan, and only then implement.

## Findings

| ID | Severity | Short problem | File | Why it matters |
|---|---|---|---|---|

## Implementation Steps

1. <Step>
2. <Step>
3. <Step>

## Acceptance Criteria

- <Criterion with evidence>

## Verification

```powershell
<command>
```

## Non-Scope

- <What the coding agent must not touch>

## Risks

- <Regression/security/architecture risk>
```

## Chat Handoff

```text
Codex reviewed and planned this with <Codex model>.

Audit: <audit path>
Plan: <plan path>
Done ledger: <done ledger path>

Do not implement the Codex plan 1:1. Read the audit, create your own independent plan, compare both plans, improve them against each other, write a fusion plan, and only then implement the fusion with verification evidence.
```
