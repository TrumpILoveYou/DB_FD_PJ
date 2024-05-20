class Message:
    def __init__(self, id, type, content):
        self.id = id  # 对应数据库表中的 `id`
        self.type = type  # 对应数据库表中的 `type`
        self.content = content  # 对应数据库表中的 `content`

    def __str__(self):
        return (f"Message ID: {self.id}\n"
                f"Type: {self.type}\n"
                f"Content: {self.content}\n")
