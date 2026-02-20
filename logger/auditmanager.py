"""Module for storing audit trail to a file"""
import logging
from functools import wraps
from pathfinder import AbsolutePathFinder
from connectors import YamlConnector


class AuditManager:
    def __init__(self):

        params_dict = YamlConnector().get_dict_from_yaml('logger_params.yaml')
        audit_folder = params_dict['logger']['audit_folder']
        audit_folder_path = AbsolutePathFinder().get_file_path(audit_folder)
        log_file_path = f"{audit_folder_path}/audit_trail.txt"

        self.audit = logging.getLogger("audit_manager")
        self.audit.setLevel(logging.INFO)

        if not self.audit.handlers:
            file_handler = logging.FileHandler(log_file_path)
            # Added %(context)s to the format to hold intermediate data
            formatter = logging.Formatter(
                '%(asctime)s | %(message)s %(context)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            self.audit.addHandler(file_handler)

    def audit_trace(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.audit.info(
                f"EXEC: {func.__name__} | PARAMS: args={args}, kwargs={kwargs}",
                extra={'context': ''})
            return func(*args, **kwargs)
        return wrapper

    # REPLACE audit_step with this:
    def get_adapter(self, **context_data):
        """Returns an adapter that injects context into every log message."""
        context_str = " | CONTEXT: " + ", ".join(
            [f"{k}={v}" for k, v in context_data.items()])
        return logging.LoggerAdapter(self.audit, {"context": context_str})


auditor = AuditManager()
