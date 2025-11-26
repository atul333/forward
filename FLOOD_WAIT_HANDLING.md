# Flood Wait Error Handling

## Overview
The bot now automatically handles Telegram's flood wait errors when forwarding messages. When you encounter a flood wait error, the bot will:

1. **Detect the error** - Catches `FloodWaitError` exceptions
2. **Calculate wait time** - Adds a 60-second buffer to the required wait time for safety
3. **Display information** - Shows detailed information about the wait
4. **Wait automatically** - Pauses for the required duration
5. **Resume forwarding** - Continues from where it left off

## What Happens During a Flood Wait

When a flood wait error occurs (e.g., "A wait of 1011 seconds is required"), you'll see:

```
======================================================================
⚠️  FLOOD WAIT ERROR on message 26434
Required wait: 1011 seconds (16.9 minutes)
Actual wait (with buffer): 1071 seconds (17.9 minutes)
Current time: 2025-11-26 19:38:00
Resume time: 2025-11-26 19:55:51
Last successful message ID: 26433
Will resume from message ID: 26434
======================================================================
Waiting for 17.9 minutes...
```

## Key Features

### 1. Automatic Wait and Retry
- The bot automatically waits for the required time
- Adds a 60-second safety buffer to avoid immediate re-triggering
- Retries the failed message after waiting
- Continues with the next messages

### 2. Progress Tracking
- Tracks the last successfully forwarded message ID
- Shows which message caused the flood wait
- Displays when forwarding will resume

### 3. Time Information
- Shows current time
- Calculates and displays resume time
- Converts seconds to minutes for easier reading

### 4. Works in All Modes
- **Mode 1**: Forward existing messages (one-time)
- **Mode 2**: Forward new messages (continuous)
- **Mode 3**: Both existing and new messages

## Example Scenario

If you're forwarding messages and hit a flood wait at message 26434:

1. **Error occurs**: "A wait of 1011 seconds is required"
2. **Bot responds**: Waits for 1071 seconds (17.9 minutes)
3. **After wait**: Retries message 26434
4. **Continues**: Forwards message 26435, 26436, etc.

## No Manual Intervention Required

You **do not** need to:
- Manually restart the script
- Remember which message failed
- Calculate wait times
- Set timers

The bot handles everything automatically!

## What You'll See

### Before the wait:
```
Forwarded message 26432 (100 total)
Forwarded message 26433 (101 total)
⚠️  FLOOD WAIT ERROR on message 26434
Waiting for 17.9 minutes...
```

### After the wait:
```
Wait complete! Resuming forwarding...
✓ Successfully forwarded message 26434 after wait
Forwarded message 26435 (102 total)
Forwarded message 26436 (103 total)
```

## Tips

1. **Let it run** - Don't interrupt the bot during the wait
2. **Monitor logs** - The bot provides detailed progress information
3. **Adjust delays** - If you get frequent flood waits, increase `DELAY_BETWEEN_FORWARDS` in `config.py`

## Configuration

To reduce flood wait errors, you can increase the delay between forwards in `config.py`:

```python
# Delay between forwarding messages (in seconds)
# Increase this if you're getting flood wait errors frequently
DELAY_BETWEEN_FORWARDS = 2  # Default is 1, try 2-5 for safer operation
```

## Technical Details

The bot catches `FloodWaitError` exceptions from Telethon and:
- Extracts the required wait time from `e.seconds`
- Adds 60 seconds buffer
- Uses `asyncio.sleep()` to wait
- Retries the same message after waiting
- Continues the iteration from the next message

This ensures no messages are skipped and forwarding resumes seamlessly!
