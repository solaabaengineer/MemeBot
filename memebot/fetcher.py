from __future__ import annotations

from dataclasses import dataclass
import random
from typing import List

import requests


@dataclass
class Meme:
    text: str
    image_url: str
    source: str


class MemeFetcher:
    def __init__(
        self,
        reddit_subreddits: List[str],
        reddit_user_agent: str,
        imgflip_username: str = "",
        imgflip_password: str = "",
    ) -> None:
        self.reddit_subreddits = reddit_subreddits
        self.reddit_user_agent = reddit_user_agent
        self.imgflip_username = imgflip_username
        self.imgflip_password = imgflip_password

    def fetch(self) -> Meme:
        # Prefer Reddit images first for rich media posts, then fallback to Imgflip.
        try:
            return self._from_reddit()
        except Exception:
            return self._from_imgflip()

    def _from_reddit(self) -> Meme:
        subreddit = random.choice(self.reddit_subreddits)
        endpoint = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=50"
        response = requests.get(
            endpoint,
            headers={"User-Agent": self.reddit_user_agent},
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()

        posts = data.get("data", {}).get("children", [])
        image_posts = []
        for post in posts:
            payload = post.get("data", {})
            url = payload.get("url_overridden_by_dest") or payload.get("url")
            title = payload.get("title", "")
            if isinstance(url, str) and url.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                image_posts.append((title, url))

        if not image_posts:
            raise RuntimeError("No image meme candidates found in Reddit feed")

        selected_title, selected_url = random.choice(image_posts)
        return Meme(text=selected_title[:250], image_url=selected_url, source=f"reddit:r/{subreddit}")

    def _from_imgflip(self) -> Meme:
        response = requests.get("https://api.imgflip.com/get_memes", timeout=15)
        response.raise_for_status()
        payload = response.json()
        if not payload.get("success"):
            raise RuntimeError("Imgflip API returned unsuccessful response")

        memes = payload.get("data", {}).get("memes", [])
        if not memes:
            raise RuntimeError("Imgflip meme list is empty")

        selected = random.choice(memes)
        text = f"{selected.get('name', 'Meme')} #MemeBot"
        return Meme(text=text[:250], image_url=selected["url"], source="imgflip")
