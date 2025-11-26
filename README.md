# Telegram Message Forwarder Bot

This bot forwards messages from a source Telegram channel to a destination channel using your logged-in Telegram account.

## Features

- ✅ Forward existing messages from source to destination
- ✅ Automatically forward new messages in real-time
- ✅ Support for all message types (text, media, files, etc.)
- ✅ Rate limiting protection
- ✅ Detailed logging

## Setup Instructions

### 1. Get API Credentials

You need to get your Telegram API credentials:

1. Go to https://my.telegram.org
2. Log in with your phone number
3. Click on "API development tools"
4. Create a new application (if you haven't already)
5. Copy your `API ID` and `API Hash`

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the Bot

1. Copy the example configuration file:
   ```bash
   copy config.example.py config.py
   ```

2. Open `config.py` and update the following values:
   ```python
   API_ID = "YOUR_API_ID"  # Replace with your API ID from step 1
   API_HASH = "YOUR_API_HASH"  # Replace with your API hash from step 1
   ```

The source and destination channels are already configured in `config.py`:
- **Source Channel**: `2515799124`
- **Destination Channel**: `https://t.me/+qUTXDWTxJh42ODhl`

You can modify these if needed.

### 4. Run the Bot

```bash
python bot.py
```

On first run, you'll be asked to:
1. Enter your phone number (with country code, e.g., +1234567890)
2. Enter the verification code sent to your Telegram account
3. If you have 2FA enabled, enter your password

This will create a session file (`session_name.session`) so you won't need to log in again.

### 5. Choose Operation Mode

The bot will present you with 3 options:

1. **Forward existing messages (one-time)**: Forwards all existing messages from the source channel
2. **Start bot to forward new messages (continuous)**: Only forwards new messages that arrive
3. **Both**: Forwards existing messages first, then continues to forward new messages

## Usage Examples

### Forward all existing messages
```
Enter your choice (1/2/3): 1
Enter starting message ID (default: 1): 1
Enter ending message ID (press Enter for all): [Press Enter]
```

### Forward messages from ID 100 onwards
```
Enter your choice (1/2/3): 1
Enter starting message ID (default: 1): 100
Enter ending message ID (press Enter for all): [Press Enter]
```

### Only forward new messages
```
Enter your choice (1/2/3): 2
```

### Forward all existing + new messages
```
Enter your choice (1/2/3): 3
Enter starting message ID (default: 1): 1
Enter ending message ID (press Enter for all): [Press Enter]
```

## Important Notes

- ⚠️ Keep your API credentials and session file secure
- ⚠️ The bot uses your personal Telegram account, not the bot token
- ⚠️ Make sure you have permission to forward messages from the source channel
- ⚠️ The bot includes a 1-second delay between forwards to avoid rate limiting
- ⚠️ Press `Ctrl+C` to stop the bot

## Troubleshooting

### "Could not find the input entity"
- Make sure you're a member of both channels
- For the destination channel, join using the invite link first

### "FloodWaitError"
- You're sending messages too fast
- The bot will automatically wait and retry
- Consider increasing the delay in the code

### Session file issues
- Delete `session_name.session` and log in again
- Make sure you're using the correct phone number

## File Structure

```
Movie_forward/
├── bot.py                  # Main bot script
├── config.py              # Your configuration (create from config.example.py)
├── config.example.py      # Example configuration file
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore            # Git ignore file
└── movie_forwarder.session  # Created after first login (don't share this!)
```

## Support

For issues with the Telegram Bot API, see: https://core.telegram.org/bots/api
