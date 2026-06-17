#!/usr/bin/env python3
"""Validate corpus task.json files: schema, reproducibility, and a secret re-scan.

Usage: validate.py <task.json> [<task.json> ...]
Exits non-zero if any file fails. Run by CI over changed tasks/*.json.
"""
import json
import re
import sys

SUPPORTED_SCHEMA = {1}
PERMISSIVE = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Unlicense", "0BSD"}

# Coarse live-credential patterns — a backstop, not the primary scrubber.
SECRET_PATTERNS = [
    (re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}"), "anthropic key"),
    (re.compile(r"sk-[A-Za-z0-9]{20,}"), "openai-style key"),
    (re.compile(r"ghp_[A-Za-z0-9]{30,}"), "github token"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "aws access key"),
    (re.compile(r"AIza[0-9A-Za-z_-]{30,}"), "google api key"),
    (re.compile(r"postgres(?:ql)?://[^:\s]+:[^@\s]+@"), "db url with password"),
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"), "private key"),
]


def reproducibility_problems(task):
    repo = task.get("repo", {})
    problems = []
    if not repo.get("remote_url"):
        problems.append("repo.remote_url missing")
    if not repo.get("is_public"):
        problems.append("repo.is_public is not true")
    if not repo.get("base_commit"):
        problems.append("repo.base_commit missing")
    if repo.get("license_spdx") not in PERMISSIVE:
        problems.append(f"repo.license_spdx {repo.get('license_spdx')!r} not OSI-permissive")
    if not task.get("prompts"):
        problems.append("no prompts (no task statement)")
    code = task.get("code", {})
    if not code.get("patch") and not code.get("test_patch"):
        problems.append("no code patch")
    return problems


def scan_secrets(obj):
    hits = []

    def walk(v):
        if isinstance(v, str):
            for pat, label in SECRET_PATTERNS:
                if pat.search(v):
                    hits.append(label)
        elif isinstance(v, dict):
            for x in v.values():
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)

    walk(obj)
    return hits


def validate(path):
    errors = []
    try:
        with open(path, encoding="utf-8") as f:
            task = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        return [f"unreadable / invalid JSON: {e}"]

    ver = task.get("corpus_schema_version")
    if ver not in SUPPORTED_SCHEMA:
        errors.append(f"unsupported corpus_schema_version: {ver!r}")
    errors += reproducibility_problems(task)
    secrets = scan_secrets(task)
    if secrets:
        errors.append("possible live secrets: " + ", ".join(sorted(set(secrets))))
    return errors


def main(argv):
    failed = False
    for path in argv[1:]:
        errs = validate(path)
        if errs:
            failed = True
            print(f"✗ {path}")
            for e in errs:
                print(f"    {e}")
        else:
            print(f"✓ {path}")
    if failed:
        print("\nvalidation failed", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
