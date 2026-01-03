# Quick Update Guide - Round-Robin Forwarding

## What Changed?

The bot now supports forwarding to **3 channels in rotation** instead of just 1 channel.

## How to Update Your config.py

### BEFORE (Old Format):
```python
DESTINATION_CHANNEL = "movie_forward"  # Single channel
```

### AFTER (New Format):
```python
# List of 3 destination channels
DESTINATION_CHANNELS = [
    "channel1_username",  # Your first channel
    "channel2_username",  # Your second channel  
    "channel3_username",  # Your third channel
]

# How many videos to send to each channel before switching
VIDEOS_PER_CHANNEL = 1000
```

## Example with Real Channels:

```python
DESTINATION_CHANNELS = [
    "movies_hindi",                        # Username
    -1001234567890,                        # Channel ID
    "https://t.me/+qUTXDWTxJh42ODhl",     # Invite link
]

VIDEOS_PER_CHANNEL = 1000  # Send 1000 videos to each channel
```

## How It Works:

1. Bot forwards 1000 videos to Channel 1
2. Then forwards 1000 videos to Channel 2
3. Then forwards 1000 videos to Channel 3
4. Then repeats: back to Channel 1, then 2, then 3, etc.

## That's It!

Just update your `config.py` and run the bot as usual:
```bash
python bot.py
```

For more details, see [ROUND_ROBIN_FEATURE.md](ROUND_ROBIN_FEATURE.md)
