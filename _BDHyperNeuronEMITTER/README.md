# _BDHyperNeuronEMITTER v2

Consumes HyperHunk NDJSON, builds the Cold Artifact SQLite graph, and owns the embedding math.

**Status: Phase 1 baseline runnable** — train, emit, and UI entrypoints are wired. Bootstrap Nucleus is live and now exposes builder-facing scaffold dials through CLI + JSON profiles. FFN Nucleus remains deferred.

## Quick start

```bat
setup_env.bat
run.bat emit --input path\to\hunks.ndjson
```

Bootstrap tuning example:

```bat
run.bat emit --input path\to\hunks.ndjson ^
  --bootstrap-profile _docs\bootstrap_profiles\python_reference_prose_tuning.json
```

Each emit run writes `bootstrap_profile_effective.json` next to the output database so probe artifacts are reproducible.
