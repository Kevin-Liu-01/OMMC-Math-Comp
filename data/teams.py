from firestore import DatabaseController

class Team(DatabaseController):
    def __init__(self, name: str, authenticated: bool = False):
        super().__init__(data="teams")

        user = self.get_data(name)
        self.profile = user

        self.username = name
        self.exists = user["exists"]
        self.authenticated = authenticated

    def __getitem__(self, item: str):
        return self.profile["data"][item]

    def update(self, **new_data):
        self.set_data(self.username, new_data)
