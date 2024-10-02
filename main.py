import requests
from bs4 import BeautifulSoup
import time

def get_game_discount(app_id, currency):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&cc={currency}&l=russian"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data[str(app_id)]['success']:
            game_data = data[str(app_id)]['data']
            if 'price_overview' in game_data:
                price_info = game_data['price_overview']
                initial_price = price_info['initial'] / 100
                final_price = price_info['final'] / 100
                discount_percent = price_info['discount_percent']
                
                genres = [genre['description'] for genre in game_data.get('genres', [])]
                short_description = game_data.get('short_description', 'Описание отсутствует.')
                
                deck_compatibility = game_data.get('steam_deck_compatibility', {}).get('deck_verified', 'Неизвестно')
                
                game_size = get_game_size(app_id)
                
                supported_languages = game_data.get('supported_languages', 'Информация о языках недоступна.')
                
                is_deck_compatible = 'совместима' if deck_compatibility else 'неизвестна'
                
                print(f"Игра: {game_data['name']}")
                print(f"Начальная цена: {initial_price} {currency.upper()}")
                print(f"Цена со скидкой: {final_price} {currency.upper()}")
                print(f"Скидка: {discount_percent}%")
                print(f"Жанры: {', '.join(genres) if genres else 'Жанры не указаны.'}")
                print(f"Короткое описание: {short_description}")
                print(f"Совместимость с Деком: {is_deck_compatible}")
                print(f"Вес игры: {game_size}")
            else:
                print(f"Информация о цене для {game_data['name']} недоступна.")
        else:
            print("Не удалось получить данные об игре.")
    else:
        print("Ошибка при подключении к Api.")

def get_game_size(app_id):
    url = f"https://store.steampowered.com/app/{app_id}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        size_info = soup.find('div', class_='game_area_sys_req_right')
        if size_info:
            size = size_info.get_text(strip=True)
            if 'Место на диске:' in size:
                return size.split('Место на диске:')[1].strip()
        return 'Информация о размере недоступна.'
    else:
        return 'Ошибка при подключении к странице Стима.'

# Впишите сюда appid игр которые вам нужны/ write down the needed appid's
games_to_check = []

currency = input("Введите код страны для валюты (например, 'kz' для тенге, 'ru' для рублей): ").lower()

while True:
    for game_id in games_to_check:
        get_game_discount(game_id, currency)
    time.sleep(3600)