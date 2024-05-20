from pymysql import Connection
from 用户 import User
from 商户 import Merchant
from 菜品 import Dish

#text_file_reader=TextFileReader(" ")

#user_data:list[User]=text_file_reader.read_data()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DB:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DB, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.conn = Connection(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="123456",
            autocommit=True,
        )
        self.conn.select_db("食堂")
        self.cursor = self.conn.cursor()

    def execute(self, sql, values=None):
        if values:
            self.cursor.execute(sql, values)
        else:
            self.cursor.execute(sql)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
        self._initialized = False

class Admin:
    def __init__(self):
        self.db = DB()

    def get_user_info(self, user_id):
        sql = "SELECT * FROM users WHERE id = %s"
        values = (user_id,)
        result = self.db.execute(sql, values)
        return result

    def add_user(self, user_info: User):
        sql = "INSERT INTO users (id, name, gender, student_id, account_information) VALUES (%s, %s, %s, %s, %s)"
        values = (user_info.id, user_info.name, user_info.gender, user_info.student_id, user_info.account_information)
        self.db.execute(sql, values)

    def update_user(self, user_id, user_info: User):
        sql = "UPDATE users SET name = %s, gender = %s, student_id = %s, account_information = %s WHERE id = %s"
        values = (user_info.name, user_info.gender, user_info.student_id, user_info.account_information, user_id)
        self.db.execute(sql, values)

    def delete_user(self, user_id):
        sql = "DELETE FROM users WHERE id = %s"
        values = (user_id,)
        self.db.execute(sql, values)

    def get_business_info(self, business_id):
        sql = "SELECT * FROM merchants WHERE id = %s"
        values = (business_id,)
        result = self.db.execute(sql, values)
        return result

    def add_business(self, business_info: Merchant):
        sql = "INSERT INTO merchants (id, name, address, main_dish) VALUES (%s, %s, %s, %s)"
        values = (business_info.id, business_info.name, business_info.address, business_info.main_dish)
        self.db.execute(sql, values)

    def update_business(self, business_id, business_info: Merchant):
        sql = "UPDATE merchants SET name = %s, address = %s, main_dish = %s WHERE id = %s"
        values = (business_info.name, business_info.address, business_info.main_dish, business_id)
        self.db.execute(sql, values)

    def delete_business(self, business_id):
        sql = "DELETE FROM merchants WHERE id = %s"
        values = (business_id,)
        self.db.execute(sql, values)

class MerchantOperations:
    def __init__(self):
        self.db = DB()

    def add_dish(self, dish_info: Dish):
        sql = """INSERT INTO dishes 
                 (id, name, price, category, description, image, ingredients, nutrition_information, allergens, queue_sales, online_sales, collection_count) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (dish_info.id, dish_info.name, dish_info.price, dish_info.category, dish_info.description, dish_info.image, 
                  dish_info.ingredients, dish_info.nutrition_information, dish_info.allergens, dish_info.queue_sales, 
                  dish_info.online_sales, dish_info.collection_count)
        self.db.execute(sql, values)

    def update_dish(self, dish_id, dish_info: Dish):
        sql = """UPDATE dishes SET name = %s, price = %s, category = %s, description = %s, image = %s, ingredients = %s, 
                 nutrition_information = %s, allergens = %s, queue_sales = %s, online_sales = %s, collection_count = %s 
                 WHERE id = %s"""
        values = (dish_info.name, dish_info.price, dish_info.category, dish_info.description, dish_info.image, 
                  dish_info.ingredients, dish_info.nutrition_information, dish_info.allergens, dish_info.queue_sales, 
                  dish_info.online_sales, dish_info.collection_count, dish_id)
        self.db.execute(sql, values)

    def delete_dish(self, dish_id):
        sql = "DELETE FROM dishes WHERE id = %s"
        values = (dish_id,)
        self.db.execute(sql, values)

#print(conn.get_server_info())


#cursor.execute("create table test_pymysql(id int);")
#cursor.execute("select * from students")

#cursor.execute("insert into students values(100,'ld')")
#conn.commit()

#list[商户]

#result:tuple=cursor.fetchall()
#for r in result:
 #   print(r)


#sql=....     cursor.execute("sql")
#conn.close()