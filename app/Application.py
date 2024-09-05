from repository.ParsHTML import parsing_page


def check_parsing():
    url = "https://minsocium.ru/"
    parsing_page(url)

if __name__ == '__main__':
    check_parsing()