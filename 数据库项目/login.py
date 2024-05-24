import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QComboBox
import 管理员
import 商户
import 用户

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("登录界面")
        self.resize(400, 300)

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

        self.setLayout(layout)

    def login(self):
        identity = self.identity_combo.currentText()
        username = self.username_edit.text()
        password = self.password_edit.text()

        # 模拟登录验证
        if identity == "管理员" and username == "admin" and password == "admin123":
            self.close()
            self.admin_window = 管理员.AdminWindow()
            self.admin_window.show()
        elif identity == "商户" and username == "merchant" and password == "merchant123":
            self.close()
            商户.main()
        elif identity == "用户" and username == "user" and password == "user123":
            self.close()
            用户.main()
        else:
            QMessageBox.warning(self, "登录失败", "用户名或密码错误")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())

