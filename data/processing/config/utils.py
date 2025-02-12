import os
import datetime

from dotenv import load_dotenv

load_dotenv()

def get_env(variable_name: str, default_value=None):
    """
    Retrieve an environment variable with an optional default value.
    """
    return os.environ.get(variable_name, default_value)

def serialize(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat(timespec="milliseconds")
    if isinstance(obj, datetime.date):
        return str(obj)
    return obj