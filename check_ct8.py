import requests
from bs4 import BeautifulSoup
import os
import datetime
from telegram import Bot

# Telegram bot token and chat ID from environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Initialize the Telegram bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

def check_registration_status():
    url = 'https://www.ct8.pl/'
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        send_telegram_message(f"请求出错: {e}")
        raise

    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.prettify())  # 调试输出 HTML 内容

    element = soup.find('span', class_='button is-large is-flexible')
    if element:
        total_accounts_text = element.text.strip().split()[0]
        total_accounts = int(total_accounts_text.replace(',', ''))
        print(f"找到的账户总数: {total_accounts}")  # 调试信息
        return total_accounts
    else:
        send_telegram_message("未能找到账户总数元素，请检查选择器是否正确。")
        raise ValueError("Could not find the total accounts element with the provided selector.")

def send_telegram_message(message):
    try:
        print(f"发送消息: {message}")  # 调试信息
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        print(f"发送消息出错: {e}")

def main():
    try:
        send_telegram_message("测试消息：脚本已启动")
        total_accounts = check_registration_status()
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"☯️查询时间: {current_time}\n☯️账户总数：{total_accounts} / 5000\n☯️请注意️注意：如果账户总数小于5000请及时注册。"
        send_telegram_message(message)
    except Exception as e:
        send_telegram_message(f"脚本运行出错: {e}")

if __name__ == '__main__':
    main()
