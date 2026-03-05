from __future__ import annotations

from typing import Callable, TypeVar
import logging
import time


T = TypeVar("T")


def run_with_retry(
    operation: Callable[[], T],
    operation_name: str,
    max_retries: int,
    base_backoff_seconds: int,
) -> T:
    last_error: Exception | None = None

    for attempt in range(1, max_retries + 1):
        try:
            return operation()
        except Exception as error:  # noqa: BLE001 - keep bot alive on any runtime failure.
            last_error = error
            sleep_seconds = base_backoff_seconds * (2 ** (attempt - 1))
            logging.exception(
                "Operation '%s' failed (attempt %s/%s). Retrying in %ss.",
                operation_name,
                attempt,
                max_retries,
                sleep_seconds,
            )
            time.sleep(sleep_seconds)

    raise RuntimeError(
        f"Operation '{operation_name}' failed after {max_retries} retries"
    ) from last_error
