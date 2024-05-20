
class User:
    def __init__(self,ID,name,gender,id_number,account_information):
        self.ID=ID
        self.name=name
        self.gender=gender
        self.id_number=id_number
        self.account_information=account_information
    def __str__(self):
        return f"{self.ID},{self.name},{self.gender},{self.id_number},{self.account_information}"