import requests
from bs4 import BeautifulSoup
import telegram
from datetime import datetime
import os

# Telegram bot token and chat ID from environment variables
bot_token = os.environ['TELEGRAM_BOT_TOKEN']
chat_id = os.environ['TELEGRAM_CHAT_ID']

# Function to check CT8.PL registration status
def check_registration_status():
    url = 'https://ct8.pl/registration_page'  # 替换为实际的注册页面 URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 根据页面结构找到账户总数信息
    total_accounts_text = soup.find('selector').text  # 替换为实际的选择器
    total_accounts = int(total_accounts_text.split(':')[-1].strip())
    
    return total_accounts

# Function to send Telegram notification
def send_telegram_message(message):
    bot = telegram.Bot(token=bot_token)
    bot.send_message(chat_id=chat_id, text=message)

# Main function
def main():
    total_accounts = check_registration_status()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if total_accounts < 5000:
        message = f'☯️查询时间: {timestamp}\n☯️账户总数：{total_accounts} / 5000\n☯️请注意️注意：如果账户总数小于5000请及时注册。'
        send_telegram_message(message)

if __name__ == "__main__":
    main()
