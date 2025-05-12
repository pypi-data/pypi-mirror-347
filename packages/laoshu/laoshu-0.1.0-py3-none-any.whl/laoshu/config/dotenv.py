import os
from pathlib import Path
from typing import Dict, Optional


def load_dotenv(dotenv_path: Optional[str] = None) -> Dict[str, str]:
    """
    Load environment variables from a .env file into os.environ.
    If an environment variable already exists, it won't be overridden.

    Args:
        dotenv_path: Path to the .env file. If None, looks for .env in the current directory.

    Returns:
        Dictionary of environment variables loaded from the .env file.
    """
    if dotenv_path is None:
        dotenv_path = ".env"

    env_path = Path(dotenv_path)
    if not env_path.exists():
        return {}

    env_vars = {}

    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            # Remove quotes if present
            if value and (value[0] == value[-1] == '"' or value[0] == value[-1] == "'"):
                value = value[1:-1]

            # Only set if the environment variable doesn't already exist
            if key not in os.environ:
                os.environ[key] = value
                env_vars[key] = value
            else:
                env_vars[key] = os.environ[key]

    return env_vars
