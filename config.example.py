# Telegram API Configuration
# Get these from https://my.telegram.org

# Your Telegram API credentials
API_ID = "38483384"  # Replace with your API ID (numeric)
API_HASH = "8a236f58a79e1c6c70229e742ce88808"  # Replace with your API hash (string)

# Bot Token (not used for forwarding, but kept for reference)
BOT_TOKEN = "8084457483:AAEHgETP6tVbqnTWBgHG_KEjtMDe1oINVFo"

# Channel Configuration
SOURCE_CHANNEL_ID = -1002515799124  # Source channel ID (private channel with -100 prefix)
DESTINATION_CHANNEL = "movie_forward"  # Destination channel username

# Session name (will create a .session file with this name)
SESSION_NAME = "movie_forwarder"

# Forwarding settings
DELAY_BETWEEN_FORWARDS = 1  # Seconds to wait between forwarding messages (to avoid rate limits)
