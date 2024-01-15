from aiogram import Bot, Dispatcher, executor, types
from aiogram.bot.api import TelegramAPIServer
from validators import url as is_valid_url
import requests

import sys
import os


TOKEN = "6878787981:AAE5Bl6VUaV_qOO-EY-0vKo5l6rpzXdRrK8"
UPLOAD_FILE_SIZE_LIMIT_MB = 2000


local_server = TelegramAPIServer.from_base("http://localhost:8081")

bot = Bot(token=TOKEN, server=local_server)
dp = Dispatcher(bot)


def make_correct_filename(filename):
    if sys.getsizeof(filename) <= 255:
        return filename
    i = len(filename) - 1
    new_filename = ""
    while i > 0 and sys.getsizeof(new_filename + filename[i]) < 255:
        i -= 1
        new_filename += filename[i]
    return new_filename


def download_file(url: str):
    with requests.get(url, stream=True, allow_redirects=True) as r:
        r.raise_for_status()
        filename = make_correct_filename(r.headers.get("filename", url.split("/")[-1]))
        with open(filename, 'wb') as f:
            file_size_mb = int(r.headers.get('content-length', 0)) / 1024 / 1024
            if file_size_mb > UPLOAD_FILE_SIZE_LIMIT_MB:
                return filename, False
            print(f"File size {file_size_mb}mb:\n{url}")
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
            print(f"File saved as {filename} ({file_size_mb}mb)")
    return filename, True


@dp.message_handler(content_types=["text"])
async def get_text(message):
    if message.text == "/start":
        user_name = message.from_user.first_name
        await bot.send_message(message.chat.id,
                               f"""👋 Hi {user_name}. Send me a file link"""
                               """ and I'll upload it here.""")

    elif is_valid_url(message.text):
        try:
            filename, downloaded = download_file(message.text)
            if downloaded:
                await bot.send_chat_action(message.chat.id, "upload_document")
                await bot.send_document(message.chat.id, types.InputFile(filename))
            else:
                await bot.send_message(message.chat.id, f"🚫 File is too large (2 Gb is maximum)")
            os.remove(filename)
        except Exception as exc:
            print(exc)
            await bot.send_message(message.chat.id, f"🚫 An error occured while fetching this file")
    else:
        await bot.send_message(message.chat.id, f"🔗 Send me a valid url")


executor.start_polling(dp, skip_updates=True)
