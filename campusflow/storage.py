import json
import tempfile
import os

class StorageError(Exception):
    """Raised when the data file cannot be read or validated safely."""

def load_tickets(path):
    try:
        with open(path, "r") as f:
            tickets = json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as err:
        raise StorageError(
            f"'{path}' contains invalid JSON ({err}). You/r data has NOT been changed."
        ) from err
    except OSError as err:
        raise StorageError(f"Could not read '{path}': {err}") from err
    if not isinstance(tickets, list):
        raise StorageError(f"'{path}' is not a valid ticket file.")
    return tickets


def save_tickets(tickets, path):
    directory = os.path.dirname(os.path.abspath(path))
    try:
        fd, temp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(tickets, handle, indent=4)
        os.replace(temp_path, path)
    except OSError as err:
        raise StorageError(f"Could not save to '{path}': {err}") from err