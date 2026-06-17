# Contributing a task

Tasks come from **real sessions** you ran on **public repos**. You don't write them by
hand — `proofswe contribute` builds them.

## 1. Install + capture

```sh
curl -fsSL https://proofswe.com/install.sh | sh
proofswe enable          # installs the local hook; captures sessions on your machine
```

Work normally in a supported coding-agent CLI. Sessions are captured locally.

## 2. Emit a task

From inside the public repo you worked in:

```sh
proofswe contribute <path-to-session.jsonl> --as @you
# add --judge to include the behavioral success axis (needs ANTHROPIC_API_KEY)
```

This will:

- reconstruct the session into a `task.json`,
- **refuse** if the repo isn't public + permissively-licensed + at a known commit + has a patch
  (those tasks can't be reproduced),
- **scrub secrets** (and report how many spans it redacted), and
- print the exact `gh` commands to open your PR.

## 3. Open the PR

```sh
gh repo fork Atharva-Kanherkar/proofswe-corpus --clone --remote
cp task-<id>.json proofswe-corpus/tasks/
cd proofswe-corpus && git checkout -b add-task-<id>
git add tasks && git commit -m "add task <id>" && gh pr create --fill
```

## What CI checks

Every PR runs [`scripts/validate.py`](scripts/validate.py) over changed `tasks/*.json`:

1. `corpus_schema_version` present and supported,
2. all reproducibility fields set (public remote, base commit, OSI license, at least one prompt, and a patch),
3. a **secret re-scan** — if a live-looking credential slipped through, the PR fails.

Eyeball your `task.json` before submitting. The scrubber is best-effort; **you** are the
last line of defense against pasting a key into the public corpus.
