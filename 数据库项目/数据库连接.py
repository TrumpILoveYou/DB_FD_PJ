from pymysql import Connection
from 商户 import Merchant
import 商户
from 用户 import User

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

    def insert_user(self, user: User):
        sql = "INSERT INTO users (id, name, gender, student_id, account_information) VALUES (%s, %s, %s, %s, %s)"
        values = (user.id, user.name, user.gender, user.student_id, user.account_information)
        self.execute(sql, values)

    def delete_user(self, user_id: int):
        sql = "DELETE FROM users WHERE id = %s"
        values = (user_id,)
        self.execute(sql, values)

    def update_user(self, user: User):
        sql = "UPDATE users SET name = %s, gender = %s, student_id = %s, account_information = %s WHERE id = %s"
        values = (user.name, user.gender, user.student_id, user.account_information, user.id)
        self.execute(sql, values)

    def insert_merchant(self, merchant: Merchant):
        sql = "INSERT INTO merchants (id, name, address, main_dish) VALUES (%s, %s, %s, %s)"
        values = (merchant.id, merchant.name, merchant.address, merchant.main_dish)
        self.execute(sql, values)

    def delete_merchant(self, merchant_id: int):
        sql = "DELETE FROM merchants WHERE id = %s"
        values = (merchant_id,)
        self.execute(sql, values)

    def update_merchant(self, merchant: Merchant):
        sql = "UPDATE merchants SET name = %s, address = %s, main_dish = %s WHERE id = %s"
        values = (merchant.name, merchant.address, merchant.main_dish, merchant.id)
        self.execute(sql, values)


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