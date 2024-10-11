from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def save_page_html(url, file_path: str):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        # Получаем HTML-код страницы
        html_content = page.content()

        # Сохраняем HTML-код в файл
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)

        print(f'HTML код страницы сохранен в файл {file_path}')

        # Закрываем браузер
        browser.close()


def normalize_html(html: str) -> str:
    # Создаем объект BeautifulSoup и используем его для нормализации HTML
    soup = BeautifulSoup(html, 'html.parser')
    # Преобразуем обратно в строку с отступами и удаляем лишние пробелы
    return soup.prettify()


# TODO Rewrite to show differences between files in test errors
def compare_two_html(first: str, second: str) -> bool:
    normalized_first = normalize_html(first)
    normalized_second = normalize_html(second)

    return normalized_first == normalized_second


def read_html_from_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        html = file.read()
    return html
