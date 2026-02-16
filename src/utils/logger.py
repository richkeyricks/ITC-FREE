import logging
import os
from datetime import datetime

# Ensure logs directory exists
LOG_FILE = "logs.txt"

def _log(level, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] [{level}] {message}"
    print(formatted)
    
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception as e:
        print(f"// Logger Write Error: {e}")

def log_info(message):
    _log("INFO", message)

def log_error(message):
    _log("ERROR", message)

def log_warning(message):
    _log("WARNING", message)

def log_critical(message):
    _log("CRITICAL", message)
