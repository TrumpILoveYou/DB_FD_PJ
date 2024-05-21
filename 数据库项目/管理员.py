from 数据库连接 import DB
from 商户 import Merchant
from 用户 import User

class Manager:
    def __init__(self, id, name):
        self.id = id  # 对应数据库表中的 `id`
        self.name = name  # 对应数据库表中的 `name`
        self.db=DB()

    def __str__(self):
        return f"Manager ID: {self.id}\nName: {self.name}"

    def get_user_info(self, user_id,page, pageSize):
        offset = (page - 1) * pageSize
        sql = "SELECT * FROM users WHERE id = %s LIMIT %s OFFSET %s"
        values = (user_id,pageSize, offset)
        result = self.db.execute(sql, values)
        self.db.close()
        return result

    def add_user(self, user_info:User):
        sql = "INSERT INTO users (name, gender, student_id, account_information,role,age) VALUES (%s, %s, %s, %s)"
        values = (user_info.name, user_info.gender, user_info.student_id, user_info.account_information,user_info.role,user_info.age)
        self.db.execute(sql, values)
        self.db.close()

    def update_user(self, user_id, user_info:User):
        sql = "UPDATE users SET name = %s, gender = %s, student_id = %s, account_information = %s,role=%s,age=%s WHERE id = %s"
        values = (user_info.name, user_info.gender, user_info.student_id, user_info.account_information,user_info.role,user_info.age, user_id)
        self.db.execute(sql, values)
        self.db.close()

    def delete_user(self, user_id):
        sql = "DELETE FROM users WHERE id = %s"
        values = (user_id,)
        self.db.execute(sql, values)
        self.db.close()

    def get_merchant_info(self, merchant_id, page, pageSize):

        offset = (page - 1) * pageSize
        sql = "SELECT * FROM merchants WHERE id = %s LIMIT %s OFFSET %s"
        values = (merchant_id,pageSize, offset)
        result = self.db.execute(sql, values)
        self.db.close()
        return result

    def add_merchant(self, merchant_info:Merchant):
        sql = "INSERT INTO merchants (name, address, main_dish) VALUES (%s, %s, %s)"
        values = (merchant_info.name, merchant_info.address,merchant_info.main_dish)
        self.db.execute(sql, values)
        self.db.close()

    def update_merchant(self, merchant_id, merchant_info:Merchant):
        sql = "UPDATE merchants SET name = %s, address = %s, main_dish = %s WHERE id = %s"
        values = (merchant_info.name, merchant_info.address,merchant_info.main_dish, merchant_id)
        self.db.execute(sql, values)
        self.db.close()

    def delete_business(self, business_id):
        sql = "DELETE FROM merchants WHERE id = %s"
        values = (business_id,)
        self.db.execute(sql, values)
        self.db.close()
