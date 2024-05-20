


class Merchant:
    def __init__(self, ID, name, gender, address,main_dish):
        self.ID=ID
        self.name = name
        self.gender = gender
        self.address = address
        self.main_dish = main_dish
    def __str__(self):
        return f""