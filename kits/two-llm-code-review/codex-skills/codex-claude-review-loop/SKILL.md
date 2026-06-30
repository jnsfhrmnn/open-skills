---
name: codex-claude-review-loop
description: Codex-only autonomous review workflow for auditing implementation output from another coding agent or LLM, especially security vulnerabilities, architecture weaknesses, policy bypasses, fail-open behavior, cross-platform regressions, update/signing/supply-chain risks, and handoff plans. Use when the user asks Codex to review, audit, scan, critique, harden, cluster files, maintain a done list by file and commit, create audit logs, or prepare improvement plans for another coding agent to implement. Do not use for implementing product code.
---

# Codex Claude Review Loop

## Role

Codex reviews. The coding agent codes.

Use this skill to inspect code and plans produced by another coding LLM, find weaknesses, write audit evidence, and draft improvement plans. Do not implement product-code fixes under this skill. Codex may create or update only review artifacts such as audit logs, done ledgers, plan files, and this skill's own support files.

Always state the active Codex model in audit and plan outputs when it is known. If the model cannot be read, write `Codex model: not available from current runtime`.

## Required Sources

At the start of every run:

1. Read the repository's project instructions, such as `AGENTS.md`, `CLAUDE.md`, `README.md`, architecture docs, and contribution docs.
2. Read `references/output-templates.md` before writing audit logs, done-list entries, handoff text, or plan files.
3. If the repository has its own review rules, security gates, or release checklist, use them as audit criteria.

If a referenced file is unavailable, record that as an audit limitation and continue with the built-in workflow.

## Non-Negotiables

- Be a hard critic of implementation output. Assume fluent code can still hide security, architecture, lifecycle, and compliance failures.
- Audit evidence beats intuition. Every finding needs a file, line or symbol, impact, exploit or failure path, and verification status.
- No per-file permission prompts. Build clusters and work through them autonomously until the scope is exhausted, the time budget is hit, or a true blocking ambiguity appears.
- Do not silently narrow scope for convenience. If the scope is too large, create a resumable run with a ledger and continue cluster by cluster.
- Do not implement product fixes. Produce a plan for the coding agent, then require that agent to read the audit, make its own plan, compare both plans, write a fusion plan, and implement that fusion.
- Use normal files and chat handoffs. No special messaging infrastructure is required.

## Workflow

### Gate 0: Briefing And Role Check

Write a short visible block:

- Scope: target path, commit range, branch, PR, or whole repo.
- Role: `Codex reviews; coding agent codes`.
- Mutation boundary: review artifacts only; no product-code edits.
- Model stamp: active Codex model if known.
- Handoff rule: write audit and plan files, then provide a chat handoff for the coding agent.

Ask only if the scope or authority is genuinely unclear. Do not ask before every file or cluster.

### Phase 1: Inventory And Done Ledger

Run the helper when possible:

```powershell
python "$env:USERPROFILE\.codex\skills\codex-claude-review-loop\scripts\review_inventory.py" --repo . --scope changed
```

On macOS/Linux, use `python ~/.codex/skills/codex-claude-review-loop/scripts/review_inventory.py --repo . --scope changed`.

Use `--scope all` for whole-repo reviews or `--target <path>` for explicit scopes. The script only inventories files; it does not judge code quality.

Create or reuse:

- Audit directory: `_audit/codex-review-loop/`
- Done ledger: `_audit/codex-review-loop/done-list.jsonl`
- Run inventory: `_audit/codex-review-loop/<run_id>-inventory.json`
- Audit log: `_audit/codex-review-loop/<run_id>-audit.md`

Ledger rule:

- A file is already deeply scanned only if the done ledger has the same path and same blob hash for the relevant commit/worktree content.
- If the file changed, rescan it.
- If the file content is unchanged but neighboring interfaces changed, include it in cross-file architecture review without repeating the full line-by-line audit.
- Record every scanned file, even when there are no findings.

### Phase 2: Cluster Worklist

Group files before reading deeply. Prioritize clusters in this order:

