# Service Tools App

This application provides internal support tools for partners, including:

1. **Provisioning Tool** – Automates Google Workspace / Cloud setup for signageOS.
2. **SignageOS Device Unlock Tool** – Removes Standalone Mode Locked policy from devices.

---

## Features

- Web-based interface with clear **Script** and **Readme** tabs.
- Safe backend to call SignageOS REST API.
- CTA buttons for **Run** and **Copy API call**.
- Manual instructions for backup.

---

## Installation

1. Clone repository:
```bash
git clone <repo-url>
cd support-app

export SIGNAGEOS_API_KEY="your_signageos_api_key"

Run app: 
python app.py


Open http://127.0.0.1:5000/.

Docker (recommended)

Create a .env file with:
