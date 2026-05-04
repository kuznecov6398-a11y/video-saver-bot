import telebot
import yt_dlp
import os
import sys

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ Ошибка: BOT_TOKEN не найден!")
    print("Добавь переменную BOT_TOKEN в Variables")
    sys.exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Бот запущен!\nКидай ссылку на видео с YouTube, TikTok или Instagram.")

@bot.message_handler(func=lambda m: True)
def download(message):
    url = message.text.strip()
    if not any(x in url for x in ['youtube.com', 'youtu.be', 'tiktok.com', 'instagram.com', 'instagr.am']):
        return bot.reply_to(message, "❌ Поддерживаю только YouTube, TikTok, Instagram!")

    bot.reply_to(message, "⏳ Скачиваю...")

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'download.%(ext)s',
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as f:
            bot.send_video(message.chat.id, f, caption="✅ Готово!")

        os.remove(filename)
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)[:200]}")

print("✅ Бот успешно запущен!")
bot.polling(none_stop=True)
