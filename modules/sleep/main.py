import time
from modules.logging.main import write_log

def goto_sleep(minutes: int):
    for remaining_minutes in range(minutes, 0, -1):
        print(f"[SLEEP] - {remaining_minutes} minute(s) left.")
        write_log(f"[SLEEP] - {remaining_minutes} minute(s) left.")
        time.sleep(60)  # Sleep for 60 seconds (1 minute)
    print("[SLEEP] - Wake up!")

