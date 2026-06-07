import json
import re
from datetime import datetime, timezone
from pathlib import Path
from lib.config import OUTPUTS_DIR, STATE_DIR


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40]


def create_run(title: str, mode: str, voice: str, film_preset: str, duration_minutes: int) -> dict:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    run_id = f"{ts}_{_slug(title)}"
    output_dir = OUTPUTS_DIR / run_id
    output_dir.mkdir(parents=True, exist_ok=True)

    run_state = {
        "run_id": run_id,
        "title": title,
        "mode": mode,
        "voice": voice,
        "film_preset": film_preset,
        "duration_minutes": duration_minutes,
        "status": "created",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "stages": {
            "script": {"status": "pending"},
            "style_card": {"status": "pending"},
            "characters": {"status": "pending"},
            "scenes": {"status": "pending"},
            "tts": {"status": "pending"},
            "timestamps": {"status": "pending"},
            "images": {"status": "pending"},
            "image_review": {"status": "pending"},
            "render": {"status": "pending"},
            "thumbnail": {"status": "pending"},
            "metadata": {"status": "pending"},
            "article": {"status": "pending"},
            "article_images": {"status": "pending"},
            "upload": {"status": "pending"},
        },
        "output_dir": str(output_dir),
    }

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state_path = STATE_DIR / f"{run_id}.json"
    state_path.write_text(json.dumps(run_state, indent=2, ensure_ascii=False), encoding='utf-8')
    return run_state


def load_run(run_id: str) -> dict:
    state_path = STATE_DIR / f"{run_id}.json"
    return json.loads(state_path.read_text(encoding='utf-8'))


def update_stage(run_id: str, stage: str, status: str, output: str = "") -> dict:
    run = load_run(run_id)
    if stage not in run["stages"]:
        run["stages"][stage] = {}
    run["stages"][stage]["status"] = status
    if output:
        run["stages"][stage]["output"] = output
    state_path = STATE_DIR / f"{run_id}.json"
    state_path.write_text(json.dumps(run, indent=2, ensure_ascii=False), encoding='utf-8')
    return run


def update_run(run_id: str, updates: dict) -> dict:
    run = load_run(run_id)
    run.update(updates)
    state_path = STATE_DIR / f"{run_id}.json"
    state_path.write_text(json.dumps(run, indent=2, ensure_ascii=False), encoding='utf-8')
    return run


def list_runs() -> list:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    runs = []
    for f in sorted(STATE_DIR.glob("*.json"), reverse=True):
        runs.append(json.loads(f.read_text(encoding='utf-8')))
    return runs
