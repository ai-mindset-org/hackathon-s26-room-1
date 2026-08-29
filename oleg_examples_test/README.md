# `oleg_examples_test` synthetic semantic corpus

`oleg_examples_test/` contains 16 independent, synthetic, public-safe scenarios.
The corpus extends the small examples in `examples/`. Its map is
hypothesis-driven. It is not a measured distribution of real work, industries,
languages, or failure rates.

## Acceptance contract

For one scenario, the target application consumes every file in its `input/`
folder as one package. Compare the final application output by meaning with that
scenario's `expected.md`. Record identity, owner or known absence, time,
lifecycle state, source links, required merges, required separations, and
negative checks are part of the result. Wording and output schema can differ.

The corpus does not require repository code to read it. All inputs are text.
No input contains private messages, real personal data, credentials, or real
production identifiers.

## Tiers

- `standard`: `T002`-`T011`, `T013`, and `T014`. Each package has at least five
  input files, 12 KiB of input, and 100 nonblank input lines.
- `scale`: `T001` and `T012`. Each package has at least 40 KiB of input. `T001`
  is the long-thread case. `T012` is the many-file case.
- `zero`: `T015` and `T016`. Each package has at least five input files, 15 KiB
  of input, and 100 nonblank input lines. The accepted registry is empty.

The size quotas and the target of at least 70% natural context are design
quotas. The validator does not measure the 70% semantic context ratio. For
`T001`, it uses 400 nonblank lines as a conservative mechanical proxy for the
map's 400-message lower bound. It does not prove that every line is a message.

## Files and measured index

- `MAP.md` defines the scenario hypotheses and semantic scope.
- `index.csv` contains one row per scenario and measured input file, byte, and
  nonblank-line counts.
- `Txxx-name/input/` contains the input package.
- `Txxx-name/expected.md` contains the semantic result and checks.
- `oleg_validate_corpus.ps1` performs read-only structural checks.

`expected_records` counts explicit top-level final records. `positive_checks`
and `negative_checks` count top-level numbered assertions in the corresponding
sections. The headings differ between scenarios. Zero-result scenarios have no
positive record assertions, so their false-positive lists count only as
negative checks. These counts are conservative metadata, not a common machine
schema for `expected.md`.

## Run the validator

From the repository root:

```powershell
powershell.exe -NoProfile -File .\oleg_examples_test\oleg_validate_corpus.ps1
```

The script reads the corpus only. It prints errors to the console and exits with
code 1 on a failure. It checks the exact roster, tier floors, index measurements,
banned evaluator phrases, mechanically extractable source paths, strong secret
shapes, reserved internet namespaces, and cross-scenario namespace roots. It
cannot prove that every proper name is synthetic or that the expected meaning is
correct.
