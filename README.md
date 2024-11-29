# Telegram File Downloader Bot

A Telegram bot built using [Aiogram](https://docs.aiogram.dev/en/latest/) that downloads files from user-provided URLs and sends them back to the user by uploading them to the Telegram cloud.

## Features

- Accepts URLs for files directly from users.  
- Downloads the specified file to the server.  
- Uploads the downloaded file to the Telegram cloud.  
- Simple and efficient file sharing solution using Telegram.  

## Prerequisites

To use this bot, you must set up your own local Telegram Bot API server. Follow the official instructions here: [Telegram Bot API Server](https://github.com/tdlib/telegram-bot-api).

### Requirements

- **Python 3.7+**
- Installed and configured **Telegram Bot API Server**
- The following Python libraries:
  - `aiogram`
  - `requests`

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/qwerty2053/fileDL_robot.git
   cd fileDL_robot
   ```

2. Install dependencies:

   ```bash
   pip install requests aiogram
   ```

3. Set up and run the Telegram Bot API server:
   - Follow the instructions in the [Telegram Bot API Server repository](https://github.com/tdlib/telegram-bot-api).
   - Once configured, start the server.

4. Insert your Telegram Bot token in the code (TOKEN variable, however this method is unsafe)

5. Run the bot:

   ```bash
   python fileDL_robot.py
   ```

## Usage

1. Start the bot in Telegram by sending the `/start` command.  
2. Send the bot a valid URL to a file (e.g., a direct download link).  
3. The bot will:
   - Download the file from the provided URL.
   - Send the file back to you via Telegram.

## Limitations

- The bot relies on your local Telegram Bot API server. Ensure it is properly configured and running.  
- Download and upload speed depends on the server's internet connection and resources.  
- Only direct URLs are supported (e.g., links that point directly to a file).  

## Technologies Used

- **Python**  
- **Aiogram**: For Telegram Bot API integration.  
- **Requests**: For handling HTTP requests and file downloads.  
- **Telegram Bot API Server**: Local server for handling bot interactions.  