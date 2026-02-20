import logging
import logging.config
import json
from datetime import datetime, timezone



class JSONFormatter(logging.Formatter):
    """
    Formats log records as single-line JSON — easy to ingest into
    CloudWatch, Datadog, GCP Logging, or any log aggregator.
    """

    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Attach exception info if present
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)


        return json.dumps(log_obj, default=str)


def configure_logging(log_level: str = "INFO", use_json: bool = False) -> None:
    """
    Call once at application startup (in main.py lifespan).

    Args:
        log_level: DEBUG | INFO | WARNING | ERROR
        use_json:  True in production (structured JSON), False in dev (readable)
    """
    formatter_class = JSONFormatter if use_json else logging.Formatter

    config = {
        "version": 1,
        "disable_existing_loggers": False,   
        "formatters": {
            "json": {
                "()": JSONFormatter,
            },
            "standard": {
                "format": "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "json" if use_json else "standard",
            },
        },
        "loggers": {

            "app": {
                "handlers": ["console"],
                "level": log_level,
                "propagate": False,
            },

            "uvicorn.access": {
                "handlers": ["console"],
                "level": "WARNING",   
                "propagate": False,
            },
            "google": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,
            },
        },

        "root": {
            "handlers": ["console"],
            "level": "WARNING",
        },
    }

    logging.config.dictConfig(config)