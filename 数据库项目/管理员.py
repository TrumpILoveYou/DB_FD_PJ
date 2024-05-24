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

    def get_user_info(self, user_id,page, pageSize):
        offset = (page - 1) * pageSize
        sql = "SELECT * FROM users WHERE id = %s LIMIT %s OFFSET %s"
        values = (user_id,pageSize, offset)
        result = self.db.execute(sql, values)
        # self.db.close()
        return result

    def add_user(self, user_info:User):
        sql = "INSERT INTO users (name, gender, student_id, account_information,role,age) VALUES (%s, %s, %s, %s)"
        values = (user_info.name, user_info.gender, user_info.student_id, user_info.account_information,user_info.role,user_info.age)
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
        sql = "INSERT INTO merchants (name, address, main_dish) VALUES (%s, %s, %s)"
        values = (merchant_info.name, merchant_info.address,merchant_info.main_dish)
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
        self.layout = QVBoxLayout()

        # 创建并添加组件
        self.user_id_label = QLabel("User ID:")
        self.user_id_input = QLineEdit()
        self.get_user_button = QPushButton("Get User Info")
        self.get_user_button.clicked.connect(self.get_user_info)

        self.layout.addWidget(self.user_id_label)
        self.layout.addWidget(self.user_id_input)
        self.layout.addWidget(self.get_user_button)

        # 创建并添加显示用户信息的表格
        self.user_info_table = QTableWidget()
        self.layout.addWidget(self.user_info_table)

        # 添加添加/更新用户信息的组件
        self.user_info_label = QLabel("User Information:")
        #self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.gender_input = QLineEdit()
        self.student_id_input = QLineEdit()
        self.account_info_input = QLineEdit()
        self.role_input = QLineEdit()
        self.age_input = QLineEdit()

        # 添加两个按钮用于添加和更新用户信息
        self.add_user_button = QPushButton("Add User")
        self.add_user_button.clicked.connect(self.add_user_info)

        self.update_user_button = QPushButton("Update User")
        self.update_user_button.clicked.connect(self.update_user_info)

        self.layout.addWidget(self.user_info_label)
        # self.layout.addWidget(QLabel("id:"))
        # self.layout.addWidget(self.id_input)
        self.layout.addWidget(QLabel("Name:"))
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(QLabel("Gender:"))
        self.layout.addWidget(self.gender_input)
        self.layout.addWidget(QLabel("Student ID:"))
        self.layout.addWidget(self.student_id_input)
        self.layout.addWidget(QLabel("Account Information:"))
        self.layout.addWidget(self.account_info_input)
        self.layout.addWidget(QLabel("Role:"))
        self.layout.addWidget(self.role_input)
        self.layout.addWidget(QLabel("Age:"))
        self.layout.addWidget(self.age_input)
        self.layout.addWidget(self.add_user_button)
        self.layout.addWidget(self.update_user_button)
        # 设置主窗口布局
        self.central_widget.setLayout(self.layout)
        # 记录当前用户的 ID，用于更新用户信息
        self.current_user_id = None

    def get_user_info(self):
        user_id = self.user_id_input.text()
        if not user_id.isdigit():
            QMessageBox.warning(self, "Input Error", "User ID must be a number")
            return
        user_info = self.manager.get_user_info(int(user_id), page=1, pageSize=10)
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