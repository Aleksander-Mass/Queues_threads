import random
import time
from threading import Thread
from queue import Queue

###  Создайте 3 класса: Table, Guest и Cafe.

# Класс для стола
class Table:
    def __init__(self, number):
        self.number = number  # Обладать атрибутами number - номер стола
        self.guest = None  # Гость за столом (по умолчанию None)

# Класс для гостя
class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name   # Обладать атрибутом name - имя гостя

    def run(self):
        # Гость "ест" случайное время от 3 до 10 секунд
        time.sleep(random.randint(3, 10))

# Класс для кафе
class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()  # Очередь гостей
        self.tables = list(tables)  # Столы в кафе

    # Обладать методами guest_arrival (прибытие гостей) и discuss_guests (обслужить гостей).

    def guest_arrival(self, *guests):
        for guest in guests:
            # Проверяем, есть ли свободный стол
            free_table = next((table for table in self.tables if table.guest is None), None)
            if free_table is not None:
                # Если свободный стол найден, сажаем гостя и запускаем поток
                free_table.guest = guest
                guest.start()
                print(f"{guest.name} сел(-а) за стол номер {free_table.number}")
            else:
                # Если свободных столов нет, добавляем гостя в очередь
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        # Обслуживание пока есть гости или очередь
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                guest = table.guest
                if guest and not guest.is_alive():  # Проверяем, завершился ли поток
                    print(f"{guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None  # Освобождаем стол

                    # Если очередь не пуста, берем гостя из очереди и сажаем за стол
                    if not self.queue.empty():
                        next_guest = self.queue.get()
                        table.guest = next_guest
                        next_guest.start()
                        print(f"{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")

            time.sleep(1)  # Задержка, чтобы уменьшить частоту проверок состояния потоков

# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()

###   Вывод на консоль:
"""
Maria сел(-а) за стол номер 1
Oleg сел(-а) за стол номер 2
Vakhtang сел(-а) за стол номер 3
Sergey сел(-а) за стол номер 4
Darya сел(-а) за стол номер 5
Arman в очереди
Vitoria в очереди
Nikita в очереди
Galina в очереди
Pavel в очереди
Ilya в очереди
Alexandra в очереди
Darya покушал(-а) и ушёл(ушла)
Стол номер 5 свободен
Arman вышел(-ла) из очереди и сел(-а) за стол номер 5
Sergey покушал(-а) и ушёл(ушла)
Стол номер 4 свободен
Vitoria вышел(-ла) из очереди и сел(-а) за стол номер 4
Arman покушал(-а) и ушёл(ушла)
Стол номер 5 свободен
Nikita вышел(-ла) из очереди и сел(-а) за стол номер 5
Vakhtang покушал(-а) и ушёл(ушла)
Стол номер 3 свободен
Galina вышел(-ла) из очереди и сел(-а) за стол номер 3
Maria покушал(-а) и ушёл(ушла)
Стол номер 1 свободен
Pavel вышел(-ла) из очереди и сел(-а) за стол номер 1
Oleg покушал(-а) и ушёл(ушла)
Стол номер 2 свободен
Ilya вышел(-ла) из очереди и сел(-а) за стол номер 2
Vitoria покушал(-а) и ушёл(ушла)
Стол номер 4 свободен
Alexandra вышел(-ла) из очереди и сел(-а) за стол номер 4
Pavel покушал(-а) и ушёл(ушла)
Стол номер 1 свободен
Galina покушал(-а) и ушёл(ушла)
Стол номер 3 свободен
Nikita покушал(-а) и ушёл(ушла)
Стол номер 5 свободен
Alexandra покушал(-а) и ушёл(ушла)
Стол номер 4 свободен
Ilya покушал(-а) и ушёл(ушла)
Стол номер 2 свободен

"""