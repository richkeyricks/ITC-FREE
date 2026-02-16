
import os
import sys

def log_debug(msg):
    with open("debug_log.txt", "a") as f:
        f.write(f"{msg}\n")
