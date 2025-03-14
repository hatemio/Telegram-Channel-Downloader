import os
import asyncio
from datetime import datetime
from telethon import TelegramClient
import pytz

# Replace these with your own Telegram API credentials
api_id = 12345  # Your API ID
api_hash = 'your_api_hash'  # Your API Hash

# Initialize the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# File to store the last processed message ID
LAST_MESSAGE_FILE = 'last_message_id.txt'

async def process_group(group, post_num):
    """Process a group of messages (e.g., an album) and save content in a folder."""
    folder = f"post_{post_num:03d}"
    os.makedirs(folder, exist_ok=True)
    text = next((m.text for m in group if m.text), None)
    if text:
        with open(os.path.join(folder, "text.txt"), "w", encoding="utf-8") as f:
            f.write(text)
    media_num = 1
    for message in group:
        if message.media:
            file_path = os.path.join(folder, f"media_{media_num}")
            await message.download_media(file=file_path)
            media_num += 1
    return group[-1].id  # Return the highest message ID in the group

async def process_single_message(message, post_num):
    """Process a single message and save its content in a folder."""
    folder = f"post_{post_num:03d}"
    os.makedirs(folder, exist_ok=True)
    if message.text:
        with open(os.path.join(folder, "text.txt"), "w", encoding="utf-8") as f:
            f.write(message.text)
    if message.media:
        file_path = os.path.join(folder, "media_1")
        await message.download_media(file=file_path)
    return message.id  # Return the message ID

def get_last_post_num():
    """Determine the last post number from existing folders."""
    existing_folders = [d for d in os.listdir() if d.startswith("post_") and os.path.isdir(d)]
    if not existing_folders:
        return 0
    numbers = [int(f.split('_')[1]) for f in existing_folders]
    return max(numbers)

def get_last_message_id():
    """Read the last processed message ID from file, or return 0 if not found."""
    if os.path.exists(LAST_MESSAGE_FILE):
        with open(LAST_MESSAGE_FILE, 'r') as f:
            return int(f.read().strip())
    return 0

def save_last_message_id(message_id):
    """Save the last processed message ID to file."""
    with open(LAST_MESSAGE_FILE, 'w') as f:
        f.write(str(message_id))

async def monitor_channel(channel_username, start_date_str, end_date_str=None, check_interval=60):
    """Monitor the channel for new posts and download them incrementally."""
    # Define UTC timezone
    utc = pytz.UTC

    # Parse start date into a UTC-aware datetime object
    start_date_naive = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")
    start_date = utc.localize(start_date_naive)

    # Parse end date if provided, otherwise keep it None for ongoing monitoring
    end_date = None
    if end_date_str:
        end_date_naive = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M:%S")
        end_date = utc.localize(end_date_naive)

    # Get the channel entity
    channel = await client.get_entity(channel_username)

    # Initialize starting points
    post_num = get_last_post_num() + 1  # e.g., 254 if post_253 exists
    last_message_id = get_last_message_id()  # From file or 0 if first run
    current_group = []

    print(f"Starting monitoring from post_{post_num:03d}, last message ID: {last_message_id}")

    while True:
        print(f"Checking for new posts at {datetime.now(utc)}...")
        new_posts_found = False
        async for message in client.iter_messages(channel, min_id=last_message_id, reverse=True):
            # Skip messages before the start date
            if message.date < start_date:
                continue
            # Stop if beyond end date (if specified)
            if end_date and message.date > end_date:
                break

            new_posts_found = True
            # Handle grouped media (albums)
            if message.grouped_id is not None:
                if current_group and current_group[0].grouped_id == message.grouped_id:
                    current_group.append(message)
                else:
                    if current_group:
                        last_message_id = await process_group(current_group, post_num)
                        save_last_message_id(last_message_id)
                        print(f"Downloaded group post_{post_num:03d}")
                        post_num += 1
                    current_group = [message]
            # Handle single messages
            else:
                if current_group:
                    last_message_id = await process_group(current_group, post_num)
                    save_last_message_id(last_message_id)
                    print(f"Downloaded group post_{post_num:03d}")
                    post_num += 1
                current_group = []
                last_message_id = await process_single_message(message, post_num)
                save_last_message_id(last_message_id)
                print(f"Downloaded single post_{post_num:03d}")
                post_num += 1

        # Process any remaining group
        if current_group:
            last_message_id = await process_group(current_group, post_num)
            save_last_message_id(last_message_id)
            print(f"Downloaded group post_{post_num:03d}")
            post_num += 1
            current_group = []

        if not new_posts_found:
            print("No new posts found.")

        # Wait before the next check
        await asyncio.sleep(check_interval)

async def main():
    """Main function to start the monitoring process."""
    channel_username = input("Enter channel username (e.g., @channelname): ")
    start_date_str = input("Enter start date (YYYY-MM-DD HH:MM:SS): ")
    end_date_str = input("Enter end date (YYYY-MM-DD HH:MM:SS, or press Enter for ongoing): ") or None
    check_interval = int(input("Enter check interval in seconds (e.g., 60): ") or 60)

    await monitor_channel(channel_username, start_date_str, end_date_str, check_interval)

# Run the script
if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
