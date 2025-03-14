# Telegram-Channel-Downloader

This script that can download the content of a Telegram channel within a specified time range.
The content of the channel consists of posts that may contain text, videos, or photos.
The script Will:
Allow you to specify a start and end date/time to filter the posts to be downloaded. Or press enter to download from start date till the last one and keep it running to monitor whenever there is a new post it will download.
Organize the downloaded content into folders, where each post is saved in its own separate folder.
If a post contains multiple media files (such as multiple images or videos), all related files should be stored together in the same folder.
Save text-based posts as well in a structured format as a .txt file inside the corresponding folder.
Maintain the original order of posts.

Prerequisites
Before running the script, you need to:
Install Telethon:
Run the following command in your terminal to install the Telethon library:

pip install telethon pytz

Obtain Telegram API Credentials:
Go to my.telegram.org and log in with your Telegram account.

Under "API development tools," create a new application to get your api_id and api_hash.

Replace the placeholder values in the script with your own api_id and api_hash.

Channel Access:
Ensure you have access to the Telegram channel (public or private). For private channels, you need to be a member, and the script will use the channel username or ID.


How It Works
1. User Input
The script prompts you to enter:
Channel username: E.g., @channelname (include the @ symbol).

Start date: In the format YYYY-MM-DD HH:MM:SS (e.g., 2023-01-01 00:00:00).

End date: Same format as above.

Dates are parsed into datetime objects for comparison with message timestamps.

2. Authentication
The first time you run the script, it will ask for your phone number and a verification code sent by Telegram to log in. This creates a session file (session_name.session) for future runs.

3. Fetching Messages
Messages are fetched from the channel in chronological order (oldest to newest) using iter_messages with reverse=True.

Messages are filtered to include only those within the specified time range.

4. Handling Media Groups
Telegram treats multiple media files sent together (e.g., photo albums) as separate messages with the same grouped_id.

The script groups these messages together and processes them as a single post, ensuring all media files are saved in the same folder.

5. Organizing Content
Each post (single message or media group) gets its own folder named post_XXX, where XXX is a zero-padded number (e.g., post_001, post_002) that increments to maintain order.

Inside each folder:
Text: Saved as text.txt if the message contains text.

Media: Saved as media_1.ext, media_2.ext, etc., where the extension (e.g., .jpg, .mp4) is automatically added by Telethon based on the media type.

6. Saving Files
Text is written to text.txt with UTF-8 encoding to handle special characters and multiple lines.

Media files (photos, videos, etc.) are downloaded using message.download_media(), which preserves the appropriate file format.

Prompts:

Enter channel username (e.g., @channelname): @examplechannel
Enter start date (YYYY-MM-DD HH:MM:SS): 2023-10-01 00:00:00
Enter end date (YYYY-MM-DD HH:MM:SS, or press Enter for ongoing): [Enter]
Enter check interval in seconds (e.g., 60): 60

Starting monitoring from post_254, last message ID: 12345
Checking for new posts at 2023-10-02 10:00:00+00:00...
Downloaded single post_254
Checking for new posts at 2023-10-02 10:01:00+00:00...
No new posts found.
