from aiogram import Bot, Dispatcher, executor, types
from aiogram.bot.api import TelegramAPIServer
from validators import url as is_valid_url
import requests

from urllib.parse import urlparse


TOKEN = "6878787981:AAE5Bl6VUaV_qOO-EY-0vKo5l6rpzXdRrK8"
UPLOAD_FILE_SIZE_LIMIT_MB = 2000


local_server = TelegramAPIServer.from_base("http://localhost:8081")

bot = Bot(token=TOKEN, server=local_server)
dp = Dispatcher(bot)


def download_file(url: str):
    filename = url.split("/")[-1]
    with open(filename, 'wb') as f:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            file_size_mb = int(r.headers.get('content-length', 0)) / 1024 / 1024
            if file_size_mb > UPLOAD_FILE_SIZE_LIMIT_MB:
                raise Exception(f"Upload file size limit error {file_size_mb}")
            print(f"File size {file_size_mb}mb:\n{url}")
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
            print(f"File downloaded ({file_size_mb}mb):\n{url}")
    return filename


@dp.message_handler(content_types=["text"])
async def get_text(message):
    if message.text == "/start":
        user_name = message.from_user.first_name
        await bot.send_message(message.chat.id,
                               f"""👋 Hi {user_name}. Send me a file link"""
                               """ and I'll upload it here.""")

    elif is_valid_url(message.text):
        try:
            filename = download_file(message.text)
            await bot.send_chat_action(message.chat.id, "upload_document")
            await bot.send_document(message.chat.id, filename)
        except Exception as exc:
            print(exc)
            await bot.send_message(message.chat.id, f"🚫 An error occured while fetching this file")
    else:
        await bot.send_message(message.chat.id, f"🔗 Send me a valid url")


executor.start_polling(dp, skip_updates=True)
