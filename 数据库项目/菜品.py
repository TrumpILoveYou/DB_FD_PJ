class Dish:
    def __init__(self, id, name, price, category, description, image, ingredients, nutrition_information, allergens, queue_sales, online_sales, collection_count):
        self.id = id  # 对应数据库表中的 `id`
        self.name = name  # 对应数据库表中的 `name`
        self.price = price  # 对应数据库表中的 `price`
        self.category = category  # 对应数据库表中的 `category`
        self.description = description  # 对应数据库表中的 `description`
        self.image = image  # 对应数据库表中的 `image`
        self.ingredients = ingredients  # 对应数据库表中的 `ingredients`
        self.nutrition_information = nutrition_information  # 对应数据库表中的 `nutrition_information`
        self.allergens = allergens  # 对应数据库表中的 `allergens`
        self.queue_sales = queue_sales  # 对应数据库表中的 `queue_sales`
        self.online_sales = online_sales  # 对应数据库表中的 `online_sales`
        self.collection_count = collection_count  # 对应数据库表中的 `collection_count`

    def __str__(self):
        return (f"Dish ID: {self.id}\n"
                f"Name: {self.name}\n"
                f"Price: {self.price}\n"
                f"Category: {self.category}\n"
                f"Description: {self.description}\n"
                f"Image: {self.image}\n"
                f"Ingredients: {self.ingredients}\n"
                f"Nutrition Information: {self.nutrition_information}\n"
                f"Allergens: {self.allergens}\n"
                f"Queue Sales: {self.queue_sales}\n"
                f"Online Sales: {self.online_sales}\n"
                f"Collection Count: {self.collection_count}\n")
