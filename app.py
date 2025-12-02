from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# ===== CONFIGURATION =====
SIGNAGEOS_API_BASE = "https://api.signageos.io/v2"
SIGNAGEOS_API_KEY = os.getenv("SIGNAGEOS_API_KEY")  # Keep secret in environment

# ===== ROUTES =====
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/unlock-device', methods=['POST'])
def unlock_device():
    data = request.json
    device_id = data.get("deviceId")
    policy_id = data.get("policyId")

    if not device_id or not policy_id:
        return jsonify({"message": "Device ID and Policy ID are required"}), 400

    url = f"{SIGNAGEOS_API_BASE}/devices/{device_id}/policies/{policy_id}"
    headers = {
        "Authorization": f"Bearer {SIGNAGEOS_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            return jsonify({"message": f"Policy {policy_id} successfully removed from device {device_id}"}), 200
        else:
            return jsonify({"message": f"Failed to remove policy: {response.status_code} - {response.text}"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# ===== RUN SERVER =====
if __name__ == "__main__":
    app.run(debug=True)
