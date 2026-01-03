# Round-Robin Forwarding Feature

## Overview
The bot now supports forwarding videos to **3 destination channels** in a **round-robin fashion**. This means:
- Forward 1000 videos to Channel 1
- Then forward 1000 videos to Channel 2
- Then forward 1000 videos to Channel 3
- Then repeat the cycle (back to Channel 1)

## Configuration

### 1. Update your `config.py`

You need to update your `config.py` file with the new configuration format. Here's what changed:

**OLD FORMAT (Single Channel):**
```python
DESTINATION_CHANNEL = "movie_forward"
```

**NEW FORMAT (3 Channels):**
```python
# Destination channels - Add your 3 channels here
DESTINATION_CHANNELS = [
    "channel1_username",  # Replace with your first channel
    "channel2_username",  # Replace with your second channel
    "channel3_username",  # Replace with your third channel
]

# Number of videos to forward to each channel before switching
VIDEOS_PER_CHANNEL = 1000
```

### 2. Channel Format Options

Each channel in the `DESTINATION_CHANNELS` list can be specified in multiple formats:

- **Username**: `"my_channel"` or `"@my_channel"`
- **Channel ID**: `-1001234567890` (numeric ID with -100 prefix)
- **Invite Link**: `"https://t.me/+AbCdEfGhIjKlMnOp"`

**Example:**
```python
DESTINATION_CHANNELS = [
    "movies_channel_1",                    # Username
    -1001234567890,                        # Channel ID
    "https://t.me/+qUTXDWTxJh42ODhl",     # Invite link
]
```

### 3. Customize Videos Per Channel

You can change how many videos are forwarded to each channel before switching:

```python
VIDEOS_PER_CHANNEL = 1000  # Default is 1000
```

For example:
- Set to `500` to forward 500 videos to each channel
- Set to `2000` to forward 2000 videos to each channel

## How It Works

### Forwarding Pattern

The bot follows this pattern:

```
Videos 1-1000    → Channel 1
Videos 1001-2000 → Channel 2
Videos 2001-3000 → Channel 3
Videos 3001-4000 → Channel 1 (cycle repeats)
Videos 4001-5000 → Channel 2
Videos 5001-6000 → Channel 3
... and so on
```

### Visual Example

```
Source Channel (All Videos)
    ↓
    ├─→ [1000 videos] → Channel 1
    ├─→ [1000 videos] → Channel 2
    ├─→ [1000 videos] → Channel 3
    ├─→ [1000 videos] → Channel 1 (repeat)
    ├─→ [1000 videos] → Channel 2
    └─→ [1000 videos] → Channel 3
```

## Running the Bot

### Step 1: Update Configuration

Make sure your `config.py` has the new format with `DESTINATION_CHANNELS` (list) instead of `DESTINATION_CHANNEL` (single value).

### Step 2: Run the Bot

```bash
python bot.py
```

### Step 3: Monitor Progress

The bot will show detailed logs including:

```
✓ All channels initialized successfully!
  Source: Source Channel Name
  Destination 1: Channel One Name
  Destination 2: Channel Two Name
  Destination 3: Channel Three Name

📊 Forwarding 1000 videos to each channel before switching

✓ Forwarded message 123 to Channel 1 (1/1000 to this channel) (Batch: 1/100, Total: 1)
✓ Forwarded message 124 to Channel 1 (2/1000 to this channel) (Batch: 2/100, Total: 2)
...
✓ Forwarded message 1122 to Channel 1 (1000/1000 to this channel) (Batch: 100/100, Total: 1000)

🔄 ======================================================================
🔄 SWITCHING TO CHANNEL 2: Channel Two Name
🔄 ======================================================================

✓ Forwarded message 1123 to Channel 2 (1/1000 to this channel) (Batch: 1/100, Total: 1001)
...
```

### Step 4: View Summary

At the end, you'll see a comprehensive summary:

```
======================================================================
📊 FORWARDING SUMMARY
======================================================================
📦 Total batches processed: 30
✅ Successfully forwarded: 3000 messages
❌ Failed to forward: 0 messages
📈 Total processed: 3000 messages
🎯 Success rate: 100.0%
----------------------------------------------------------------------
📺 Per-Channel Distribution:
  Channel 1 (Channel One Name): 1000 videos
  Channel 2 (Channel Two Name): 1000 videos
  Channel 3 (Channel Three Name): 1000 videos
----------------------------------------------------------------------
```

## Features

### ✅ Automatic Channel Switching
The bot automatically switches to the next channel after forwarding the configured number of videos.

### ✅ Flood Wait Handling
If Telegram rate limits are hit, the bot will automatically wait and resume.

### ✅ Per-Channel Statistics
Track exactly how many videos were sent to each channel.

### ✅ Works for Both Modes
- **Existing messages**: Round-robin forwarding of all existing videos
- **New messages**: Continues round-robin pattern for incoming videos

## Troubleshooting

### Error: "DESTINATION_CHANNELS not found"
- Make sure you updated `config.py` with the new format
- Change `DESTINATION_CHANNEL` to `DESTINATION_CHANNELS` (plural)
- Make it a list with 3 channels

### Error: "Failed to initialize all channels"
- Ensure you've joined all 3 destination channels
- Verify the channel usernames/IDs/links are correct
- Check that you have posting permissions in all channels

### Videos not distributing evenly
- Check the `VIDEOS_PER_CHANNEL` setting in `config.py`
- Verify the bot completed without errors
- Check the final summary for per-channel distribution

## Migration from Old Version

If you were using the old single-channel version:

1. **Backup your current `config.py`**
2. **Update the configuration**:
   ```python
   # OLD:
   DESTINATION_CHANNEL = "my_channel"
   
   # NEW:
   DESTINATION_CHANNELS = [
       "my_channel_1",
       "my_channel_2", 
       "my_channel_3"
   ]
   VIDEOS_PER_CHANNEL = 1000
   ```
3. **Run the bot** - it will now distribute videos across all 3 channels

## Notes

- The bot maintains the round-robin state even across flood waits
- Each batch of 100 videos still has a 1-minute delay (configurable via `DELAY_BETWEEN_FORWARDS`)
- The round-robin counter persists for new incoming messages as well
- All 3 channels must be accessible before the bot starts forwarding
