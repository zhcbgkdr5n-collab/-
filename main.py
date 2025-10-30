import os
import time
import threading
import requests
from flask import Flask
from telegram import Bot

# === 1. Автоматическая установка нужных пакетов ===
os.system("pip uninstall -y telegram")
os.system("pip uninstall -y python-telegram-bot")
os.system("pip install python-telegram-bot==13.15 flask")

# === 2. Настройки ===
RAPIDAPI_KEY = "37cdf53eaamsh9f6ffa70e489729p1c017djsn82a841f4e291"
TELEGRAM_TOKEN = "7560867717:AAF9De0J5qBdR03M4TTxvb8KfXRrsmrmZ48"
TG_CHAT_ID = "764321364"
TIKTOK_USERS = [
    "footballfact_official",
    "offalexppv",
    "climborstay"
]

bot = Bot(token=TELEGRAM_TOKEN)

# === 3. Flask-сервер для постоянной работы ===
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Бот запущен и работает 24/7!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# === 4. Проверка TikTok ===
def check_tiktok(username):
    url = "https://tiktok-scraper7.p.rapidapi.com/user/posts"
    querystring = {"unique_id": username}
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "tiktok-scraper7.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        data = response.json()
        if "data" in data and "videos" in data["data"]:
            return data["data"]["videos"][0]["video_id"]
        else:
            return None
    except Exception as e:
        print(f"⚠️ Ошибка у @{username}: {e}")
        return None

# === 5. Основной цикл ===
def start_bot():
    last_videos = {user: None for user in TIKTOK_USERS}
    print(f"✅ Бот следит за {', '.join('@' + u for u in TIKTOK_USERS)}")

    while True:
        for user in TIKTOK_USERS:
            video = check_tiktok(user)
            if video and video != last_videos[user]:
                last_videos[user] = video
                video_url = f"https://www.tiktok.com/@{user}/video/{video}"
                bot.send_message(chat_id=TG_CHAT_ID, text=f"🎬 Новое видео у @{user}!\n{video_url}")
                print(f"📢 Отправлено: {video_url}")
            else:
                print(f"⏳ Новых видео у @{user} нет...")
        time.sleep(60)

# === 6. Запуск ===
if __name__ == "__main__":
    keep_alive()
    start_bot()
