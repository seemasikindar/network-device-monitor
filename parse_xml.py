import xml.etree.ElementTree as ET
from datetime import datetime
from db import get_db
import os

def load_device_data(folder="devices"):
    db = get_db()
    logs = db.logs

    for file in os.listdir(folder):
        if file.endswith(".xml"):
            tree = ET.parse(os.path.join(folder, file))
            root = tree.getroot()
            device_id = root.find("DeviceID").text
            status = root.find("Status").text
            timestamp = root.find("Timestamp").text

            # Simple cleansing: validate timestamp
            try:
                datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                print(f"Invalid timestamp in {file}, skipping...")
                continue

            doc = {"device_id": device_id, "status": status, "timestamp": timestamp}
            logs.update_one({"device_id": device_id}, {"$set": doc}, upsert=True)
            print(f"Loaded {device_id} -> {status}")

if __name__ == "__main__":
    load_device_data()
