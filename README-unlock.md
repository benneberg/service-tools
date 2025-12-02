# SignageOS Device Unlock Tool

## Purpose
Removes the **Standalone Mode Locked** policy from specific devices in SignageOS. Useful when partners need a device unlocked without giving them full admin access.

## Features
- Enter Device ID and Policy ID in the UI.
- Click **Run** to remove the policy.
- Optional **Copy API Call** button for CLI-based backup.
- Manual instructions for fallback.

## Usage (Web UI)
1. Open the **SignageOS Unlock** tool in the Service Tools App.
2. Enter **Device ID** and **Policy ID**.
3. Click **Run** to remove policy.
4. Optionally, click **Copy API Call** for CLI use.

## Manual Fallback (portal):
1. Log in to SignageOS with admin account.
2. Navigate to **Organizations → [Target Org] → Devices**.
3. Select the device → **Policies**.
4. Remove the **Standalone Mode Locked** policy.
5. Verify removal and inform the partner.

## Security
- Only authorized support staff should unlock devices.
- Ensure API key is restricted to **devices:write** and **devices:read** scopes.
- Log all unlock actions for audit.
