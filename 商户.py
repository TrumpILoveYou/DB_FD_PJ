from 数据库连接 import DB
from 菜品 import Dish


class Merchant:
    def __init__(self, name, address, main_dish):
        # !!! self.id = id  # 对应数据库表中的 `id`
        self.name = name  # 对应数据库表中的 `name`
        self.address = address  # 对应数据库表中的 `address`
        self.main_dish = main_dish  # 对应数据库表中的 `main_dish`
        self.db=DB()

    def __str__(self):
        return (f"Merchant ID: {self.id}\n"
                f"Name: {self.name}\n"
                f"Address: {self.address}\n"
                f"Main Dish: {self.main_dish}\n")
    def add_dish(self, dish_info:Dish):
        sql = """INSERT INTO dishes 
                 (merchant_id,name, price, category, description, image, ingredients, nutrition_information, allergens, queue_sales, online_sales, collection_count) 
                 VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (dish_info.merchant_id,dish_info.name, dish_info.price, dish_info.category, dish_info.description, dish_info.image, dish_info.ingredients,
                  dish_info.nutrition_information, dish_info.allergens, 0,0,0)
        self.db.execute(sql, values)
        self.db.close()

    def update_dish(self, dish_id, dish_info: Dish):
        sql = """UPDATE dishes SET name = %s, price = %s, category = %s, description = %s, image = %s, ingredients = %s, 
                 nutrition_information = %s, allergens = %s, queue_sales = %s, online_sales = %s, collection_count = %s 
                 WHERE id = %s"""
        values = (dish_info.name, dish_info.price, dish_info.category, dish_info.description, dish_info.image,
                  dish_info.ingredients, dish_info.nutrition_information, dish_info.allergens, dish_info.queue_sales,
                  dish_info.online_sales, dish_info.collection_count, dish_id)
        self.db.execute(sql, values)
        self.db.close()

    def delete_dish(self, dish_id):
        sql = "DELETE FROM dishes WHERE id = %s"
        values = (dish_id,)
        self.db.execute(sql, values)
        self.db.close()
