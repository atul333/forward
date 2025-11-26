import asyncio
from telethon import TelegramClient
import logging
from config import API_ID, API_HASH, SOURCE_CHANNEL_ID, SESSION_NAME

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def check_channel_messages():
    """Check what messages exist in the source channel"""
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    
    try:
        await client.start()
        logger.info("Client started successfully!")
        
        # Get source channel
        source_channel = await client.get_entity(SOURCE_CHANNEL_ID)
        logger.info(f"Source channel: {source_channel.title}")
        
        # Get channel info
        logger.info("\n" + "=" * 70)
        logger.info("📊 CHANNEL MESSAGE INFORMATION")
        logger.info("=" * 70)
        
        # Get the latest message
        latest_messages = await client.get_messages(source_channel, limit=1)
        if latest_messages:
            latest_msg = latest_messages[0]
            logger.info(f"📈 Latest message ID: {latest_msg.id}")
            logger.info(f"📅 Latest message date: {latest_msg.date}")
        else:
            logger.warning("⚠️  No messages found in the channel!")
            return
        
        # Get the first few messages
        logger.info("\n" + "-" * 70)
        logger.info("First 5 messages in the channel:")
        logger.info("-" * 70)
        
        first_messages = await client.get_messages(source_channel, limit=5, reverse=True)
        for msg in first_messages:
            msg_type = "Text" if msg.text else "Media" if msg.media else "Other"
            logger.info(f"  ID: {msg.id:6d} | Date: {msg.date} | Type: {msg_type}")
        
        # Get the last few messages
        logger.info("\n" + "-" * 70)
        logger.info("Last 5 messages in the channel:")
        logger.info("-" * 70)
        
        last_messages = await client.get_messages(source_channel, limit=5)
        for msg in last_messages:
            msg_type = "Text" if msg.text else "Media" if msg.media else "Other"
            logger.info(f"  ID: {msg.id:6d} | Date: {msg.date} | Type: {msg_type}")
        
        # Count total messages (approximate)
        logger.info("\n" + "-" * 70)
        logger.info("📊 Message Statistics:")
        logger.info("-" * 70)
        
        # Get total count by iterating (this might take a while for large channels)
        logger.info("Counting total messages (this may take a moment)...")
        total_count = 0
        async for message in client.iter_messages(source_channel):
            total_count += 1
            if total_count % 100 == 0:
                logger.info(f"  Counted {total_count} messages so far...")
        
        logger.info(f"\n✅ Total messages in channel: {total_count}")
        logger.info(f"📍 Message ID range: {first_messages[0].id if first_messages else 'N/A'} to {latest_msg.id}")
        
        logger.info("\n" + "=" * 70)
        logger.info("💡 TIP: Use these message IDs when forwarding:")
        logger.info(f"   - To forward ALL messages: start_id=1 (or {first_messages[0].id if first_messages else 1})")
        logger.info(f"   - To forward recent messages: start_id={latest_msg.id - 100} to end_id={latest_msg.id}")
        logger.info("=" * 70 + "\n")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await client.disconnect()
        logger.info("Disconnected!")

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🔍 TELEGRAM CHANNEL MESSAGE CHECKER")
    print("=" * 70)
    print("This script will check what messages exist in your source channel")
    print("and help you determine the correct message ID range to use.")
    print("=" * 70 + "\n")
    
    try:
        asyncio.run(check_channel_messages())
    except KeyboardInterrupt:
        logger.info("\nStopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
