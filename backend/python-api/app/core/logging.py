import logging
import re

SENSITIVE_KEYS = [
    "authorization",
    "token",
    "password",
    "secret",
    "email",
]


class SensitiveDataFilter(logging.Filter):
    _pattern = re.compile(r"(?i)(authorization|token|password|secret|email)\\s*[=:]\\s*[^\\s,;]+")

    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        redacted = self._pattern.sub(lambda match: f"{match.group(1)}=<redacted>", message)
        if redacted != message:
            record.msg = redacted
            record.args = ()
        return True


def configure_logging(level: str) -> None:
    logger = logging.getLogger()
    logger.handlers.clear()

    handler = logging.StreamHandler()
    handler.addFilter(SensitiveDataFilter())
    formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(level.upper())
