# 🤖 Telegram Message Forwarder Bot

## 📋 What You Have

Your Telegram message forwarder bot is ready! Here's what has been created:

### ✅ Files Created

1. **bot.py** - Main bot script that handles message forwarding
2. **config.py** - Configuration file (you need to add your API credentials here)
3. **config.example.py** - Template configuration file
4. **requirements.txt** - Python dependencies (already installed ✓)
5. **README.md** - Detailed documentation
6. **QUICKSTART.md** - Step-by-step setup guide
7. **start.bat** - Windows script to easily start the bot
8. **.gitignore** - Protects your sensitive files

### 🎯 What It Does

- ✅ Forwards messages from source channel to destination channel
- ✅ Can forward existing messages (one-time)
- ✅ Can forward new messages automatically (continuous)
- ✅ Supports all message types (text, images, videos, files, etc.)
- ✅ Includes rate limiting protection
- ✅ Detailed logging

### 📊 Your Configuration

**Source Channel**: `https://t.me/c/2515799124/`
**Destination Channel**: `https://t.me/+qUTXDWTxJh42ODhl`
**Bot Token**: `8084457483:AAEHgETP6tVbqnTWBgHG_KEjtMDe1oINVFo`

---

## 🚀 Next Steps (IMPORTANT!)

### Step 1: Get API Credentials ⚠️

You **MUST** get your Telegram API credentials before the bot will work:

1. Go to: **https://my.telegram.org**
2. Log in with your phone number
3. Click "API development tools"
4. Create an application (any name is fine)
5. Copy your **api_id** and **api_hash**

### Step 2: Configure the Bot

1. Open `config.py` in a text editor
2. Replace these lines:
   ```python
   API_ID = "YOUR_API_ID"      # Put your api_id here
   API_HASH = "YOUR_API_HASH"  # Put your api_hash here
   ```

### Step 3: Run the Bot

**Option A - Easy Way (Recommended)**:
- Double-click `start.bat`

**Option B - Manual Way**:
- Open terminal in this folder
- Run: `python bot.py`

### Step 4: First Time Setup

When you run the bot for the first time:
1. Enter your phone number (with country code, e.g., +1234567890)
2. Enter the verification code from Telegram
3. If you have 2FA, enter your password

### Step 5: Choose Mode

The bot will ask what you want to do:
- **Option 1**: Forward all existing messages (one-time)
- **Option 2**: Only forward new messages (continuous)
- **Option 3**: Both (recommended)

---

## 📖 Documentation

- **Quick Start**: Read `QUICKSTART.md` for detailed step-by-step instructions
- **Full Docs**: Read `README.md` for complete documentation
- **Help**: Check the troubleshooting section in README.md

---

## ⚠️ Important Notes

1. **Security**: Never share your `config.py` or `.session` files
2. **Permissions**: Make sure you're a member of both channels
3. **Rate Limits**: The bot includes delays to avoid Telegram rate limits
4. **Account**: The bot uses YOUR Telegram account (not the bot token)

---

## 🎉 You're All Set!

Once you add your API credentials to `config.py`, you can start the bot and it will begin forwarding messages!

**Need help?** Check the QUICKSTART.md or README.md files for detailed instructions.
