import json
import os
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
SESSIONS_FILE = ROOT / "artifacts" / "sauce_sessions.json"
DOWNLOAD_DIR = ROOT / "artifacts" / "sauce_assets"


def _get_credentials():
    username = os.getenv("SAUCE_USERNAME")
    access_key = os.getenv("SAUCE_ACCESS_KEY")
    if not username or not access_key:
        raise RuntimeError("Set SAUCE_USERNAME and SAUCE_ACCESS_KEY to download assets.")
    return username, access_key


def _api_base():
    api_url = os.getenv("SAUCE_API_URL")
    if api_url:
        return api_url
    region = os.getenv("SAUCE_REGION", "eu-central-1")
    return f"https://api.{region}.saucelabs.com"


def _load_sessions():
    if not SESSIONS_FILE.exists():
        raise FileNotFoundError(f"Missing session file: {SESSIONS_FILE}")
    return json.loads(SESSIONS_FILE.read_text())


def _safe_write(path: Path, content: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def main():
    username, access_key = _get_credentials()
    base = _api_base()
    sessions = _load_sessions()

    for session in sessions:
        job_id = session["session_id"]
        job_dir = DOWNLOAD_DIR / job_id
        job_dir.mkdir(parents=True, exist_ok=True)

        job_info_url = f"{base}/rest/v1/{username}/jobs/{job_id}"
        job_info_resp = requests.get(job_info_url, auth=(username, access_key), timeout=30)
        _safe_write(job_dir / "job.json", job_info_resp.content)

        assets_list_url = f"{base}/rest/v1/{username}/jobs/{job_id}/assets"
        assets_resp = requests.get(
            assets_list_url, auth=(username, access_key), timeout=30
        )

        asset_names = []
        try:
            data = assets_resp.json()
            if isinstance(data, dict) and "assets" in data:
                asset_names = data["assets"]
            elif isinstance(data, list):
                asset_names = data
        except ValueError:
            asset_names = []

        if not asset_names:
            asset_names = [
                "video.mp4",
                "selenium-server.log",
                "log.json",
                "console.log",
                "network.har",
            ]

        for name in asset_names:
            asset_url = f"{base}/rest/v1/{username}/jobs/{job_id}/assets/{name}"
            resp = requests.get(asset_url, auth=(username, access_key), timeout=60)
            if resp.status_code == 200:
                _safe_write(job_dir / name, resp.content)


if __name__ == "__main__":
    main()
