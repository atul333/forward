import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import InputChannel
from telethon.errors import FloodWaitError
import logging
from datetime import datetime, timedelta
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
            
            # Get destination channel - handle invite links, usernames, or IDs
            try:
                # Check if DESTINATION_CHANNEL is a string (username or invite link) or integer (channel ID)
                if isinstance(DESTINATION_CHANNEL, str) and ('+' in DESTINATION_CHANNEL or 'joinchat' in DESTINATION_CHANNEL):
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
                    # Regular channel username (string) or ID (integer)
                    dest_type = "ID" if isinstance(DESTINATION_CHANNEL, int) else "username"
                    logger.info(f"Getting destination channel by {dest_type}: {DESTINATION_CHANNEL}")
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
            except FloodWaitError as e:
                wait_seconds = e.seconds + 60
                wait_minutes = wait_seconds / 60
                resume_time = datetime.now() + timedelta(seconds=wait_seconds)
                
                logger.warning("=" * 70)
                logger.warning(f"⚠️  FLOOD WAIT ERROR on new message {event.message.id}")
                logger.warning(f"Required wait: {e.seconds} seconds ({e.seconds/60:.1f} minutes)")
                logger.warning(f"Actual wait (with buffer): {wait_seconds} seconds ({wait_minutes:.1f} minutes)")
                logger.warning(f"Resume time: {resume_time.strftime('%Y-%m-%d %H:%M:%S')}")
                logger.warning("=" * 70)
                
                logger.info(f"Waiting for {wait_minutes:.1f} minutes...")
                await asyncio.sleep(wait_seconds)
                
                # Retry forwarding
                try:
                    await self.client.forward_messages(
                        self.destination_channel,
                        event.message
                    )
                    logger.info(f"✓ Message {event.message.id} forwarded successfully after wait!")
                except Exception as retry_error:
                    logger.error(f"Failed to forward message {event.message.id} after wait: {retry_error}")
            except Exception as e:
                logger.error(f"Error forwarding message: {e}")
        
        logger.info("Bot is now running and listening for new messages...")
        logger.info("Press Ctrl+C to stop")
    
    async def forward_existing_messages(self, start_id=1, end_id=None, limit=None):
        """Forward existing messages from source to destination with flood wait handling"""
        try:
            # Validate channels are initialized
            if self.source_channel is None or self.destination_channel is None:
                logger.error("Channels not initialized! Cannot forward messages.")
                logger.error(f"Source: {self.source_channel}, Destination: {self.destination_channel}")
                return
            
            logger.info("Starting to forward existing messages in batches of 100...")
            logger.info(f"Source: {self.source_channel.title}")
            logger.info(f"Destination: {self.destination_channel.title}")
            logger.info("⏱️  Waiting 1 minute between each batch of 100 videos")
            
            # Statistics tracking
            start_time = datetime.now()
            messages_forwarded = 0
            messages_failed = 0
            flood_wait_count = 0
            last_successful_msg_id = None
            first_msg_id = None
            batch_count = 0
            
            # Build parameters for iter_messages
            # IMPORTANT: Explicitly set limit=None to override Telethon's default 100 message limit
            iter_params = {
                'reverse': True,  # Iterate from oldest to newest (chronological order)
                'limit': None if limit is None else limit  # None = unlimited, otherwise use provided limit
            }
            
            
            # IMPORTANT: Manual iteration to avoid Telethon's hidden limits
            # We'll fetch messages in batches and continue until we run out
            end_msg = f" to {end_id}" if end_id else " onwards"
            logger.info(f"Starting manual iteration from message ID {start_id}{end_msg}")
            
            current_offset_id = 0  # Start from the beginning
            batch_size = 100  # Fetch 100 messages at a time
            
            while True:
                # Fetch a batch of messages
                messages_batch = await self.client.get_messages(
                    self.source_channel,
                    limit=batch_size,
                    offset_id=current_offset_id,
                    reverse=True  # Get messages in chronological order
                )
                
                # If no more messages, we're done
                if not messages_batch:
                    logger.info("No more messages to process")
                    break
                
                batch_count += 1
                batch_forwarded = 0
                logger.info("")
                logger.info("=" * 70)
                logger.info(f"📦 BATCH #{batch_count} - Processing {len(messages_batch)} messages")
                logger.info("=" * 70)
                
                # Process each message in the batch
                for message in messages_batch:
                    # Update offset for next batch
                    current_offset_id = message.id
                    
                    # Skip messages before start_id
                    if message.id < start_id:
                        continue
                    
                    # Skip messages after end_id (if specified)
                    if end_id is not None and message.id > end_id:
                        logger.info(f"Reached end_id {end_id}, stopping")
                        break
    
                    # Track first message ID
                    if first_msg_id is None:
                        first_msg_id = message.id
                    
                    try:
                        # Forward message to destination
                        await self.client.forward_messages(
                            self.destination_channel,
                            message
                        )
                        messages_forwarded += 1
                        batch_forwarded += 1
                        last_successful_msg_id = message.id
                        logger.info(f"✓ Forwarded message {message.id} (Batch: {batch_forwarded}/{len(messages_batch)}, Total: {messages_forwarded})")
                        
                        # Add a small delay to avoid rate limiting
                        await asyncio.sleep(DELAY_BETWEEN_FORWARDS)
                        
                    except FloodWaitError as e:
                        flood_wait_count += 1
                        # Calculate wait time (add 60 seconds buffer for safety)
                        wait_seconds = e.seconds + 60
                        wait_minutes = wait_seconds / 60
                        
                        # Calculate resume time
                        resume_time = datetime.now() + timedelta(seconds=wait_seconds)
                        
                        logger.warning("=" * 70)
                        logger.warning(f"⚠️  FLOOD WAIT ERROR #{flood_wait_count} on message {message.id}")
                        logger.warning(f"Required wait: {e.seconds} seconds ({e.seconds/60:.1f} minutes)")
                        logger.warning(f"Actual wait (with buffer): {wait_seconds} seconds ({wait_minutes:.1f} minutes)")
                        logger.warning(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        logger.warning(f"Resume time: {resume_time.strftime('%Y-%m-%d %H:%M:%S')}")
                        logger.warning(f"Last successful message ID: {last_successful_msg_id}")
                        logger.warning(f"Will resume from message ID: {message.id}")
                        logger.warning("=" * 70)
                        
                        # Wait for the required time
                        logger.info(f"Waiting for {wait_minutes:.1f} minutes...")
                        await asyncio.sleep(wait_seconds)
                        
                        logger.info("Wait complete! Resuming forwarding...")
                        
                        # Retry forwarding this message
                        try:
                            await self.client.forward_messages(
                                self.destination_channel,
                                message
                            )
                            messages_forwarded += 1
                            batch_forwarded += 1
                            last_successful_msg_id = message.id
                            logger.info(f"✓ Successfully forwarded message {message.id} after wait")
                            
                            # Add delay after successful retry
                            await asyncio.sleep(DELAY_BETWEEN_FORWARDS)
                            
                        except Exception as retry_error:
                            messages_failed += 1
                            logger.error(f"Failed to forward message {message.id} even after waiting: {retry_error}")
                            continue
                        
                    except Exception as e:
                        messages_failed += 1
                        logger.error(f"Error forwarding message {message.id}: {e}")
                        continue
                
                # Batch complete - show summary and wait before next batch
                logger.info("")
                logger.info(f"✅ Batch #{batch_count} complete: {batch_forwarded} messages forwarded")
                
                # Check if we should continue (if there might be more messages)
                if len(messages_batch) == batch_size:
                    # Wait 1 minute before processing next batch
                    logger.info("⏱️  Waiting 60 seconds before next batch...")
                    logger.info("")
                    await asyncio.sleep(60)
                else:
                    # Last batch was smaller than batch_size, likely no more messages
                    logger.info("Last batch processed (fewer than 100 messages)")
                    break

            
            # Calculate statistics
            end_time = datetime.now()
            elapsed_time = end_time - start_time
            total_messages = messages_forwarded + messages_failed
            success_rate = (messages_forwarded / total_messages * 100) if total_messages > 0 else 0
            
            # Warn if no messages were found
            if total_messages == 0:
                logger.warning("")
                logger.warning("⚠️  No messages found to forward!")
                logger.warning("Possible reasons:")
                logger.warning(f"  1. The source channel has no messages in the specified range")
                logger.warning(f"  2. Starting message ID ({start_id}) might be higher than the latest message")
                logger.warning(f"  3. You might not have permission to read messages from the source channel")
                logger.warning("Tip: Try checking the source channel to see what message IDs exist")
                logger.warning("")
            
            
            # Display comprehensive summary
            logger.info("")
            logger.info("=" * 70)
            logger.info("📊 FORWARDING SUMMARY")
            logger.info("=" * 70)
            logger.info(f"📦 Total batches processed: {batch_count}")
            logger.info(f"✅ Successfully forwarded: {messages_forwarded} messages")
            logger.info(f"❌ Failed to forward: {messages_failed} messages")
            logger.info(f"📈 Total processed: {total_messages} messages")
            logger.info(f"🎯 Success rate: {success_rate:.1f}%")
            logger.info("-" * 70)
            logger.info(f"🔢 First message ID: {first_msg_id}")
            logger.info(f"🔢 Last message ID forwarded: {last_successful_msg_id}")
            logger.info("-" * 70)
            logger.info(f"⏱️  Time elapsed: {elapsed_time}")
            logger.info(f"⏸️  Flood wait occurrences: {flood_wait_count}")
            logger.info(f"📅 Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"📅 Finished: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info("=" * 70)
            logger.info("")
            
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
    
    choice = "1"
    
    # Initialize the bot
    await forwarder.start()
    
    if choice == "1":
        # Forward existing messages only
        
        start_id = 1
        
        
        end_id = None
        
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
