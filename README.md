# MemeBot

MemeBot is an autonomous Python agent that posts memes to X (Twitter) on a schedule.  
It is built for resilient, continuous operation with logging, retry handling, and configurable meme sources.

This repository ships a production-ready baseline you can run locally or deploy to a VM/container.

## Mission

MemeBot exists to automate meme publishing reliably and transparently:

- Fetch meme content from configurable sources (Imgflip and Reddit JSON feeds).
- Post to X every hour using Twitter API v2.
- Persist structured post logs to disk for auditing and analytics.
- Recover automatically from transient API and network failures.

## Project Structure

```text
MemeBot/
├── .env.example
├── requirements.txt
├── run.py
├── scripts/
│   └── post_counter.py
└── memebot/
	├── __init__.py
	├── bot.py
	├── config.py
	├── fetcher.py
	├── post_logger.py
	├── retry.py
	└── twitter_client.py
```

## Requirements

- Python 3.10+
- X Developer account and API v2 credentials

## Setup

1. Clone repository and enter project directory.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Create `.env` from `.env.example` and fill credentials.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Configuration

Set the following in `.env`:

- `TWITTER_BEARER_TOKEN`
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_TOKEN_SECRET`
- `POST_INTERVAL_MINUTES` (default `60`)
- `MAX_RETRIES` (default `5`)
- `RETRY_BACKOFF_SECONDS` (default `2`)
- `POST_LOG_PATH` (default `./data/post_log.json`)
- `IMGFLIP_USERNAME` / `IMGFLIP_PASSWORD` (optional)
- `REDDIT_SUBREDDITS` (comma-separated, default meme subs)
- `REDDIT_USER_AGENT` (optional)
- `SOLANA_DONATION_WALLET` (for README donation section)

## Run MemeBot

```bash
python run.py
```

At startup, MemeBot schedules an hourly job and executes one immediate post attempt so you can verify connectivity quickly.

## Live Post Counter

MemeBot writes post history to `POST_LOG_PATH`. You can read a live post count with:

```bash
python scripts/post_counter.py
```

Expected output:

```text
Total posts logged: 42
Successful posts: 39
Failed posts: 3
```

## Logging Format

Each attempt is appended to JSON with fields:

- `timestamp`
- `source`
- `meme_text`
- `media_url`
- `status` (`success` or `failed`)
- `tweet_id`
- `error`

## Solana Donations

To fund MemeBot infrastructure and legal support, set your wallet in `.env`:

```text
SOLANA_DONATION_WALLET=REPLACE_WITH_YOUR_SOLANA_WALLET
```

Then display it publicly in your deployment docs or profile:

```text
Donation Wallet (SOL): REPLACE_WITH_YOUR_SOLANA_WALLET
```

## Notes

- Respect X automation rules and platform terms.
- Validate subreddit/source policies before deployment.
- For 24/7 uptime, run under a process manager (systemd, Docker restart policy, or supervisord).