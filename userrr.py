class User:
    def __init__(self,user_id, username, password, role, full_name):
        self.id = user_id
        self.username = username
        self.password = password
        self.role = role
        self.full_name = full_name