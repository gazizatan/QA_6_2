import json
from datetime import datetime
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS_FILE = ROOT / "artifacts" / "test_results.json"
OUT_DIR = ROOT / "reports"
OUT_FILE = OUT_DIR / "test_report.html"


def _load_results():
    if not RESULTS_FILE.exists():
        raise FileNotFoundError(f"Missing results file: {RESULTS_FILE}")
    return json.loads(RESULTS_FILE.read_text())


def _row(result):
    def td(value):
        return f"<td>{escape(value)}</td>"

    screenshot = result.get("screenshot", "")
    screenshot_cell = ""
    if screenshot:
        screenshot_cell = (
            f"<a href='{escape(screenshot)}' target='_blank'>screenshot</a>"
        )

    status = result.get("status", "")
    status_cell = f"<span class='{escape(status)}'>{escape(status)}</span>"

    return (
        "<tr>"
        + td(str(result.get("id", "")))
        + td(result.get("name", ""))
        + td(result.get("browser", ""))
        + td(result.get("steps", ""))
        + td(result.get("expected_result", ""))
        + td(result.get("actual_result", ""))
        + f"<td>{status_cell}</td>"
        + td(result.get("comments", ""))
        + f"<td>{screenshot_cell}</td>"
        + "</tr>"
    )


def main():
    results = _load_results()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    rows = "\n".join(_row(r) for r in results)
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Test Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; color: #222; }}
    h1 {{ margin-bottom: 8px; }}
    .meta {{ color: #555; margin-bottom: 16px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ccc; padding: 8px; vertical-align: top; }}
    th {{ background: #f3f3f3; text-align: left; }}
    tr:nth-child(even) {{ background: #fafafa; }}
    .Passed {{ color: #0a7b34; font-weight: bold; }}
    .Failed {{ color: #b00020; font-weight: bold; }}
  </style>
</head>
<body>
  <h1>Cross-Browser Test Report</h1>
  <div class="meta">Generated: {generated_at}</div>
  <table>
    <thead>
      <tr>
        <th>ID</th>
        <th>Test Case</th>
        <th>Browser</th>
        <th>Test Steps</th>
        <th>Expected Result</th>
        <th>Actual Result</th>
        <th>Pass/Fail</th>
        <th>Comments</th>
        <th>Screenshot</th>
      </tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>
</body>
</html>
"""

    OUT_FILE.write_text(html)
    print(OUT_FILE)


if __name__ == "__main__":
    main()
