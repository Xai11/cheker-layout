from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def pars_web_page(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    html = driver.page_source
    elements = driver.find_elements(By.CLASS_NAME, "articles-group__link link link--non-cached")
    print(elements)
