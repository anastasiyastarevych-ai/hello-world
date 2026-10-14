def calculate(a, b, operation):
    if operation == "+":
        return a + b
    elif operation == "-":
        return a - b
    elif operation == "*":
        return a * b
    elif operation == "/":
        return a / b


def main():
    try:
        a = float(input("Перше число: ").replace(",", "."))
        b = float(input("Друге число: ").replace(",", "."))
    except ValueError:
        print("Помилка: потрібно ввести число")
        return

    operation = input("Операція (+, -, *, /): ").strip()
    if operation not in ("+", "-", "*", "/"):
        print("Помилка: невідома операція")
        return
    if operation == "/" and b == 0:
        print("Помилка: на нуль ділити не можна")
        return

    result = round(calculate(a, b, operation), 10)
    if result.is_integer():
        result = int(result)
    print("Результат:", result)


if __name__ == "__main__":
    main()