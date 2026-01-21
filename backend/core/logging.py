import logging


class EndpointFilter(logging.Filter):
    """Remove specific endpoint access logs."""

    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        # do not log version endpoint access
        return "GET /version" not in message
