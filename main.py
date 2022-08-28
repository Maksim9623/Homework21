from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def __init__(self, items, capacity):
        self.items = items
        self.capacity = capacity

    @abstractmethod
    def add(self, title, count):
        pass

    @abstractmethod
    def remove(self, title, count):
        pass

    @property
    @abstractmethod
    def get_free_space(self):
        pass

    @property
    @abstractmethod
    def get_items(self):
        pass

    @property
    @abstractmethod
    def get_unique_items_count(self):
        pass


class Store(Storage):
    def __init__(self):
        self._items = {}
        self._capacity = 100

    def add(self, title, count):
        if title in self._items:
            self._items[title] += count
        else:
            self._items[title] = count
        self._capacity -= count

    def remove(self, title, count):
        result = self._items[title] - count
        if result > 0:
            self._items[title] = result
        else:
            del self._items[title]
        self._capacity += count

    @property
    def get_free_space(self):
        # возврвщает кол-во свободных мест
        return self._capacity

    @property
    def get_items(self):
        # возвращает содержание склада
        return self._items

    @get_items.setter
    def get_items(self, new_items):
        self._items = new_items
        self._capacity -= sum(self._items.values())

    @property
    def get_unique_items_count(self):
        # возвращает кол-во уникальных товаров
        return len(self._items.keys())


class Shop(Store):
    def __init__(self):
        super().__init__()
        self._capacity = 20


class Request:
    def __init__(self, info):
        self.info = self._split_info(info)
        self.from_ = self.info[4]
        self.to = self.info[6]
        self.amount = int(self.info[1])
        self.product = self.info[2]

    @staticmethod
    def _split_info(info):
        return info.split(' ')

    def __repr__(self):
        return f"Доставить {self.amount} {self.product} из {self.from_} в {self.to}"


def main():
    while(True):
        user_input = input("Введите запрос: ")

        if user_input == 'stop':
            break

        request = Request(user_input)

        if request.from_ == request.to:
            print('Пункт назначения == Пункту отправления')
            continue
        if request.from_ == 'склад':
            if request.product in store.get_items:
                print(f'Нужный товар есть в пункте \"{request.from_}\" ')
            else:
                print(f'В пункте \"{request.from_}\" нет такого товара')
                continue

            if store.get_items[request.product] >= request.amount:
                print(f"Нужное колличество есть в пункте \"{request.from_}\"")
            else:
                print(f'В пункте \"{request.from_}\" не хватает {request.amount - store.get_items[request.product]}')
                continue

            if shop.get_free_space >= request.amount:
                print(f'В пункте \"{request.to}\" достаточно места')
            else:
                print(f'В пункте \"{request.to}\" не хватает {request.amount - shop.get_free_space} места')
                continue

            if request.to == "магазин" and shop.get_unique_items_count == 5 and request.product not in shop.items:
                print('В магазине достаточно уникальных значений')
                continue

            store.remove(request.product, request.amount)
            print(f'Курьер забрал {request.amount} {request.product} со {request.from_}')
            print(f'Курьер забрал {request.amount} {request.product} со {request.from_} в {request.to}')

            shop.add(request.product, request.amount)
            print(f'Курьер доставил {request.amount} {request.product} в  {request.to}')
        else:
            if request.product in shop.get_items:
                print(f'Нужный товар есть в пункте \"{request.from_}\" ')
            else:
                print(f'В пункте \"{request.from_}\" нет такого товара')
                continue

            if shop.get_items[request.product] >= request.amount:
                print(f"Нужное колличество есть в пункте \"{request.from_}\"")
            else:
                print(f'В пункте \"{request.from_}\" не хватает {request.amount - shop.get_items[request.product]} места')
                continue

            if store.get_free_space >= request.amount:
                print(f'В пункте \"{request.to}\" достаточно места')
            else:
                print(f'В пункте \"{request.to}\" не хватает {request.amount - store.get_free_space}')
                continue

            shop.remove(request.product, request.amount)
            print(f'Курьер забрал {request.amount} {request.product} со {request.from_}')
            print(f'Курьер забрал {request.amount} {request.product} со {request.from_} в {request.to}')

            store.add(request.product, request.amount)
            print(f'Курьер доставил {request.amount} {request.product} в  {request.to}')

        print('==' * 30)
        print('На складе: ')
        for title, count in store.get_items.items():
            print(f'{title}: {count}')
        print('==' * 30)

        print('В магазине: ')
        for title, count in shop.get_items.items():
            print(f'{title}: {count}')
        print('==' * 30)


if __name__ == "__main__":
    store = Store()
    shop = Shop()

    store_items = {
        "хлеб": 10,
        "мороженное": 20,
        "чипсы": 5,
        "печеньки": 15,
    }

    store.get_items = store_items

    main()
