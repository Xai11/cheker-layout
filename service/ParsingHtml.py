from selenium import webdriver

# Указать путь к драйверу (например, chromedriver для Chrome)
driver_path = 'alex/PycharmProjects/ml-for-blinds/geckodriver/'

# Создать экземпляр драйвера
driver = webdriver.Chrome(driver_path)

# Открыть нужный сайт
driver.get('https://example.com')

# Получить ширину окна
window_width = driver.execute_script("return window.innerWidth;")
print(f'Ширина окна: {window_width}')

# Получить ширину документа
document_width = driver.execute_script("return document.body.scrollWidth;")
print(f'Ширина документа: {document_width}')

# Закрыть драйвер
driver.quit()