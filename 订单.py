class Order:
    def __init__(self, id,method,user_id, merchant_id, dish_id, order_status):
        self.id = id  # 对应数据库表中的 `id`
        self.method=method
        self.user_id = user_id  # 对应数据库表中的 `user_id`
        self.merchant_id = merchant_id  # 对应数据库表中的 `merchant_id`
        self.dish_id = dish_id  # 对应数据库表中的 `dish_id`
        self.order_status = order_status  # 对应数据库表中的 `order_status`


    def __str__(self):
        return (f"Order ID: {self.id}\n"
                f"User ID: {self.user_id}\n"
                f"Merchant ID: {self.merchant_id}\n"
                f"Dish ID: {self.dish_id}\n"
                f"Order Status: {self.order_status}\n")
