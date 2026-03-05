from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv


def main() -> int:
    load_dotenv()
    log_path = Path(os.getenv("POST_LOG_PATH", "./data/post_log.json"))

    if not log_path.exists():
        print("Total posts logged: 0")
        print("Successful posts: 0")
        print("Failed posts: 0")
        return 0

    entries = json.loads(log_path.read_text(encoding="utf-8"))
    total = len(entries)
    success = sum(1 for entry in entries if entry.get("status") == "success")
    failed = sum(1 for entry in entries if entry.get("status") == "failed")

    print(f"Total posts logged: {total}")
    print(f"Successful posts: {success}")
    print(f"Failed posts: {failed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
