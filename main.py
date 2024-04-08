import requests
from lxml import html
import csv


def fetch_news_data():
    # URL для запроса
    url = 'https://news.mail.ru/'

    # Заголовок HTTP-запроса с пользовательским агентом
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    }

    # Отправка GET-запроса
    response = requests.get(url, headers=headers)

    # Проверка успешности запроса
    if response.status_code == 200:
        # Парсинг HTML-контента
        tree = html.fromstring(response.content)

        # Используем XPath для выбора таблицы новостей (пример)
        news_table = tree.xpath('//div[@class="newsitem newsitem_height_fixed js-ago-wrapper"]')

        # Создаем список для хранения данных
        news_data = []

        # Извлекаем данные из каждой строки таблицы
        for item in news_table:
            # Пример XPath для извлечения заголовка новости
            title = item.xpath('.//span[@class="newsitem__title-inner"]/text()')
            # Пример XPath для извлечения ссылки на новость
            link = item.xpath('.//a[@class="newsitem__title link-holder"]/attribute::href')

            # Проверяем, что данные были найдены
            if title and link:
                # Добавляем данные в список
                news_data.append({'title': title[0], 'link': link[0]})

        return news_data
    else:
        # Если запрос завершился неудачей, выводим сообщение об ошибке
        print("Ошибка при выполнении запроса:", response.status_code)
        return None


def save_to_csv(data, filename):
    # Записываем данные в CSV-файл
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for item in data:
            writer.writerow(item)


if __name__ == "__main__":
    # Получаем данные
    news_data = fetch_news_data()

    if news_data:
        # Сохраняем данные в CSV-файл
        save_to_csv(news_data, 'news_data.csv')
        print("Данные успешно сохранены в файл 'news_data.csv'")
    else:
        print("Не удалось получить данные.")

