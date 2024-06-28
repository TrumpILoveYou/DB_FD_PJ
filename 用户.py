from 数据库连接 import DB
from 订单 import Order
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, 
    QLineEdit, QLabel, QMessageBox, QTableWidget, QTableWidgetItem, QFormLayout
)
import sys

class User:
    def __init__(self, name, gender, student_id, account_information,role,age):
        self.id = None  # 对应数据库表中的 `id`
        self.name = name  # 对应数据库表中的 `name`
        self.gender = gender  # 对应数据库表中的 `gender`
        self.student_id = student_id  # 对应数据库表中的 `student_id`
        self.account_information = account_information  # 对应数据库表中的 `account_information`
        self.role = role
        self.age=age
        self.db = DB()

    def __str__(self):
        return (f"User ID: {self.id}\n"
                f"Name: {self.name}\n"
                f"Gender: {self.gender}\n"
                f"Student ID: {self.student_id}\n"
                f"Account Information: {self.account_information}\n")

    def getSelfInfo_user(self):
        sql=("SELECT * FROM users WHERE id = %s ")
        values=(self.id)
        result = self.db.execute(sql, values)
        return result

    def createOrder(self, orderInfo: Order):
        sql = "INSERT INTO orders (user_id,merchant_id,dish_id,order_status,method) VALUES (%s, %s, %s,%s,%s)"
        values = (self.id, orderInfo.merchant_id, orderInfo.dish_id, "preparing", orderInfo.method)
        self.db.execute(sql, values)

    def getOrderInfo(self, order_id):
        sql = ("SELECT * FROM orders WHERE user_id = %s and orders.id=%s ")
        values = (self.id, order_id)
        result = self.db.execute(sql, values)
        return result

    def getUserHistoryOrders(self):
        sql = "SELECT * FROM orders WHERE user_id = %s ORDER BY id"
        values = (self.id,)
        result = self.db.execute(sql, values)
        return result


    def comment(self, merchant_id, dish_id, score, content):
        if dish_id:
            sql = "INSERT INTO comments (user_id,merchant_id,dish_id,score,content) VALUES (%s, %s, %s, %s,%s)"
            values = (self.id, merchant_id, dish_id, score, content)
        else:
            sql = "INSERT INTO comments (user_id,merchant_id,score,content) VALUES (%s, %s, %s, %s)"
            values = (self.id, merchant_id, score, content)
        self.db.execute(sql, values)

    def searchMerchants(self):
        sql = "SELECT * FROM merchants ORDER BY id"
        result = self.db.execute(sql)
        return result


    def getMerchantAllInfos(self, merchant_id):
        sql = ("SELECT merchants.id, merchants.name, merchants.address, merchants.main_dish, dishes.id AS dish_id, dishes.name AS dish_name, "
            "dishes.description, comments.score, comments.content "
            "FROM merchants "
            "JOIN dishes ON dishes.merchant_id = merchants.id "
            "LEFT JOIN comments ON comments.merchant_id = merchants.id AND comments.dish_id IS NULL "
            "WHERE merchants.id = %s")
        values = (merchant_id,)
        result = self.db.execute(sql, values)
        return result


    def getDishInfos(self, merchant_id):
        sql = "SELECT id, name, price, image FROM dishes WHERE merchant_id = %s"
        values = (merchant_id)
        result = self.db.execute(sql, values)
        return result


    def getDishAllInfos(self, merchant_id, dish_id):
        sql = "SELECT * FROM dishes WHERE merchant_id = %s AND id = %s"
        values = (merchant_id, dish_id)
        result = self.db.execute(sql, values)
        return result

    def getMerchantDishFavorites(self, merchant_id):
        sql = "SELECT id, name, collection_count FROM dishes WHERE merchant_id = %s"
        values = (merchant_id,)
        result = self.db.execute(sql, values)
        return result

    def addFavorites(self, merchant_id, dish_id=None):
        if dish_id:
            sql = "INSERT INTO collections (user_id,merchant_id,dish_id) VALUES (%s, %s, %s)"
            values = (self.id, merchant_id, dish_id)
        else:
            sql = "INSERT INTO collections (user_id,merchant_id) VALUES (%s, %s)"
            values = (self.id, merchant_id)
        self.db.execute(sql, values)


class UserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Management")
        self.setGeometry(100, 100, 800, 600)
        self.db = DB()

        # 创建用户实例
        self.user = User(name="", gender="", student_id="", account_information="", role="", age=0)

        # 创建主窗口部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建布局
        self.layout = QVBoxLayout()

        # 创建左侧布局和部件
        self.left_layout = QVBoxLayout()
        self.user_id_label = QLabel("User ID:")
        self.user_id_input = QLineEdit()
        self.order_id_label = QLabel("Order ID:")
        self.order_id_input = QLineEdit()
        self.merchant_id_label = QLabel("Merchant ID:")
        self.merchant_id_input = QLineEdit()
        self.dish_id_label = QLabel("Dish ID:")
        self.dish_id_input = QLineEdit()
        self.order_method_label = QLabel("Order Method:")
        self.order_method_input = QLineEdit()

        self.create_order_button = QPushButton("Create Order")
        self.create_order_button.clicked.connect(self.create_order_frontend)

        self.get_order_info_button = QPushButton("Get Order Info")
        self.get_order_info_button.clicked.connect(self.get_order_info_frontend)

        self.get_user_history_button = QPushButton("Get User History Orders")
        self.get_user_history_button.clicked.connect(self.get_user_history_orders_frontend)

        self.search_merchants_button = QPushButton("Search Merchants")
        self.search_merchants_button.clicked.connect(self.search_merchants_frontend)

        self.get_merchant_all_infos_button = QPushButton("Get Merchant All Infos")
        self.get_merchant_all_infos_button.clicked.connect(self.get_merchant_all_infos_frontend)

        self.get_dish_info_button = QPushButton("Get Dish Info")
        self.get_dish_info_button.clicked.connect(self.get_dish_info_frontend)

        self.get_dish_all_info_button = QPushButton("Get Dish All Info")
        self.get_dish_all_info_button.clicked.connect(self.get_dish_all_info_frontend)

        self.get_merchant_dish_favorites_button = QPushButton("Get Merchant Dish Favorites")
        self.get_merchant_dish_favorites_button.clicked.connect(self.get_merchant_dish_favorites_frontend)

        self.add_favorites_button = QPushButton("Add Favorites")
        self.add_favorites_button.clicked.connect(self.add_favorites_frontend)

        # 添加左侧部件到左侧布局
        self.left_layout.addWidget(self.user_id_label)
        self.left_layout.addWidget(self.user_id_input)
        self.left_layout.addWidget(self.order_id_label)
        self.left_layout.addWidget(self.order_id_input)
        self.left_layout.addWidget(self.merchant_id_label)
        self.left_layout.addWidget(self.merchant_id_input)
        self.left_layout.addWidget(self.dish_id_label)
        self.left_layout.addWidget(self.dish_id_input)
        self.left_layout.addWidget(self.order_method_label)
        self.left_layout.addWidget(self.order_method_input)
        self.left_layout.addWidget(self.create_order_button)
        self.left_layout.addWidget(self.get_dish_info_button)
        self.left_layout.addWidget(self.get_dish_all_info_button)
        self.left_layout.addWidget(self.get_order_info_button)
        self.left_layout.addWidget(self.get_user_history_button)
        self.left_layout.addWidget(self.search_merchants_button)
        self.left_layout.addWidget(self.get_merchant_all_infos_button)
        self.left_layout.addWidget(self.get_merchant_dish_favorites_button)
        self.left_layout.addWidget(self.add_favorites_button)

        # 创建右侧布局和部件
        self.right_layout = QVBoxLayout()
        self.comment_merchant_id_label = QLabel("Merchant ID:")
        self.comment_merchant_id_input = QLineEdit()
        self.comment_dish_id_label = QLabel("Dish ID (optional):")
        self.comment_dish_id_input = QLineEdit()
        self.comment_score_label = QLabel("Score:")
        self.comment_score_input = QLineEdit()
        self.comment_content_label = QLabel("Content:")
        self.comment_content_input = QLineEdit()

        self.comment_button = QPushButton("Comment")
        self.comment_button.clicked.connect(self.comment_frontend)

        # 添加右侧部件到右侧布局
        self.right_layout.addWidget(self.comment_merchant_id_label)
        self.right_layout.addWidget(self.comment_merchant_id_input)
        self.right_layout.addWidget(self.comment_dish_id_label)
        self.right_layout.addWidget(self.comment_dish_id_input)
        self.right_layout.addWidget(self.comment_score_label)
        self.right_layout.addWidget(self.comment_score_input)
        self.right_layout.addWidget(self.comment_content_label)
        self.right_layout.addWidget(self.comment_content_input)
        self.right_layout.addWidget(self.comment_button)

        # 创建表格部件
        self.table_widget = QTableWidget()
        
        # 添加表格到主布局
        self.layout.addLayout(self.left_layout)
        self.layout.addWidget(self.table_widget)
        self.layout.addLayout(self.right_layout)

        # 设置主窗口布局
        self.central_widget.setLayout(self.layout)

    def set_user(self, user_id):
        self.user_id = user_id
        sql = "SELECT * FROM users WHERE id = %s"
        result = self.db.execute(sql, (user_id,))
        if result:
            user_data = result[0]
            self.user = User(name=user_data[1], gender=user_data[2], student_id=user_data[3],
                             account_information=user_data[4], role=user_data[5], age=user_data[6])
            self.user.id = user_data[0]  # set user id
            print('user set!')

    def create_order_frontend(self):
        merchant_id = self.merchant_id_input.text()
        dish_id = self.dish_id_input.text()
        order_method = self.order_method_input.text()

        if not all([merchant_id, dish_id, order_method]):
            QMessageBox.warning(self, "Input Error", "All fields are required")
            return

        if (not order_method=="queue") and (not order_method=="online"):
            QMessageBox.warning(self, "Input Error", "queue or online")
            return

        if not merchant_id.isdigit() or not dish_id.isdigit():
            QMessageBox.warning(self, "Input Error", "Merchant ID and Dish ID must be numbers")
            return

        order_info = Order(id=None, user_id=0, merchant_id=int(merchant_id), dish_id=int(dish_id), order_status="preparing", method=order_method)

        # 调用用户实例的 createOrder 方法
        self.user.createOrder(order_info)

        QMessageBox.information(self, "Success", "Order created successfully")
        self.clear_inputs()

    def get_order_info_frontend(self):
        order_id = self.order_id_input.text()

        if not order_id:
            QMessageBox.warning(self, "Input Error", "Order ID is required")
            return

        if not order_id.isdigit():
            QMessageBox.warning(self, "Input Error", "Order ID must be a number")
            return

        # 调用用户实例的 getOrderInfo 方法
        order_info = self.user.getOrderInfo(int(order_id))

        if not order_info:
            QMessageBox.warning(self, "No Data", "No order found with the given ID")
            return

        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(len(order_info[0]))
        self.table_widget.setHorizontalHeaderLabels([desc[0] for desc in self.db.cursor.description])

        for row_data in order_info:
            row = self.table_widget.rowCount()
            self.table_widget.insertRow(row)
            for column, data in enumerate(row_data):
                self.table_widget.setItem(row, column, QTableWidgetItem(str(data)))

    def get_user_history_orders_frontend(self):
        # 调用用户实例的 getUserHistoryOrders 方法
        history_orders = self.user.getUserHistoryOrders()

        if not history_orders:
            QMessageBox.warning(self, "No Data", "No history orders found for the user")
            return

        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(len(history_orders[0]))
        self.table_widget.setHorizontalHeaderLabels([desc[0] for desc in self.db.cursor.description])

        for row_data in history_orders:
            row = self.table_widget.rowCount()
            self.table_widget.insertRow(row)
            for column, data in enumerate(row_data):
                self.table_widget.setItem(row, column, QTableWidgetItem(str(data)))

    def search_merchants_frontend(self):
        # 调用用户实例的 searchMerchants 方法
        merchants = self.user.searchMerchants()

        if not merchants:
            QMessageBox.warning(self, "No Data", "No merchants found")
            return

        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(len(merchants[0]))
        self.table_widget.setHorizontalHeaderLabels([desc[0] for desc in self.db.cursor.description])

        for row_data in merchants:
            row = self.table_widget.rowCount()
            self.table_widget.insertRow(row)
            for column, data in enumerate(row_data):
                if not column==4:
                  self.table_widget.setItem(row, column, QTableWidgetItem(str(data)))

    def comment_frontend(self):
        merchant_id = self.comment_merchant_id_input.text()
        dish_id = self.comment_dish_id_input.text()

        score = self.comment_score_input.text()
        content = self.comment_content_input.text()

        if not all([merchant_id, score, content]):
            QMessageBox.warning(self, "Input Error", "All fields except Dish ID are required")
            return

        if not merchant_id.isdigit() or (dish_id and not dish_id.isdigit()):
            QMessageBox.warning(self, "Input Error", "Merchant ID and Dish ID must be numbers")
            return

        if not score.isdigit() or not (1 <= int(score) <= 5):
            QMessageBox.warning(self, "Input Error", "Score must be a number between 1 and 5")
            return


        self.user.comment(int(merchant_id), int(dish_id) if dish_id and dish_id.isdigit() else None, int(score), content)



        QMessageBox.information(self, "Success", "Comment added successfully")
        self.clear_comment_inputs()

    def get_merchant_all_infos_frontend(self):
        merchant_id = self.merchant_id_input.text()
        if not merchant_id:
            QMessageBox.warning(self, "Input Error", "Merchant ID is required")
            return

        if not merchant_id.isdigit():
            QMessageBox.warning(self, "Input Error", "Merchant ID must be a number")
            return

        # 调用用户实例的 getMerchantAllInfos 方法
        merchant_info = self.user.getMerchantAllInfos(int(merchant_id))

        if not merchant_info:
            QMessageBox.warning(self, "No Data", "No merchant found with the given ID")
            return

        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(len(merchant_info[0]))
        self.table_widget.setHorizontalHeaderLabels([desc[0] for desc in self.db.cursor.description])

        for row_data in merchant_info:
            row = self.table_widget.rowCount()
            self.table_widget.insertRow(row)
            for column, data in enumerate(row_data):
                self.table_widget.setItem(row, column, QTableWidgetItem(str(data)))

    def get_dish_info_frontend(self):
        merchant_id = self.merchant_id_input.text()


        if not all(merchant_id):
            QMessageBox.warning(self, "Input Error", "All fields are required")
            return

        if not merchant_id.isdigit() :
            QMessageBox.warning(self, "Input Error", "Merchant ID and Dish ID must be numbers")
            return

        # 调用用户实例的 getDishInfos 方法
        dish_info = self.user.getDishInfos(int(merchant_id))

        self.table_widget.setRowCount(len(dish_info))
        self.table_widget.setColumnCount(len(dish_info[0]))
        self.table_widget.setHorizontalHeaderLabels([desc[0] for desc in self.db.cursor.description])

        for row_data in dish_info:
            row = self.table_widget.rowCount()
            self.table_widget.insertRow(row)
            for column, data in enumerate(row_data):
                self.table_widget.setItem(row, column, QTableWidgetItem(str(data)))
        self.merchant_id_input.clear()
        self.dish_id_input.clear()

    def get_dish_all_info_frontend(self):
        merchant_id = self.merchant_id_input.text()
        dish_id = self.dish_id_input.text()

        if not all([merchant_id, dish_id]):
            QMessageBox.warning(self, "Input Error", "All fields are required")
            return

        if not merchant_id.isdigit() or not dish_id.isdigit():
            QMessageBox.warning(self, "Input Error", "Merchant ID and Dish ID must be numbers")
            return

        # 调用用户实例的 getDishInfos 方法
        dish_info = self.user.getDishAllInfos(int(merchant_id), int(dish_id))

        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(len(dish_info[0]))
        self.table_widget.setHorizontalHeaderLabels([desc[0] for desc in self.db.cursor.description])

        for row_data in dish_info:
            row = self.table_widget.rowCount()
            self.table_widget.insertRow(row)
            for column, data in enumerate(row_data):
                self.table_widget.setItem(row, column, QTableWidgetItem(str(data)))
        self.merchant_id_input.clear()
        self.dish_id_input.clear()

    def get_merchant_dish_favorites_frontend(self):
        merchant_id = self.merchant_id_input.text()

        if not merchant_id:
            QMessageBox.warning(self, "Input Error", "Merchant ID is required")
            return

        if not merchant_id.isdigit():
            QMessageBox.warning(self, "Input Error", "Merchant ID must be a number")
            return

        # 调用用户实例的 getMerchantDishFavorites 方法
        merchant_dish_favorites = self.user.getMerchantDishFavorites(int(merchant_id))

        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(len(merchant_dish_favorites[0]))
        self.table_widget.setHorizontalHeaderLabels([desc[0] for desc in self.db.cursor.description])

        for row_data in merchant_dish_favorites:
            row = self.table_widget.rowCount()
            self.table_widget.insertRow(row)
            for column, data in enumerate(row_data):
                self.table_widget.setItem(row, column, QTableWidgetItem(str(data)))
        self.merchant_id_input.clear()
        self.dish_id_input.clear()

    def add_favorites_frontend(self):
        merchant_id = self.merchant_id_input.text()
        dish_id = self.dish_id_input.text()

        if not merchant_id:
            QMessageBox.warning(self, "Input Error", "Merchant ID is required")
            return

        if not merchant_id.isdigit():
            QMessageBox.warning(self, "Input Error", "Merchant ID must be a number")
            return

        # 如果未提供dish_id，则调用用户实例的 addFavorites 方法添加商户收藏
        if not dish_id:
            self.user.addFavorites(int(merchant_id))
        else:
            if not dish_id.isdigit():
                QMessageBox.warning(self, "Input Error", "Dish ID must be a number")
                return
            # 否则，调用用户实例的 addFavorites 方法添加菜品收藏
            self.user.addFavorites(int(merchant_id), int(dish_id))

        QMessageBox.information(self, "Success", "Favorites added successfully")
        self.merchant_id_input.clear()
        self.dish_id_input.clear()


    def clear_inputs(self):
        self.user_id_input.clear()
        self.order_id_input.clear()
        self.merchant_id_input.clear()
        self.dish_id_input.clear()
        self.order_method_input.clear()

    def clear_comment_inputs(self):
        self.comment_merchant_id_input.clear()
        self.comment_dish_id_input.clear()
        self.comment_score_input.clear()
        self.comment_content_input.clear()

def main():
    app = QApplication(sys.argv)
    window = UserWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
