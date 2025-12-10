// SignageOS ChromeOS Provisioning Script
const gcloudScript = `#!/bin/bash
# This script will guide you through provisioning the necessary Google Cloud
# resources for signageOS ChromeOS device management.
#
# It will:
# 1. Prompt you to create or select a Google Cloud Project.
# 2. Enable the required APIs.
# 3. Create a Service Account.
# 4. Download a JSON key for that account.
# 5. Output the values you need for the **two mandatory manual steps**
#    (Domain-Wide Delegation and Admin Role Privileges).

set -e
echo "--- DISE/signageOS Provisioning Script ---"
echo ""

# 1. Set Project
read -p "Enter a NEW or EXISTING Google Cloud Project ID (e.g., my-signageos-project): " PROJECT_ID
if [ -z "$PROJECT_ID" ]; then
  echo "Project ID cannot be empty."
  exit 1
fi

echo "Configuring project: $PROJECT_ID"
# Try to create the project; if it exists, gcloud will notify and continue.
gcloud projects create $PROJECT_ID || echo "Project may already exist. Continuing..."
gcloud config set project $PROJECT_ID

echo "Project set to $PROJECT_ID"
echo ""

# 2. Enable APIs
echo "Enabling necessary APIs (Admin SDK, Chrome Management, IAM)..."
gcloud services enable admin.googleapis.com \\
                        chromemanagement.googleapis.com \\
                        iam.googleapis.com

echo "APIs enabled."
echo ""

# 3. Create Service Account
# We use a timestamp to ensure the SA name is unique
SA_NAME="signageos-integration-$(date +%s)"
SA_DISPLAY_NAME="SignageOS Integration"
echo "Creating Service Account: $SA_DISPLAY_NAME ($SA_NAME)"

gcloud iam service-accounts create $SA_NAME \\
  --display-name="$SA_DISPLAY_NAME" \\
  --description="Service Account for signageOS ChromeOS management"

SA_EMAIL=$(gcloud iam service-accounts list --filter="displayName:$SA_DISPLAY_NAME" --format="value(email)" --limit=1)
if [ -z "$SA_EMAIL" ]; then
  echo "Failed to create or find Service Account. Exiting."
  exit 1
fi
echo "Service Account created: $SA_EMAIL"
echo ""

# 4. Create JSON Key
KEY_FILE="./signageos-key.json"
echo "Generating and downloading JSON key to $KEY_FILE..."
gcloud iam service-accounts keys create $KEY_FILE \\
  --iam-account=$SA_EMAIL
echo "Key file created: $KEY_FILE"
echo ""

# 5. Get values for manual steps
echo "Fetching required IDs for manual setup..."
# Get the Unique ID (Client ID) for DWD
SA_CLIENT_ID=$(gcloud iam service-accounts describe $SA_EMAIL --format="value(oauth2ClientId)")
# Get the Customer ID
CUSTOMER_ID=$(gcloud auth print-access-token | xargs -I {} curl -s -H "Authorization: Bearer {}" https://admin.googleapis.com/admin/directory/v1/customers/my_customer | grep -o '"id": "[^"]*"' | cut -d'"' -f4)

if [ -z "$SA_CLIENT_ID" ] || [ -z "$CUSTOMER_ID" ]; then
  echo "Error: Could not retrieve all necessary IDs."
  echo "Please check your permissions. You must be a Workspace Admin."
  exit 1
fi

echo "--- SCRIPT FINISHED ---"
echo ""
echo "--- ⚠️ REQUIRED MANUAL STEPS ---"
echo "The script has finished. You MUST now complete these two manual steps in your Google Workspace Admin Console to finalize setup."
echo ""
echo "--- 1. DOMAIN-WIDE DELEGATION (DWD) ---"
echo "DWD authorizes the Service Account to access user data. You must delegate authority to a user who has the necessary ChromeOS Admin Role privileges (see Step 2)."
echo ""
echo "1. Go to: https://admin.google.com"
echo "2. Navigate to: Security > Access and data control > API Controls > Domain-wide Delegation"
echo "3. Click 'Add new'."
echo "4. For 'Client ID', enter this value:"
echo "   $SA_CLIENT_ID"
echo ""
echo "5. For 'OAuth scopes', paste the following text (comma-separated):"
echo "   https://www.googleapis.com/auth/admin.directory.device.chromeos,https://www.googleapis.com/auth/admin.directory.orgunit,https://www.googleapis.com/auth/chromemanagement.appdetails"
echo ""
echo "6. Click 'Authorize'."
echo ""
echo "--- 2. ADMIN ROLE PRIVILEGES ---"
echo "You must ensure the user whose email you will use for DWD (the delegate user) has the required privileges to manage ChromeOS devices."
echo ""
echo "1. In the Admin Console, navigate to: Account -> Admin roles."
echo "2. Edit an existing role (e.g., a custom role) or create a new one, and assign it to your chosen delegate user."
echo "3. Under 'Privileges', ensure the following options are CHECKED under the 'Chrome management' section:"
echo "   - Manage User Settings"
echo "   - Manage ChromeOS Devices"
echo "   - Manage ChromeOS Device Settings"
echo "   - View Reports"
echo ""
echo "--- PROVISIONING COMPLETE ---"
echo "You can now use the following details for your signageOS setup:"
echo ""
echo "   Customer ID: $CUSTOMER_ID"
echo "   Service Account Email: $SA_EMAIL"
echo "   Service Account Key File: $KEY_FILE (the file generated in your current directory)"
echo ""
`;

// Initialize the tool when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  const scriptCode = document.getElementById('scriptCode');
  const copyScriptBtn = document.getElementById('copyScriptBtn');
  const downloadScriptBtn = document.getElementById('downloadScriptBtn');

  // Put the script text into the <pre><code> block
  if (scriptCode) {
    scriptCode.textContent = gcloudScript;
  }

  // Wire up the copy button
  if (copyScriptBtn) {
    copyScriptBtn.addEventListener('click', () => {
      copyText(gcloudScript);
    });
  }

  // Wire up the download button
  if (downloadScriptBtn) {
    downloadScriptBtn.addEventListener('click', () => {
      downloadScript(gcloudScript, 'signageos-chromeos-provisioning.sh');
    });
  }
});
