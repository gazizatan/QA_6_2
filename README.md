# QA6_2 - Cross-Browser Testing (Sauce Labs)

This repository contains automated Selenium tests (Python) executed on Sauce Labs across Chrome and Firefox.

## Contents
- `tests/test_cross_browser.py` — automated tests
- `data/test_cases.xlsx` — test data & expected results
- `REPORT.md` — report with positive/negative test cases
- `artifacts/` — screenshots, session IDs, downloaded video/logs

## Quick Start
```bash
python3 -m pip install -r requirements.txt
export SAUCE_USERNAME="<your_sauce_username>"
export SAUCE_ACCESS_KEY="<your_sauce_access_key>"
export SAUCE_REGION="eu-central-1"
pytest -q
python3 scripts/download_sauce_assets.py
```

Artifacts will appear under `artifacts/`.
# QA_6_2
