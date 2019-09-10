import requests
import csv
from bs4 import BeautifulSoup  as bs

headers = {'accept': '*/*', #инфа с какой системы мы заходим
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36' }

base_url = 'https://2gis.kz/almaty/search/магазин?queryState=center%2F76.944981%2C43.23845%2Fzoom%2F12'

def twogis_parse(base_url, headers):
    shops = []
    urls = []
    urls.append(base_url)
    session = requests.Session() #2гис будет думать что зашел один пользователь, ищет множество магазинов
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        request = session.get(base_url, headers=headers)
        soup = bs(request.content, 'lxml') #весь ответ который нам отправляет сервер(ускоренный)
        try:
            pagination = soup.find_all('nav', attrs={'nav': 'pagination__pages'}) #парсинг нескольких страниц
            count = int(pagination[-1].text)
            for i in range(count):
                url = f'https://2gis.kz/almaty/search/%D0%BC%D0%B0%D0%B3%D0%B0%D0%B7%D0%B8%D0%BD?queryState=center%2F76.944981%2C43.23845%2Fzoom%2F12'
                if url not in urls:
                    urls.append(url)
        except:
            pass

    for url in urls:
        request = session.get(url, headers=headers)
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('h2', attrs={'class': 'searchResults__headerName'})
        for div in divs:
            try:
                title = div.find('h1', attrs={'class': 'cardHeader__headerNameText'}).text
                location = div.find('address', attrs={'class': 'card__address'}).text
                worktime = div.find('div', attrs={'class': 'microSchedule__title'}).text
                telephone = div.find('bdo', attrs={'class': 'contact__phonesItemLinkNumber'}).text
                shops.append({
                    'title': title, #название
                    'location': location, #адрес
                    'worktime': worktime, #время
                    'telephone': telephone #телефон
            })
            except:
                pass
            print(shops)
    else:
        print('ERROR or Done. Status_code = ' + str(request.status_code))
    return shops


def files_writer(shops):
    with open('parser_jobs.csv', 'w') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('Название магазина', 'адрес', 'время работы', 'телефон'))
        for shop in shops:
            a_pen.writerow((shop['title'], shop['location'], shop['worktime'], shop['telephone']))


shops = twogis_parse(base_url, headers)
files_writer(shops)