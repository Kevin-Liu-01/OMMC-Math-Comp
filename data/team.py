from data.firestore import DatabaseController

class Team(DatabaseController):
    def __init__(self, name: str):
        super().__init__(data="teams")

        user = self.get_data(name)
        self.profile = user

        self.name = name
        self.exists = user["exists"]

    def __getitem__(self, item: str):
        return self.profile["data"][item]

    def update(self, **new_data):
        self.set_data(self.name, new_data)
