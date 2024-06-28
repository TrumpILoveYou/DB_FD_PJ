from pymysql import Connection

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

        #  修改点
        self.conn = Connection(
            host="localhost",
            port=3306,
            user="root",
            password="", # password
            autocommit=True,
        )
        self.conn.select_db("canteen")
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




