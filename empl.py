from userrr import User
class Employee(User):
    def __init__(self, user_id, username, password, full_name):
        super().__init__(user_id, username, password, 'Employee', full_name)