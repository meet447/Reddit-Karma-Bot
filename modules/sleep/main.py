import time
from modules.logging.main import write_log
import random

time1 = [12,3,4,8,2,7,8,9,11,22,1,3,5,6,7,9]

def goto_sleep(minutes: int):
    t = random.choice(time1)
    minutes = minutes + t
    for remaining_minutes in range(minutes, 0, -1):
        print(f"[SLEEP] - {remaining_minutes} minute(s) left.")
        write_log(f"[SLEEP] - {remaining_minutes} minute(s) left.")
        time.sleep(60)  # Sleep for 60 seconds (1 minute)
        
    print("[SLEEP] - Wake up!")



