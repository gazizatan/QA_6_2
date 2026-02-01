# Cross-Browser Testing Report (Task 2)

## Target
- Site: https://www.browserstack.com
- Platform: Sauce Labs (Automate)
- Browsers: Chrome (latest), Firefox (latest)
- Platform: Windows 11
- Region: eu-central-1

## Test Data Source
- `data/test_cases.xlsx`

## Test Cases

### Positive
1) Home page title
- Step: Open https://www.browserstack.com
- Expected: Title contains "BrowserStack"

### Negative
2) Non-existent page shows 404
- Step: Open https://www.browserstack.com/this-page-should-not-exist-qa6
- Expected: Page contains "404" (or not found message)

## Execution Results (January 31, 2026)
| Test | Browser | Session ID | Status |
| --- | --- | --- | --- |
| 1 - Home page title | Chrome | af070ac338de4bbba7f618be5ab4b2b7 | Passed |
| 1 - Home page title | Firefox | cc5aeed9296b41d2afc1f8ed35bf275a | Passed |
| 2 - Non-existent page shows 404 | Chrome | a6a044bf67584a86b330a1b8d1826e9a | Passed |
| 2 - Non-existent page shows 404 | Firefox | b5641d30449e448596483cbd01743a61 | Passed |

## Execution Evidence
Artifacts are generated under `artifacts/`:
- `artifacts/screenshots/` — screenshots captured from remote sessions
- `artifacts/sauce_sessions.json` — session IDs and results
- `artifacts/sauce_assets/` — downloaded video/logs from Sauce Labs API
- `reports/test_report.html` — HTML report with steps/expected/actual/pass-fail/comments

## How to Run
```bash
python3 -m pip install -r requirements.txt
export SAUCE_USERNAME="<your_sauce_username>"
export SAUCE_ACCESS_KEY="<your_sauce_access_key>"
export SAUCE_REGION="eu-central-1"
pytest -q
python3 scripts/download_sauce_assets.py
python3 scripts/generate_html_report.py
```

## Expected Outputs
- Videos: `artifacts/sauce_assets/<session_id>/video.mp4`
- Logs: `artifacts/sauce_assets/<session_id>/selenium-server.log` or `log.json`
- Job metadata: `artifacts/sauce_assets/<session_id>/job.json`

## Notes
- If assets are not available (plan-dependent), use the Sauce Labs dashboard to download video/logs for the session IDs listed in `artifacts/sauce_sessions.json`.
