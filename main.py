import telebot
import yt_dlp
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Бот работает!\n\nКидай ссылку на видео.")

@bot.message_handler(func=lambda m: True)
def download(message):
    url = message.text.strip()
    
    if not any(x in url for x in ['youtube.com', 'youtu.be', 'tiktok.com', 'instagram.com', 'instagr.am']):
        return bot.reply_to(message, "❌ Только YouTube, TikTok, Instagram!")

    bot.reply_to(message, "⏳ Скачиваю...")

    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': 'download.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'android', 'web'],
                    'skip': ['dash', 'hls']
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as f:
            if filename.lower().endswith(('.mp4', '.mov', '.webm')):
                bot.send_video(message.chat.id, f, caption="✅ Готово!")
            else:
                bot.send_document(message.chat.id, f, caption="✅ Готово!")

        os.remove(filename)

    except Exception as e:
        error = str(e).lower()
        if "sign in" in error or "bot" in error:
            bot.reply_to(message, "❌ Это видео заблокировано YouTube.\nПопробуй другое видео (обычно короткие работают лучше).")
        else:
            bot.reply_to(message, f"❌ Ошибка: {str(e)[:180]}")

print("✅ Бот запущен!")
bot.polling(none_stop=True)
