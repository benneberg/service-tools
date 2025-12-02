#!/usr/bin/env python3
import os
import json
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from flask import Flask, request, jsonify, render_template, abort
import requests

# ---------- Config ----------
SIGNAGEOS_API_BASE = os.getenv("SIGNAGEOS_API_BASE", "https://api.signageos.io/v2")
# Two supported auth methods:
#  - X_AUTH (preferred): set SIGNAGEOS_X_AUTH to "tokenId:tokenSecret" (will be used as X-Auth header)
#  - BEARER token: set SIGNAGEOS_API_KEY to a bearer token (used as Authorization: Bearer ...)
SIGNAGEOS_X_AUTH = os.getenv("SIGNAGEOS_X_AUTH")  # optional (tokenId:tokenSecret)
SIGNAGEOS_API_KEY = os.getenv("SIGNAGEOS_API_KEY")  # optional (Bearer)
if not (SIGNAGEOS_X_AUTH or SIGNAGEOS_API_KEY):
    raise RuntimeError("Set either SIGNAGEOS_X_AUTH (tokenId:tokenSecret) or SIGNAGEOS_API_KEY (Bearer token) in env")

AUDIT_LOG_PATH = os.getenv("AUDIT_LOG_PATH", "./data/audit.log")
os.makedirs(os.path.dirname(AUDIT_LOG_PATH) or ".", exist_ok=True)
MAX_LOG_BYTES = int(os.getenv("AUDIT_LOG_MAX_BYTES", "5242880"))
BACKUP_COUNT = int(os.getenv("AUDIT_LOG_BACKUP_COUNT", "3"))

# ---------- Logging / Audit ----------
logger = logging.getLogger("service_tools_audit")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(AUDIT_LOG_PATH, maxBytes=MAX_LOG_BYTES, backupCount=BACKUP_COUNT)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def audit(entry: dict):
    # Ensure timestamps & json string
    entry = dict(entry)
    entry.setdefault("timestamp", datetime.utcnow().isoformat() + "Z")
    logger.info(json.dumps(entry, ensure_ascii=False))

# ---------- Flask ----------
app = Flask(__name__, template_folder="templates", static_folder="static")

def _signageos_headers():
    """
    Build headers for signageOS API. Prefers X-Auth if configured, else Bearer token.
    """
    headers = {"Content-Type": "application/json"}
    if SIGNAGEOS_X_AUTH:
        headers["X-Auth"] = SIGNAGEOS_X_AUTH
    else:
        headers["Authorization"] = f"Bearer {SIGNAGEOS_API_KEY}"
    return headers

def find_device_by_ip(device_ip: str, page_limit: int = 250):
    """
    Attempt to find a signageOS device with a matching public/local IP.
    Strategy:
      - GET /devices (paginated) and search for any object that contains the IP in common fields.
    Returns device object or None.
    """
    headers = _signageos_headers()
    # iterate pages (if supported). We'll request in pages and attempt to match common fields.
    page = 0
    per_page = 100
    while True:
        params = {"limit": per_page, "offset": page * per_page}
        try:
            resp = requests.get(f"{SIGNAGEOS_API_BASE}/devices", headers=headers, params=params, timeout=15)
        except Exception as e:
            raise RuntimeError(f"Error calling signageOS devices list: {e}")

        if resp.status_code != 200:
            # return None but include body for diagnostics
            raise RuntimeError(f"signageOS responded {resp.status_code}: {resp.text}")

        try:
            data = resp.json()
        except Exception:
            # if not JSON, bail
            raise RuntimeError("signageOS returned invalid JSON for devices list")

        # Data may be an array or object with 'items' depending on API shape
        items = None
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            # common patterns: { items: [...], data: [...] } or { devices: [...] }
            items = data.get("items") or data.get("data") or data.get("devices") or []
        else:
            items = []

        if not items:
            break

        # Check device entries for IP (some fields commonly used: 'ip', 'networkInterfaces', 'lastKnownIp', 'privateIp')
        for dev in items:
            # Search simple keys
            candidates = []
            # common simple keys
            for k in ("ip", "lastKnownIp", "privateIp", "publicIp", "ipAddress"):
                v = dev.get(k) if isinstance(dev, dict) else None
                if v:
                    candidates.append(str(v))
            # nested network info
            if isinstance(dev, dict):
                # networkInterfaces, interfaces, network
                for nk in ("networkInterfaces", "interfaces", "network"):
                    ni = dev.get(nk)
                    if ni and isinstance(ni, list):
                        for entry in ni:
                            if isinstance(entry, dict):
                                for fk in ("ip", "address", "ipv4", "ipv6"):
                                    fv = entry.get(fk)
                                    if fv:
                                        candidates.append(str(fv))
                    elif ni and isinstance(ni, dict):
                        for fk in ("ip", "address", "ipv4", "ipv6"):
                            fv = ni.get(fk)
                            if fv:
                                candidates.append(str(fv))
                # metadata may contain ip
                meta = dev.get("metadata") or dev.get("systemInfo") or dev.get("info")
                if meta and isinstance(meta, dict):
                    for _, v in meta.items():
                        if isinstance(v, str) and device_ip in v:
                            candidates.append(v)
            # normalize and compare
            candidates = [c.strip() for c in candidates if isinstance(c, str)]
            if device_ip in candidates or any(device_ip == c for c in candidates):
                return dev

        # If we received fewer than per_page items, stop
        if len(items) < per_page:
            break
        page += 1

    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/api/signageos/unlock", methods=["POST"])
