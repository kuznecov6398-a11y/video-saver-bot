import telebot
import yt_dlp
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Бот работает!\nКидай ссылку.\n\nДля сложных видео могу использовать cookies (напиши /help)")

@bot.message_handler(func=lambda m: True)
def download(message):
    url = message.text.strip()
    if not any(x in url for x in ['youtube.com', 'youtu.be', 'tiktok.com', 'instagram.com', 'instagr.am']):
        return bot.reply_to(message, "❌ Только YouTube, TikTok, Instagram!")

    bot.reply_to(message, "⏳ Скачиваю...")

    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
            'outtmpl': 'download.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'extractor_args': {'youtube': {'player_client': ['ios', 'android', 'web']}},
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as f:
            bot.send_video(message.chat.id, f, caption="✅ Готово!")

        os.remove(filename)

    except Exception as e:
        bot.reply_to(message, "❌ YouTube заблокировал скачивание.\n\nПопробуй другое видео или напиши /help")

print("Бот запущен!")
bot.polling(none_stop=True)
