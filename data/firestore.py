import firebase_admin
from firebase_admin import credentials, firestore, threading

firebase_admin.initialize_app(credentials.Certificate("serviceAccount.json"))
firestore = firestore.client()

class DatabaseController:
    def __init__(self, **options):
        self.database = firestore.collection(options.get("data", "users"))
        self._requested = {}

    def get_data(self, name: str):
        if self._requested.get(name, False):
            return self._requested[name]

        finished_callback = threading.Event()
        document = self.database.document(name)
        doc_ref = document.get()

        object = {
            "id": doc_ref.id,
            "exists": doc_ref.exists,
            "data": doc_ref.to_dict()
        }

        def snapshot_received(snapshots, changes, time):
            for doc in snapshots:
                if doc.id == name:
                    object["data"] = doc.to_dict()

            finished_callback.set()

        document.on_snapshot(snapshot_received)
        self._requested[name] = object
        return object

    def set_data(self, name: str, new_data):
        self.database.document(name).set(new_data, merge=True)
