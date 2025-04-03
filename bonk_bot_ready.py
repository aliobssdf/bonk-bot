from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
import aiohttp
import logging

# إعدادات
API_TOKEN = '7694179338:AAEttTXyiONe2MZLG7wln4y-jLCneBJHA1E'
TIKTOK_API = 'https://api.tikwm.com'

# تهيئة البوت
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# رسالة البداية
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("""👋 هلا! أنا بوت Bonk.
ارسل لي رابط فيديو من تيك توك، وأنا راح أرجع لك الفيديو بدون علامة مائية.""")

# معالجة روابط تيك توك
@dp.message_handler(lambda message: 'tiktok.com' in message.text)
async def download_tiktok_video(message: Message):
    url = message.text.strip()
    await message.reply("⏳ جاري تحميل الفيديو...")

    params = {'url': url}
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{TIKTOK_API}/video", params=params) as resp:
            data = await resp.json()
            if data.get("data") and data["data"].get("play"):
                video_url = data['data']['play']
                await bot.send_video(message.chat.id, video_url, caption="✅ تم التحميل من Bonk")
            else:
                await message.reply("❌ ما قدرت أجيب الفيديو. تأكد من الرابط أو جرب بعدين.")

# تشغيل البوت
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)