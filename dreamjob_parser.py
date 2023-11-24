import requests
import html
from bs4 import BeautifulSoup
from urllib.parse import urlencode

# Декодируем HTML-символы и удаляем лищние пробелы
def clean_text(input_text):
    decoded_text = html.unescape(input_text)
    cleaned_text = ' '.join(decoded_text.split())
    return cleaned_text

# Формирование URL для следующей страницы
def next_page_url(base_url, current_page, sort_key="-created_at"):
    # Увеличиваем номер страницы на 1
    next_page = current_page + 1
    # Формируем параметры запроса, включая сортировку и номер страницы
    params = {"sort": sort_key, "page": next_page}
    # Преобразуем параметры в строку и добавляем их к базовому URL
    next_page_url = f"{base_url}?{urlencode(params)}"
    print("загружаем страницу", next_page_url)
    return next_page_url

# Сбор отзывов на странице
def collect_reviews(response, current_page):
    # Проверяем успешность запроса и используем BeautifulSoup для парсинга страницы
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Собираем все отзывы со страницы и считаем их количество
        reviews = soup.find_all('div', class_='review')
        reviewsCount = len(reviews)
        print(f"Количество отзывов на странице: {reviewsCount}")

        # Выводим данные каждого отзыва
        for review_div in reviews:
            reviewName = review_div.find('h2', class_='review__header').text
            reviewDate = review_div.find('div', class_='review__date').text
            reviewRating = review_div.find('div', class_='dj-rating').text
            reviewPlus = review_div.find('div', class_='review__title-plus').find_next('div').text
            reviewMinus = review_div.find('div', class_='review__title-minus').find_next('div').text
            reviewHelpful = review_div.find('span', class_='bt__count').text
            print(f"Отзыв '{clean_text(reviewName)}' с рейтингом {clean_text(reviewRating)} ({clean_text(reviewHelpful)}) {clean_text(reviewDate)}")#\n + {clean_text(reviewPlus)}\n - {clean_text(reviewMinus)}")
    else:
        print(f"Ошибка загрузки страницы: {response.status_code}")
    # Проверяем наличие маркера следующей страницы
    if response.find('div', class_='ajax-loader'):
        current_page += 1
    else: current_page = 0

    return current_page
    


url = "https://dreamjob.ru/employers/25920"
response = requests.get(url)
current_page = 2
collect_reviews(response, current_page)
while current_page > 1:
    response = requests.get(next_page_url(url,current_page))
    collect_reviews(response, current_page)