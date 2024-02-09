from aiogram import Bot, Dispatcher, executor, types
from aiogram.bot.api import TelegramAPIServer
from validators import url as is_valid_url
import requests

import sys
import os


TOKEN = "6878787981:AAE5Bl6VUaV_qOO-EY-0vKo5l6rpzXdRrK8"
UPLOAD_FILE_SIZE_LIMIT_MB = 4000
CHUNK_SIZE_MB = 20

local_server = TelegramAPIServer.from_base("http://localhost:8081")

bot = Bot(token=TOKEN, server=local_server)
dp = Dispatcher(bot)


def make_correct_filename(filename):
    if filename.startswith("attachment; filename="):
        filename = filename[22:-1]
    if sys.getsizeof(filename) <= 255 and len(filename) <= 60:
        return filename
    i = len(filename) - 1
    new_filename = ""
    while i > 0 and sys.getsizeof(new_filename + filename[i]) < 255 and len(new_filename) < 59:
        new_filename += filename[i]
        i -= 1
    return new_filename[::-1]


def download_file(url: str):
    with requests.get(url, stream=True, allow_redirects=True) as r:
        r.raise_for_status()
        filename = make_correct_filename(r.headers.get("Content-Disposition", url.split("/")[-1]))
        with open(filename, 'wb') as f:
            file_size_mb = int(r.headers.get('content-length', 0)) / 1024 / 1024
            if file_size_mb > UPLOAD_FILE_SIZE_LIMIT_MB:
                return filename, 0
            print(f"File size {file_size_mb}mb:\n{url}")
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
            print(f"File saved as {filename} ({file_size_mb}mb)")
    return filename, file_size_mb


def split_file(filename: str):
    print(f"Splitting {filename}")
    parts_dir = "".join([ch if ch.isalnum() else "_" for ch in filename])
    os.makedirs(parts_dir, exist_ok=True)
    os.system(f"split -b {CHUNK_SIZE_MB}MB {filename} {parts_dir}/")
    print(f"Splitted {filename}")
    return os.listdir(parts_dir), parts_dir


@dp.message_handler(content_types=["text"])
async def get_text(message):
    if message.text == "/start":
        user_name = message.from_user.first_name
        await bot.send_message(message.chat.id,
                               f"""👋 Hi {user_name}. Send me a file link"""
                               """ and I'll upload it here.""")

    elif is_valid_url(message.text):
        try:
            filename, file_size_mb = download_file(message.text)
            if file_size_mb:
                await bot.send_chat_action(message.chat.id, "upload_document")
                if file_size_mb <= CHUNK_SIZE_MB:
                    await bot.send_document(message.chat.id, types.InputFile(filename))
                else:
                    splitted_files, parts_dir = split_file(filename)
                    await bot.send_message(message.chat.id, f"Sending {len(splitted_files)} splitted files")
                    for part_filename in splitted_files:
                        bot.send_document(message.chat.id, types.InputFile(part_filename))
                    os.system(f"rm -rf {parts_dir}")
            else:
                await bot.send_message(message.chat.id, f"🚫 File is too large (4 Gb is maximum)")
            os.remove(filename)
        except Exception as exc:
            print(exc)
            await bot.send_message(message.chat.id, f"🚫 An error occured while fetching this file")
    else:
        await bot.send_message(message.chat.id, f"🔗 Send me a valid url")


executor.start_polling(dp, skip_updates=True)
