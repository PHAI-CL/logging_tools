"""Module for storing audit trail to a file"""
import logging
from functools import wraps


class AuditManager:
    def __init__(self, log_file="audit_trail.txt"):
        self.logger = logging.getLogger("audit_manager")
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            file_handler = logging.FileHandler(log_file)
            # Added %(context)s to the format to hold intermediate data
            formatter = logging.Formatter(
                '%(asctime)s | %(message)s %(context)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def audit_trace(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.logger.info(
                f"EXEC: {func.__name__} | PARAMS: args={args}, kwargs={kwargs}",
                extra={'context': ''})
            return func(*args, **kwargs)
        return wrapper

    # REPLACE audit_step with this:
    def get_adapter(self, **context_data):
        """Returns an adapter that injects context into every log message."""
        context_str = " | CONTEXT: " + ", ".join(
            [f"{k}={v}" for k, v in context_data.items()])
        return logging.LoggerAdapter(self.logger, {"context": context_str})


auditor = AuditManager()
