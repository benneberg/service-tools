# dise-provisioning-service
A Dise provisioning service tool for Dise Partners


# DISE — SignageOS Google Provisioning (Web module)

Single-file web module to let partners easily produce the **Google Workspace Customer ID** and a **Service Account JSON key** required by SignageOS ChromeOS provisioning.

This repo is intended for hosting on GitHub Pages (or any HTTPS origin).

---

## Contents

- `index.html` — Single page app (UI + logic)
- `README.md` — This file

---

## What the tool does (flows)

### Variant A — Create service account & key (recommended)
1. Partner authenticates with Google (Workspace Admin).
2. App fetches Workspace **Customer ID** via Admin SDK (`customers.get`).
3. App creates a new service account in the provided GCP **project**.
4. App creates a service account key (JSON) and shows it in the browser.
5. Partner downloads the JSON and mails it to `support@dise.com`.

### Variant B — Use existing service account
1. Partner authenticates with Google (Workspace Admin).
2. App fetches **Customer ID**.
3. Partner provides an existing service account email; the app creates a new JSON key for that account.
4. Partner downloads and mails it to support.

---

## One-time setup (owner / admin of the dev Google Cloud project)

1. **Create or choose a Google Cloud project** that will be used for OAuth client & to enable APIs.

2. **Enable APIs** in that project:
   - Admin SDK API
   - IAM API

3. **Configure OAuth consent screen**
   - Console → APIs & Services → OAuth consent screen
   - App name, support email (support@dise.com), authorized domains (e.g. `benneberg.github.io`)
   - For External apps, Google may require verification if requesting sensitive scopes in production. For initial testing you can use External with up to 100 test users.

4. **Create OAuth 2.0 Client ID** (Web application)
   - Console → APIs & Services → Credentials → Create Credentials → OAuth client ID → Web application
   - **Authorized JavaScript origins**: add your site origin(s), for example:
     - `https://benneberg.github.io`
     - `https://benneberg.github.io/dise-provisioning-service/`
   - Copy the **Client ID** (e.g. `1234-abcd...apps.googleusercontent.com`)

5. Paste the Client ID into the `index.html` UI or edit the file to hardcode it (optional).

---

## Running / Testing locally (recommended to test before publishing)

1. Serve the `index.html` from a local HTTPS server OR push to GitHub Pages (GitHub Pages serves over HTTPS).
   - For quick local testing you can use `http-server` with a valid TLS proxy, but easiest is to host on GitHub Pages while developing.
2. Open `index.html`, paste your OAuth Client ID, choose a variant, and click **Authenticate & Run**.
3. Sign in with a **Workspace Super Admin** account and follow prompts.

---

## Deployment: GitHub Pages

1. Create a repository `dise-provisioning-service` (or use the existing one).
2. Add `index.html` and `README.md` to the repo.
3. In GitHub repository settings → Pages → Source: choose `main` branch and `/ (root)` folder.
4. After a few minutes, the site will be available at `https://<username>.github.io/dise-provisioning-service/`.
5. Add that origin to your OAuth client’s Authorized JavaScript origins.

---

## Troubleshooting (common errors and fixes)

### "Missing OAuth scopes" / permission errors
**Symptom**: Error message mentions `insufficient authentication scopes` or failing Admin SDK.
**Fix**:
- Ensure the token flow requested the Admin SDK and IAM scopes.
- Make sure the signed-in account is a **Workspace Super Admin**.

### "Permission denied" or "Insufficient permissions"
**Symptom**: IAM create service account or key fails.
**Fix**:
- For Variant A the user must have IAM roles (e.g. `Service Account Admin` or `Owner`) in the chosen project.
- If the organization prevents key creation, ask the partner’s Cloud Admin to allow it or provide an existing service account/key.

### "Organization policy denies this request"
**Symptom**: Error message references org policy or constraint.
**Fix**:
- The partner’s Org Policy may block service account keys. Partner Cloud Admin must either:
  - Allow service account key creation for the project, or
  - Provide an existing service account key (Variant B), or
  - Use an alternate secure flow (server-side).

### "Admin SDK not enabled"
**Symptom**: `customers.get` returns not found or 403.
**Fix**:
- Ensure Admin SDK API is enabled in the OAuth project and that the signed-in user is an Admin.

### CORS / origin blocked
**Symptom**: Browser console shows CORS or origin errors.
**Fix**:
- Ensure your page origin is added to the OAuth client’s **Authorized JavaScript origins**.
- Make sure the page is served over HTTPS.

---

## Security notes & recommendations

- This tool displays a service account private key (JSON) in the browser. That key is sensitive — treat it like a password.
- **Do not** store private keys on public servers unless they are encrypted and access-controlled.
- For production automation, replace the `mailto:` step with a secure HTTPS POST endpoint that:
  - Accepts data over TLS,
  - Requires authentication,
  - Stores keys encrypted at rest,
  - Records consent and audit logs.
- Consider rotating keys and setting automated expiry or using Workload Identity Federation where possible for higher security.

---

## Audit & support

- The app keeps an **audit log** (downloadable) with timestamps for each action and error. When a partner reports an issue, ask them to attach the audit log — it makes debugging much faster.

---

## Screenshots 
Add to the repo and reference them in the README where helpful.

---

## Next steps & production notes

- Replace `mailto:` with a secure server endpoint (preferred).
- Add server-side verification & storage, and automatic POST to SignageOS API if desired.
- Add better UX for domain-wide delegation instructions if you plan to use Admin impersonation for other actions.
- Optionally implement a short-lived key or rotate keys, and record an acceptance flow.

---

## Contact / Support

