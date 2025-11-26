# Quick Start Guide

Follow these steps to get your Telegram message forwarder up and running:

## Step 1: Get API Credentials (5 minutes)

1. Open your browser and go to: **https://my.telegram.org**
2. Log in with your phone number (the same one you use for Telegram)
3. Click on **"API development tools"**
4. If you haven't created an app before:
   - Fill in the form:
     - App title: `Message Forwarder` (or any name you like)
     - Short name: `forwarder` (or any short name)
     - Platform: Choose any (e.g., Desktop)
   - Click **Create application**
5. You'll see your credentials:
   - **api_id**: A number (e.g., 12345678)
   - **api_hash**: A string (e.g., 0123456789abcdef0123456789abcdef)
6. **Keep this page open** - you'll need these values in the next step

## Step 2: Install Dependencies (2 minutes)

Open your terminal/command prompt in the `Movie_forward` folder and run:

```bash
pip install -r requirements.txt
```

Wait for the installation to complete.

## Step 3: Configure the Bot (2 minutes)

1. In the `Movie_forward` folder, copy the example config:
   ```bash
   copy config.example.py config.py
   ```

2. Open `config.py` in any text editor (Notepad, VS Code, etc.)

3. Replace these two lines:
   ```python
   API_ID = "YOUR_API_ID"      # Replace with the api_id from Step 1
   API_HASH = "YOUR_API_HASH"  # Replace with the api_hash from Step 1
   ```
   
   Example:
   ```python
   API_ID = "12345678"
   API_HASH = "0123456789abcdef0123456789abcdef"
   ```

4. Save the file

## Step 4: Run the Bot (1 minute)

1. In your terminal, run:
   ```bash
   python bot.py
   ```

2. **First time only**: You'll be asked to log in:
   - Enter your phone number (with country code, e.g., `+1234567890`)
   - Enter the verification code sent to your Telegram app
   - If you have 2FA enabled, enter your password

3. Choose what you want to do:
   - Type `1` to forward all existing messages (one-time)
   - Type `2` to only forward new messages (continuous)
   - Type `3` to do both (recommended)

4. If you chose option 1 or 3:
   - Enter starting message ID (press Enter for `1`)
   - Enter ending message ID (press Enter to forward all)

5. The bot will start forwarding! You'll see logs like:
   ```
   Forwarded message 1 (1 total)
   Forwarded message 2 (2 total)
   ...
   ```

## Step 5: Monitor and Stop

- The bot will keep running and show you progress
- To stop the bot, press `Ctrl+C`
- You can run it again anytime with `python bot.py`

## Troubleshooting

### "Could not find the input entity for..."
**Solution**: Make sure you're a member of both channels. Join the destination channel using the invite link first.

### "No module named 'telethon'"
**Solution**: Run `pip install -r requirements.txt` again.

### "Invalid API_ID or API_HASH"
**Solution**: Double-check your credentials in `config.py`. Make sure API_ID is a number (no quotes) and API_HASH is a string (with quotes).

### "FloodWaitError"
**Solution**: You're sending too many messages. The bot will automatically wait. If it keeps happening, increase `DELAY_BETWEEN_FORWARDS` in `config.py`.

## What Happens Next?

- **Existing messages**: If you chose option 1 or 3, all messages from the source channel will be forwarded to the destination
- **New messages**: If you chose option 2 or 3, the bot will automatically forward any new messages posted in the source channel
- **Session file**: A `.session` file is created so you don't need to log in again next time

## Need Help?

- Check the full [README.md](README.md) for more details
- Make sure you have permission to access both channels
- Ensure your Telegram account is not restricted

---

**That's it! Your message forwarder is now running! 🎉**
