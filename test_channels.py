import asyncio
from telethon import TelegramClient
import logging
from config import API_ID, API_HASH, SOURCE_CHANNEL_ID, DESTINATION_CHANNEL, SESSION_NAME

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def test_channels():
    """Test if both source and destination channels are accessible"""
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    
    try:
        await client.start()
        logger.info("Client started successfully!")
        
        print("\n" + "=" * 70)
        print("TESTING CHANNEL CONFIGURATION")
        print("=" * 70)
        print()
        
        # Test source channel
        try:
            source = await client.get_entity(SOURCE_CHANNEL_ID)
            print(f"[OK] Source Channel:")
            print(f"     Name: {source.title}")
            print(f"     ID: {source.id}")
            print(f"     Type: {'Private' if source.username is None else 'Public'}")
            if source.username:
                print(f"     Username: @{source.username}")
            print()
        except Exception as e:
            print(f"[ERROR] Could not access source channel: {e}")
            print()
        
        # Test destination channel
        try:
            destination = await client.get_entity(DESTINATION_CHANNEL)
            print(f"[OK] Destination Channel:")
            print(f"     Name: {destination.title}")
            print(f"     ID: {destination.id}")
            print(f"     Type: {'Private' if destination.username is None else 'Public'}")
            if destination.username:
                print(f"     Username: @{destination.username}")
            print()
            
            # Check if we can post
            try:
                me = await client.get_me()
                participant = await client.get_permissions(destination, me)
                can_post = participant.is_admin or participant.post_messages
                print(f"     Posting Permission: {'YES' if can_post else 'NO'}")
                if not can_post:
                    print(f"     [WARNING] You may not have permission to post in this channel!")
            except Exception as perm_error:
                print(f"     [WARNING] Could not check permissions: {perm_error}")
            print()
            
        except Exception as e:
            print(f"[ERROR] Could not access destination channel: {e}")
            print(f"[TIP] Make sure you have joined the channel and have posting permissions")
            print()
        
        print("=" * 70)
        print("Configuration test complete!")
        print("=" * 70)
        print()
        
    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await client.disconnect()
        logger.info("Disconnected!")

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("CHANNEL CONFIGURATION TEST")
    print("=" * 70)
    print("This script will verify your source and destination channels")
    print("are properly configured and accessible.")
    print("=" * 70 + "\n")
    
    try:
        asyncio.run(test_channels())
    except KeyboardInterrupt:
        logger.info("\nStopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
