# Manufacturing Defect Management & Prediction
Manage &amp; Predict the manufacturing defects
Lightweight pipeline to ingest a defects CSV, validate rows, compute simple analytics, and write two JSON outputs:

- `data/summary.json` — aggregates and metrics for valid defects
- `data/rejected.json` — list of rejected rows with validation failure reasons

This repository is a compact example used for processing manufacturing defect records.

## Contents

- `main.py` — pipeline entrypoint (reads CSV, validates, writes JSON)
- `data/defects_data.csv` — input dataset (sample)
- `ingestion/` — CSV reader and mapper to the domain model
- `domain/defect.py` — `Defect` data model
- `validation/` — validators and engine for rules (position, cost, severity, date)
- `analytics/` — aggregation helpers (defects by type, cost by position)
- `storage/` — JSON writer used to persist outputs
- `utils/` — helper utilities and custom exceptions

## Requirements

- Python 3.8+ (the project uses only stdlib modules currently)
- Optional: if you want more flexible date parsing, install `python-dateutil`

## Setup (recommended)

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. (Optional) Install dateutil for more robust date parsing:

```bash
pip install python-dateutil
```

There is no requirements file by default — the code runs with stdlib only.

## Run

From the project root run:

```bash
python3 main.py
```

This will read `data/defects_data.csv`, validate each row, and write:

- `data/summary.json` — aggregated metrics for valid defects
- `data/rejected.json` — rejected rows with `defect_id` and `reasons`

If the files are not created, check for errors printed to the console and ensure `data/` is writable.

## Validation rules

Validators are implemented under `validation/validators.py` and currently include:

- `PositionValidator` — checks allowed locations (component/internal/surface)
- `CostValidator` — ensures `repair_cost` is numeric and non-negative
- `SeverityValidator` — checks severity values (critical/moderate/minor)
- `DateValidator` — ensures the `defect_date` parses against common formats

Add or modify validators to implement your project's rules. The `ValidationEngine` collects failing validator class names and they are written to `data/rejected.json`.

## Extending the pipeline

- Add new analytics under `analytics/` and include them in `main.py`'s `summary` dict.
- Add storage targets under `storage/` (S3, database) by implementing a writer with a compatible `write(data, filepath)` API.
- Improve rejection messages: change `ValidationEngine` to return (validator_name, message) pairs if you want more descriptive reasons.

## Troubleshooting

- "No JSON files created": run `python3 main.py` and inspect console for tracebacks. Common causes:
	- Malformed CSV rows (the mapper now handles malformed numbers and marks defects rejected rather than raising).
	- Permission issues writing to `data/`.
- Git push rejected (non-fast-forward): fetch + rebase or merge the remote changes before pushing. Example safe commands:

```bash
git fetch origin
git branch backup-main-$(date +%Y%m%d%H%M%S)
git rebase origin/main
git push --force-with-lease origin main
```

## Tests and CI

There are no tests in the repository yet. Suggested next steps:

- Add unit tests for `ingestion.mapper`, validators, and `storage.writer`.
- Add a lightweight GitHub Actions workflow to run tests on push.

## Contributing

1. Fork the repo
2. Create a feature branch
3. Open a PR with your changes

Be careful when rewriting `main` history: prefer merge-based workflows if multiple contributors push to the same branch.

## License

Add a LICENSE file if you intend to publish this project. Currently there is no license file in the repository.

---

If you'd like, I can also:
- add a `requirements.txt` or `pyproject.toml` with pinned dependencies,
- add an example GitHub Action workflow to run the pipeline in CI,
- or include sample unit tests covering the new date/cost validation behavior.



