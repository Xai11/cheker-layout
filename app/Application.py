from selenium import webdriver
from axe_selenium_python import Axe

# Инициализация веб-драйвера
driver = webdriver.Chrome()

# Открытие веб-сайта
driver.get('https://doka.guide/a11y/?view=themes')

# Инициализация Axe
axe = Axe(driver)

# Запуск тестов доступности
axe.inject()
results = axe.run()

# Закрытие драйвера
driver.quit()


# Функция для расчета балла
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

    for violation in violations:
        impact = violation['impact']
        nodes_count = len(violation['nodes'])

        # Получаем приоритетный балл
        priority_score = priority_scores.get(impact, 1)

        # Вычисляем штраф за текущую ошибку
        penalty = priority_score * (nodes_count * 0.1)

        # Вычитаем штраф из общего балла
        score -= penalty

    # Ограничение балла от 0 до 100
    final_score = max(min(score, 100), 0)
    return final_score


# Расчет итогового балла
final_score = calculate_accessibility_score(results)

# Вывод результата
print(f"Итоговый балл доступности: {final_score:.2f}/100")
