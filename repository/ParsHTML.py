from http.client import responses
from xml.dom import SyntaxErr

import requests
import  pandas as pd
from bs4 import BeautifulSoup


def parsing_page(url):
    request = requests.get(URL_TEMPLATE)
    print(request.status_code)
    soup = BeautifulSoup(request.content, 'html.parser')
    print(soup)

URL_TEMPLATE = "https://minsocium.ru/"
