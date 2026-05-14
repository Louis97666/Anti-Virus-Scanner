import psutil
import time
import os
from datetime import datetime

# Configuration
LOG_FILE = "process_log.txt"
UPDATE_INTERVAL = 2  # Seconds between refreshes
VIRUS_PATH = r"C:\Users\Louis\Desktop\Test-Virus.txt"

def monitor_processes():
    virus_detected = False # To ensure the alert triggers only once
    
    # Initialize the log file with a header
    with open(LOG_FILE, "w") as f:
        f.write(f"Monitoring Session Started: {datetime.now()}\n")
        f.write(f"{'Timestamp':<20} | {'PID':<10} | {'Process Name':<25} | {'CPU %':<10} | {'Mem (MB)':<10}\n")
        f.write("-" * 85 + "\n")

    try:
        while True:
            # Clear the terminal screen
            os.system('cls' if os.name == 'nt' else 'clear')
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"--- Real-Time Process Monitor ---")
            print(f"Logging active: Writing to {LOG_FILE}")
            print(f"{'PID':<10} | {'Name':<25} | {'CPU %':<10} | {'Memory (MB)':<10}")
            print("-" * 65)

            with open(LOG_FILE, "a") as f:
                # 1. Check if Virus File still exists
                if not os.path.exists(VIRUS_PATH) and not virus_detected:
                    status = "!!! DETECTION: Virus file was removed from Desktop !!!\n"
                    print(status)
                    f.write(f"{current_time:<20} | {status}")
                    virus_detected = True # Lock the alert

                # 2. Iterate through all running processes
                for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
                    try:
                        pid = proc.info['pid']
                        name = proc.info['name']
                        cpu = proc.info['cpu_percent']
                        mem_mb = proc.info['memory_info'].rss / (1024 * 1024)

                        # Print to console
                        print(f"{pid:<10} | {name[:25]:<25} | {cpu:<10.2f} | {mem_mb:<10.2f}")
                        
                        # Log active processes
                        if cpu > 0.1 or "Test-Virus" in name:
                            f.write(f"{current_time:<20} | {pid:<10} | {name[:25]:<25} | {cpu:<10.2f} | {mem_mb:<10.2f}\n")

                        # 3. Defender Activity Check
                        if name == "MsMpEng.exe" and cpu > 10.0:
                            alert = "!!! ALERT: High Defender Activity detected (Scan in progress) !!!\n"
                            print(alert)
                            f.write(f"{current_time:<20} | {alert}")

                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        continue
            
            time.sleep(UPDATE_INTERVAL)
            
    except KeyboardInterrupt:
        print(f"\n[!] Monitoring stopped by user. Summary saved in {LOG_FILE}")

if __name__ == "__main__":
    monitor_processes()