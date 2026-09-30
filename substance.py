def has_valid_types(quantity, temperature):
    """Перевіряє типи: кількість має бути int, температура мфє бути float."""
    if isinstance(quantity, bool) or not isinstance(quantity, int):
        return False
    if isinstance(temperature, bool) or not isinstance(temperature, float):
        return False
    return True


def check_temperature(temperature):
    """Повертає стан температури зберігання."""
    if temperature < 5:
        return "Надто холодно"
    elif temperature > 25:
        return "Надто жарко"
    else:
        return "Норма"


def check_category(category):
    """Повертає статус за категорією препарату."""
    match category:
        case "antibiotic":
            return "Рецептурний препарат"
        case "vitamin":
            return "Вільний продаж"
        case "vaccine":
            return "Потребує спецзберігання"
        case _:
            return "Невідома категорія"


def check_batch(batch):
    """Приймає список препаратів, поіертає список результатів перевірки."""
    results = []
    for name, quantity, category, temperature in batch:
        if has_valid_types(quantity, temperature):
            category_status = check_category(category)
            temperature_status = check_temperature(temperature)
        else:
            category_status = "Помилка даних"
            temperature_status = "Помилка даних"

        results.append({
            "name": name,
            "category_status": category_status,
            "temperature_status": temperature_status,
        })
    return results

batch = [
    ("Амоксицилін", 100, "antibiotic", 20.0),
    ("Вітамін C", 250, "vitamin", 5.0),
    ("Вакцина А", 50, "vaccine", 2.5),
    ("Омега-3", 120, "vitamin", 25.0),
    ("Пробіотик", 60, "probiotic", 26.5),
    ("Іммуноглобулін", "багато", "vaccine", 4.0),
    ("Цефтриаксон", 30, "antibiotic", "тепло"),
]

for item in check_batch(batch):
    print(f"{item['name']}: {item['category_status']} — {item['temperature_status']}")