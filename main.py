import requests, random, os
from time import sleep
from bs4 import BeautifulSoup
from colorama import Fore, init
init()

"""
ОГРОМНАЯ просьба: не использовать этот скрипт просто так. Его быстро пофиксят. Лично я использовал 1 раз, чтобы почиллить одному в зале))
Делал я его изначально не для публичного показа, а переделывать и убирать все Nestы мне лень, так что в 
некоторых моментах код кринж (малолетние сеньоры, не надо плакать в комментарии и писать Issue о том,
какой же код хуевый, как же нейросеть палится и как же мне надо прыгнуть в окно)
"""

catch_link = input(f'Пример: {Fore.CYAN}https://kinoteatr.ru/raspisanie-kinoteatrov/city/kinoteatralka/?date=2021-01-01{Fore.RESET}\nВведите ссылку на страницу с {Fore.CYAN}фильмами{Fore.RESET}:\t{Fore.CYAN}').strip()
print(Fore.RESET, end='')

headers_post = {
    "authority": "kinoteatr.ru",
    "method": "POST",
    "path": "/cgi-bin/api_widget.pl",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-length": "526",
    "content-type": "text/plain;charset=UTF-8",
    "origin": "https://kinoteatr.ru",
    "priority": "u=1, i",
    "referer": "https://kinoteatr.ru/raspisanie-kinoteatrov/mega-himki/?date=2025-07-10",
    "sec-ch-ua": '"Chromium";v="137", "Not/A)Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}
headers_get = {
    "authority": "kinoteatr.ru",
    "method": "GET",
    "path": "/raspisanie-kinoteatrov/mega-himki/?date=2025-07-10",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "if-modified-since": "Fri, 04 Jul 2025 13:15:11 GMT",
    "priority": "u=0, i",
    "sec-ch-ua": '"Chromium";v="137", "Not/A)Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}
#proxies = requests.get('https://github.com/TheSpeedX/PROXY-List/raw/refs/heads/master/socks5.txt').text.split('\n')
#proxies = requests.get('https://proxylist.geonode.com/api/proxy-list?country=RU&speed=fast&limit=500&page=1&sort_by=lastChecked&sort_type=desc').json()['data']
# Если найдете норм способ парсинга прокси - можете добавить Pull request на Github

if not os.path.exists('proxies.txt'):
    input(f'Файл с прокси {Fore.RED}не найден{Fore.RESET}')
    os._exit(1)
with open('proxies.txt', 'r') as f:
    proxies = f.read().strip().split('\n')
print(f'Доступно {Fore.CYAN}{len(proxies)}{Fore.RESET} прокси')
sleep(1)

def fetch_page_soup(catch_link):
    r = requests.get(catch_link, headers=headers_get)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

page_soup = fetch_page_soup(catch_link)

def add_to_busket(session_id, places, proxy):
    r = requests.post('https://kinoteatr.ru/cgi-bin/api_widget.pl', json={
        "method_type": "widget",
        "method": "AddTicketsToBasket",
        "params": {
            "BuySessionId": session_id,
            "Option": "DeleteOldTickets",
            "TicketsList": places
        }
    }, headers=headers_post, proxies={
        'http': proxy,
        'https': proxy,   
    })
    return r.json()

def arent_places(session_id, proxy, catch_link):
    r = requests.post('https://kinoteatr.ru/cgi-bin/api_widget.pl', json={
        "method_type": "widget",
        "method": "PayOrder",
        "params": {
            "BuySessionId": session_id,
            "Phone": "+7 (931) 120 41 04",
            "SourceUrl": catch_link,
            "Mail": "Leon@gmail.com",
            "MailTo": "",
            "Name": "",
            "NameTo": "",
            "TextTo": "",
            "PayType": "SBP",
            "DiscountCode": 0,
            "PaymentToken": "",
            "DeliveryBarType": "",
            "DeliveryBarDateTime": "",
            "DeliveryBarSessionId": "",
            "DeliveryBarRow": "",
            "DeliveryBarPlace": ""
        }
    }, headers=headers_post, proxies={
        'http': proxy,
        'https': proxy,   
    })
    return r.json()

def get_hall_places(data_id, catch_link):
    r = requests.post('https://kinoteatr.ru/cgi-bin/api_widget.pl', json={
        "method_type":"widget","method":"GetHallPlan",
        "params":{
            "SessionId":data_id,
            "SourceUrl":catch_link,
            "Suboption":""
        },
    }, headers=headers_post)
    #print(r.text)
    return r.json()

def get_nice_proxy(proxies):
    while True:
        proxy = random.choice(proxies)
        print(f"Ищем прокси... Текущая проверка: {Fore.CYAN}{proxy.split('@')[1]}{Fore.RESET}")
        try:
            r = requests.get('https://example.com',
                proxies={
                    'http': proxy,
                    'https': proxy
                }, timeout=5
            )
            if r.status_code == 407 or r.status_code == 400: continue
            print(f'Получены новые {Fore.CYAN}прокси{Fore.RESET}')
            return proxy
        except Exception as e:
            print(e)

soup = fetch_page_soup(catch_link)
films = soup.find_all(class_='shedule_movie bordered gtm_movie')
all_films_times = []
id = 0
for film in films:
    film_name = film.get("data-gtm-list-item-filmname", "Неизвестное название")
    print(f'Фильм: {Fore.CYAN}{film_name}{Fore.RESET}')
    data_infos = film.find_all(class_='buy_seance shedule_session')
    for data_info in data_infos:
        time = data_info.find(class_='shedule_session_time')
        id += 1
        all_films_times.append({'time': time.text.strip(), 'id': int(data_info['data-id']), 'name': film_name})
        print(f"[{Fore.CYAN}{id}{Fore.RESET}] {Fore.CYAN}{time.text.strip()}{Fore.RESET} ({Fore.CYAN}{data_info['data-id']}{Fore.RESET})")

choice_id = input(f'Номер сеанса:\t{Fore.CYAN}')
print(Fore.RESET, end='')
if not choice_id.isnumeric():
    print('Неверный ID')
    os._exit(1)
choice_id = int(choice_id)-1
if choice_id < 0 or choice_id > id-1:
    print('Неверный ID')
    os._exit(1)

print(f'Выбор: {Fore.CYAN}{all_films_times[choice_id]["name"]}{Fore.RESET} ({Fore.CYAN}{all_films_times[choice_id]["time"]}{Fore.RESET})')

while True:
    try:
        hall_places = get_hall_places(all_films_times[choice_id]['id'], catch_link)
        if 'error' in hall_places.keys():
            print(f'Ошибка при получении мест: {Fore.RED}{hall_places["error"]["code"]} {hall_places["error"]["message"]}{Fore.RESET}')
            sleep(15)
            continue
        print(f'''Информация о фильме и зале:
Дата показа: {Fore.CYAN}{hall_places["result"]["SessionInfo"]["Date_string"]}{Fore.RESET}
Количество мест: {Fore.CYAN}{hall_places["result"]["HallPlan"]["PlacesCount"]}{Fore.RESET}
Количество свободных мест: {Fore.CYAN}{hall_places["result"]["HallPlan"]["NumberFreePlaces"]}{Fore.RESET}
Количество занятых мест: {Fore.CYAN}{int(hall_places["result"]["HallPlan"]["PlacesCount"])-hall_places["result"]["HallPlan"]["NumberFreePlaces"]}{Fore.RESET}
Возрастное ограничение: {Fore.CYAN}{hall_places["result"]["MovieInfo"]["Age_limit"]}{Fore.RESET}
Страна происхождения: {Fore.CYAN}{hall_places["result"]["MovieInfo"]["Countries"]}{Fore.RESET}
Тип фильма: {Fore.CYAN}{hall_places["result"]["MovieInfo"]["Genres"]}{Fore.RESET}''')
        session_id = hall_places['result']['BuySessionId']
        splitted_hall = [hall_places['result']['HallPlan']['Place'][i:i+5] for i in range(0, len(hall_places['result']['HallPlan']['Place']), 5)]
        proxy = get_nice_proxy(proxies)
        botted_places = 0
        for places in splitted_hall:
            while True:
                try:
                    payload = []
                    for place in places:
                        if place['Status'] != '1': continue
                        payload.append({
                            "PlaceID": place['ID'],
                            "Price": 670,
                            "Row": place['Row'],
                            "Place": place['Place'],
                            "PlaceType": place['Type']
                        })
                    if payload == []: break
                    result = add_to_busket(session_id, payload, proxy)
                    print(result['result']['message'])
                    result = arent_places(session_id, proxy, catch_link)
                    if 'error' in result.keys():
                        print(result['error']['message'])
                        proxy = get_nice_proxy(proxies)
                        arent_places(session_id, proxy, catch_link)
                    else:
                        print(result['result']['message'])
                    botted_places += len(payload)
                    print(f'Забронировано {Fore.CYAN}{int(hall_places["result"]["HallPlan"]["PlacesCount"])-hall_places["result"]["HallPlan"]["NumberFreePlaces"]+botted_places}{Fore.RESET}/{Fore.CYAN}{hall_places["result"]["HallPlan"]["PlacesCount"]}{Fore.RESET} мест')
                    break
                except Exception as e:
                    print(f'Ошибка: {Fore.CYAN}{e}{Fore.RESET}')
    except Exception as e:
        print(f'Ошибка: {Fore.CYAN}{e}{Fore.RESET}')