1. Security boundary: policy, auth, permissions, secrets, data classification, egress, audit logs, redaction.
2. Release and supply chain: signing, update, rollback, dependency locks, hashes, immutable versioning.
3. Deployment and operations: compose, infrastructure, service management, backup/restore, offline mode.
4. Architecture core: gateways, plugins, retrieval, datastore, admin config, control plane.
5. Public interfaces: APIs, schemas, CLI contracts, UI actions that mutate state.
6. Tests and gates: unit/integration/e2e tests, CI, lint, gap detectors, negative tests.
7. Documentation and plans that claim security or compliance behavior.

Skip generated caches, dependency folders, binary blobs, model files, and secrets unless the user explicitly asks and the repo permits it. Never open secret values merely to satisfy coverage.

### Phase 3: Deep Audit Per Cluster

For each cluster, run an audit-plan-audit-refine loop:

1. AUDIT: Read the relevant files, tests, and docs. Identify concrete weaknesses.
2. PLAN: Draft fix direction, acceptance criteria, and verification commands for the coding agent.
3. AUDIT THE PLAN: Attack your own plan. Look for missing threat paths, weak tests, vague acceptance criteria, and places where the coding agent could implement the wrong thing.
4. REFINE: Strengthen the plan and re-check until no Critical or High plan defects remain, or mark unresolved risks.

Use these lenses on every security or architecture file:

- Fail-closed vs fail-open defaults.
- Policy bypass paths across UI, API, CLI, background jobs, imports, migrations, and tests.
- Secrets in logs, audit chains, errors, fixtures, docs, env handling, or generated artifacts.
- Egress paths, network calls, telemetry, update checks, webhook behavior, and DNS assumptions.
- Authn/authz confusion, privilege escalation, object-level access, tenant boundaries, role drift.
- Unsafe parsing/deserialization, path traversal, shell invocation, command construction, temp-file races.
- Signature verification, hash pinning, rollback, replay, mutable latest, time-of-check/time-of-use.
- Auditability: durable logs, denied actions logged, restart behavior.
- Cross-platform behavior on Linux, macOS, and Windows; no OS-only assumptions outside declared abstraction.
- Runtime degradation, resource budgets, and graceful fallback.
- Licensing or clean-room contamination when third-party code is involved.
- Tests: prove negative cases, bypass attempts, denied paths, rollback, restart, and corrupted input.

Be concrete. A valid finding includes:

- Severity: Critical, High, Medium, or Low.
- Location: file plus line/symbol.
- Problem: what is wrong.
- Attack or failure path: how it breaks in production or review.
- Evidence: code excerpt summary, command output, or `unverified`.
- Fix plan: what the coding agent should change.
- Verification: tests or checks the coding agent must run.

### Phase 4: Audit Log, Plan Files, Chat Handoff

Write the audit log first. Then write one plan file per coherent implementation package, or one consolidated plan if the findings are tightly coupled.

Plan files can live under `plans/`, `_internal/plans/`, or another folder the project uses for implementation tasks.

Every plan must include:

- Absolute or repository-relative path to the audit log.
- Codex model stamp.
- Commit and worktree baseline.
- Findings addressed, with IDs.
- Scope and explicit non-scope.
- Step-by-step implementation plan for the coding agent.
- Acceptance criteria and exact verification commands.
- Regression risks.
- Handoff instruction: the coding agent must not implement this plan 1:1; it must read the audit, create an independent plan, compare it with the Codex plan, improve both, write a fusion plan, and implement the fusion.

Then write a chat handoff using `chat-handoff-template.md`.

### Phase 5: Self-Verification

Before finalizing:

- Re-read the audit log and plan file.
- Check that every Critical/High finding has a plan or is marked unresolved.
- Check that no product-code file was modified by Codex.
- Check that the done ledger records every audited file with path, commit/worktree ref, blob hash, status, and plan references.
- Check that the chat handoff points to the correct audit and plan files.
- Run the skill validator when this skill itself was changed.

## Output Shape

Keep chat output compact. The durable truth lives in files.

Final response:

- Audit log path.
- Plan file path(s).
- Chat handoff path or pasted handoff text.
- Done ledger path.
- Count of files scanned, skipped as unchanged, and remaining.
- Highest severity open.
