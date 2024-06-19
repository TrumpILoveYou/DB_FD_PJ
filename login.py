import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QComboBox
from PyQt5.QtWidgets import QDialog, QFormLayout
import 管理员
import 商户
import 用户
from 用户 import User
from 商户 import Merchant
from 数据库连接 import DB

class RegisterWindow(QDialog):
    def __init__(self, identity):
        super().__init__()
        self.identity = identity
        self.setWindowTitle(f"{identity} 注册")
        self.resize(400, 300)
        self.db=DB()

        layout = QFormLayout()
        
        self.username_label = QLabel("用户名:")
        self.username_edit = QLineEdit()
        layout.addRow(self.username_label, self.username_edit)

        self.password_label = QLabel("密码:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addRow(self.password_label, self.password_edit)

        if identity == "商户":
            self.extra_label = QLabel("地址:")
            self.extra_edit = QLineEdit()
            layout.addRow(self.extra_label, self.extra_edit)
        elif identity == "用户":
            self.extra_label = QLabel("性别:")
            self.extra_edit = QLineEdit()
            layout.addRow(self.extra_label, self.extra_edit)
        elif identity == "管理员":
            self.extra_edit = QLineEdit()

        self.register_button = QPushButton("注册")
        self.register_button.clicked.connect(self.register)
        layout.addRow(self.register_button)

        self.setLayout(layout)

    def register(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        extra_info = self.extra_edit.text()

        if not username or not password:
            QMessageBox.warning(self, "注册失败", "所有字段都是必填项")
            return

        # 模拟注册过程
        if self.identity == "商户":
            # 创建新商户
            merchant_info = Merchant(name=username, address=extra_info, main_dish="")
            sql = "INSERT INTO merchants (name, address, main_dish, password) VALUES (%s, %s, %s, %s)"
            values = (merchant_info.name, merchant_info.address, merchant_info.main_dish, password)
            self.db.execute(sql, values)
            QMessageBox.information(self, "注册成功", f"商户 {username} 注册成功")
        elif self.identity == "用户":
            # 创建新用户
            user_info = User(name=username, gender=extra_info, student_id="", account_information="", role="", age=0)
            # 存储原始密码到数据库
            sql = "INSERT INTO users (name, gender, student_id, account_information, role, age, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (user_info.name, user_info.gender, user_info.student_id, user_info.account_information,user_info.role,user_info.age, password)
            self.db.execute(sql, values)
            QMessageBox.information(self, "注册成功", f"用户 {username} 注册成功")
        elif self.identity == "管理员":
            # 创建新管理员
            sql = "INSERT INTO managers (name, password) VALUES (%s, %s)"
            values = (username, password)
            self.db.execute(sql, values)
            QMessageBox.information(self, "注册成功", f"管理员 {username} 注册成功")

        self.accept()


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("登录界面")
        self.resize(400, 300)
        self.db = DB()

        layout = QVBoxLayout()

        self.label = QLabel("请选择身份类型:")
        layout.addWidget(self.label)

        self.identity_combo = QComboBox()
        self.identity_combo.addItem("管理员")
        self.identity_combo.addItem("商户")
        self.identity_combo.addItem("用户")
        layout.addWidget(self.identity_combo)

        self.username_label = QLabel("用户名:")
        layout.addWidget(self.username_label)
        self.username_edit = QLineEdit()
        layout.addWidget(self.username_edit)

        self.password_label = QLabel("密码:")
        layout.addWidget(self.password_label)
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_edit)

        self.login_button = QPushButton("登录")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("注册")
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def login(self):
        identity = self.identity_combo.currentText()
        username = self.username_edit.text()
        password = self.password_edit.text()

        # 模拟登录验证
        if identity == "管理员":
            sql = "SELECT password FROM managers WHERE name = %s"
            result = self.db.execute(sql, (username,))
            for row in result:
                if password == row[0]:
                    self.close()
                    self.window = 管理员.AdminWindow()
                    self.window.show()
                    return
        elif identity == "商户":
            # 从数据库中取出密码进行比较
            sql = "SELECT password FROM merchants WHERE name = %s"
            result = self.db.execute(sql, (username,))
            # print('result', result, '\npassword', password)
            for row in result:
                if password == row[0]:
                    self.close()
                    self.window = 商户.MerchantWindow()
                    self.window.show()
                    return
        elif identity == "用户":
            # 从数据库中取出密码进行比较
            sql = "SELECT password FROM users WHERE name = %s"
            result = self.db.execute(sql, (username,))
            # print('result', result, '\npassword', password)
            for row in result:
                if password == row[0]:
                    self.close()
                    sql1 = "SELECT id FROM users WHERE name = %s"
                    result1 = self.db.execute(sql1, (username,))
                    user_id = result1[0]
                    # print('user_id', user_id)
                    self.window = 用户.UserWindow()
                    self.window.set_user(user_id)  # 将用户ID传递给用户窗口
                    self.window.show()
                    return

        QMessageBox.warning(self, "登录失败", "用户名或密码错误")

    def register(self):
        identity = self.identity_combo.currentText()
        self.register_window = RegisterWindow(identity)
        self.register_window.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
