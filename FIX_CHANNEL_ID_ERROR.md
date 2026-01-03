# Common Configuration Errors - Quick Fix Guide

## Error: "Cannot find any entity corresponding to..."

### Problem
You're seeing an error like:
```
ERROR - Cannot find any entity corresponding to "-1003680603642"
```

### Cause
Channel IDs in `config.py` are wrapped in quotes (making them strings) when they should be integers.

### Solution

#### ❌ WRONG (Channel ID with quotes):
```python
DESTINATION_CHANNELS = [
    "-1003680603642",  # ❌ WRONG - Has quotes
    "-1002515799124",  # ❌ WRONG - Has quotes
    "channel3",
]
```

#### ✅ CORRECT (Channel ID without quotes):
```python
DESTINATION_CHANNELS = [
    -1003680603642,    # ✅ CORRECT - No quotes (integer)
    -1002515799124,    # ✅ CORRECT - No quotes (integer)
    "channel3",        # ✅ CORRECT - Username needs quotes
]
```

## Quick Reference

### When to Use Quotes vs No Quotes

| Type | Example | Use Quotes? |
|------|---------|-------------|
| **Channel ID** | `-1003680603642` | ❌ NO - Must be integer |
| **Username** | `my_channel` | ✅ YES - Must be string |
| **Invite Link** | `https://t.me/+ABC123` | ✅ YES - Must be string |

### Examples

#### All Channel IDs (integers - no quotes):
```python
DESTINATION_CHANNELS = [
    -1003680603642,
    -1002515799124,
    -1001234567890,
]
```

#### All Usernames (strings - with quotes):
```python
DESTINATION_CHANNELS = [
    "movies_hindi",
    "movies_english",
    "movies_dubbed",
]
```

#### Mixed (IDs, usernames, and links):
```python
DESTINATION_CHANNELS = [
    -1003680603642,                    # ID - no quotes
    "movies_channel",                  # Username - with quotes
    "https://t.me/+qUTXDWTxJh42ODhl",  # Link - with quotes
]
```

## How to Fix Your config.py

1. **Open `config.py`**

2. **Find your `DESTINATION_CHANNELS` section**

3. **Remove quotes from channel IDs:**
   - Change `"-1003680603642"` to `-1003680603642`
   - Change `"-1002515799124"` to `-1002515799124`

4. **Keep quotes for usernames and links:**
   - `"my_channel"` stays as is
   - `"https://t.me/+ABC"` stays as is

5. **Save the file**

6. **Run the bot again:**
   ```bash
   python bot.py
   ```

## Still Having Issues?

### Make sure you've joined all channels
```
1. Open Telegram
2. Join all 3 destination channels
3. Verify you can post in them
4. Then run the bot
```

### Verify channel IDs are correct
```
1. Right-click on channel in Telegram Desktop
2. Copy channel link
3. If link is like: https://t.me/c/3680603642/123
4. Add -100 prefix: -1003680603642
```

### Check for typos
- No spaces in channel IDs
- Negative sign (-) at the beginning
- All digits after the negative sign
- No quotes around the number
