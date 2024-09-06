import io
from time import sleep, time


import numpy as np
from PIL import Image
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def pars_web_page(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    sleep(5)
    html = driver.page_source

    check_scalability(driver)
    sleep(10)
    check_scripts_keyboard(driver)

    check_contrast(driver)

    check_description_image(driver)

def check_size_page(driver):
    window_width = driver.execute_script("return window.innerWidth;")
    print(f'Ширина окна: {window_width}')

    # Получить ширину документа
    document_width = driver.execute_script("return document.body.scrollWidth;")
    print(f'Ширина документа: {document_width}')

    # Проверка наличия горизонтальной прокрутки
    if document_width > window_width:
        print("На сайте есть горизонтальное прокручивание.")
    else:
        print("На сайте нет горизонтального прокручивания.")

def check_scripts_keyboard(driver):
    # Поиск всех кнопок по тегу <button>
    buttons = driver.find_elements(By.XPATH, '//button[@type="button"]')

    for button in buttons:
        print('Found button:', button.get_attribute('outerHTML'))

def check_contrast(driver):
    screenshot = driver.get_screenshot_as_png()

    # Откройте изображение с помощью Pillow
    image = Image.open(io.BytesIO(screenshot))

    # Преобразуйте изображение в градации серого
    gray_image = image.convert('L')

    # Преобразуйте изображение в массив numpy
    image_array = np.array(gray_image)

    # Вычислите контрастность
    # Контрастность можно определить как стандартное отклонение интенсивности пикселей
    contrast = image_array.std()

    print(f'Контрастность изображения: {contrast}')

def check_scalability(driver):
    meta_viewport = driver.execute_script(
        "return document.querySelector('meta[name=\"viewport\"]').getAttribute('content')"
    )

    if meta_viewport:
        print(f'Мета-тег viewport найден: {meta_viewport}')
    else:
        print('Мета-тег viewport не найден.')

    # Эмуляция различных размеров экранов
    sizes = [(320, 480), (768, 1024), (1024, 768), (1920, 1080)]
    count_size = 0;
    for width, height in sizes:
        driver.set_window_size(width, height)
        window_width = driver.execute_script("return window.innerWidth;")
        document_width = driver.execute_script("return document.body.scrollWidth;")

        # Проверка наличия горизонтальной прокрутки
        if document_width > window_width:
            count_size+=1
    if count_size > 0:
        print("При изменении масштаба появилась горизонтальная прокрутка")
    else:
        print("Сайт масштабируется правильно")
    print(f'Установлен размер окна: {width}x{height}')
    # Здесь вы можете добавить дополнительные проверки, например, скриншоты или анализ элементов

def check_description_image(driver):
    try:
        image = driver.find_element(By.TAG_NAME, 'img')
        alt_text = image.get_attribute('alt')
        print(alt_text)

        if alt_text:
            print(f'Описание изображения: {alt_text}')
        else:
            print('Атрибут alt не найден.')
    finally:
        print("No image!")