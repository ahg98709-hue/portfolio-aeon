import sys
import os

# Add the project root to sys.path if running directly
if __package__ is None and not hasattr(sys, "frozen"):
    # Current file is .../AEON/aeon/__main__.py
    # We want .../AEON/
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

from aeon.core.engine import Engine
from aeon.config import check_config
from aeon.utils.io import error

def main():
    if not check_config():
        error("Configuration missing. Please copy .env.example to .env and set your GROQ_API_KEY.")
        return

    try:
        engine = Engine()
        engine.run_loop()
    except Exception as e:
        error(f"Fatal Error: {e}")

if __name__ == "__main__":
    main()
