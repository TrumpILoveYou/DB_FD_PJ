class User:
    def __init__(self, id, name, gender, student_id, account_information):
        self.id = id  # 对应数据库表中的 `id`
        self.name = name  # 对应数据库表中的 `name`
        self.gender = gender  # 对应数据库表中的 `gender`
        self.student_id = student_id  # 对应数据库表中的 `student_id`
        self.account_information = account_information  # 对应数据库表中的 `account_information`

    def __str__(self):
        return (f"User ID: {self.id}\n"
                f"Name: {self.name}\n"
                f"Gender: {self.gender}\n"
                f"Student ID: {self.student_id}\n"
                f"Account Information: {self.account_information}\n")
