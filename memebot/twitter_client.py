from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional

import requests
import tweepy


class TwitterPoster:
    def __init__(
        self,
        *,
        bearer_token: str,
        api_key: str,
        api_secret: str,
        access_token: str,
        access_token_secret: str,
    ) -> None:
        self.client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            wait_on_rate_limit=True,
        )

        auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
        self.media_api = tweepy.API(auth)

    def _download_media(self, media_url: str) -> Path:
        response = requests.get(media_url, timeout=20)
        response.raise_for_status()

        suffix = Path(media_url).suffix or ".jpg"
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(response.content)
            return Path(tmp_file.name)

    def create_post(self, text: str, media_url: str) -> Optional[str]:
        media_path = self._download_media(media_url)
        try:
            media = self.media_api.media_upload(filename=str(media_path))
            tweet = self.client.create_tweet(text=text, media_ids=[media.media_id_string])
            tweet_id = tweet.data.get("id") if tweet and tweet.data else None
            return str(tweet_id) if tweet_id else None
        finally:
            media_path.unlink(missing_ok=True)
