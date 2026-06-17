# `task.json` schema

`corpus_schema_version: 1`. Additive-only — fields are added, never removed or
repurposed. Consumers must be tolerant readers (ignore unknown fields). The
authoritative definition lives in
[`internal/corpus/task.go`](https://github.com/Atharva-Kanherkar/proofswe/blob/main/internal/corpus/task.go).

| field | type | notes |
|---|---|---|
| `corpus_schema_version` | int | contract version (currently `1`) |
| `task_id` | string | `sha256:…` content hash of `remote_url + base_commit + starting prompt`; dedup key |
| `contributed_at` | RFC3339 | when the task was emitted |
| `contributor` | string? | optional attribution, e.g. `@handle` |
| `harness` | string | supported harness id emitted by proofswe |
| `model` | string | the agent model id from the session |
| `repo` | object | **reproducibility root** — see below |
| `prompts[]` | object | `{turn_index, role, text}` — the developer's turns |
| `transcript` | object | `assistant_messages[]`, `tool_calls[]`, `tool_outputs[]` (each `{turn_index, name?, text}`) |
| `code` | object | `patch`, `test_patch`, `files[] {path, role}` |
| `outcome` | object | deterministic, transcript-derived result |
| `scorecard` | object? | provisional execution score (`composite`, `axes[]`) |
| `scrub` | object | `{scrubber_version, spans_redacted, notice}` |

### `repo` (must be reproducible)

| field | type | required for corpus |
|---|---|---|
| `remote_url` | string | ✅ public host (github.com / gitlab.com / codeberg.org) |
| `base_commit` | string | ✅ the starting commit |
| `branch` | string | — |
| `license_spdx` | string | ✅ OSI-permissive (MIT, Apache-2.0, BSD-*, ISC, Unlicense, 0BSD) |
| `is_public` | bool | ✅ `true` |

### `outcome`

`verification` (`passed`/`failed`/`""`), `landed` (committed/pushed/PR), `landing_quality`,
`termination` (`clean`/`abandoned`), `human_turns`, `human_corrections`, `human_acceptances`,
`rework_count`, `interruptions`, `files_touched`, `test_files_touched`, `skills_used[]`, `skill_assisted`.

A submission is **rejected** by CI if any required `repo` field is missing, `prompts` is empty,
or both `code.patch` and `code.test_patch` are empty — those tasks are not reproducible.
