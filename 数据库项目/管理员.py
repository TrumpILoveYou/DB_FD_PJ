from 数据库连接 import DB
from 商户 import Merchant

class Manager:
    def __init__(self, id, name):
        self.id = id  # 对应数据库表中的 `id`
        self.name = name  # 对应数据库表中的 `name`

    def __str__(self):
        return f"Manager ID: {self.id}\nName: {self.name}"

    def insert_merchant(self, merchant: Merchant):
        db = DB()
        sql = "INSERT INTO merchants (id, name, address, main_dish) VALUES (%s, %s, %s, %s)"
        values = (merchant.id, merchant.name, merchant.address, merchant.main_dish)
        db.do(sql, values)
        db.close()

    def delete_merchant(self, merchant: Merchant):
        db = DB()
        sql = "DELETE FROM merchants WHERE id=%s"
        values = (merchant.id,)
        db.do(sql, values)
        db.close()

    def update_merchant(self, merchant: Merchant):
        db = DB()
        sql = """
        UPDATE merchants 
        SET name=%s, address=%s, main_dish=%s 
        WHERE id=%s
        """
        values = (merchant.name, merchant.address, merchant.main_dish, merchant.id)
        db.do(sql, values)
        db.close()
