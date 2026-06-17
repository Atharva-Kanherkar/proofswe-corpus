# proofswe-corpus

The open, reproducible task corpus for [**proofswe**](https://github.com/Atharva-Kanherkar/proofswe) —
a benchmark built from **real developer sessions**, not synthetic tasks.

Each entry in [`tasks/`](tasks/) is one `task.json`: a coding session captured from
a supported coding-agent harness, reduced to a **reproducible benchmark task** —

- the **starting repo state** (`remote_url` + `base_commit` + license) so anyone can
  `git clone && git checkout` into the exact conditions the session began,
- the developer's **prompts** (the ambiguous, oracle-less ask),
- the agent's **trajectory** (assistant turns, tool calls, tool outputs),
- the resulting **code**,
- the deterministic **outcome** (what verified / landed / survived), and
- an optional **scorecard**.

With those, anyone can re-run the same task against a different model and score it the
same way. That is the whole point: **provable, reproducible, comparable.**

## Why only public-repo sessions

A task is only reproducible if its starting state is cloneable. So the corpus is the
**OSS subset**: sessions on public repos with a permissive license. Private-repo work
can still contribute *aggregate statistics* to the leaderboard, but it is not a
re-runnable task and does not belong here.

## Contribute

```sh
# one-time: install + start capturing locally
curl -fsSL https://proofswe.com/install.sh | sh && proofswe enable

# then, from inside a public repo you worked in:
proofswe contribute <path-to-session.jsonl> --as @you
```

`proofswe contribute` builds a schema-valid `task.json`, **scrubs secrets**, refuses
sessions that aren't reproducible, and prints the exact `gh` commands to open a PR here.
See [CONTRIBUTING.md](CONTRIBUTING.md) and the [schema](SCHEMA.md).

## What we keep out

The one filter the corpus enforces is a **secret scrubber** (API keys, tokens, DB URLs).
Not for privacy ideology — a public dataset shipping live credentials gets pulled and
burns its contributors. Everything else (code, prompts, reasoning) is published as-is,
because open data is the product.

## Licensing

Each task's code is redistributable under its **source repository's license**
(recorded in `repo.license_spdx`; only OSI-permissive licenses are accepted). The corpus
metadata and tooling in this repo are MIT.
