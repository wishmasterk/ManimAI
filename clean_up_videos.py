import os
import time
from pathlib import Path

# --- Configuration ---
# The folder where final videos are stored.
VIDEOS_DIR = Path.cwd() / "final_videos"
# The maximum age of a file in seconds (e.g., 24 hours = 86400 seconds).
# Users will have this much time to download their video.
MAX_AGE_SECONDS = 86400

def cleanup_old_videos():
    """
    Deletes files in the VIDEOS_DIR that are older than MAX_AGE_SECONDS.
    This script should be run on a schedule (e.g., a daily cron job).
    """
    print(f"--- Running cleanup on directory: {VIDEOS_DIR} ---")
    if not VIDEOS_DIR.exists():
        print("Videos directory does not exist. Nothing to clean.")
        return

    now = time.time()
    files_deleted = 0

    for filename in os.listdir(VIDEOS_DIR):
        file_path = VIDEOS_DIR / filename
        
        if file_path.is_file():
            try:
                # Get the file's modification time and calculate its age
                file_age_seconds = now - file_path.stat().st_mtime
                
                # Check if the file is older than the configured max age
                if file_age_seconds > MAX_AGE_SECONDS:
                    print(f"Deleting old file: {filename} (Age: {file_age_seconds / 3600:.2f} hours)")
                    os.remove(file_path)
                    files_deleted += 1
            except OSError as e:
                print(f"Error deleting file {file_path}: {e}")

    print(f"--- Cleanup complete. Deleted {files_deleted} file(s). ---")

if __name__ == "__main__":
    cleanup_old_videos()
