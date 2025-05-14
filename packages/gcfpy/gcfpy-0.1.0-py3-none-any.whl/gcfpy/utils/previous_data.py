import os

# Path to store the recent files history
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "last_files.txt")
MAX_HISTORY = 5


def save_previous_file(file_path):
    """
    Saves the path of the recently loaded file into history.

    Keeps only the last MAX_HISTORY entries and avoids duplicates in succession.
    """
    if not file_path:
        return

    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                files = f.read().splitlines()
        else:
            files = []

        # Skip if it's already the last one recorded
        if files and files[-1] == file_path:
            return

        files.append(file_path)
        files = files[-MAX_HISTORY:]

        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(files))

    except Exception as e:
        print(f"[Error] Could not save file history: {e}")


def load_previous_file(index=-1):
    """
    Loads a file path from history.

    Args:
        index (int): Use -1 for the last file, -2 for the previous one, etc.

    Returns:
        str or None: Path to the previous file, or None if not available.

    """
    if not os.path.exists(HISTORY_FILE):
        print("[Warning] No file history found.")
        return None

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            files = f.read().splitlines()

        if abs(index) > len(files):
            print(f"[Warning] No file found at index {index}.")
            return None

        candidate = files[index]

        if not os.path.exists(candidate):
            print(f"[Warning] File not found: {candidate}")
            return None

        return candidate

    except Exception as e:
        print(f"[Error] Failed to load previous file: {e}")
        return None
