from axe_selenium_python import Axe
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from service.ParsingHtml import pars_web_page

from service.ParsingHtml import pars_web_page

url = "https://www.selenium.dev/documentation/webdriver/elements/finders/"

pars_web_page(url)















