# Action Required: Update Your config.py

## ⚠️ IMPORTANT: Your config.py needs to be updated!

The bot has been modified to support **round-robin forwarding across 3 channels**.

### What You Need to Do:

1. **Open your `config.py` file**

2. **Find this line:**
   ```python
   DESTINATION_CHANNEL = "movie_forward"
   ```

3. **Replace it with:**
   ```python
   # Destination channels - Add your 3 channels here
   DESTINATION_CHANNELS = [
       "your_channel_1",  # Replace with your first channel username/ID/link
       "your_channel_2",  # Replace with your second channel username/ID/link
       "your_channel_3",  # Replace with your third channel username/ID/link
   ]
   
   # Number of videos to forward to each channel before switching
   VIDEOS_PER_CHANNEL = 1000
   ```

4. **Replace the placeholder channel names** with your actual 3 channels

5. **Save the file**

6. **Run the bot:**
   ```bash
   python bot.py
   ```

### Example:

If your 3 channels are:
- `movies_channel_1`
- `movies_channel_2`  
- `movies_channel_3`

Your config.py should have:
```python
DESTINATION_CHANNELS = [
    "movies_channel_1",
    "movies_channel_2",
    "movies_channel_3",
]

VIDEOS_PER_CHANNEL = 1000
```

### How It Will Work:

```
Source → [1000 videos] → Channel 1
      → [1000 videos] → Channel 2
      → [1000 videos] → Channel 3
      → [1000 videos] → Channel 1 (repeats)
      → [1000 videos] → Channel 2
      → [1000 videos] → Channel 3
      ... and so on
```

---

**Need help?** Check these files:
- `UPDATE_ROUND_ROBIN.md` - Quick update guide
- `ROUND_ROBIN_FEATURE.md` - Full documentation
