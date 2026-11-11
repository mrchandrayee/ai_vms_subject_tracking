from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]
EVENT_DIR = BASE_DIR / "data" / "events"
SNAPSHOT_DIR = EVENT_DIR / "snapshots"
EVENT_DIR.mkdir(parents=True, exist_ok=True)
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
