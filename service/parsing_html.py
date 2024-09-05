import requests

def parsing_by_url(url):
    request = requests.get(url)
    return request

