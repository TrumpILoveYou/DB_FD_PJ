from 数据库连接 import DB
from 订单 import Order


class User:
    def __init__(self, id, name, gender, student_id, account_information,role,age):
        self.id = id  # 对应数据库表中的 `id`
        self.name = name  # 对应数据库表中的 `name`
        self.gender = gender  # 对应数据库表中的 `gender`
        self.student_id = student_id  # 对应数据库表中的 `student_id`
        self.account_information = account_information  # 对应数据库表中的 `account_information`
        self.role=role
        self.age=age
        self.db = DB()

    def __str__(self):
        return (f"User ID: {self.id}\n"
                f"Name: {self.name}\n"
                f"Gender: {self.gender}\n"
                f"Student ID: {self.student_id}\n"
                f"Account Information: {self.account_information}\n")

    def createOrder(self, orderInfo: Order):
        sql = "INSERT INTO orders (user_id,merchant_id,dish_id,order_status,method) VALUES (%s, %s, %s, %s,%s,%s)"
        values = (self.id, orderInfo.merchant_id, orderInfo.dish_id,orderInfo.order_status,orderInfo.method)
        self.db.execute(sql, values)
        self.db.close()

    def getOrderInfo(self, order_id):
        sql = ("SELECT * FROM orders WHERE user_id = %s and orders.id=%s ")
        values = (self.id, order_id)
        result = self.db.execute(sql, values)
        self.db.close()
        return result

    def getUserHistoryOrders(self, userID, page, pageSize):
        offset = (page - 1) * pageSize
        sql = ("SELECT * FROM orders WHERE user_id = %s ORDER BY id LIMIT %s OFFSET %s")
        values = (userID, pageSize, offset)
        result = self.db.execute(sql, values)
        self.db.close()
        return result

    def comment(self, merchant_id, dish_id, score, content):
        if dish_id:
            sql = "INSERT INTO comments (user_id,merchant_id,dish_id,score,content) VALUES (%s, %s, %s, %s,%s)"
            values = (self.id, merchant_id, dish_id, score, content)
        else:
            sql = "INSERT INTO comments (user_id,merchant_id,score,content) VALUES (%s, %s, %s)"
            values = (self.id, merchant_id, score, content)
        self.db.execute(sql, values)
        self.db.close()

    def searchMerchants(self, page, pageSize):
        offset = (page - 1) * pageSize
        sql = ("SELECT * FROM merchants ORDER BY id LIMIT %s OFFSET %s")
        values = (pageSize, offset)
        result = self.db.execute(sql, values)
        self.db.close()
        return result

    def getMerchantAllInfos(self, merchant_id, page, pageSize):
        offset = (page - 1) * pageSize
        sql = ("SELECT merchants.id,merchants.name,merchants.address,merchants.main_dish,dishes.id,dishes.name,"
               "dishes.description,comments.score,comments.content   FROM merchants,dishes,comments where "
               "merchants.id=%s and"
               "comments.merchant_id=merchants.id and comments.dish_id=null and"
               "dishes.merchant_id=merchants.id LIMIT %s OFFSET %s")
        values = (merchant_id, pageSize, offset)

        result = self.db.execute(sql, values)
        self.db.close()
        return result

    def getDishInfos(self, merchant_id, dish_id, page, pageSize):
        offset = (page - 1) * pageSize
        sql = ("SELECT id,name,price,picture FROM dishes where merchant_id=%s and id=%s  LIMIT %s OFFSET %s")
        values = (merchant_id, dish_id, pageSize, offset)
        result = self.db.execute(sql, values)
        self.db.close()
        return result

    def getDishAllInfos(self, merchant_id, dish_id, page, pageSize):
        offset = (page - 1) * pageSize
        sql = ("SELECT * FROM dishes where merchant_id=%s and id=%s  LIMIT %s OFFSET %s")
        values = (merchant_id, dish_id, pageSize, offset)
        result = self.db.execute(sql, values)
        self.db.close()
        return result

    def getMerchantDishFavorites(self, merchant_id, page, pageSize):
        offset = (page - 1) * pageSize
        sql = ("SELECT id,name,collection_count FROM dishes  where dishes.merchant_id=%s  LIMIT %s OFFSET %s")
        values = (merchant_id, pageSize, offset)
        result = self.db.execute(sql, values)
        self.db.close()
        return result

    def addFavorites(self, merchant_id, dish_id):
        if dish_id:
            sql = "INSERT INTO collections (user_id,merchant_id,dish_id) VALUES (%s, %s, %s)"
            values = (self.id, merchant_id, dish_id)
        else:
            sql = "INSERT INTO collections (user_id,merchant_id) VALUES (%s, %s)"
            values = (self.id, merchant_id)
        self.db.execute(sql, values)
        self.db.close()
