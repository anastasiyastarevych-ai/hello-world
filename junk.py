SEPARATOR = "|"


def check_type(value, kind, label):
    if type(value) is not kind:
        raise TypeError(f"{label} має бути {kind.__name__}")


class JunkItem:
    def __init__(self, name: str, quantity: int, value: float):
        check_type(name, str, "name")
        check_type(quantity, int, "quantity")
        check_type(value, float, "value")
        self.name, self.quantity, self.value = name, quantity, value

    def __eq__(self, other):
        return isinstance(other, JunkItem) and vars(self) == vars(other)

    def __repr__(self):
        return f"{self.name}: {self.quantity} шт., цінність {self.value}"


class JunkRepository:
    def save(self, items): raise NotImplementedError
    def load(self): raise NotImplementedError


class JunkStorage(JunkRepository):
    def __init__(self, filename):
        self.filename = filename

    def save(self, items):
        self.serialize(items, self.filename)

    def load(self):
        try:
            return self.parse(self.filename)
        except FileNotFoundError:
            return []

    @staticmethod
    def serialize(items, filename):
        with open(filename, "w", encoding="utf-8") as file:
            for item in items:
                value = str(item.value).replace(".", ",")
                file.write(f"{item.name}{SEPARATOR}{item.quantity}{SEPARATOR}{value}\n")

    @staticmethod
    def parse(filename):
        items = []
        with open(filename, encoding="utf-8") as file:
            for number, line in enumerate(file, start=1):
                line = line.strip()
                try:
                    name, quantity, value = line.split(SEPARATOR)
                    items.append(JunkItem(name, int(quantity), float(value.replace(",", "."))))
                except ValueError:
                    print(f"Попередження: рядок {number} пропущено: {line!r}")
        return items


class MemoryJunkStorage(JunkRepository):
    def __init__(self):
        self._rows = []

    def save(self, items):
        self._rows = [(i.name, i.quantity, i.value) for i in items]

    def load(self):
        return [JunkItem(*row) for row in self._rows]


class Warehouse:
    def __init__(self, repository):
        self._repository = repository
        self._items = repository.load()

    def add(self, item):
        self._items.append(item)

    def take(self, name, quantity):
        for item in self._items:
            if item.name == name and 0 < quantity <= item.quantity:
                item.quantity -= quantity
                if item.quantity == 0:
                    self._items.remove(item)
                return JunkItem(name, quantity, item.value)
        raise ValueError(f"не можна дістати {quantity} шт. «{name}»")

    def find(self, text):
        return [i for i in self._items if text.lower() in i.name.lower()]

    def all_items(self):
        return list(self._items)

    def save(self):
        self._repository.save(self._items)


if __name__ == "__main__":
    items = [JunkItem("Бляшанка", 5, 2.5), JunkItem("Стара плата", 3, 7.8),
             JunkItem("Купка дротів", 10, 1.2)]

    JunkStorage.serialize(items, "junk.csv")
    with open("junk.csv", encoding="utf-8") as file:
        print(file.read(), end="")
    print("Значення збережені правильно:", JunkStorage.parse("junk.csv") == items)

    with open("junk_broken.csv", "w", encoding="utf-8") as file:
        file.write("Бляшанка|5|2,5\nСтара плата|3\nКупка дротів|багато|1,2\n"
                   "Магніт|4|дорого\nБолт|7|0,3\n")
    print("Правильних рядків:", len(JunkStorage.parse("junk_broken.csv")))

    memory = MemoryJunkStorage()
    memory.save(items)
    for repository in (JunkStorage("junk.csv"), memory):
        warehouse = Warehouse(repository)
        warehouse.add(JunkItem("Магніт", 4, 0.5))
        print("Дістали:", warehouse.take("Бляшанка", 2))
        print("Знайшли:", warehouse.find("пла"))
        warehouse.save()
        print("Після перезавантаження:", Warehouse(repository).all_items())