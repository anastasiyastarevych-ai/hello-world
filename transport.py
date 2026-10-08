from abc import ABC, abstractmethod

def check_type(value, kind, label):
    if type(value) is not kind:
        raise TypeError(f"{label} має бути {kind.__name__}")


class Transport(ABC):
    def __init__(self, name: str, speed: int, capacity: int):
        check_type(name, str, "name")
        check_type(speed, int, "speed")
        check_type(capacity, int, "capacity")
        self.name, self.speed, self.capacity = name, speed, capacity

    @abstractmethod
    def move(self, distance: float) -> float: ...

    @abstractmethod
    def fuel_consumption(self, distance: float) -> float: ...

    @abstractmethod
    def info(self) -> str: ...

    def calculate_cost(self, distance: float, price_per_unit: float) -> float:
        return self.fuel_consumption(distance) * price_per_unit


class Car(Transport):
    def move(self, distance):
        return distance / self.speed

    def fuel_consumption(self, distance):
        return distance * 0.07

    def info(self):
        return f"Автомобіль «{self.name}»: {self.speed} км/год, місць {self.capacity}"


class Bus(Transport):
    def __init__(self, name, speed, capacity, passengers=0):
        super().__init__(name, speed, capacity)
        check_type(passengers, int, "passengers")
        self.passengers = passengers

    def move(self, distance):
        return distance / self.speed

    def fuel_consumption(self, distance):
        return distance * 0.15

    def info(self):
        warning = ". Перевантажено!" if self.passengers > self.capacity else ""
        return (f"Автобус «{self.name}»: {self.speed} км/год, "
                f"пасажирів {self.passengers}/{self.capacity}{warning}")


class Bicycle(Transport):
    def __init__(self, name, speed, capacity):
        super().__init__(name, speed, capacity)
        self.speed = min(speed, 20)

    def move(self, distance):
        return distance / self.speed

    def fuel_consumption(self, distance):
        return 0.0

    def info(self):
        return f"Велосипед «{self.name}»: {self.speed} км/год, місць {self.capacity}"


class ElectricCar(Car):
    def battery_usage(self, distance):
        return distance * 0.2

    def fuel_consumption(self, distance):
        return 0.0

    def calculate_cost(self, distance, price_per_unit):
        return self.battery_usage(distance) * price_per_unit

    def info(self):
        return f"Електромобіль «{self.name}»: {self.speed} км/год, місць {self.capacity}"


if __name__ == "__main__":
    tesla = ElectricCar("Tesla Model 3", 120, 5)
    fleet = [
        (Car("Toyota Corolla", 100, 5), 55.0),
        (Bus("Богдан A092", 60, 40, 35), 55.0),
        (Bus("Еталон A081", 50, 30, 36), 55.0),
        (Bicycle("Міський велосипед", 35, 1), 0.0),
        (tesla, 8.0),
    ]
    for t, price in fleet:
        print(t.info(), f"| {t.move(100):.2f} год | {t.fuel_consumption(100):.2f} л",
              f"| {t.calculate_cost(100, price):.2f} грн")
    print(f"Батарея {tesla.name}: {tesla.battery_usage(100):.2f} кВт·год на 100 км")
