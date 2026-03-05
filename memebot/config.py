from __future__ import annotations

from dataclasses import dataclass
from typing import List
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class BotConfig:
    twitter_bearer_token: str
    twitter_api_key: str
    twitter_api_secret: str
    twitter_access_token: str
    twitter_access_token_secret: str
    post_interval_minutes: int
    max_retries: int
    retry_backoff_seconds: int
    post_log_path: str
    imgflip_username: str
    imgflip_password: str
    reddit_subreddits: List[str]
    reddit_user_agent: str
    solana_donation_wallet: str


def _required_env(key: str) -> str:
    value = os.getenv(key, "").strip()
    if not value:
        raise ValueError(f"Missing required environment variable: {key}")
    return value


def load_config() -> BotConfig:
    subreddits_raw = os.getenv("REDDIT_SUBREDDITS", "memes,dankmemes,wholesomememes")
    subreddits = [item.strip() for item in subreddits_raw.split(",") if item.strip()]

    return BotConfig(
        twitter_bearer_token=_required_env("TWITTER_BEARER_TOKEN"),
        twitter_api_key=_required_env("TWITTER_API_KEY"),
        twitter_api_secret=_required_env("TWITTER_API_SECRET"),
        twitter_access_token=_required_env("TWITTER_ACCESS_TOKEN"),
        twitter_access_token_secret=_required_env("TWITTER_ACCESS_TOKEN_SECRET"),
        post_interval_minutes=int(os.getenv("POST_INTERVAL_MINUTES", "60")),
        max_retries=int(os.getenv("MAX_RETRIES", "5")),
        retry_backoff_seconds=int(os.getenv("RETRY_BACKOFF_SECONDS", "2")),
        post_log_path=os.getenv("POST_LOG_PATH", "./data/post_log.json"),
        imgflip_username=os.getenv("IMGFLIP_USERNAME", "").strip(),
        imgflip_password=os.getenv("IMGFLIP_PASSWORD", "").strip(),
        reddit_subreddits=subreddits,
        reddit_user_agent=os.getenv("REDDIT_USER_AGENT", "MemeBot/1.0"),
        solana_donation_wallet=os.getenv("SOLANA_DONATION_WALLET", "").strip(),
    )
