import os
from config import LOCK_FILE


def acquire_lock():
    abs_path = os.path.abspath(LOCK_FILE)
    if os.path.exists(LOCK_FILE):
        return False  # уже запущен
    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))
    return True

def release_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)
        print(f"[DEBUG] Lock file removed: {os.path.abspath(LOCK_FILE)}")