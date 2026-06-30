#!/usr/bin/env python3
"""Create a review inventory for the Codex Claude review loop.

This script is intentionally mechanical: it lists candidate files, computes
content hashes, groups them coarsely, and marks whether an identical blob was
already recorded in the done ledger. It does not judge code quality.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import subprocess
import sys
from typing import Iterable


SKIP_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "dist",
    "node_modules",
    "secrets",
    "venv",
    "models",
}

BINARY_EXTS = {
    ".7z",
    ".bin",
    ".bmp",
    ".dll",
    ".exe",
    ".gif",
    ".ico",
    ".jpg",
    ".jpeg",
    ".mp4",
    ".onnx",
    ".pdf",
    ".png",
    ".pyc",
    ".so",
    ".zip",
}

SKIP_FILES = {"desktop.ini", "thumbs.db", ".ds_store"}

SCAN_STATUSES = {"scanned", "scanned-no-findings", "scanned-findings"}


def run_git(repo: pathlib.Path, args: list[str]) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.STDOUT)


def git_text(repo: pathlib.Path, args: list[str], default: str = "") -> str:
    try:
        return run_git(repo, args).decode("utf-8", errors="replace").strip()
    except subprocess.CalledProcessError:
        return default


def split_z(data: bytes) -> list[str]:
    return [item.decode("utf-8", errors="replace") for item in data.split(b"\0") if item]


def git_paths(repo: pathlib.Path, args: list[str]) -> list[str]:
    try:
        return split_z(run_git(repo, args))
    except subprocess.CalledProcessError as exc:
        print(exc.output.decode("utf-8", errors="replace"), file=sys.stderr)
        return []


def is_git_repo(repo: pathlib.Path) -> bool:
    try:
        subprocess.check_output(
            ["git", "-C", str(repo), "rev-parse", "--is-inside-work-tree"],
            stderr=subprocess.DEVNULL,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").strip("/")


def iter_target_files(repo: pathlib.Path, targets: list[str]) -> set[str]:
    result: set[str] = set()
    for target in targets:
        abs_target = (repo / target).resolve()
        if abs_target.is_file():
            result.add(normalize_path(str(abs_target.relative_to(repo))))
        elif abs_target.is_dir():
            for root, dirs, files in os.walk(abs_target):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for name in files:
                    file_path = pathlib.Path(root) / name
                    try:
                        result.add(normalize_path(str(file_path.resolve().relative_to(repo))))
                    except ValueError:
                        continue
    return result


def iter_all_files(repo: pathlib.Path) -> set[str]:
    result: set[str] = set()
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            file_path = pathlib.Path(root) / name
            try:
                result.add(normalize_path(str(file_path.resolve().relative_to(repo))))
            except ValueError:
                continue
    return result


def collect_paths(repo: pathlib.Path, scope: str, targets: list[str]) -> set[str]:
    if targets:
        return iter_target_files(repo, targets)
    if not is_git_repo(repo):
        return iter_all_files(repo) if scope == "all" else set()
    if scope == "all":
        return set(git_paths(repo, ["ls-files", "-z"]))
    changed: set[str] = set()
    changed.update(git_paths(repo, ["diff", "--name-only", "-z", "HEAD", "--"]))
    changed.update(git_paths(repo, ["diff", "--name-only", "--cached", "-z", "--"]))
    changed.update(git_paths(repo, ["ls-files", "--others", "--exclude-standard", "-z"]))
    return changed


def is_skipped(path: str, abs_path: pathlib.Path, max_bytes: int) -> tuple[bool, str]:
    parts = pathlib.PurePosixPath(path).parts
    if parts and parts[-1].lower() in SKIP_FILES:
        return True, "system-file"
    if any(part in SKIP_DIRS for part in parts):
        return True, "skip-dir"
    if abs_path.suffix.lower() in BINARY_EXTS:
        return True, "binary-extension"
    try:
        size = abs_path.stat().st_size
    except OSError:
        return True, "missing"
    if size > max_bytes:
        return True, "too-large"
    return False, ""


def file_sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def line_count(path: pathlib.Path) -> int | None:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            return None
    except OSError:
        return None
    if not text:
        return 0
    return text.count("\n") + (0 if text.endswith("\n") else 1)


def cluster_for(path: str) -> str:
    lower = path.lower()
    parts = pathlib.PurePosixPath(path).parts
    joined = "/".join(parts[:3])
    if any(token in lower for token in ["policy", "egress", "auth", "permission", "secret", "audit", "redact"]):
        return "security-boundary"
    if any(token in lower for token in ["sign", "update", "rollback", "sbom", "module", "lock", "provenance"]):
        return "release-supply-chain"
    if any(token in lower for token in ["deploy", "compose", "ansible", "backup", "restore", "service"]):
        return "deployment-operations"
    if any(token in lower for token in ["gateway", "skillrunner", "retriev", "rag", "connector", "datastore", "admin"]):
        return "architecture-core"
    if any(token in lower for token in ["test_", "_test", ".spec.", ".test.", "pytest", "ci", "lint"]):
        return "tests-gates"
    if parts and parts[0] in {"docs", "_internal", "licenses"}:
        return "docs-plans-legal"
    return joined or "root"


def load_done(ledger: pathlib.Path) -> set[tuple[str, str]]:
    done: set[tuple[str, str]] = set()
    if not ledger.exists():
        return done
    with ledger.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            status = entry.get("audit_status")
            path = entry.get("path")
            blob = entry.get("blob_sha256")
            if status in SCAN_STATUSES and path and blob:
                done.add((normalize_path(path), blob))
    return done


def build_inventory(repo: pathlib.Path, scope: str, targets: list[str], ledger: pathlib.Path, max_bytes: int) -> dict:
    now = dt.datetime.now(dt.timezone.utc)
    run_id = now.strftime("%Y%m%d-%H%M%S-codex-review")
    branch = git_text(repo, ["branch", "--show-current"], "unknown")
    commit = git_text(repo, ["rev-parse", "HEAD"], "unknown")
    dirty = bool(git_text(repo, ["status", "--porcelain"], ""))
    done = load_done(ledger)
    paths = sorted(collect_paths(repo, scope, targets))

    files = []
    summary = {"candidates": 0, "needs_scan": 0, "skipped_unchanged": 0, "skipped_other": 0}
    clusters: dict[str, dict[str, int]] = {}

    for rel in paths:
        rel = normalize_path(rel)
        abs_path = repo / rel
        skipped, reason = is_skipped(rel, abs_path, max_bytes)
        if skipped:
            summary["skipped_other"] += 1
            files.append({"path": rel, "status": "skipped", "reason": reason, "cluster": cluster_for(rel)})
            continue
        blob = file_sha256(abs_path)
        size = abs_path.stat().st_size
        lines = line_count(abs_path)
        cluster = cluster_for(rel)
        previously_done = (rel, blob) in done
        status = "skipped-unchanged" if previously_done else "needs-scan"
        summary["candidates"] += 1
        summary["skipped_unchanged" if previously_done else "needs_scan"] += 1
        clusters.setdefault(cluster, {"needs_scan": 0, "skipped_unchanged": 0, "files": 0})
        clusters[cluster]["files"] += 1
        clusters[cluster]["skipped_unchanged" if previously_done else "needs_scan"] += 1
        files.append(
            {
                "path": rel,
                "status": status,
                "cluster": cluster,
                "blob_sha256": blob,
                "size_bytes": size,
                "line_count": lines,
                "commit": commit,
                "content_ref": "worktree" if dirty else "commit",
            }
        )

    return {
        "run_id": run_id,
        "timestamp_utc": now.isoformat().replace("+00:00", "Z"),
        "repo": repo.name,
        "repo_path": str(repo),
        "branch": branch,
        "commit": commit,
        "worktree_dirty": dirty,
        "scope": scope,
        "targets": targets,
        "ledger": str(ledger),
        "summary": summary,
        "clusters": clusters,
        "files": files,
    }


def write_inventory(repo: pathlib.Path, inventory: dict, output: pathlib.Path | None) -> pathlib.Path:
    if output is None:
        out_dir = repo / "_audit" / "codex-review-loop"
        out_dir.mkdir(parents=True, exist_ok=True)
        output = out_dir / f"{inventory['run_id']}-inventory.json"
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return output


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".", help="Repository root")
    parser.add_argument("--scope", choices=["changed", "all"], default="changed")
    parser.add_argument("--target", action="append", default=[], help="File or directory to inventory")
    parser.add_argument("--ledger", default="_audit/codex-review-loop/done-list.jsonl")
    parser.add_argument("--output", default="")
    parser.add_argument("--max-bytes", type=int, default=1_500_000)
    args = parser.parse_args(list(argv) if argv is not None else None)

    repo = pathlib.Path(args.repo).resolve()
    ledger = (repo / args.ledger).resolve()
    output = pathlib.Path(args.output).resolve() if args.output else None
    inventory = build_inventory(repo, args.scope, args.target, ledger, args.max_bytes)
    out_path = write_inventory(repo, inventory, output)
    print(json.dumps({"inventory": str(out_path), "summary": inventory["summary"], "clusters": inventory["clusters"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
