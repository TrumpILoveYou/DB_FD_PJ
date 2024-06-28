from 数据库连接 import DB
from 菜品 import Dish
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
import sys

class Merchant:
    def __init__(self,id, name, address, main_dish):
        self.id = id  # 对应数据库表中的 `id`
        self.name = name  # 对应数据库表中的 `name`
        self.address = address  # 对应数据库表中的 `address`
        self.main_dish = main_dish  # 对应数据库表中的 `main_dish`
        self.db=DB()

    def __str__(self):
        return (f"Merchant ID: {self.id}\n"
                f"Name: {self.name}\n"
                f"Address: {self.address}\n"
                f"Main Dish: {self.main_dish}\n")

    def getSelfInfo_merchant(self):
        sql=("SELECT * FROM merchants WHERE id = %s ")
        values=(self.id)
        result = self.db.execute(sql, values)
        return result

    def add_dish(self, dish_info:Dish):
        sql = """INSERT INTO dishes 
                 (merchant_id,name, price, category, description, image, ingredients, nutrition_information, allergens, queue_sales, online_sales, collection_count) 
                 VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (dish_info.merchant_id,dish_info.name, dish_info.price, dish_info.category, dish_info.description, dish_info.image, dish_info.ingredients,
                  dish_info.nutrition_information, dish_info.allergens, 0,0,0)
        self.db.execute(sql, values)
        self.db.close()

    def update_dish(self, dish_id, dish_info: Dish):
        sql = """UPDATE dishes SET name = %s, price = %s, category = %s, description = %s, image = %s, ingredients = %s, 
                 nutrition_information = %s, allergens = %s
                 WHERE id = %s"""
        values = (dish_info.name, dish_info.price, dish_info.category, dish_info.description, dish_info.image,
                  dish_info.ingredients, dish_info.nutrition_information, dish_info.allergens, dish_id)
        self.db.execute(sql, values)
        self.db.close()

    def delete_dish(self, dish_id):
        sql = "DELETE FROM dishes WHERE id = %s"
        values = (dish_id,)
        self.db.execute(sql, values)
        self.db.close()


class MerchantWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Merchant Management")
        self.setGeometry(100, 100, 800, 600)

        # 创建商户实例
        self.merchant = None

        # 创建主窗口部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建布局
        self.layout = QVBoxLayout()

        # 创建商户相关的组件
        self.merchant_id_label = QLabel("Merchant ID(更新时这里输入dish_id):")
        self.merchant_id_input = QLineEdit()
        self.name_label = QLabel("Dish Name:")
        self.name_input = QLineEdit()
        self.price_label = QLabel("Price:")
        self.price_input = QLineEdit()
        self.category_label = QLabel("Category:")
        self.category_input = QLineEdit()
        self.description_label = QLabel("Description:")
        self.description_input = QLineEdit()
        self.image_label = QLabel("Image URL:")
        self.image_input = QLineEdit()
        self.ingredients_label = QLabel("Ingredients:")
        self.ingredients_input = QLineEdit()
        self.nutrition_label = QLabel("Nutrition Info:")
        self.nutrition_input = QLineEdit()
        self.allergens_label = QLabel("Allergens:")
        self.allergens_input = QLineEdit()

        self.add_dish_button = QPushButton("Add Dish")
        self.add_dish_button.clicked.connect(self.add_dish)

        self.update_dish_button = QPushButton("Update Dish")
        self.update_dish_button.clicked.connect(self.update_dish)

        self.dish_id_label = QLabel("Dish ID:")
        self.dish_id_input = QLineEdit()

        self.delete_dish_button = QPushButton("Delete Dish")
        self.delete_dish_button.clicked.connect(self.delete_dish)

        # 添加组件到布局
        self.layout.addWidget(self.merchant_id_label)
        self.layout.addWidget(self.merchant_id_input)
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.price_label)
        self.layout.addWidget(self.price_input)
        self.layout.addWidget(self.category_label)
        self.layout.addWidget(self.category_input)
        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.description_input)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.image_input)
        self.layout.addWidget(self.ingredients_label)
        self.layout.addWidget(self.ingredients_input)
        self.layout.addWidget(self.nutrition_label)
        self.layout.addWidget(self.nutrition_input)
        self.layout.addWidget(self.allergens_label)
        self.layout.addWidget(self.allergens_input)
        self.layout.addWidget(self.add_dish_button)
        self.layout.addWidget(self.update_dish_button)
        self.layout.addWidget(self.dish_id_label)
        self.layout.addWidget(self.dish_id_input)
        self.layout.addWidget(self.delete_dish_button)

        # 设置主窗口布局
        self.central_widget.setLayout(self.layout)

    def add_dish(self):
        # TODO
        merchant_id = self.merchant_id_input.text()
        name = self.name_input.text()
        price = self.price_input.text()
        category = self.category_input.text()
        description = self.description_input.text()
        image = self.image_input.text()
        ingredients = self.ingredients_input.text()
        nutrition_information = self.nutrition_input.text()
        allergens = self.allergens_input.text()

        if not all([merchant_id, name, price, category, description, image, ingredients, nutrition_information, allergens]):
            QMessageBox.warning(self, "Input Error", "All fields are required")
            return

        if not merchant_id.isdigit():
            QMessageBox.warning(self, "Input Error", "Merchant ID must be a number")
            return

        dish_info = Dish(id=None, merchant_id=int(merchant_id), name=name, price=float(price), category=category, description=description, image=image, ingredients=ingredients, nutrition_information=nutrition_information, allergens=allergens, queue_sales=0, online_sales=0, collection_count=0)
        
        # Initialize merchant instance
        self.merchant = Merchant(id=-1,name="", address="", main_dish="")
        self.merchant.add_dish(dish_info)

        QMessageBox.information(self, "Success", "Dish added successfully")
        self.clear_inputs()

    def update_dish(self):
        dish_id = self.merchant_id_input.text()
        name = self.name_input.text()
        price = self.price_input.text()
        category = self.category_input.text()
        description = self.description_input.text()
        image = self.image_input.text()
        ingredients = self.ingredients_input.text()
        nutrition_information = self.nutrition_input.text()
        allergens = self.allergens_input.text()

        if not all([dish_id, name, price, category, description, image, ingredients, nutrition_information, allergens]):
            QMessageBox.warning(self, "Input Error", "All fields are required")
            return

        if not dish_id.isdigit():
            QMessageBox.warning(self, "Input Error", "Dish ID must be a number")
            return

        dish_info = Dish(id=int(dish_id), merchant_id=None, name=name, price=float(price), category=category, description=description, image=image, ingredients=ingredients, nutrition_information=nutrition_information, allergens=allergens, queue_sales=0, online_sales=0, collection_count=0)

        # Initialize merchant instance
        self.merchant = Merchant(id=-1,name="", address="", main_dish="")
        self.merchant.update_dish(int(dish_id), dish_info)

        QMessageBox.information(self, "Success", "Dish updated successfully")
        self.clear_inputs()

    def delete_dish(self):
        dish_id = self.dish_id_input.text()

        if not dish_id:
            QMessageBox.warning(self, "Input Error", "Dish ID is required")
            return

        if not dish_id.isdigit():
            QMessageBox.warning(self, "Input Error", "Dish ID must be a number")
            return

        # Initialize merchant instance
        self.merchant = Merchant(id=-1,name="", address="", main_dish="")
        self.merchant.delete_dish(int(dish_id))

        QMessageBox.information(self, "Success", "Dish deleted successfully")
        self.clear_inputs()

    def clear_inputs(self):
        self.merchant_id_input.clear()
        self.name_input.clear()
        self.price_input.clear()
        self.category_input.clear()
        self.description_input.clear()
        self.image_input.clear()
        self.ingredients_input.clear()
        self.nutrition_input.clear()
        self.allergens_input.clear()


def main():
    window = MerchantWindow()
    window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main()
    sys.exit(app.exec_())