import os 
import requests
from bs4 import BeautifulSoup
import csv

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
}

def get_emails(url):
    emails = set()  # используем множество для автоматического удаления дубликатов
    result  = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, 'html.parser')
    for mail in soup.find_all('a', href=True):
        href = mail.get('href')
        # for decoded email
        if href.startswith('/cdn-cgi/l/email-protection#'):
            decoded_email = href.replace('/cdn-cgi/l/email-protection#', '')

            key = int(decoded_email[:2], 16)
            hex_str = decoded_email[2:]

            email = ''
            for i in range(0, len(hex_str), 2):
                email += chr(int(hex_str[i:i+2], 16) ^ key)
            emails.add(email)  # добавляем адрес во множество

        # for default email
        elif href.startswith('mailto:'):
            default_email = href.replace('mailto:', '')
            emails.add(default_email)  # добавляем адрес во множество
    return emails

def main():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'Emailupd.csv')

    websites = []
    while True:
        website = input("Enter a website (or 'q' to quit): ")
        if website.lower() == 'q':
            break
        websites.append(website)
    
    # Открываем файл на дозапись
    with open(file_path, mode='a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        # Если файл пустой, записываем заголовок
        if os.path.getsize(file_path) == 0:
            writer.writerow(['Сайт', 'Почта'])
        
        # Перебираем веб-сайты и записываем почты
        for site in websites:
            resultEmails = get_emails(site)
            for email in resultEmails:
                writer.writerow([site, email])
    
    # Выводим сообщение о завершении
    if os.path.exists(file_path):
        print('Загрузка в csv файл завершена! Посмотрите его в папке, где находится main.py:', current_dir)
    else:
        print('Не удалось создать csv файл.')


if __name__ == "__main__":
    main()
