SEPARATOR = "|"

class JunkItem:
    def __init__(self, name: str, quantity: int, value: float):
        if not isinstance(name, str):
            raise TypeError("name має бути str")
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise TypeError("quantity має бути int")
        if isinstance(value, bool) or not isinstance(value, float):
            raise TypeError("value має бути float")

        self.name = name
        self.quantity = quantity
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, JunkItem):
            return NotImplemented
        return (self.name, self.quantity, self.value) == (
            other.name,
            other.quantity,
            other.value,
        )

    def __repr__(self):
        return f"JunkItem({self.name!r}, {self.quantity}, {self.value})"

class JunkRepository:

    def save(self, items: list) -> None:
        raise NotImplementedError

    def load(self) -> list:
        raise NotImplementedError

def parse_line(line: str) -> JunkItem:
    parts = line.split(SEPARATOR)
    if len(parts) != 3:
        raise ValueError("має бути рівно три поля")

    name, quantity_text, value_text = parts

    if name.strip() == "":
        raise ValueError("порожня назва")

    try:
        quantity = int(quantity_text)
    except ValueError:
        raise ValueError("кількість не ціле число") from None

    if "." in value_text:
        raise ValueError("дріб має бути через кому")
    try:
        value = float(value_text.replace(",", "."))
    except ValueError:
        raise ValueError("ціна не число") from None

    return JunkItem(name, quantity, value)

class JunkStorage(JunkRepository):
    def __init__(self, filename: str):
        self.filename = filename

    def save(self, items: list) -> None:
        self.serialize(items, self.filename)

    def load(self) -> list:
        try:
            return self.parse(self.filename)
        except FileNotFoundError:
            return []

    @staticmethod
    def serialize(items: list, filename: str) -> None:
        lines = []
        for item in items:
            if SEPARATOR in item.name or "\n" in item.name or "\r" in item.name:
                raise ValueError(f"у назві '{item.name}' є заборонений символ")
            value_text = str(item.value).replace(".", ",")
            lines.append(SEPARATOR.join([item.name, str(item.quantity), value_text]))
        with open(filename, "w", encoding="utf-8", newline="\n") as file:
            for line in lines:
                file.write(line + "\n")

    @staticmethod
    def parse(filename: str) -> list:
        items = []
        with open(filename, "r", encoding="utf-8") as file:
            for number, raw_line in enumerate(file, start=1):
                line = raw_line.rstrip("\r\n")
                if line.strip() == "":
                    continue
                try:
                    items.append(parse_line(line))
                except ValueError as error:
                    print(f"Попередження: рядок {number} пропущено ({error}): {line!r}")
        return items

class MemoryJunkStorage(JunkRepository):
    def __init__(self):
        self._items = []

    def save(self, items: list) -> None:
        self._items = [JunkItem(i.name, i.quantity, i.value) for i in items]

    def load(self) -> list:
        return [JunkItem(i.name, i.quantity, i.value) for i in self._items]

class Warehouse:
    def __init__(self, repository: JunkRepository):
        self._repository = repository
        self._items = repository.load()

    def add(self, item: JunkItem) -> None:
        for existing in self._items:
            if existing.name == item.name:
                existing.quantity += item.quantity
                return
        self._items.append(item)

    def take(self, name: str, quantity: int) -> JunkItem:
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("кількість має бути додатним цілим числом")
        for existing in self._items:
            if existing.name == name:
                if quantity > existing.quantity:
                    raise ValueError(
                        f"на складі лише {existing.quantity} шт. «{name}», "
                        f"а потрібно {quantity}"
                    )
                taken = JunkItem(name, quantity, existing.value)
                existing.quantity -= quantity
                if existing.quantity == 0:
                    self._items.remove(existing)
                return taken
        raise ValueError(f"предмета «{name}» немає на складі")

    def find(self, text: str) -> list:
        text = text.lower()
        return [item for item in self._items if text in item.name.lower()]

    def all_items(self) -> list:
        return list(self._items)

    def save(self) -> None:
        self._repository.save(self._items)

def describe(item: JunkItem) -> str:
    return f"{item.name}: {item.quantity} шт., цінність {item.value}"


def demo_file_roundtrip(filename: str) -> list:
    print("1. Запис у файл і читання назад")
    items = [
        JunkItem("Бляшанка", 5, 2.5),
        JunkItem("Стара плата", 3, 7.8),
        JunkItem("Купка дротів", 10, 1.2),
    ]
    JunkStorage.serialize(items, filename)

    print("Вміст файлу:")
    with open(filename, "r", encoding="utf-8") as file:
        print(file.read(), end="")

    restored = JunkStorage.parse(filename)
    print("Прочитано назад:")
    for item in restored:
        print(f"  {describe(item)}")
    print("Значення збережені правильно:", restored == items)
    return items


def demo_broken_lines(filename: str) -> None:
    print("2. Зіпсовані рядки")
    with open(filename, "w", encoding="utf-8") as file:
        file.write("Бляшанка|5|2,5\n")
        file.write("Стара плата|3\n")
        file.write("Купка дротів|багато|1,2\n")
        file.write("Магніт|4|дорого\n")
        file.write("Гайка|2|1.5\n")
        file.write("Болт|7|0,3\n")

    good = JunkStorage.parse(filename)
    print("Прочитано правильних рядків:", len(good))
    for item in good:
        print(f"  {describe(item)}")


def work_with_warehouse(repository: JunkRepository, title: str) -> None:
    print(f"--- {title} ---")
    warehouse = Warehouse(repository)

    warehouse.add(JunkItem("Магніт", 4, 0.5))
    taken = warehouse.take("Бляшанка", 2)
    print(f"Дістали: {taken.name} x{taken.quantity}")

    try:
        warehouse.take("Бляшанка", 100)
    except ValueError as error:
        print(f"Помилка: {error}")

    for item in warehouse.find("пла"):
        print(f"Знайшли: {describe(item)}")

    warehouse.save()

    reloaded = Warehouse(repository)
    print("Після перезавантаження складу:")
    for item in reloaded.all_items():
        print(f"  {describe(item)}")


if __name__ == "__main__":
    items = demo_file_roundtrip("junk.csv")
    print()
    demo_broken_lines("junk_broken.csv")
    print()
    print("3. Склад працює з будь-яким сховищем")
    work_with_warehouse(JunkStorage("junk.csv"), "Файл")
    print()
    memory = MemoryJunkStorage()
    memory.save(items)
    work_with_warehouse(memory, "Пам'ять")