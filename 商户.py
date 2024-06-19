from 数据库连接 import DB
from 菜品 import Dish
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
import sys

class Merchant:
    def __init__(self, name, address, main_dish):
        # !!! self.id = id  # 对应数据库表中的 `id`
        self.name = name  # 对应数据库表中的 `name`
        self.address = address  # 对应数据库表中的 `address`
        self.main_dish = main_dish  # 对应数据库表中的 `main_dish`
        self.db=DB()

    def __str__(self):
        return (f"Merchant ID: {self.id}\n"
                f"Name: {self.name}\n"
                f"Address: {self.address}\n"
                f"Main Dish: {self.main_dish}\n")
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
                 nutrition_information = %s, allergens = %s, queue_sales = %s, online_sales = %s, collection_count = %s 
                 WHERE id = %s"""
        values = (dish_info.name, dish_info.price, dish_info.category, dish_info.description, dish_info.image,
                  dish_info.ingredients, dish_info.nutrition_information, dish_info.allergens, dish_info.queue_sales,
                  dish_info.online_sales, dish_info.collection_count, dish_id)
        self.db.execute(sql, values)
        self.db.close()

    def delete_dish(self, dish_id):
        sql = "DELETE FROM dishes WHERE id = %s"
        values = (dish_id,)
        self.db.execute(sql, values)
        self.db.close()

    def analyzeMerchantDishes(self, merchant_id):
        """菜品数据分析：某个商户所有菜品的评分 、销量以及购买该菜品次数最多的人"""
        sql = ("""
                    WITH user_orders AS (
            SELECT
                o.dish_id,
                o.user_id,
                COUNT(o.id) AS order_count
            FROM
                orders o
            GROUP BY
                o.dish_id, o.user_id
        ), top_buyers AS (
            SELECT
                dish_id,
                user_id,
                MAX(order_count) AS top_buyer_order_count
            FROM
                user_orders
            GROUP BY
                dish_id
        )
        SELECT 
            d.id AS dish_id,
            d.name AS dish_name,
            IFNULL(AVG(c.score), 0) AS average_score,
            d.queue_sales + d.online_sales AS total_sales,
            tb.top_buyer_order_count,
            u.name AS top_buyer_name
        FROM
            dishes d
        LEFT JOIN
            comments c ON d.id = c.dish_id
        LEFT JOIN
            top_buyers tb ON d.id = tb.dish_id
        LEFT JOIN
            users u ON tb.user_id = u.id
        WHERE
            d.merchant_id = %s
        GROUP BY
            d.id, tb.top_buyer_order_count, u.name
        ORDER BY
            d.id, tb.top_buyer_order_count DESC;""")
        values = (merchant_id)
        result = self.db.execute(sql, values)
        self.db.close()
        return result

    def analyzeMerchantFans(self, merchant_id, threshold):
        """一段时间内某个商户的忠实粉丝在该商户的消费分布。"""
        sql = ("""
                    -- 定义时间范围和商户ID
                    SET @start_date = '2023-01-01';
                    SET @end_date = '2025-12-31';
                    
                    -- 查询忠实粉丝在各个菜品上的购买次数分布
                    SELECT
                        u.id AS user_id,
                        u.name AS user_name,
                        d.id AS dish_id,
                        d.name AS dish_name,
                        COUNT(o.id) AS purchase_count
                    FROM
                        orders o
                    JOIN
                        users u ON o.user_id = u.id
                    JOIN
                        dishes d ON o.dish_id = d.id
                    WHERE
                        o.merchant_id = %s
                        AND o.created_at BETWEEN @start_date AND @end_date
                        AND o.user_id IN (
                            SELECT
                                user_id
                            FROM
                                orders
                            WHERE
                                merchant_id = %s
                                AND created_at BETWEEN @start_date AND @end_date
                            GROUP BY
                                user_id
                            HAVING
                                COUNT(id) > %s
                        )
                    GROUP BY
                        u.id, d.id
                    ORDER BY
                        u.id, d.id;
                    """
            )
        values = (merchant_id, merchant_id, threshold)
        result = self.db.execute(sql, values)
        self.db.close()
        return result

    def getTheMostPopularDish(self, merchant_id):
        sql = ("""
                    SELECT 
                        d.id AS dish_id,
                        d.name AS dish_name,
                        d.merchant_id,
                        m.name AS merchant_name,
                        d.queue_sales,
                        d.online_sales,
                        (d.queue_sales + d.online_sales) AS total_sales
                    FROM 
                        dishes d
                    where d.merchant_id=%s
                    JOIN 
                        merchants m ON d.merchant_id = m.id
                    ORDER BY 
                        total_sales DESC
                    """
            )
        values = (merchant_id)
        result = self.db.execute(sql, values)
        self.db.close()
        return result



class MerchantWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Merchant Management")
        self.setGeometry(100, 100, 800, 600)

        # 创建商户实例
        self.merchant = Merchant("", "", "")

        # 创建主窗口部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建布局
        self.layout = QVBoxLayout()

        # 创建商户相关的组件
        self.merchant_id_label = QLabel("Merchant ID:")
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

        # 商户数据分析
        self.merchant_analysis_label = QLabel("Analyze Merchant Dishes:")
        self.layout.addWidget(self.merchant_analysis_label)
        self.merchant_id_input = QLineEdit()
        self.layout.addWidget(QLabel("Merchant ID:"))
        self.layout.addWidget(self.merchant_id_input)
        self.analyze_merchant_button = QPushButton("Analyze Merchant Dishes")
        self.layout.addWidget(self.analyze_merchant_button)
        self.merchant_info_table = QTableWidget()
        self.layout.addWidget(self.merchant_info_table)
        self.analyze_merchant_button.clicked.connect(self.analyze_merchant_dishes_callback)

        # Create the main layout
        self.layout = QVBoxLayout(self.central_widget)

        # Analyze Merchant Fans Section
        self.fans_analysis_label = QLabel("Analyze Merchant Fans:")
        self.layout.addWidget(self.fans_analysis_label)
        self.merchant_id_input = QLineEdit()
        self.layout.addWidget(QLabel("Merchant ID:"))
        self.layout.addWidget(self.merchant_id_input)
        self.threshold_input = QLineEdit()
        self.layout.addWidget(QLabel("Threshold:"))
        self.layout.addWidget(self.threshold_input)
        self.analyze_fans_button = QPushButton("Analyze Merchant Fans")
        self.layout.addWidget(self.analyze_fans_button)
        self.fans_info_table = QTableWidget()
        self.layout.addWidget(self.fans_info_table)
        self.analyze_fans_button.clicked.connect(self.analyze_merchant_fans_callback)

        # Get the Most Popular Dish Section
        self.popular_dish_label = QLabel("Get Most Popular Dish:")
        self.layout.addWidget(self.popular_dish_label)
        self.popular_dish_merchant_id_input = QLineEdit()
        self.layout.addWidget(QLabel("Merchant ID:"))
        self.layout.addWidget(self.popular_dish_merchant_id_input)
        self.get_popular_dish_button = QPushButton("Get Most Popular Dish")
        self.layout.addWidget(self.get_popular_dish_button)
        self.popular_dish_table = QTableWidget()
        self.layout.addWidget(self.popular_dish_table)
        self.get_popular_dish_button.clicked.connect(self.get_popular_dish_callback)

        # 设置主窗口布局
        self.central_widget.setLayout(self.layout)

    def add_dish(self):
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
        self.merchant = Merchant(name="", address="", main_dish="")
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
        self.merchant = Merchant(name="", address="", main_dish="")
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
        self.merchant = Merchant(name="", address="", main_dish="")
        self.merchant.delete_dish(int(dish_id))

        QMessageBox.information(self, "Success", "Dish deleted successfully")
        self.clear_inputs()

    def analyze_merchant_dishes_callback(self):
        merchant_id = self.merchant_id_input.text()
        if not merchant_id.isdigit():
            QMessageBox.warning(self, "Input Error", "Merchant ID must be a number")
            return

        # Call the analyzeMerchantDishes function and get the result
        result = self.merchant.analyzeMerchantDishes(int(merchant_id))
        
        # Check if there's no result
        if not result:
            QMessageBox.information(self, "No Data", "No data found for the given Merchant ID")
            return
        
        # Populate the table with the results
        self.merchant_info_table.setRowCount(len(result))
        self.merchant_info_table.setColumnCount(len(result[0]))
        self.merchant_info_table.setHorizontalHeaderLabels(['Dish ID', 'Dish Name', 'Average Score', 'Total Sales', 'Top Buyer Order Count', 'Top Buyer Name'])
        
        for row_idx, row_data in enumerate(result):
            for col_idx, col_data in enumerate(row_data):
                self.merchant_info_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
   
    def analyze_merchant_fans_callback(self):
        merchant_id = self.merchant_id_input.text()
        threshold = self.threshold_input.text()
        if not merchant_id.isdigit() or not threshold.isdigit():
            QMessageBox.warning(self, "Input Error", "Merchant ID and Threshold must be numbers")
            return

        # Call the analyzeMerchantFans function and get the result
        result = self.merchant.analyzeMerchantFans(int(merchant_id), int(threshold))
        
        # Check if there's no result
        if not result:
            QMessageBox.information(self, "No Data", "No data found for the given Merchant ID and Threshold")
            return
        
        # Populate the table with the results
        self.fans_info_table.setRowCount(len(result))
        self.fans_info_table.setColumnCount(len(result[0]))
        self.fans_info_table.setHorizontalHeaderLabels(['User ID', 'User Name', 'Total Orders', 'Total Amount'])
        
        for row_idx, row_data in enumerate(result):
            for col_idx, col_data in enumerate(row_data):
                self.fans_info_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def get_popular_dish_callback(self):
        merchant_id = self.popular_dish_merchant_id_input.text()
        if not merchant_id.isdigit():
            QMessageBox.warning(self, "Input Error", "Merchant ID must be a number")
            return

        result = self.merchant.getTheMostPopularDish(int(merchant_id))
        if not result:
            QMessageBox.information(self, "No Data", "No popular dish found for the given Merchant ID")
            return
        
        self.popular_dish_table.setRowCount(len(result))
        self.popular_dish_table.setColumnCount(len(result[0]))
        self.popular_dish_table.setHorizontalHeaderLabels(['Dish ID', 'Dish Name', 'Merchant ID', 'Merchant Name', 'Queue Sales', 'Online Sales', 'Total Sales'])
        
        for row_idx, row_data in enumerate(result):
            for col_idx, col_data in enumerate(row_data):
                self.popular_dish_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))


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