from 数据库连接 import DB
from 商户 import Merchant


class manager:
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name

    def __str__(self):
        return f""

    def insert_business(self, business: Business):
        db = DB()
        sql = "insert into business (ID, name, gender, address, main_dish) values (%s, %s, %s, %s, %s)"
        values = (business.ID, business.name, business.gender, business.address, business.main_dish)
        db.do(sql, values)
        db.close()

    def delete_business(self, business: Business):
        db = DB()
        sql = "delete from business where ID=%s"
        values = (business.ID)
        db.do(sql, values)
        db.close()

    def update_business(self, business: Business):
        db = DB()
       # sql = "update business set where ID=%s"
        values = (business.ID)
        #db.do(sql, values)
        db.close()
        

