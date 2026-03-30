#!/usr/bin/env python3
#go to https://my.telegram.org to create app and get api_id and api_hash, then put them in config.cfg

#pip install telethon

import asyncio
import configparser
import os
import sys
from datetime import datetime
from telethon import TelegramClient, events

# ==========================
# LOAD CONFIG
# ==========================
CONFIG_FILE = "config.cfg"

if not os.path.exists(CONFIG_FILE):
    print(f"ERROR: {CONFIG_FILE} not found")
    sys.exit(1)

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

# ==========================
# TELEGRAM CONFIG
# ==========================
try:
    API_ID = int(config.get("telegram", "api_id"))
    API_HASH = config.get("telegram", "api_hash").strip()
except Exception as e:
    print(f"ERROR reading telegram config: {e}")
    sys.exit(1)

# ==========================
# SETTINGS
# ==========================
DELETE_OWN_MESSAGES = config.getboolean("settings", "delete_own_messages", fallback=False)

target_chats_raw = config.get("settings", "target_chats", fallback="").strip()
TARGET_CHATS = []

if target_chats_raw:
    try:
        TARGET_CHATS = [int(x.strip()) for x in target_chats_raw.split(",") if x.strip()]
    except ValueError:
        print("ERROR: target_chats must be comma-separated integers")
        sys.exit(1)

# ==========================
# LOGGING
# ==========================
ENABLE_LOGS = config.getboolean("log", "enable_logs", fallback=True)
LOG_FILE = config.get("log", "log_file", fallback="telegram_sticker_cleaner.log")

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} {msg}"

    print(line)

    if ENABLE_LOGS:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")

# ==========================
# INIT CLIENT
# ==========================
SESSION_NAME = "sticker_cleaner"
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# ==========================
# HELPERS
# ==========================
def is_target_chat(chat_id):
    if not TARGET_CHATS:
        return True
    return chat_id in TARGET_CHATS

# ==========================
# HANDLER
# ==========================
@client.on(events.NewMessage)
async def handler(event):
    msg = event.message

    if not is_target_chat(event.chat_id):
        return

    if not DELETE_OWN_MESSAGES and msg.out:
        return

    if msg.sticker:
        try:
            await msg.delete()
            log(f"[DELETED] Sticker in chat {event.chat_id}")
        except Exception as e:
            log(f"[ERROR] Failed to delete in chat {event.chat_id}: {e}")

# ==========================
# MAIN
# ==========================
async def main():
    log("Starting Telegram Sticker Cleaner...")

    await client.start()
    log("Logged in successfully")

    await client.run_until_disconnected()

# ==========================
# ENTRY
# ==========================
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log("Stopped by user")
