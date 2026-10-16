# vietstock/config.py
from __future__ import annotations

import logging


class Config:
    # -------------------------------------------------------------------------
    # HTTP request settings
    # -------------------------------------------------------------------------
    # Default timeout (in seconds) for any network request
    REQUEST_TIMEOUT: int = 30

    # Number of retry attempts on transient failures
    RETRIES: int = 3

    # Tenacity backoff strategy parameters
    BACKOFF_MULTIPLIER: float = 1.0
    BACKOFF_MIN: float = 2  # minimum wait between retries (seconds)
    BACKOFF_MAX: float = 10  # maximum wait between retries (seconds)

    # -------------------------------------------------------------------------
    # Block detection (CDN / WAF)
    # -------------------------------------------------------------------------
    # Master switch for recognising "the source blocked us" responses.
    BLOCK_DETECTION_ENABLED: bool = True

    # Max bytes of a response body read while sniffing for block markers.
    # CDN block pages always put their marker near the top, so reading the whole
    # body is never necessary.
    BODY_SNIFF_LIMIT: int = 8192

    # Honour a Retry-After header only when the wait is at most this long, and
    # only retry once. Anything longer stops immediately and hands the decision
    # back to the caller instead of hanging their process.
    RETRY_AFTER_MAX_WAIT: float = 30.0

    # -------------------------------------------------------------------------
    # Per-host circuit breaker
    # -------------------------------------------------------------------------
    CIRCUIT_BREAKER_ENABLED: bool = True

    # Default cooldown per kind of block signal (seconds).
    BLOCK_COOLDOWN_RATE_LIMIT: float = 60.0
    BLOCK_COOLDOWN_CHALLENGE: float = 300.0
    BLOCK_COOLDOWN_DENIED: float = 300.0

    # Clamp applied to every cooldown, including one derived from Retry-After.
    BLOCK_COOLDOWN_MIN: float = 5.0
    BLOCK_COOLDOWN_MAX: float = 900.0

    # Upper bound on tracked hosts before the breaker prunes expired entries.
    CIRCUIT_MAX_ENTRIES: int = 256

    # -------------------------------------------------------------------------
    # Caching
    # -------------------------------------------------------------------------
    # Max entries for LRU‑cached methods
    CACHE_SIZE: int = 128

    # -------------------------------------------------------------------------
    # Logging
    # -------------------------------------------------------------------------
    # Default logging level for all vietstock modules
    LOG_LEVEL: int = logging.DEBUG

    @classmethod
    def apply_logging_config(cls):
        """
        Call once at startup to configure vietstock logging.
        """
        logging.getLogger("vietstock").setLevel(cls.LOG_LEVEL)
