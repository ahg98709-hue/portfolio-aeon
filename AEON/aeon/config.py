
import os
from dotenv import load_dotenv

# Load .env file
# Try to find .env in current or parent directories
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
load_dotenv(env_path)

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Configuration
AEON_MODEL = os.getenv("AEON_MODEL", "llama-3.1-8b-instant")

def check_config():
    """Checks if essential config is present."""
    if not GROQ_API_KEY:
        return False
    return True
