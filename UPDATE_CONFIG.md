# ⚠️ IMPORTANT: Configuration Update Required

You need to update your **config.py** file (NOT config.example.py) with the following changes:

## Issue 1: Wrong File Updated
You updated `config.example.py` but the bot uses `config.py`. Please open `config.py` and make the changes there.

## Issue 2: Source Channel ID Format
The source channel `https://t.me/c/2515799124/` is a **private channel**. 
For private channels, you need to add `-100` prefix to the channel ID.

## Required Changes in config.py:

```python
# Change this line:
SOURCE_CHANNEL_ID = 2515799124

# To this:
SOURCE_CHANNEL_ID = -1002515799124  # Note: -100 prefix added

# Also change:
DESTINATION_CHANNEL = "https://t.me/+qUTXDWTxJh42ODhl"

# To this (use just the username):
DESTINATION_CHANNEL = "movie_forward"
```

## Complete config.py should look like:

```python
# Telegram API Configuration
# Get these from https://my.telegram.org

# Your Telegram API credentials
API_ID = "38483384"  # Your API ID
API_HASH = "8a236f58a7..."  # Your API hash (keep your full hash)

# Bot Token (not used for forwarding, but kept for reference)
BOT_TOKEN = "8084457483:AAEHgETP6tVbqnTWBgHG_KEjtMDe1oINVFo"

# Channel Configuration
SOURCE_CHANNEL_ID = -1002515799124  # Source channel ID (with -100 prefix for private channels)
DESTINATION_CHANNEL = "movie_forward"  # Destination channel (just the username)

# Session name (will create a .session file with this name)
SESSION_NAME = "movie_forwarder"

# Forwarding settings
DELAY_BETWEEN_FORWARDS = 1  # Seconds to wait between forwarding messages (to avoid rate limits)
```

## After making these changes:
1. Save config.py
2. Run: `python test_config.py` to verify
3. If test passes, run: `python bot.py`
