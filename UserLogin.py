from flask_login import UserMixin

class UserLogin(UserMixin):
    def from_db(self, user):
        self.id = user["id"]
        self.username = user["username"]
        self.password_hash = user["password_hash"]
        return self