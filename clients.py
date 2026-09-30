def check_amount(amount):
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        return "Фальшиві дані"
    if amount < 100:
        return "Дрібнота"
    elif amount < 1000:
        return "Середнячок"
    else:
        return "Великий клієнт"


def check_status(status):
    match status:
        case "clean":
            return "Працювати без питань"
        case "suspicious":
            return "Перевірити документи"
        case "fraud":
            return "У чорний список"
        case _:
            return "Невідомий статус"


def sort_clients(deals):
    clients = []
    for name, amount, status in deals:
        client = {
            "name": name,
            "category": check_amount(amount),
            "decision": check_status(status),
        }
        clients.append(client)
    return clients

deals = [
    ("Олег", 50, "clean"),
    ("Марина", 100, "suspicious"),
    ("Іван", 999.99, "clean"),
    ("Софія", 1000, "fraud"),
    ("Петро", 5000.5, "clean"),
    ("Влад", "багато", "clean"),
    ("Оксана", 300, "unknown"),
]

result = sort_clients(deals)

for client in result:
    print(f"{client['name']}: {client['category']} — {client['decision']}")
