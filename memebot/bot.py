from __future__ import annotations

import logging
import signal
from threading import Event

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from memebot.config import BotConfig
from memebot.fetcher import MemeFetcher
from memebot.post_logger import PostLogger
from memebot.retry import run_with_retry
from memebot.twitter_client import TwitterPoster


class MemeBot:
    def __init__(self, config: BotConfig) -> None:
        self.config = config
        self.logger = PostLogger(config.post_log_path)
        self.fetcher = MemeFetcher(
            reddit_subreddits=config.reddit_subreddits,
            reddit_user_agent=config.reddit_user_agent,
            imgflip_username=config.imgflip_username,
            imgflip_password=config.imgflip_password,
        )
        self.poster = TwitterPoster(
            bearer_token=config.twitter_bearer_token,
            api_key=config.twitter_api_key,
            api_secret=config.twitter_api_secret,
            access_token=config.twitter_access_token,
            access_token_secret=config.twitter_access_token_secret,
        )
        self.scheduler = BlockingScheduler(timezone="UTC")
        self.stop_event = Event()

    def post_once(self) -> None:
        def _operation() -> None:
            meme = self.fetcher.fetch()
            tweet_id = self.poster.create_post(text=meme.text, media_url=meme.image_url)
            self.logger.append(
                source=meme.source,
                meme_text=meme.text,
                media_url=meme.image_url,
                status="success",
                tweet_id=tweet_id,
                error=None,
            )
            logging.info("Posted meme successfully from %s (tweet_id=%s)", meme.source, tweet_id)

        try:
            run_with_retry(
                operation=_operation,
                operation_name="post_once",
                max_retries=self.config.max_retries,
                base_backoff_seconds=self.config.retry_backoff_seconds,
            )
        except Exception as error:  # noqa: BLE001 - keep scheduler alive indefinitely.
            logging.exception("Final post attempt failed after retries: %s", error)
            self.logger.append(
                source="unknown",
                meme_text="",
                media_url="",
                status="failed",
                tweet_id=None,
                error=str(error),
            )

    def run_forever(self) -> None:
        logging.info(
            "Starting MemeBot with interval=%s minute(s), max_retries=%s",
            self.config.post_interval_minutes,
            self.config.max_retries,
        )

        self.scheduler.add_job(
            func=self.post_once,
            trigger=IntervalTrigger(minutes=self.config.post_interval_minutes),
            id="hourly_meme_post",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )

        self.post_once()

        def _shutdown_handler(signum: int, _frame: object) -> None:
            logging.info("Received signal %s, shutting down MemeBot.", signum)
            self.stop_event.set()
            self.scheduler.shutdown(wait=False)

        signal.signal(signal.SIGINT, _shutdown_handler)
        signal.signal(signal.SIGTERM, _shutdown_handler)

        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logging.info("MemeBot stopped.")
