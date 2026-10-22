import json

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
            f"'{path}' contains invalid JSON ({err}). Your data has NOT been changed."
        ) from err
    except OSError as err:
        raise StorageError(f"Could not read '{path}': {err}") from err
    if not isinstance(tickets, list):
        raise StorageError(f"'{path}' is not a valid ticket file.")
    return tickets

def save_tickets(tickets, path):
    try:
        with open(path, "w") as f:
            json.dump(tickets, f, indent=4)
    except OSError as err:
        raise StorageError(f"Could not save to '{path}': {err}") from err