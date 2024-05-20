class Merchant:
    def __init__(self, id, name, address, main_dish):
        self.id = id  # 对应数据库表中的 `id`
        self.name = name  # 对应数据库表中的 `name`
        self.address = address  # 对应数据库表中的 `address`
        self.main_dish = main_dish  # 对应数据库表中的 `main_dish`

    def __str__(self):
        return (f"Merchant ID: {self.id}\n"
                f"Name: {self.name}\n"
                f"Address: {self.address}\n"
                f"Main Dish: {self.main_dish}\n")
