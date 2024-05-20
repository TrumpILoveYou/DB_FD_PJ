from pymysql import Connection
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
        self.do = self.cursor.execute
        self.show = self.cursor.fetchall

    def close(self):
        self.cursor.close()
        self.conn.close()
        self._initialized = False


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