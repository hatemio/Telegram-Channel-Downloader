Telegram Channel Content Downloader

📌 Overview

This script allows you to download and organize content from a Telegram channel within a specified time range. The content includes text, images, videos, and other media. It can also run continuously to monitor and download new posts automatically.

✨ Features:

Filter by Date Range: Specify a start and end date/time to download posts within that period.

Continuous Monitoring: Leave the end date blank to keep downloading new posts as they appear.

Organized Storage: Each post is stored in its own separate folder.

Handles Multiple Media Files: All related files (images, videos, etc.) of a post are saved together.

Preserves Original Order: Posts are downloaded in chronological order.

Saves Text Posts: Text-based posts are saved as .txt files.

📋 Prerequisites

Before running the script, ensure you have the following:

🛠 Required Installations

Install Telethon and pytz by running:

pip install telethon pytz

🔑 Telegram API Credentials

Get API Credentials:

Go to my.telegram.org.

Log in with your Telegram account.

Under API Development Tools, create a new application.

Note down your api_id and api_hash.

Configure the Script:

Replace the placeholder values in the script with your api_id and api_hash.

📡 Channel Access

Public Channels: You can fetch posts using the channel username.

Private Channels: You must be a member. The script uses the channel username or ID.

🚀 How It Works

🔹 User Input

The script prompts you to enter:

Channel username (e.g., @channelname)

Start date (format: YYYY-MM-DD HH:MM:SS)

End date (same format or press Enter for continuous monitoring)

Check interval (in seconds, for continuous monitoring)

Example input:

Enter channel username (e.g., @channelname): @examplechannel
Enter start date (YYYY-MM-DD HH:MM:SS): 2023-10-01 00:00:00
Enter end date (YYYY-MM-DD HH:MM:SS, or press Enter for ongoing): [Enter]
Enter check interval in seconds (e.g., 60): 60

🔹 Authentication

On the first run, it asks for your phone number and a verification code from Telegram.

It saves a session file (session_name.session) to avoid repeated logins.

🔹 Fetching Messages

Messages are fetched in chronological order.

Filters apply to only include messages within the specified time range.

🔹 Handling Media Groups

Telegram treats multiple media files in a post as separate messages with the same grouped_id.

The script detects and saves them together in the same folder.

🔹 Organizing Downloaded Content

Each post is stored in a separate folder, named like:

post_001/
    ├── text.txt   # (If text content exists)
    ├── media_1.jpg
    ├── media_2.mp4

🔹 Saving Files

Text posts → Saved as text.txt (UTF-8 encoded)

Media files → Named as media_X.ext (where .ext matches the file type, e.g., .jpg, .mp4)

Uses message.download_media() to preserve the original format.

🔹 Continuous Monitoring (If Enabled)

Starting monitoring from post_254, last message ID: 12345
Checking for new posts at 2023-10-02 10:00:00+00:00...
Downloaded single post_254
Checking for new posts at 2023-10-02 10:01:00+00:00...
No new posts found.

🛠 Future Enhancements

Support for other file types (documents, audio, etc.)

Better error handling for connection issues

Option to filter messages by keywords

📌 Conclusion

This script is a powerful tool for downloading and organizing Telegram channel content. It allows flexible date filtering, automated monitoring, and structured storage of posts with media and text.

🚀 Start using it today to automate your Telegram content downloads! 🚀
