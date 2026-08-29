# ZEH8 Engine

`oleg_engine` reads a folder of text inputs and creates one obligation registry. It keeps tasks, events, recurring duties, owners, deadlines, lifecycle status, and exact source quotes. A later run merges new evidence into the same registry instead of adding a second row for the same obligation.

## Run

From the repository root:

```powershell
python -m oleg_engine run `
  --input "examples/01-разнородный-вход/input" `
  --registry "oleg_engine/out/demo/registry.json"
```

The command writes `registry.json` and `registry.md` beside it. The final stdout line is always a JSON summary:

```json
{"created":8,"updated":0,"closed":0,"total_open":8,"run_id":"run_..."}
```

Merge a later input into the same file:

```powershell
python -m oleg_engine run `
  --input "examples/02-повторный-прогон/input" `
  --registry "oleg_engine/out/demo/registry.json"
```

Use `--now YYYY-MM-DD` to set the reference date. Without it, the engine uses the latest leading chat timestamp in the input, then the local current date. This avoids treating a future deadline as the document date.

## Flags and defaults

| Flag | Default | Effect |
|---|---|---|
| `--mode auto\|parallel\|sequential` | `auto` | `auto` extracts multiple new files concurrently. Adjudication remains global in every mode. |
| `--backend codex\|claude` | `codex` | Codex uses `gpt-5.6-sol` with high reasoning. After two failed Codex attempts, the engine falls back to Claude `opus`. |
| `--model NAME` | backend default | Selects the first backend model. |
| `--now YYYY-MM-DD` | inferred | Sets the reference date for relative dates. |
| `--json` | off | Suppresses the human progress line. The final JSON line is present in both modes. |
| `--prefilter` | off | For files over 16 KiB only, sends signal-bearing 60-line chunks plus one neighbour. Coverage records skipped chunks. |
| `--adjudicate` | on | Runs semantic deduplication, timeline resolution, and lifecycle merging. |
| `--no-adjudicate` | off | Debug switch. It disables semantic merging and is not suitable for repeated runs. |

The prefilter is experimental and defaults to off. With it off, every chunk in every new file is sent and `chunks_sent == chunks_total`. With it on, first-run model cost can follow likely relevance, but recall is not guaranteed.

## Registry shape

`registry.json` has version `1` and four main lists:

- `sources`: SHA-256, relative path, channel, byte size, and ingestion time. The input text is not stored.
- `runs`: run ID, time, effective mode/backend/model, and per-file chunk coverage.
- `obligations`: stable ID, action, owner, normalized and original deadline, kind, recurrence, status, source pointers, history, and manual-edit marker.
- Each source pointer contains only the file SHA-256, relative path, exact quote, and 1-based line range.

A known source hash is skipped before any model call. A fully identical rerun does not rewrite `registry.json`; its summary counts are all zero.

## Limits

- Inputs are decoded as UTF-8 text. Binary PDF and image OCR are outside this module; supply extracted text.
- Semantic quality depends on the selected model. The engine validates exact quotes and dates, but it cannot prove that the model found every real obligation.
- `--prefilter` is a recall/cost tradeoff and is not enabled by default.
- Manual edits are preserved only when the `manual` field is already present. There is no interactive editor in this slice.
