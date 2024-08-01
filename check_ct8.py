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
    url = 'https://www.ct8.pl/'  # 替换为实际的 API URL 或页面 URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 调试输出 HTML 内容
    print(soup.prettify())

    # 使用实际的选择器查找总账户数
    element = soup.find('span', class_='button is-large is-flexible')
    
    if element:
        total_accounts_text = element.text.strip().split()[0]  # 提取账户总数
        total_accounts = int(total_accounts_text.replace(',', ''))  # 转换为整数
        return total_accounts
    else:
        raise ValueError("Could not find the total accounts element with the provided selector.")

def send_telegram_message(message):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

def main():
    total_accounts = check_registration_status()
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f"☯️查询时间: {current_time}\n☯️账户总数：{total_accounts} / 5000\n☯️请注意️注意：如果账户总数小于5000请及时注册。"
    send_telegram_message(message)

if __name__ == '__main__':
    main()
