
# SignageOS – Un Lock StandAloneDevice

Purpose
- Let support remove the Standalone Mode Locked device policy for a device identified by its LAN IP.

How it works
1. Support enters the device IP (assigned during provisioning), Policy ID, and optionally Org ID and Support User.
2. The backend calls signageOS `GET /devices` and looks for the device object that matches the IP.
3. The backend calls `DELETE /devices/{deviceId}/policies/{policyId}`.
4. The action is audited into `./data/audit.log`.

Authentication (two options)
- Preferred (X-Auth): set `SIGNAGEOS_X_AUTH` environment variable to `tokenId:tokenSecret`.
- Alternative (Bearer): set `SIGNAGEOS_API_KEY` environment variable.

Security
- Protect the host (run behind an internal reverse proxy / private network).
- Do not commit credentials; use environment variables.
- Audit log persists to `./data/audit.log` (rotating).

Manual fallback (Box UI)
- Log into signageOS Box, go to Organizations → Devices, find device by IP/name and remove the policy in the Policies tab.
