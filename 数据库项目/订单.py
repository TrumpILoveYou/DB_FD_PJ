


class order:
    def __init__(self, ID, user_id, merchant_id, dish_id,quantity,order_status,message_id):
        self.ID = ID
        self.user_id = user_id
        self.merchant_id = merchant_id
        self.dish_id = dish_id
        self.quantity=quantity
        self.order_status=order_status
        self.message_id=message_id


    def __str__(self):
        return f""