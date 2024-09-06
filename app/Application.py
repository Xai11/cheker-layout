from axe_selenium_python import Axe
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

driver = webdriver.Chrome()

# Открытие веб-сайта
driver.get('https://www.livejournal.com')


# Инициализация Axe
axe = Axe(driver)

# Запуск тестов доступности
axe.inject()
results = axe.run()




def find_popup_selector(driver):
    potential_selectors = [
        "[role='dialog']",
        ".modal",
        ".popup",
        "#cookie-banner",
        "#cookieWarning",
        "#cookieHolder",
        ".cookie-banner",
        ".cookie-popup",
        ".cookie-consent",
        "[aria-label='cookie consent']",
        "[id*='cookie']",
        "[class*='cookie']"
    ]

    for selector in potential_selectors:
        elements = driver.find_elements(By.CSS_SELECTOR, selector)
        for element in elements:
            if element.is_displayed():
                return element
    return None


def calculate_accessibility_score(results):
    violations = results['violations']

    # Начальный балл
    score = 100

    # Приоритеты для различных уровней серьезности
    priority_scores = {
        'critical': 5,
        'serious': 3,
        'moderate': 2,
        'minor': 1
    }

    # Критерии, которые несут только одну ошибку
    single_error_criteria = {
        'document-title',
        'heading-order'
    }

    print("\nДетали штрафов за ошибки:")
    for violation in violations:
        impact = violation['impact']
        nodes_count = len(violation['nodes'])

        # Получаем приоритетный балл
        priority_score = priority_scores.get(impact, 1)

        # Проверяем, является ли критерий таким, который несет только одну ошибку
        if violation['id'] in single_error_criteria:
            penalty = priority_score * 10
            print(f"Критерий: {violation['id']} | Приоритет: {priority_score} | Штраф: {priority_score} * 10 = {penalty}")
        else:
            penalty = priority_score * nodes_count
            print(f"Критерий: {violation['id']} | Приоритет: {priority_score} | Кол-во ошибок: {nodes_count} | Штраф: {priority_score} * {nodes_count} = {penalty}")

        # Вычитаем штраф из общего балла
        score -= penalty

    # Ограничение балла от 0 до 100
    final_score = max(min(score, 100), 0)
    return final_score



def is_popup_keyboard_accessible(driver, popup):
    if popup is None:
        print("Всплывающее окно не найдено.")
        return False

    focusable_elements = popup.find_elements(By.CSS_SELECTOR, 'a, button, input, select, textarea, [tabindex]')

    try:
        initial_focus = WebDriverWait(driver, 10).until(
            EC.visibility_of(focusable_elements[0])
        )
        initial_focus.send_keys(Keys.TAB)

        for element in focusable_elements:
            WebDriverWait(driver, 10).until(
                EC.visibility_of(element)
            )
            element.send_keys(Keys.TAB)
            if not element == driver.switch_to.active_element:
                return False
        return True
    except TimeoutException:
        print("Элемент не доступен для взаимодействия.")
        return False


popup = find_popup_selector(driver)
accessible = is_popup_keyboard_accessible(driver, popup)
if accessible:
    print("Всплывающее окно доступно для управления с клавиатуры.")
elif popup is not None:
    print("Всплывающее окно недоступно для управления с клавиатуры.")




# Функция для вывода ошибок по важным критериям
def print_important_violations(results):
    important_criteria = [
        'keyboard',  # Использование клавиатуры
        'image-alt',  # Альтернативный текст для изображений
        'color-contrast',  # Контрастность текста
        'document-title',  # Заголовки страниц
        'label',  # Формы и их описание
        'aria-roles',  # Использование ARIA
        'heading-order'  # Структура заголовков
    ]

    print("\nОшибки по важным критериям:")
    for violation in results['violations']:
        if violation['id'] in important_criteria:
            print(f"\nКритерий: {violation['id']}")
            print(f"Описание: {violation['description']}")
            print(f"Количество элементов с ошибками: {len(violation['nodes'])}")

driver.quit()

# Расчет итогового балла
final_score = calculate_accessibility_score(results)

# Вывод результата
print(f"Итоговый балл доступности: {final_score:.2f}/100")

# Вывод ошибок по важным критериям
print_important_violations(results)
