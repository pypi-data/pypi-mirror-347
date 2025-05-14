import logging
from datetime import datetime
import os
import json

class AuditLogger:
    def __init__(self, config: dict = None):
        config = config or {}

        # Allow disabling via config or env
        self.enabled = config.get("enabled", True)
        if os.getenv("SAFE_AUDIT_LOG") == "0":
            self.enabled = False

        # File paths from config or default
        self.txt_log_path = config.get("destination", "safentic/logs/txt_logs/safentic_audit.log")
        self.jsonl_path = config.get("jsonl", "safentic/logs/json_logs/safentic_audit.jsonl")

        # Ensure directories exist
        os.makedirs(os.path.dirname(self.txt_log_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.jsonl_path), exist_ok=True)

        # Set up logger
        self.logger = logging.getLogger("safentic.audit")

        level_str = config.get("level", "INFO").upper()
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }
        level = level_map.get(level_str, logging.INFO)
        self.logger.setLevel(level)

        # Prevent duplicate handlers (e.g., in notebooks)
        if not self.logger.handlers:
            formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

            file_handler = logging.FileHandler(self.txt_log_path)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def log(self, agent_id: str, tool: str, allowed: bool, reason: str = None):
        if not self.enabled:
            return

        entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": agent_id,
            "tool": tool,
            "allowed": allowed,
            "reason": reason or "No violation"
        }

        log_level = logging.INFO if allowed else logging.WARNING
        self.logger.log(log_level, f"[AUDIT] {entry}")

        try:
            with open(self.jsonl_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            self.logger.error(f"Failed to write structured audit log: {e}")

    def set_level(self, level: str):
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }

        level = level.upper()
        if level in level_map:
            self.logger.setLevel(level_map[level])
        else:
            raise ValueError(f"Unsupported log level: {level}")
