# proofswe-corpus

Public, reproducible tasks for the `proofswe` coding-agent benchmark.

Each file in `tasks/` is a single real developer session converted into a
re-runnable task. A task records the starting repository state, the user's
prompts, the agent trajectory, the resulting patch, outcome signals, and an
optional scorecard.

## Task Requirements

A task must be reproducible:

- public source repository
- fixed `base_commit`
- OSI-permissive license
- at least one user prompt
- non-empty code patch or test patch
- no live secrets

CI validates changed `tasks/*.json` files with `scripts/validate.py`.

## Contribute

Generate a task from the repository where the session happened:

```sh
npx -y proofswe contribute <transcript.jsonl> --as @you
```

Then open a pull request adding the generated file under `tasks/`.

```sh
git checkout -b add-task-<id>
cp task-<id>.json tasks/
git add tasks
git commit -m "add task <id>"
gh pr create --fill
```

Review the generated JSON before submitting. Automated redaction is a backstop,
not a guarantee.

## Schema

Current schema version: `corpus_schema_version: 1`.

Required top-level fields:

- `task_id`
- `contributed_at`
- `harness`
- `model`
- `repo`
- `prompts`
- `transcript`
- `code`
- `outcome`
- `scrub`

The authoritative Go type lives in the main `proofswe` repository under
`internal/corpus/task.go`. Consumers should be tolerant readers: ignore unknown
fields and treat additions as backwards-compatible.

## License

Corpus metadata and tooling are MIT. Task code remains governed by the source
repository license recorded in each task's `repo.license_spdx`.
