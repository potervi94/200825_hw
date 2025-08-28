# -*- coding: utf-8 -*-
# Курс: AI+Python 
# Модуль 11. ООП 
# Тема: ООП. Частина 1
#  Завдання 1 
# Створіть клас Cart(кошик клієнта магазину) з атрибутами 
# client(ім’я клієнта) та items(список товарів).  
# Додайте метод який додає новий товар до кошика 
# Додайте метод який видаляє товар з кошика 
# Додайте метод для виведення інформації про кошик 
# Завдання 2 
# Створіть клас Phone з атрибутами number та battery_level. 
# Додайте метод який зменшує заряд телефона(на скільки 
# зменшити відсотків передається як параметр), якщо він 
# опуститься нижче 20%, вивести повідомлення 
# Додайте метод для виведення інформації про телефон.

from __future__ import annotations

from typing import List, Optional


# реалізація класу Cart.
# Обрав зберігання товарів у списку простих рядків,
# щоб було просто додавати/видаляти.
# Додав окремі методи для рядкового подання та друку.
class Cart:
    def __init__(self, client: str, items: Optional[List[str]] = None) -> None:
        # items за замовчуванням — порожній список; копіюю, щоб уникнути спільних посилань.
        self.client: str = client
        self.items: List[str] = list(items) if items is not None else []

    def add_item(self, item: str) -> None:
        # захищаюсь від порожніх назв товарів — ігнорую такі додавання.
        if not isinstance(item, str):
            raise TypeError("Назва товару має бути рядком (str).")
        cleaned = item.strip()
        if cleaned:
            self.items.append(cleaned)

    def remove_item(self, item: str) -> bool:
        # видаляю лише перше входження; повертаю True/False як індикатор успіху.
        try:
            self.items.remove(item)
            return True
        except ValueError:
            return False

    def get_info(self) -> str:
        # формую опис кошика.
        items_text = ", ".join(self.items) if self.items else "(порожньо)"
        return f"Кошик клієнта: {self.client}\nТовари: {items_text}"

# реалізація класу Phone.
# Рівень заряду зберігаю як ціле число 0..100 та
# обмежую його в цих межах.
# Додав повідомлення при падінні нижче 20%.
class Phone:
    def __init__(self, name: str, battery_level: int = 100) -> None:
        self.name: str = name
        # значення в межах [0, 100], щоб уникнути некоректних станів.
        self.battery_level: int = max(0, min(int(battery_level), 100))

    def _adjust_battery(self, percent: float, mode: str) -> None:
        # єдина точка зміни заряду; mode: 'decrease' або 'increase'
        if percent is None:
            raise TypeError("Параметр percent має бути числом.")
        if mode not in ("decrease", "increase"):
            raise ValueError("Параметр mode має бути 'decrease' або 'increase'.")
        amount = max(0.0, float(percent))

        if mode == "decrease":
            new_level = int(max(0, self.battery_level - amount))
        else:
            new_level = int(min(100, self.battery_level + amount))

        self.battery_level = new_level

        # повідомлення показуємо лише при зменшенні і коли рівень нижче 20%.
        if mode == "decrease" and self.battery_level < 20:
            print(f"Увага: заряд батареї нижче 20% (поточний: {self.battery_level}%).")

    def decrease_battery(self, percent: float) -> None:
        # використовуємо спільний метод, щоб уникнути дублювання логіки.
        self._adjust_battery(percent, "decrease")

    def charging_battery(self, percent: float) -> None:
        # заряджаємо батарею через спільний механізм; вище 100% не піднімаємо.
        self._adjust_battery(percent, "increase")

    def get_info(self) -> str:
        # опис стану телефона.
        return f"Телефон {self.name}: заряд {self.battery_level}%"


# демонстрація роботи обох класів.
if __name__ == "__main__":
    # Cart
    print("-" * 40)

    cart = Cart("Ірина")
    cart.add_item("Хліб")
    cart.add_item("Молоко")
    cart.add_item("")  # буде проігноровано
    print(cart.get_info())
    removed = cart.remove_item("Хліб")
    print(f"Видалено 'Хліб'? {removed}")
    print(cart.get_info())

    print("-" * 40)
    print()

    # Phone
    print("-" * 40)
    phone = Phone("Samsung", battery_level=35)
    print(phone.get_info())
    phone.decrease_battery(20)  # опуститься до 15% і виведе попередження
    print(phone.get_info())
    phone.charging_battery(1)
    print(phone.get_info())
    phone.decrease_battery(20)  # не спрацює -4% не буде встановлено, 0%
    print(phone.get_info())
    phone.decrease_battery(20)  # не спрацює -5% не буде встановлено, 0%
    print(phone.get_info())
    phone.charging_battery(120) # буде встановлено, 100%
    print(phone.get_info())
