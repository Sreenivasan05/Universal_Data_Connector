from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable
from functools import wraps
import time
import logging


logger = logging.getLogger(__name__)


def with_retry(max_attempt:int = 3, base_delay:float = 2.0):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            delay = base_delay
            for attempt in range(1, max_attempt+1):
                try:
                    return fn(*args, **kwargs)
                except ResourceExhausted as exc:
                    if attempt == max_attempt:
                        logger.error("Rate limit hit, max retries exhausted")
                        raise 
                    logger.warning(
                        "429 rate limit on attempt %d/%d - retrying in %.1fs", attempt, max_attempt, delay
                    )
                    time.sleep(delay)
                    delay *= 2
                except ServiceUnavailable:
                    if attempt == max_attempt:
                        raise
                    logger.warning(
                        "503 on attempt %d — retrying in %.1fs", attempt, delay
                    )
                    time.sleep(delay)
                    delay *= 2
        return wrapper
    return decorator