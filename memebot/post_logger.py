from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class PostLogEntry:
    timestamp: str
    source: str
    meme_text: str
    media_url: str
    status: str
    tweet_id: Optional[str]
    error: Optional[str]


class PostLogger:
    def __init__(self, log_path: str) -> None:
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def _read_all(self) -> List[Dict[str, Any]]:
        if not self.log_path.exists():
            return []

        try:
            return json.loads(self.log_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            # If file is corrupted, keep the bot running and reset history.
            return []

    def append(self, *, source: str, meme_text: str, media_url: str, status: str, tweet_id: Optional[str], error: Optional[str]) -> None:
        entries = self._read_all()
        payload = PostLogEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            source=source,
            meme_text=meme_text,
            media_url=media_url,
            status=status,
            tweet_id=tweet_id,
            error=error,
        )
        entries.append(asdict(payload))
        self.log_path.write_text(json.dumps(entries, indent=2), encoding="utf-8")
