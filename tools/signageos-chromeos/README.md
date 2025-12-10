# SignageOS ChromeOS Provisioning Tool

## Description
Automates the provisioning of Google Workspace and Google Cloud for use with signageOS ChromeOS device management.

## Features
- **Automated Script Generation**: Generates a complete bash script for gcloud provisioning
- **Download Functionality**: Download the script as a `.sh` file
- **Copy to Clipboard**: Quick copy functionality for the entire script
- **Comprehensive Documentation**: Detailed README with step-by-step instructions

## What the Script Does
1. Creates or selects a Google Cloud Project
2. Enables required APIs (Admin SDK, Chrome Management, IAM)
3. Creates a Service Account
4. Generates and downloads a JSON key
5. Provides Customer ID and Service Account Client ID
6. Shows exact manual steps for Domain-Wide Delegation and Admin Role Privileges

## Requirements
- Google Workspace Super Admin account
- Access to Google Cloud Shell or local gcloud CLI

## Usage
1. Navigate to the SignageOS - ChromeOS page
2. Click "Download" to get the script file, or "Copy" to copy to clipboard
3. Run the script in your Google Cloud Shell or local environment
4. Follow the manual steps provided in the script output

## Review Status
✅ Script reviewed and verified (2025-03-11)
- All gcloud commands current and correct
- API enablement steps verified
- OAuth scopes validated for ChromeOS device management

## Files
- `index.html` - Page structure and UI
- `script.js` - Script generation and interaction logic
- `README.md` - This documentation
