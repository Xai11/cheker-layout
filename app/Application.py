from selenium import webdriver
from axe_selenium_python import Axe
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def check_accessibility(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    axe = Axe(driver)
    axe.inject()
    results = axe.run()

    # Запись результатов в файл
    axe.write_results(results, 'axe_report.json')

    # Вывод информации о нарушениях в консоль
    violations = results['violations']
    if violations:
        print(f"Найдено {len(violations)} нарушений:")
        for violation in violations:
            print(f"\nПроблема: {violation['description']}")
            print(f"Влияние: {violation['impact']}")
            print("Элементы:")
            for node in violation['nodes']:
                print(f"  - {node['html']}")
            print(f"Рекомендации: {violation['helpUrl']}")
    else:
        print("Нарушения не найдены.")

    driver.quit()

check_accessibility('https://nuoflix.de')

