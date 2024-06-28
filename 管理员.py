from 数据库连接 import DB
from 商户 import Merchant
from 用户 import User
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QHBoxLayout, QFormLayout, QMessageBox
import sys

class Manager:
    def __init__(self, id, name):
        self.id = id  # 对应数据库表中的 `id`
        self.name = name  # 对应数据库表中的 `name`
        self.db=DB()

    def __str__(self):
        return f"Manager ID: {self.id}\nName: {self.name}"

    def get_user_info(self, user_id):
        sql = "SELECT * FROM users WHERE id = %s"
        values = (user_id,)
        result = self.db.execute(sql, values)
        # self.db.close()
        return result

    def add_user(self, user_info:User):
        sql = "INSERT INTO users (name, gender, student_id, account_information, role, age,password) VALUES (%s, %s, %s, %s, %s, %s,%s)"
        values = (user_info.name, user_info.gender, user_info.student_id, user_info.account_information,user_info.role,user_info.age,"123456")
        self.db.execute(sql, values)
        # self.db.close()

    def update_user(self, user_id, user_info:User):
        sql = "UPDATE users SET name = %s, gender = %s, student_id = %s, account_information = %s,role=%s,age=%s WHERE id = %s"
        values = (user_info.name, user_info.gender, user_info.student_id, user_info.account_information,user_info.role,user_info.age, user_id)
        self.db.execute(sql, values)
        # self.db.close()

    def delete_user(self, user_id):
        sql = "DELETE FROM users WHERE id = %s"
        values = (user_id,)
        self.db.execute(sql, values)
        # self.db.close()

    def get_merchant_info(self, merchant_id, page, pageSize):

        offset = (page - 1) * pageSize
        sql = "SELECT * FROM merchants WHERE id = %s LIMIT %s OFFSET %s"
        values = (merchant_id,pageSize, offset)
        result = self.db.execute(sql, values)
        # self.db.close()
        return result

    def add_merchant(self, merchant_info:Merchant):
        sql = "INSERT INTO merchants (name, address, main_dish,password) VALUES (%s, %s, %s,%s)"
        values = (merchant_info.name, merchant_info.address,merchant_info.main_dish,"123456")
        self.db.execute(sql, values)
        # self.db.close()

    def update_merchant(self, merchant_id, merchant_info:Merchant):
        sql = "UPDATE merchants SET name = %s, address = %s, main_dish = %s WHERE id = %s"
        values = (merchant_info.name, merchant_info.address,merchant_info.main_dish, merchant_id)
        self.db.execute(sql, values)
        # self.db.close()

    def delete_business(self, business_id):
        sql = "DELETE FROM merchants WHERE id = %s"
        values = (business_id,)
        self.db.execute(sql, values)
        # self.db.close()

