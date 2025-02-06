from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, name, surname, username, password, creator, profilepic):
        self.username = username
        self.name = name
        self.surname = surname
        self.password = password
        self.creator = creator
        self.profilepic = profilepic

    def get_id(self):
           return (self.username)