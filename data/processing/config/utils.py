import os

from dotenv import load_dotenv

load_dotenv()

def get_env(variable_name: str, default_value=None):
    """
    Retrieve an environment variable with an optional default value.
    """
    return os.environ.get(variable_name, default_value)
