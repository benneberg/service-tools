# SignageOS Unlock StandAloneDevice Tool

## Description
Tool for unlocking SignageOS standalone devices by removing the "Standalone Mode Locked" policy through the REST API or manual procedure.

## Features
- **REST API Integration**: Automated unlock via API call
- **Manual Procedure Guide**: Step-by-step instructions for manual unlocking
- **Copy API Call**: Generate and copy cURL command for the unlock operation
- **Audit Trail Support**: Optional fields for Org ID and support user tracking

## Security Notice
⚠️ **Important**: Only remove the policy for authorized requests to prevent accidental security risks.

## Usage

### Automated (REST API)
1. Enter the Device IP (assigned during Google provisioning)
2. Enter the Policy ID you wish to remove
3. Optionally enter Org ID and support user for audit tracking
4. Click "Run" to execute the unlock operation
5. Check the output for success/error messages

### Copy API Call
Click "Copy API Call" to generate a cURL command that can be run from command line or shared with technical support.

### Manual Procedure
1. Log into the SignageOS portal (box.signageos) with admin rights
2. Navigate to Organizations → [Target Org] → Devices
3. Search for the device by ID, serial number, or name
4. Click the device and go to Policies
5. Find the "Standalone Mode Locked" policy
6. Click Remove / Disable
7. Confirm removal
8. Verify the device no longer has the policy applied
9. Set standalone mode to unlocked and verify persistence
10. Communicate completion to partner
11. Inform partner to notify support when device should be locked again

## API Endpoint
- **Method**: POST
- **Endpoint**: `/api/signageos/unlock`
- **Content-Type**: application/json
- **Body**:
  ```json
  {
    "deviceIp": "192.168.10.5",
    "policyId": "policy-xxxx",
    "orgId": "optional",
    "supportUser": "optional"
  }
  ```

## Files
- `index.html` - Page structure and UI
- `script.js` - API interaction and form handling logic
- `README.md` - This documentation

## Last Updated
2025-12-02
