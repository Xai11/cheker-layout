import requests

URL_TEMPLATE = "https://www.gosuslugi.ru/"
request = requests.get(URL_TEMPLATE)
print(request.status_code)

print(request.text)