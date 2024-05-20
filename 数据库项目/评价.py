


class comment:
    def __init__(self, ID, user_id, merchant_id, dish_id,score,content):
        self.ID = ID
        self.user_id = user_id
        self.merchant_id = merchant_id
        self.dish_id = dish_id
        self.score=score
        self.content=content

    def __str__(self):
        return f""