import asyncio
from telethon import TelegramClient
import logging
from config import API_ID, API_HASH, SOURCE_CHANNEL_ID, DESTINATION_CHANNEL, SESSION_NAME

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def test_config():
    """Test if the configuration is correct"""
    print("=" * 60)
    print("Configuration Test")
    print("=" * 60)
    print(f"\nAPI_ID: {API_ID}")
    print(f"API_HASH: {API_HASH[:10]}... (hidden)")
    print(f"SOURCE_CHANNEL_ID: {SOURCE_CHANNEL_ID}")
    print(f"DESTINATION_CHANNEL: {DESTINATION_CHANNEL}")
    print(f"SESSION_NAME: {SESSION_NAME}")
    print("=" * 60)
    
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    
    try:
        await client.start()
        logger.info("✓ Successfully connected to Telegram!")
        
        # Test source channel
        try:
            source = await client.get_entity(SOURCE_CHANNEL_ID)
            logger.info(f"✓ Source channel found: {source.title}")
            logger.info(f"  - ID: {source.id}")
            logger.info(f"  - Username: @{source.username if hasattr(source, 'username') and source.username else 'N/A'}")
        except Exception as e:
            logger.error(f"✗ Error getting source channel: {e}")
            return
        
        # Test destination channel
        try:
            logger.info(f"\nTrying to get destination channel: {DESTINATION_CHANNEL}")
            dest = await client.get_entity(DESTINATION_CHANNEL)
            logger.info(f"✓ Destination channel found: {dest.title}")
            logger.info(f"  - ID: {dest.id}")
            logger.info(f"  - Username: @{dest.username if hasattr(dest, 'username') and dest.username else 'N/A'}")
            
            # Check if we can post
            logger.info("\n✓ All checks passed! Bot should work correctly.")
            
        except Exception as e:
            logger.error(f"✗ Error getting destination channel: {e}")
            logger.error("\nPossible solutions:")
            logger.error("1. Make sure you've joined the destination channel")
            logger.error("2. Check if the channel username/link is correct")
            logger.error("3. Try using just the username without 'https://t.me/'")
            logger.error(f"   Example: DESTINATION_CHANNEL = 'movie_forward'")
            return
            
    except Exception as e:
        logger.error(f"✗ Connection error: {e}")
    finally:
        await client.disconnect()
        logger.info("\nTest completed!")

if __name__ == '__main__':
    asyncio.run(test_config())
