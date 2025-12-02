import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from flask import Flask, request, jsonify, render_template, abort

import requests

# Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")

# Configuration from environment
SIGNAGEOS_API_BASE = os.getenv("SIGNAGEOS_API_BASE", "https://api.signageos.io/v2")
SIGNAGEOS_API_KEY = os.getenv("SIGNAGEOS_API_KEY")  # REQUIRED
AUDIT_LOG_PATH = os.getenv("AUDIT_LOG_PATH", "./audit.log")
MAX_LOG_BYTES = int(os.getenv("AUDIT_LOG_MAX_BYTES", "5242880"))  # 5MB
BACKUP_COUNT = int(os.getenv("AUDIT_LOG_BACKUP_COUNT", "3"))

if not SIGNAGEOS_API_KEY:
    raise RuntimeError("SIGNAGEOS_API_KEY must be set as an environment variable")

# Setup structured-ish audit logger (rotating file)
logger = logging.getLogger("service_tools_audit")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(AUDIT_LOG_PATH, maxBytes=MAX_LOG_BYTES, backupCount=BACKUP_COUNT)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Helper: write audit entry
def audit(action, device_id=None, policy_id=None, org_id=None, user=None, remote_addr=None, status="OK", detail=None):
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "device_id": device_id,
        "policy_id": policy_id,
        "org_id": org_id,
        "user": user,
        "remote_addr": remote_addr,
        "status": status,
        "detail": detail
    }
    logger.info(entry)

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/unlock-device", methods=["POST"])
def unlock_device():
    """
    Body JSON:
    {
      "deviceId": "...",
      "policyId": "...",
      "orgId": "...",           # optional
      "supportUser": "john.d"   # optional - the support staff identifier for auditing
    }
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, description="Invalid or missing JSON body")

    device_id = data.get("deviceId") or data.get("device_id")
    policy_id = data.get("policyId") or data.get("policy_id")
    org_id = data.get("orgId") or data.get("org_id")
    support_user = data.get("supportUser") or data.get("support_user")
    remote_addr = request.remote_addr

    if not device_id or not policy_id:
        audit(
            action="unlock_attempt",
            device_id=device_id,
            policy_id=policy_id,
            org_id=org_id,
            user=support_user,
            remote_addr=remote_addr,
            status="BAD_REQUEST",
            detail="deviceId and policyId are required"
        )
        return jsonify({"message": "deviceId and policyId are required"}), 400

    # Build SignageOS API url
    url = f"{SIGNAGEOS_API_BASE}/devices/{device_id}/policies/{policy_id}"
    headers = {
        "Authorization": f"Bearer {SIGNAGEOS_API_KEY}",
        "Content-Type": "application/json"
    }

    # Call SignageOS API to remove policy
    try:
        resp = requests.delete(url, headers=headers, timeout=15)
    except Exception as e:
        audit(
            action="unlock_attempt",
            device_id=device_id,
            policy_id=policy_id,
            org_id=org_id,
            user=support_user,
            remote_addr=remote_addr,
            status="EXCEPTION",
            detail=str(e)
        )
        return jsonify({"message": f"Exception during request: {str(e)}"}), 500

    if resp.status_code in (200, 204):
        audit(
            action="unlock",
            device_id=device_id,
            policy_id=policy_id,
            org_id=org_id,
            user=support_user,
            remote_addr=remote_addr,
            status="SUCCESS",
            detail=f"SignageOS {resp.status_code}"
        )
        return jsonify({"message": f"Policy {policy_id} removed from device {device_id} (status {resp.status_code})"}), 200
    else:
        # Attempt to capture explanation from SignageOS response
        detail_text = None
        try:
            detail_text = resp.json()
        except Exception:
            detail_text = resp.text

        audit(
            action="unlock_attempt",
            device_id=device_id,
            policy_id=policy_id,
            org_id=org_id,
            user=support_user,
            remote_addr=remote_addr,
            status="FAILED",
            detail=f"status={resp.status_code}, body={detail_text}"
        )
        return jsonify({"message": f"Failed to remove policy: {resp.status_code} - {detail_text}"}), 400

# Health check
@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    # Local dev run
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=False)
