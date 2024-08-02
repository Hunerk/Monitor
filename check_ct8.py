import requests
from bs4 import BeautifulSoup
import os
import datetime

# 从环境变量中获取 Telegram Bot Token 和 Chat ID
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"发送消息到Telegram失败: {response.text}")
    except Exception as e:
        print(f"发送消息到Telegram时出错: {e}")

def check_registration_status():
    url = 'https://www.ct8.pl/'  # 替换为实际的 API URL 或页面 URL
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
    except requests.RequestException as e:
        send_telegram_message(f"请求出错: {e}")
        raise

    soup = BeautifulSoup(response.text, 'html.parser')

    # 调试输出 HTML 内容（在生产环境中考虑禁用）
    print(soup.prettify())

    # 使用实际的选择器查找总账户数
    element = soup.find('span', class_='button is-large is-flexible')
    
    if element:
        total_accounts_text = element.text.strip().split()[0]  # 提取账户总数
        total_accounts = int(total_accounts_text.replace(',', ''))  # 转换为整数
        return total_accounts
    else:
        send_telegram_message("未能找到账户总数元素，请检查选择器是否正确。")
        raise ValueError("Could not find the total accounts element with the provided selector.")

def main():
    try:
        total_accounts = check_registration_status()
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"☯️查询时间: {current_time}\n☯️账户总数：{total_accounts} / 5000\n☯️请注意️注意：如果账户总数小于5000请及时注册。"
        send_telegram_message(message)
    except Exception as e:
        send_telegram_message(f"脚本运行出错: {e}")

if __name__ == '__main__':
    main()
