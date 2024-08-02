from telegram import Bot
import os

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

bot = Bot(token=TELEGRAM_BOT_TOKEN)

try:
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="测试消息：脚本已启动")
    print("消息已发送")
except Exception as e:
    print(f"发送消息出错: {e}")
