import time
import random
import json
from instagrapi import Client
import schedule
import os

# Load configuration
with open("config.json", "r") as f:
    config = json.load(f)

USERNAME = config["username"]
PASSWORD = config["password"]
GROUP_IDS = config["group_ids"]
INTERVAL = config["interval_minutes"]

# Load messages
with open("messages.txt", "r") as f:
    MESSAGES = [line.strip() for line in f if line.strip()]

# Login
cl = Client()

# Try loading saved session
if os.path.exists("session.json"):
    try:
        cl.load_settings("session.json")
        cl.login(USERNAME, PASSWORD)
        cl.dump_settings("session.json")
    except:
        print("Session load failed. Trying fresh login...")
        cl.login(USERNAME, PASSWORD)
        cl.dump_settings("session.json")
else:
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings("session.json")

# Send message
def send_message():
    message = random.choice(MESSAGES)
    for group_id in GROUP_IDS:
        try:
            cl.direct_send(message, [group_id])
            print(f"[SENT to {group_id}] {message}")
        except Exception as e:
            print(f"[ERROR] Sending to {group_id}: {e}")

# Schedule
schedule.every(INTERVAL).minutes.do(send_message)

# Run loop
while True:
    schedule.run_pending()
    time.sleep(5)
