from flask import Flask, jsonify
from db import get_db
from parse_xml import load_device_data

app = Flask(__name__)

# Home route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API is running!"})

# Load XML data
@app.route("/load", methods=["GET"])
def load_data():
    try:
        load_device_data()  # Make sure this function exists in parse_xml.py
        return jsonify({"message": "XML data loaded successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get all devices
@app.route("/devices", methods=["GET"])
def get_devices():
    try:
        db = get_db()
        devices = list(db.logs.find({}, {"_id": 0}))
        return jsonify(devices)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get devices with status DOWN
@app.route("/devices/down", methods=["GET"])
def get_down_devices():
    try:
        db = get_db()
        devices = list(db.logs.find({"status": "DOWN"}, {"_id": 0}))
        return jsonify(devices)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get devices with status UP
@app.route("/devices/up", methods=["GET"])
def get_up_devices():
    try:
        db = get_db()
        devices = list(db.logs.find({"status": "UP"}, {"_id": 0}))
        return jsonify(devices)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get devices with status RUNNING
@app.route("/devices/running", methods=["GET"])
def get_running_devices():
    try:
        db = get_db()
        devices = list(db.logs.find({"status": "RUNNING"}, {"_id": 0}))
        return jsonify(devices)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Bind to all interfaces (optional) and enable debug
    app.run(debug=True, host="0.0.0.0", port=5000)
