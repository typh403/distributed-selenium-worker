import json
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Determine execution path (EXE vs. Script)
if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(base_path, 'config.json')
LOG_PATH = os.path.join(base_path, 'logs.txt')

def write_log(message):
    """Writes output to both console and the log file."""
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"{message}\n")
    print(message)

def main():
    driver = None
    try:
        # 1. Load Configuration
        if not os.path.exists(CONFIG_PATH):
            raise FileNotFoundError(f"Configuration file missing at: {CONFIG_PATH}")

        with open(CONFIG_PATH, 'r', encoding="utf-8") as f:
            config = json.load(f)

        write_log("---- INITIALIZING WORKER ---")
        write_log(f"Channel/Task: {config.get('channel_name', 'Unknown')}")
        write_log(f"Proxy: {config.get('proxy')}")
        write_log(f"Username: {config.get('username')}")

        # 2. Chrome Options & Fingerprint Isolation
        options = Options()
        if config.get('proxy'):
            options.add_argument(f'--proxy-server=http://{config["proxy"]}')
        
        # Isolate session data to avoid cross-contamination between workers
        profile_path = os.path.join(base_path, "profile")
        options.add_argument(f'--user-data-dir={profile_path}')
        options.add_argument('--disable-blink-features=AutomationControlled') # Anti-detection

        # 3. Initialize WebDriver
        write_log("[INFO] Launching isolated browser instance...")
        driver = webdriver.Chrome(options=options)
        
        # Test connection (IP verification)
        driver.get("https://whatismyipaddress.com/")

        # 4. Process Holding State (Replace with actual automation logic)
        input("Process completed. Press Enter to exit...")

    except Exception as e:
        write_log(f"[CRITICAL ERROR] {str(e)}")
        input("An error occurred. Press Enter to close...")

    finally:
        if driver:
            try:
                driver.quit()
                write_log("[INFO] Browser instance closed safely.")
            except Exception:
                pass

if __name__ == "__main__":
    main()