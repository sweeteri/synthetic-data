import random
from datetime import datetime, timedelta
import json
import pytz
import numpy as np


STORES_NUM = 30
MIN_ITEMS = 5
CARD_USE_RESTRICTION = 5
CATEGORIES_NUM = 50
BANKS = ['Сбербанк', 'ВТБ', 'Т-Банк', 'Альфа-банк']
PAYMENT_SYSTEMS = ['Visa', 'MasterCard', 'Мир']

with open('datasets/stores.json', 'r', encoding='utf-8') as f: stores = json.load(f)
with open('datasets/categories_prices.json', 'r', encoding='utf-8') as f: categories_prices = json.load(f)

timezone = pytz.timezone('Europe/Moscow')


def generate_time(working_hours)->str:
    time_convert = {'1': '10:00 20:00', '2': '10:00 22:00', '3': '09:00 21:00'}
    open_time = datetime.strptime(time_convert[working_hours].split()[0], '%H:%M')
    close_time = datetime.strptime(time_convert[working_hours].split()[1], '%H:%M')

    today = datetime.today()
    random_date = today - timedelta(days=random.randint(0, 30))
    random_time = open_time + timedelta(minutes=random.randint(0, int((close_time - open_time).total_seconds() // 60)))
    naive_datetime = datetime.combine(random_date.date(), random_time.time())
    aware_datetime = timezone.localize(naive_datetime)
    iso_format_datetime = aware_datetime.isoformat()

    return iso_format_datetime

card_count = {}
def generate_card_number(pay_system, bank)->str:
    dict_bank_paysystem = {'Сбербанк;Мир': 2202,
                           'Сбербанк;MasterCard': 5469,
                           'Сбербанк;Visa': 4276,
                           'Т-Банк;Мир': 2202,
                           'Т-Банк;MasterCard': 5489,
                           'Т-Банк;Visa': 4277,
                           'ВТБ;Мир': 2200,
                           'ВТБ;MasterCard': 5443,
                           'ВТБ;Visa': 4272,
                           'Альфа-банк;Мир': 2206,
                           'Альфа-банк;MasterCard': 5406,
                           'Альфа-банк;Visa': 4279,
                           }
    while True:
        card_number = f'{dict_bank_paysystem[f"{bank};{pay_system}"]}{random.randint(1000, 9999)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}'
        if card_number not in card_count:
            card_count[card_number] = 0
        if card_count[card_number] < CARD_USE_RESTRICTION:
            card_count[card_number] += 1
            return card_number

def generate_row(BANK_PROBABILITIES, PAYMENT_SYSTEMS_PROBABILITIES)->dict:
    store_id = str(random.randint(1, STORES_NUM))
    store_name = stores[store_id]['store_name']
    coordinates = stores[store_id]['coordinates']
    category = random.choice([i[0] for i in stores[store_id]['category_with_brands'].items()])
    brand = random.choice(stores[store_id]['category_with_brands'][category])
    num_items = random.randint(MIN_ITEMS, 20)
    min_cost, max_cost = categories_prices[category]['low_price'], categories_prices[category]['high_price']
    price_diff = max_cost - min_cost
    if price_diff >= 3:
        random_addition = random.randint(1, price_diff // 3)
    else:
        random_addition = 100
    total_cost = num_items * np.average([min_cost, max_cost]) + random_addition

    working_hours = stores[store_id]['working_hours']
    purchase_time = generate_time(working_hours)

    bank = random.choices(BANKS, weights=BANK_PROBABILITIES, k=1)[0]
    payment_system = random.choices(PAYMENT_SYSTEMS, weights=PAYMENT_SYSTEMS_PROBABILITIES, k=1)[0]
    card_number = generate_card_number(payment_system, bank)


    return {
        "Магазин": store_name,
        "Координаты": coordinates,
        "Дата и время": purchase_time,
        "Категория": category,
        "Бренд": brand,
        "Номер карты": card_number,
        "Банк": bank,
        "Платёжная система": payment_system,
        "Количество товаров": num_items,
        "Стоимость": total_cost
    }


def generate_data(BANK_PROBABILITIES, PAYMENT_SYSTEMS_PROBABILITIES, NUM_ROWS)->list[dict]:
    return [generate_row(BANK_PROBABILITIES, PAYMENT_SYSTEMS_PROBABILITIES) for _ in range(NUM_ROWS)]
