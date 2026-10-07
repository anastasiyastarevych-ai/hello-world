from abc import ABC, abstractmethod


class Transport(ABC):
    def __init__(self, name: str, speed: int, capacity: int):
        if not isinstance(name, str):
            raise TypeError("name має бути str")
        if isinstance(speed, bool) or not isinstance(speed, int):
            raise TypeError("speed має бути int")
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise TypeError("capacity має бути int")
        if speed <= 0:
            raise ValueError("speed має бути більше 0")
        if capacity < 0:
            raise ValueError("capacity не може бути від'ємним")

        self.name = name
        self.speed = speed
        self.capacity = capacity

    @staticmethod
    def _check_non_negative(value, label: str) -> None:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{label} має бути числом")
        if value < 0:
            raise ValueError(f"{label} не може бути від'ємним")

    @abstractmethod
    def move(self, distance: float) -> float:
        pass

    @abstractmethod
    def fuel_consumption(self, distance: float) -> float:
        pass

    @abstractmethod
    def info(self) -> str:
        pass

    def calculate_cost(self, distance: float, price_per_unit: float) -> float:
        self._check_non_negative(price_per_unit, "price_per_unit")
        return self.fuel_consumption(distance) * price_per_unit


class Car(Transport):
    FUEL_PER_KM = 0.07

    def move(self, distance: float) -> float:
        self._check_non_negative(distance, "distance")
        return distance / self.speed

    def fuel_consumption(self, distance: float) -> float:
        self._check_non_negative(distance, "distance")
        return distance * self.FUEL_PER_KM

    def info(self) -> str:
        return (
            f"Автомобіль «{self.name}»: швидкість {self.speed} км/год, "
            f"місць {self.capacity}"
        )


class Bus(Transport):
    FUEL_PER_KM = 0.15

    def __init__(self, name: str, speed: int, capacity: int, passengers: int = 0):
        super().__init__(name, speed, capacity)
        if isinstance(passengers, bool) or not isinstance(passengers, int):
            raise TypeError("passengers має бути int")
        if passengers < 0:
            raise ValueError("passengers не може бути від'ємним")
        self.passengers = passengers

    def move(self, distance: float) -> float:
        self._check_non_negative(distance, "distance")
        return distance / self.speed

    def fuel_consumption(self, distance: float) -> float:
        self._check_non_negative(distance, "distance")
        return distance * self.FUEL_PER_KM

    def info(self) -> str:
        text = (
            f"Автобус «{self.name}»: швидкість {self.speed} км/год, "
            f"місць {self.capacity}, пасажирів {self.passengers}"
        )
        if self.passengers > self.capacity:
            text += ". Перевантажено!"
        return text


class Bicycle(Transport):
    MAX_SPEED = 20

    def __init__(self, name: str, speed: int, capacity: int):
        super().__init__(name, speed, capacity)
        self.speed = min(self.speed, self.MAX_SPEED)

    def move(self, distance: float) -> float:
        self._check_non_negative(distance, "distance")
        return distance / self.speed

    def fuel_consumption(self, distance: float) -> float:
        self._check_non_negative(distance, "distance")
        return 0.0

    def info(self) -> str:
        return (
            f"Велосипед «{self.name}»: швидкість {self.speed} км/год "
            f"(максимум {self.MAX_SPEED}), місць {self.capacity}"
        )


class ElectricCar(Car):
    ENERGY_PER_KM = 0.2

    def battery_usage(self, distance: float) -> float:
        self._check_non_negative(distance, "distance")
        return distance * self.ENERGY_PER_KM

    def fuel_consumption(self, distance: float) -> float:
        self._check_non_negative(distance, "distance")
        return 0.0

    def calculate_cost(self, distance: float, price_per_unit: float) -> float:
        self._check_non_negative(price_per_unit, "price_per_unit")
        return self.battery_usage(distance) * price_per_unit

    def info(self) -> str:
        return (
            f"Електромобіль «{self.name}»: швидкість {self.speed} км/год, "
            f"місць {self.capacity}, пальне не використовує"
        )


def print_report(transports: list, distance: int) -> None:
    for transport in transports:
        print(transport.info())
        print(f"  Час на {distance} км: {transport.move(distance):.2f} год")
        print(f"  Пальне на {distance} км: {transport.fuel_consumption(distance):.2f} л")


def print_costs(trips: list, distance: int) -> None:
    for transport, price in trips:
        cost = transport.calculate_cost(distance, price)
        print(f"{transport.name}: {cost:.2f} грн")


if __name__ == "__main__":
    car = Car("Toyota Corolla", 100, 5)
    bus = Bus("Богдан A092", 60, 40, 35)
    full_bus = Bus("Еталон A081", 50, 30, 36)
    bicycle = Bicycle("Міський велосипед", 35, 1)
    tesla = ElectricCar("Tesla Model 3", 120, 5)

    transports = [car, bus, full_bus, bicycle, tesla]

    print("1. Звіт по всьому транспорту")
    print_report(transports, 100)

    print()
    print("2. Батарея електромобіля")
    print(f"{tesla.name}: {tesla.battery_usage(100):.2f} кВт·год на 100 км")

    print()
    print("3. Вартість поїздки на 100 км")
    fuel_price = 55.0
    power_price = 8.0
    trips = [
        (car, fuel_price),
        (bus, fuel_price),
        (full_bus, fuel_price),
        (bicycle, fuel_price),
        (tesla, power_price),
    ]
    print_costs(trips, 100)

    print()
    print("4. Перевірки")
    try:
        Transport("Щось", 10, 1)
    except TypeError:
        print("Transport створити не можна: клас абстрактний")

    try:
        Car("Дивна", "швидко", 4)
    except TypeError as error:
        print(f"Помилка типу: {error}")

    print("ElectricCar це Car:", isinstance(tesla, Car))