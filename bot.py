import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import InputChannel
import logging
from config import (
    API_ID, 
    API_HASH, 
    SOURCE_CHANNEL_ID, 
    DESTINATION_CHANNEL, 
    SESSION_NAME,
    DELAY_BETWEEN_FORWARDS
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class MessageForwarder:
    def __init__(self):
        self.client = None
        self.source_channel = None
        self.destination_channel = None
        
    async def start(self):
        """Initialize and start the bot"""
        # Create client using your account (not bot account)
        self.client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
        
        await self.client.start()
        logger.info("Client started successfully!")
        
        # Get the channels
        try:
            # Get source channel
            self.source_channel = await self.client.get_entity(SOURCE_CHANNEL_ID)
            logger.info(f"Source channel found: {self.source_channel.title}")
            
            # Get destination channel - handle invite links
            try:
                # If it's an invite link (contains +), we need to join first
                if '+' in DESTINATION_CHANNEL or 'joinchat' in DESTINATION_CHANNEL:
                    logger.info("Destination is an invite link, attempting to join...")
                    # Extract the hash from the invite link
                    invite_hash = DESTINATION_CHANNEL.split('+')[-1].split('/')[-1]
                    
                    # Try to join the channel using the invite link
                    try:
                        from telethon.tl.functions.messages import ImportChatInviteRequest
                        updates = await self.client(ImportChatInviteRequest(invite_hash))
                        # Get the channel from the updates
                        if hasattr(updates, 'chats') and updates.chats:
                            self.destination_channel = updates.chats[0]
                            logger.info(f"Joined and found destination channel: {self.destination_channel.title}")
                        else:
                            logger.error("Could not get channel info after joining")
                            raise Exception("Failed to get channel after joining")
                    except Exception as join_error:
                        # Maybe already a member, try to get entity directly
                        logger.info(f"Join attempt failed (might already be a member): {join_error}")
                        logger.info("Trying to get channel entity directly...")
                        # Try with the full link
                        self.destination_channel = await self.client.get_entity(DESTINATION_CHANNEL)
                        logger.info(f"Destination channel found: {self.destination_channel.title}")
                else:
                    # Regular channel username or ID
                    logger.info(f"Getting destination channel: {DESTINATION_CHANNEL}")
                    self.destination_channel = await self.client.get_entity(DESTINATION_CHANNEL)
                    logger.info(f"Destination channel found: {self.destination_channel.title}")
                    
            except Exception as dest_error:
                logger.error(f"Error getting destination channel: {dest_error}")
                logger.error("Please make sure:")
                logger.error("1. You have joined the destination channel")
                logger.error("2. The channel username/link is correct in config.py")
                logger.error("3. You have permission to post in the channel")
                raise
            
            # Validate both channels are set
            if self.source_channel is None or self.destination_channel is None:
                logger.error("Failed to initialize channels!")
                logger.error(f"Source channel: {self.source_channel}")
                logger.error(f"Destination channel: {self.destination_channel}")
                raise Exception("Channel initialization failed")
            
            logger.info("✓ Both channels initialized successfully!")
            
        except Exception as e:
            logger.error(f"Error getting channels: {e}")
            raise
    
    def setup_listener(self):
        """Setup event listener for new messages"""
        # Start listening for new messages
        @self.client.on(events.NewMessage(chats=self.source_channel))
        async def handler(event):
            try:
                logger.info(f"New message received: {event.message.id}")
                # Forward the message to destination channel
                await self.client.forward_messages(
                    self.destination_channel,
                    event.message
                )
                logger.info(f"Message {event.message.id} forwarded successfully!")
            except Exception as e:
                logger.error(f"Error forwarding message: {e}")
        
        logger.info("Bot is now running and listening for new messages...")
        logger.info("Press Ctrl+C to stop")
    
    async def forward_existing_messages(self, start_id=1, end_id=None, limit=None):
        """Forward existing messages from source to destination"""
        try:
            # Validate channels are initialized
            if self.source_channel is None or self.destination_channel is None:
                logger.error("Channels not initialized! Cannot forward messages.")
                logger.error(f"Source: {self.source_channel}, Destination: {self.destination_channel}")
                return
            
            logger.info("Starting to forward existing messages...")
            logger.info(f"Source: {self.source_channel.title}")
            logger.info(f"Destination: {self.destination_channel.title}")
            
            messages_forwarded = 0
            
            # Build parameters for iter_messages
            iter_params = {
                'limit': limit
            }
            
            # Set up the ID range for iteration
            if end_id is not None:
                # If end_id is specified, iterate from end_id down to start_id
                iter_params['max_id'] = end_id
                iter_params['min_id'] = start_id - 1
            else:
                # If no end_id, start from start_id and go backwards (to older messages)
                # We use offset_id to start from start_id
                iter_params['offset_id'] = start_id
                iter_params['min_id'] = 0  # Go all the way to the beginning
            
            # Get messages from source channel
            async for message in self.client.iter_messages(
                self.source_channel,
                **iter_params
            ):
                try:
                    # Forward message to destination
                    await self.client.forward_messages(
                        self.destination_channel,
                        message
                    )
                    messages_forwarded += 1
                    logger.info(f"Forwarded message {message.id} ({messages_forwarded} total)")
                    
                    # Add a small delay to avoid rate limiting
                    await asyncio.sleep(DELAY_BETWEEN_FORWARDS)
                    
                except Exception as e:
                    logger.error(f"Error forwarding message {message.id}: {e}")
                    continue
            
            logger.info(f"Finished! Total messages forwarded: {messages_forwarded}")
            
        except Exception as e:
            logger.error(f"Error in forward_existing_messages: {e}")

async def main():
    forwarder = MessageForwarder()
    
    print("=" * 60)
    print("Telegram Message Forwarder Bot")
    print("=" * 60)
    print("\nOptions:")
    print("1. Forward existing messages (one-time)")
    print("2. Start bot to forward new messages (continuous)")
    print("3. Both (forward existing + listen for new)")
    print("=" * 60)
    
    choice = input("\nEnter your choice (1/2/3): ").strip()
    
    # Initialize the bot
    await forwarder.start()
    
    if choice == "1":
        # Forward existing messages only
        start_msg = input("Enter starting message ID (default: 1): ").strip()
        start_id = int(start_msg) if start_msg else 1
        
        end_msg = input("Enter ending message ID (press Enter for all): ").strip()
        end_id = int(end_msg) if end_msg else None
        
        await forwarder.forward_existing_messages(start_id=start_id, end_id=end_id)
        
        # Disconnect after forwarding
        await forwarder.client.disconnect()
        logger.info("Forwarding complete! Bot disconnected.")
        
    elif choice == "2":
        # Just listen for new messages
        logger.info("Listening for new messages only...")
        forwarder.setup_listener()
        await forwarder.client.run_until_disconnected()
        
    elif choice == "3":
        # Forward existing messages first, then listen for new ones
        start_msg = input("Enter starting message ID (default: 1): ").strip()
        start_id = int(start_msg) if start_msg else 1
        
        end_msg = input("Enter ending message ID (press Enter for all): ").strip()
        end_id = int(end_msg) if end_msg else None
        
        await forwarder.forward_existing_messages(start_id=start_id, end_id=end_id)
        
        logger.info("Now listening for new messages...")
        forwarder.setup_listener()
        await forwarder.client.run_until_disconnected()
    else:
        logger.error("Invalid choice!")
        await forwarder.client.disconnect()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\nBot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
