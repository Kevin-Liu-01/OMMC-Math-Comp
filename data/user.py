from firestore import DatabaseController

class User(DatabaseController):
    def __init__(self, name: str, authenticated: bool = False):
        super().__init__(data="users")

        user = self.get_data(name)
        self.profile = user

        self.username = name
        self.exists = user["exists"]
        self.authenticated = authenticated

    def __getitem__(self, item: str):
        return self.profile["data"][item]

    def update(self, **new_data):
        self.set_data(self.username, new_data)

    def authenticate(self):
        if self.exists:
            self.authenticated = True

    # flask-login requirements
    def get_id(self):
        return self.username

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return self.authenticated
