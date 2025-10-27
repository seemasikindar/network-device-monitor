# db.py
# Temporary in-memory DB for testing
db_store = {"logs": []}

class InMemoryCollection:
    def __init__(self, name):
        self.name = name
        self.data = db_store[name]

    def update_one(self, query, update, upsert=False):
        # Simple upsert by device_id
        device_id = update["$set"]["device_id"]
        found = False
        for i, doc in enumerate(self.data):
            if doc["device_id"] == device_id:
                self.data[i] = update["$set"]
                found = True
                break
        if not found and upsert:
            self.data.append(update["$set"])

    def find(self, query=None, projection=None):
        if query is None:
            return self.data
        result = []
        for doc in self.data:
            match = True
            for k, v in query.items():
                if doc.get(k) != v:
                    match = False
                    break
            if match:
                result.append(doc)
        return result

def get_db():
    class DB:
        logs = InMemoryCollection("logs")
    return DB()

