This repository contains several small analytics projects. The goal of these instructions is to give an AI coding agent immediate, actionable context so it can be productive without asking for basics.

- Root layout
  - `bigquery-cloud-analytics/` — BigQuery-related SQL and examples. Look in `data/` and `README.md` for dataset notes.
  - `forecasting-python/` — Python forecasting experiments. No package manifests detected; expect plain scripts or notebooks.
  - `python-data-cleaning-eda/` — Python data cleaning and exploratory analysis. Check `data/` and `README.md` for data sources.
  - `powerbi-operations-dashboard/` — Power BI assets and screenshots. Not a code project but contains PBIX/screenshots and a README.
  - `sql-analytics-portfolio/` — SQL query collection and examples.

- Big picture & intent
  - These are independent, folder-scoped analytics projects rather than a single monorepo app. Each top-level folder is self-contained. Treat changes per-folder and avoid cross-folder refactors unless the user requests a workspace-wide consolidation.
  - The repository is documentation-first: each project has a `README.md` with the intended purpose. Use those READMEs as the authoritative guidance for data sources and expected outputs.

- Developer workflows (discoverable)
  - There are no detected `requirements.txt`, `pyproject.toml`, or Dockerfiles at the repo root. Assume local Python virtualenvs when running scripts. When adding dependency files, prefer `requirements.txt` with pinned versions.
  - Typical actions an engineer will run:
    - Inspect `README.md` inside a project folder for data notes and local commands.
    - Open Jupyter notebooks (if any) inside the project folder and run cells interactively for EDA/experiments.

- Project-specific patterns to follow
  - Small, single-purpose scripts and notebooks: prefer lightweight, well-documented functions and small helper scripts (avoid heavy framework scaffolding).
  - Data files live under `*/data/`. When referencing or modifying datasets, maintain paths relative to the project folder (do not hardcode absolute system paths).
  - SQL examples are standalone files in `sql-analytics-portfolio/` or `bigquery-cloud-analytics/`; keep queries readable, include comments for purpose/expected result, and avoid changing formatting that reduces clarity.

- Integration & external dependencies
  - BigQuery-related work likely depends on Google Cloud auth and BigQuery client libraries. Do not add credentials to the repo. When adding code that uses BigQuery, read/write through standard clients and document required environment variables (e.g., `GOOGLE_APPLICATION_CREDENTIALS`).
  - Power BI assets are binary (PBIX); do not attempt to parse or programmatically modify them in-place.

- How the agent should propose changes
  - Provide minimal, well-scoped diffs restricted to a single project folder unless the user asks for cross-project changes.
  - When adding Python code, include a small README fragment or comment documenting how to run it (python -m venv, pip install -r requirements.txt, then `python script.py`), and add `requirements.txt` if introducing third-party packages.
  - For notebooks, avoid converting entire exploratory notebooks into production scripts automatically. Instead, propose a small extraction of core logic into a new module and add a brief test or runnable example.

- Examples from this repo
  - If asked to modify SQL examples, edit files under `sql-analytics-portfolio/` and keep the existing query-comment style.
  - For forecasting experiments, search `forecasting-python/README.md` and add new scripts inside that folder; include a short usage snippet in the README.

- Safety and repository rules
  - Never add secrets, service-account JSON, or large data files. If changes require credentials, document required environment variables and mock values for local testing.

If anything in these notes is unclear or you want the instructions to target a single project (for example, only `forecasting-python/`), tell me which folder to focus on and I will update the guidance.
