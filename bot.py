import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.constants import ParseMode

# Токен от BotFather
TOKEN = '5785662822:AAFqLpaEituI8IlpAuZla-Iup_YxoGkP60c'

# ID чата, в который бот будет отправлять сообщения
CHAT_ID = '416967192'

# URL категории на ss.lv
url = 'https://www.ss.lv/ru/real-estate/premises/garages/bauska-and-reg/sell/'

# Создаем экземпляр бота
bot = Bot(token=TOKEN)

# Храним ссылки на уже отправленные объявления
sent_ads = set()

async def get_new_ads():
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Пример парсинга ссылок на объявления
    ads = soup.find_all('a', class_='am')  # Найдём все объявления по классу
    ads_list = []

    for ad in ads:
        ad_url = 'https://www.ss.lv' + ad['href']
        ads_list.append(ad_url)

    return ads_list

async def check_new_ads():
    ads = await get_new_ads()
    new_ads = [ad for ad in ads if ad not in sent_ads]

    for ad in new_ads:
        await bot.send_message(chat_id=CHAT_ID, text=f"Новое объявление: {ad}")
        sent_ads.add(ad)

async def main():
    # Отправка тестового сообщения
    await bot.send_message(chat_id=CHAT_ID, text="Привет! Я бот и буду отправлять тебе новые объявления.")

    # Периодически проверяем сайт на наличие новых объявлений
    while True:
        await check_new_ads()
        await asyncio.sleep(900)  # Проверяем каждые 15 минут

if __name__ == "__main__":
    asyncio.run(main())