def api_signageos_unlock():
    """
    Body: JSON {
      deviceIp: "192.168.10.5",
      policyId: "policy-id",
      orgId: "org-id",            # optional, only used for audit
      supportUser: "jane.doe"     # optional, used for audit
    }
    """
    payload = request.get_json(force=True, silent=True)
    if not payload:
        return jsonify({"message": "Invalid JSON body"}), 400

    device_ip = payload.get("deviceIp")
    policy_id = payload.get("policyId")
    org_id = payload.get("orgId")
    support_user = payload.get("supportUser")
    remote_addr = request.remote_addr

    if not device_ip or not policy_id:
        audit({
            "action": "unlock_attempt",
            "device_ip": device_ip,
            "policy_id": policy_id,
            "org_id": org_id,
            "user": support_user,
            "remote_addr": remote_addr,
            "status": "BAD_REQUEST",
            "detail": "deviceIp and policyId are required"
        })
        return jsonify({"message": "deviceIp and policyId are required"}), 400

    # Find device by IP
    try:
        device = find_device_by_ip(device_ip)
    except Exception as e:
        audit({
            "action": "unlock_attempt",
            "device_ip": device_ip,
            "policy_id": policy_id,
            "org_id": org_id,
            "user": support_user,
            "remote_addr": remote_addr,
            "status": "ERROR",
            "detail": str(e)
        })
        return jsonify({"message": f"Error while searching for device by IP: {str(e)}"}), 500

    if not device:
        audit({
            "action": "unlock_attempt",
            "device_ip": device_ip,
            "policy_id": policy_id,
            "org_id": org_id,
            "user": support_user,
            "remote_addr": remote_addr,
            "status": "NOT_FOUND",
            "detail": "No device matched IP"
        })
        return jsonify({"message": "No device found for the provided IP"}), 404

    # Determine device id from common fields
    device_id = device.get("id") or device.get("deviceId") or device.get("uid") or device.get("uuid")
    if not device_id:
        # attempt to return raw device for debugging
        audit({
            "action": "unlock_attempt",
            "device_ip": device_ip,
            "policy_id": policy_id,
            "org_id": org_id,
            "user": support_user,
            "remote_addr": remote_addr,
            "status": "NO_DEVICE_ID",
            "detail": f"device found but no id field, device={device}"
        })
        return jsonify({"message": "Device found but could not determine device id; check device object"}), 500

    # Call signageOS API to delete policy
    headers = _signageos_headers()
    try:
        resp = requests.delete(f"{SIGNAGEOS_API_BASE}/devices/{device_id}/policies/{policy_id}", headers=headers, timeout=15)
    except Exception as e:
        audit({
            "action": "unlock_attempt",
            "device_ip": device_ip,
            "device_id": device_id,
            "policy_id": policy_id,
            "org_id": org_id,
            "user": support_user,
            "remote_addr": remote_addr,
            "status": "EXCEPTION",
            "detail": str(e)
        })
        return jsonify({"message": f"Exception during signageOS request: {str(e)}"}), 500

    if resp.status_code in (200, 204):
        audit({
            "action": "unlock",
            "device_ip": device_ip,
            "device_id": device_id,
            "policy_id": policy_id,
            "org_id": org_id,
            "user": support_user,
            "remote_addr": remote_addr,
            "status": "SUCCESS",
            "detail": f"signageOS_status={resp.status_code}"
        })
        return jsonify({"message": f"Policy {policy_id} removed from device {device_id}"}), 200
    else:
        detail = None
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text
        audit({
            "action": "unlock_attempt",
            "device_ip": device_ip,
            "device_id": device_id,
            "policy_id": policy_id,
            "org_id": org_id,
            "user": support_user,
            "remote_addr": remote_addr,
            "status": "FAILED",
            "detail": f"status={resp.status_code}, body={detail}"
        })
        return jsonify({"message": f"Failed to remove policy: {resp.status_code} - {detail}"}), 400

# Run local dev server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
