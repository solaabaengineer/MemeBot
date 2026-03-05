from __future__ import annotations

import logging
import sys

from memebot.bot import MemeBot
from memebot.config import load_config


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    try:
        config = load_config()
    except ValueError as error:
        logging.error("Configuration error: %s", error)
        return 1

    bot = MemeBot(config)
    bot.run_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