class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Window")
        self.setGeometry(100, 100, 800, 600)

        # 创建Manager实例
        self.manager = Manager(id=1, name="Admin")

        # 创建主窗口部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建布局
        self.layout = QHBoxLayout()

        # 创建用户相关的布局
        self.user_layout = QVBoxLayout()
        self.create_user_widgets()

        # 创建商户相关的布局
        self.merchant_layout = QVBoxLayout()
        self.create_merchant_widgets()

        # 将用户和商户布局添加到主布局中
        self.layout.addLayout(self.user_layout)
        self.layout.addLayout(self.merchant_layout)

        # 设置主窗口布局
        self.central_widget.setLayout(self.layout)

        # 初始化用户信息表格
        self.user_info_table = QTableWidget()
        self.user_layout.addWidget(self.user_info_table)
        # 初始化商户信息表格
        self.merchant_info_table = QTableWidget()
        self.merchant_layout.addWidget(self.merchant_info_table)

    def create_user_widgets(self):
        # 创建用户相关的组件
        self.user_id_label = QLabel("User ID:")
        self.user_id_input = QLineEdit()
        self.get_user_button = QPushButton("Get User Info")
        self.get_user_button.clicked.connect(self.get_user_info)

        self.user_info_label = QLabel("User Information:")
        self.name_input = QLineEdit()
        self.gender_input = QLineEdit()
        self.student_id_input = QLineEdit()
        self.account_info_input = QLineEdit()
        self.role_input = QLineEdit()
        self.age_input = QLineEdit()

        self.add_user_button = QPushButton("Add User")
        self.add_user_button.clicked.connect(self.add_user_info)
        self.update_user_button = QPushButton("Update User")
        self.update_user_button.clicked.connect(self.update_user_info)

        self.delete_user_label = QLabel("User ID to delete:")
        self.delete_user_input = QLineEdit()
        self.delete_user_button = QPushButton("Delete User")
        self.delete_user_button.clicked.connect(self.delete_user_info)

        # 将用户相关的组件添加到用户布局中
        self.user_layout.addWidget(self.user_id_label)
        self.user_layout.addWidget(self.user_id_input)
        self.user_layout.addWidget(self.get_user_button)
        self.user_layout.addWidget(self.user_info_label)
        self.user_layout.addWidget(QLabel("Name:"))
        self.user_layout.addWidget(self.name_input)
        self.user_layout.addWidget(QLabel("Gender:"))
        self.user_layout.addWidget(self.gender_input)
        self.user_layout.addWidget(QLabel("Student ID:"))
        self.user_layout.addWidget(self.student_id_input)
        self.user_layout.addWidget(QLabel("Account Information:"))
        self.user_layout.addWidget(self.account_info_input)
        self.user_layout.addWidget(QLabel("Role:"))
        self.user_layout.addWidget(self.role_input)
        self.user_layout.addWidget(QLabel("Age:"))
        self.user_layout.addWidget(self.age_input)
        self.user_layout.addWidget(self.add_user_button)
        self.user_layout.addWidget(self.update_user_button)
        self.user_layout.addWidget(self.delete_user_label)
        self.user_layout.addWidget(self.delete_user_input)
        self.user_layout.addWidget(self.delete_user_button)

    def create_merchant_widgets(self):
        self.get_merchant_label = QLabel("Merchant ID to retrieve:")
        self.get_merchant_input = QLineEdit()
        self.get_merchant_button = QPushButton("Get Merchant Info")
        self.get_merchant_button.clicked.connect(self.get_merchant_info)

        self.merchant_layout.addWidget(self.get_merchant_label)
        self.merchant_layout.addWidget(self.get_merchant_input)
        self.merchant_layout.addWidget(self.get_merchant_button)

        self.add_merchant_label = QLabel("Add/Update Merchant Info:")
        self.add_merchant_name_input = QLineEdit()
        self.add_merchant_address_input = QLineEdit()
        self.add_merchant_main_dish_input = QLineEdit()
        self.add_merchant_button = QPushButton("Add Merchant")
        self.add_merchant_button.clicked.connect(self.add_merchant_info)

        self.update_merchant_button = QPushButton("Update Merchant")
        self.update_merchant_button.clicked.connect(self.update_merchant_info)

        self.delete_merchant_label = QLabel("Merchant ID to delete:")
        self.delete_merchant_input = QLineEdit()
        self.delete_merchant_button = QPushButton("Delete Merchant")
        self.delete_merchant_button.clicked.connect(self.delete_merchant_info)

        self.merchant_layout.addWidget(self.add_merchant_label)
        self.merchant_layout.addWidget(QLabel("Name:"))
        self.merchant_layout.addWidget(self.add_merchant_name_input)
        self.merchant_layout.addWidget(QLabel("Address:"))
        self.merchant_layout.addWidget(self.add_merchant_address_input)
        self.merchant_layout.addWidget(QLabel("Main Dish:"))
        self.merchant_layout.addWidget(self.add_merchant_main_dish_input)
        self.merchant_layout.addWidget(self.add_merchant_button)
        self.merchant_layout.addWidget(self.update_merchant_button)
        self.merchant_layout.addWidget(self.delete_merchant_label)
        self.merchant_layout.addWidget(self.delete_merchant_input)
        self.merchant_layout.addWidget(self.delete_merchant_button)

    def get_user_info(self):
        user_id = self.user_id_input.text()
        if not user_id.isdigit():
            QMessageBox.warning(self, "Input Error", "User ID must be a number")
            return
        user_info = self.manager.get_user_info(int(user_id))
        if not user_info:
            QMessageBox.information(self, "No Data", "No user found with the given ID")
            return
        self.current_user_id = int(user_id)
        self.user_info_table.setRowCount(len(user_info))
        self.user_info_table.setColumnCount(len(user_info[0]))
        self.user_info_table.setHorizontalHeaderLabels([desc[0] for desc in self.manager.db.cursor.description])
        for row_idx, row_data in enumerate(user_info):
            for col_idx, col_data in enumerate(row_data):
                self.user_info_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        # 将用户信息填充到输入框中以便更新
        # self.id_input.setText(str(user_info[0][0]))
        self.name_input.setText(user_info[0][1])  # Name
        self.gender_input.setText(user_info[0][2])  # Gender
        self.student_id_input.setText(user_info[0][3])  # Student ID
        self.account_info_input.setText(user_info[0][4])  # Account Information
        self.role_input.setText(user_info[0][5])  # Role
        self.age_input.setText(str(user_info[0][6]))  # Age

    def add_user_info(self):
        # 获取输入框中的信息
        # id = self.id_input.text()
        name = self.name_input.text()
        gender = self.gender_input.text()
        student_id = self.student_id_input.text()
        account_info = self.account_info_input.text()
        role = self.role_input.text()
        age = self.age_input.text()
        # 检查输入是否完整
        if not all([name, gender, student_id, account_info, role, age]):
            QMessageBox.warning(self, "Input Error", "All fields are required")
            return
        # 创建用户信息对象
        user_info = User(name=name, gender=gender, student_id=student_id, account_information=account_info, role=role, age=int(age))
        # 调用 Manager 的方法添加用户
        self.manager.add_user(user_info)
        # 提示用户添加成功
        QMessageBox.information(self, "Success", "User added successfully")
        # 清空输入框
        self.clear_inputs()

    def update_user_info(self):
        # 获取输入框中的信息
        # id = self.id_input.text()
        name = self.name_input.text()
        gender = self.gender_input.text()
        student_id = self.student_id_input.text()
        account_info = self.account_info_input.text()
        role = self.role_input.text()
        age = self.age_input.text()
        # 检查是否选择了要更新的用户
        if not self.current_user_id:
            QMessageBox.warning(self, "User Not Selected", "Please select a user to update")
            return
        # 检查输入是否完整
        if not all([name, gender, student_id, account_info, role, age]):
            QMessageBox.warning(self, "Input Error", "All fields are required")
            return
        # 创建用户信息对象
        user_info = User(name=name, gender=gender, student_id=student_id, account_information=account_info, role=role, age=int(age))
        # 调用 Manager 的方法更新用户
        self.manager.update_user(self.current_user_id, user_info)
        # 提示用户更新成功
        QMessageBox.information(self, "Success", "User information updated successfully")
        # 清空输入框
        self.clear_inputs()
    
    def delete_user_info(self):
        # 获取要删除的用户 ID
        user_id = self.delete_user_input.text()
        if not user_id.isdigit():
            QMessageBox.warning(self, "Input Error", "User ID must be a number")
            return
        # 调用 Manager 的方法删除用户
        self.manager.delete_user(int(user_id))
        # 提示用户删除成功
        QMessageBox.information(self, "Success", "User deleted successfully")
        # 清空输入框
        self.delete_user_input.clear()

    def get_merchant_info(self):
        merchant_id = self.get_merchant_input.text()
        if not merchant_id.isdigit():
            QMessageBox.warning(self, "Input Error", "Merchant ID must be a number")
            return
        merchant_info = self.manager.get_merchant_info(int(merchant_id), page=1, pageSize=10)
        if not merchant_info:
            QMessageBox.information(self, "No Data", "No merchant found with the given ID")
            return
        self.current_merchant_id = int(merchant_id)
        self.merchant_info_table.setRowCount(len(merchant_info))
        self.merchant_info_table.setColumnCount(len(merchant_info[0]))
        self.merchant_info_table.setHorizontalHeaderLabels([desc[0] for desc in self.manager.db.cursor.description])
        for row_idx, row_data in enumerate(merchant_info):
            for col_idx, col_data in enumerate(row_data):
                self.merchant_info_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        # 将商户信息填充到输入框中以便更新
        self.add_merchant_name_input.setText(merchant_info[0][1])  # Name
        self.add_merchant_address_input.setText(merchant_info[0][2])  # Address
        self.add_merchant_main_dish_input.setText(merchant_info[0][3])  # Main Dish

    def add_merchant_info(self):
        name = self.add_merchant_name_input.text()
        address = self.add_merchant_address_input.text()
        main_dish = self.add_merchant_main_dish_input.text()
        if not all([name, address, main_dish]):
            QMessageBox.warning(self, "Input Error", "All fields are required")
            return
        merchant_info = Merchant(id=-1,name=name, address=address, main_dish=main_dish)
        self.manager.add_merchant(merchant_info)
        QMessageBox.information(self, "Success", "Merchant added successfully")
        self.clear_merchant_inputs()

    def update_merchant_info(self):
        # merchant_id = self.update_merchant_id_input.text()
        name = self.add_merchant_name_input.text()
        address = self.add_merchant_address_input.text()
        main_dish = self.add_merchant_main_dish_input.text()
        if not self.current_merchant_id:
            QMessageBox.warning(self, "Input Error", "Merchant ID must be a number")
            return
        if not all([name, address, main_dish]):
            QMessageBox.warning(self, "Input Error", "All fields are required")
            return
        merchant_info = Merchant(id=-1,name=name, address=address, main_dish=main_dish)
        self.manager.update_merchant(self.current_merchant_id, merchant_info)
        QMessageBox.information(self, "Success", "Merchant information updated successfully")
        self.clear_merchant_inputs()

    def delete_merchant_info(self):
        merchant_id = self.delete_merchant_input.text()
        if not merchant_id.isdigit():
            QMessageBox.warning(self, "Input Error", "Merchant ID must be a number")
            return
        self.manager.delete_business(int(merchant_id))
        QMessageBox.information(self, "Success", "Merchant deleted successfully")
        self.delete_merchant_input.clear()

    def clear_merchant_inputs(self):
        self.get_merchant_input.clear()
        self.add_merchant_name_input.clear()
        self.add_merchant_address_input.clear()
        self.add_merchant_main_dish_input.clear()

    def clear_inputs(self):
        # 清空输入框
        # self.id_input.clear()
        self.user_id_input.clear()
        self.name_input.clear()
        self.gender_input.clear()
        self.student_id_input.clear()
        self.account_info_input.clear()
        self.role_input.clear()
        self.age_input.clear()


def main():
    admin_window = AdminWindow()
    admin_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main()
    sys.exit(app.exec_())