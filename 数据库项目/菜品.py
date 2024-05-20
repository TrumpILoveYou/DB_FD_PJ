

class dish:
    def __init__(self,ID,name,price,category,description,picture,ingredients,nutrition_information,allergens,queue_sales,online_sales,collection_count):
        self.ID = ID
        self.name = name
        self.price = price
        self.category = category
        self.description = description
        self.picture = picture
        self.ingredients = ingredients
        self.nutrition_information = nutrition_information
        self.allergens = allergens
        self.queue_sales = queue_sales
        self.online_sales = online_sales
        self.collection_count = collection_count

    def __str__(self):
        return f""