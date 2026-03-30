# Telegram Sticker Cleaner

Automatically removes messages containing stickers from your Telegram chats using a userbot (MTProto).

---

## Features

* Deletes incoming sticker messages in real-time
* Works in private chats, groups, and channels (with permissions)
* Config-driven (`config.cfg`)
* Supports filtering by chat IDs
* Optional logging to file
* Runs as a background service (nohup / systemd)

---

## Important

This project uses the Telegram user API (MTProto) via Telethon.

* It runs as your Telegram account (not a bot)
* It has access to your messages
* Use responsibly

Telegram Bot API cannot do this.

---

## Requirements

* Python 3.8+
* telethon

Install dependency:

```bash
pip install telethon
```

---

## Getting API Credentials

1. Go to: https://my.telegram.org
2. Log in with your phone number
3. Open API development tools
4. Create an app
5. Copy:

   * api_id
   * api_hash

---

## Configuration

Create `config.cfg` in the same folder as the script:

```ini
[telegram]
api_id = 123456
api_hash = your_api_hash_here

[settings]
delete_own_messages = false

# empty = all chats
# example: -1001234567890,123456789
target_chats = 

[log]
enable_logs = true
log_file = telegram_sticker_cleaner.log
```

---

## Usage

### First run (interactive login)

```bash
python3 telegram_sticker_cleaner.py
```

You will be prompted for:

* phone number
* verification code
* 2FA password (if enabled)

A session file will be created:

```
sticker_cleaner.session
```

---

### Run in background

```bash
nohup python3 telegram_sticker_cleaner.py > cleaner.log 2>&1 &
```

---

## How it works

* Monitors all incoming messages
* Detects sticker messages
* Deletes them instantly

---

## Configuration Examples

### All chats

```ini
target_chats =
```

### Single chat

```ini
target_chats = -10031234567
```

### Multiple chats

```ini
target_chats = -10031234567,123456789
```

---

## Limitations

* Cannot edit messages, only delete
* Cannot delete messages without permission
* Requires admin rights in groups to delete others' messages
* Cannot access channels where you are not a member

---

## Security Notes

* Keep your api_hash secret
* Do not share your .session file
* This script runs with full access to your Telegram account

---

## Running as a service (optional)

Example systemd service:

```
[Unit]
Description=Telegram Sticker Cleaner
After=network.target

[Service]
User=youruser
WorkingDirectory=/path/to/script
ExecStart=/usr/bin/python3 telegram_sticker_cleaner.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:

```bash
systemctl daemon-reload
systemctl enable telegram-cleaner
systemctl start telegram-cleaner
```

---

## License

MIT License

---
## Author

Davege1107
---

## Notes

* This tool is intended for personal automation
* Use responsibly and respect Telegram terms of service
