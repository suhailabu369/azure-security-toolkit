# 🔧 Step 6 — Troubleshooting

Common errors and how to fix them.

---

## ❌ Error: `ModuleNotFoundError: No module named 'requests'`

**Cause:** Dependencies not installed, or virtual environment not active.

**Fix:**
```bash
# Activate virtual environment first
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Then install dependencies
pip install -r requirements.txt
```

---

## ❌ Error: `Missing credentials. Please check your .env file`

**Cause:** `.env` file is missing, in the wrong folder, or has empty values.

**Fix:**
1. Confirm `.env` exists in the project root (same folder as `audit.py`)
2. Open the file and confirm all 3 values are filled:
```
TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
CLIENT_SECRET=your-secret-value
```
3. Make sure the file is saved as `.env` and not `.env.txt`

**Windows tip:** File Explorer hides extensions by default. To verify:
- Open the folder → View → check **File name extensions**
- The file should show as `.env` not `.env.txt`

---

## ❌ Error: `401 Unauthorized` or `InvalidAuthenticationToken`

**Cause:** Client secret is wrong, expired, or copied incorrectly.

**Fix:**
1. Go to Azure Portal → App registrations → your app → Certificates & secrets
2. Check if your secret has expired
3. If expired — create a new secret and update your `.env` file
4. Make sure there are no extra spaces when copying the secret value

---

## ❌ Error: `403 Forbidden` or `Authorization_RequestDenied`

**Cause:** API permissions not granted or admin consent not given.

**Fix:**
1. Go to Azure Portal → App registrations → your app → API permissions
2. Verify all 5 permissions are listed
3. Check the status column — all should show green ✅ **Granted**
4. If not granted, click **Grant admin consent for [your org]** → Yes

---

## ❌ Error: `python is not recognized` (Windows)

**Cause:** Python not added to PATH during installation.

**Fix Option 1:** Reinstall Python and check **"Add Python to PATH"** during setup.

**Fix Option 2:** Use full path:
```bash
C:\Users\YourName\AppData\Local\Programs\Python\Python310\python.exe audit.py
```

**Fix Option 3:** Try `py` instead of `python`:
```bash
py audit.py
```

---

## ❌ Script runs but shows no findings

**Cause:** Your tenant may be well configured — or the beta API endpoint for sign-in activity may need an Entra ID P1/P2 license.

**Note:** The stale account check (`signInActivity`) requires **Entra ID P1 or P2**.  
If you're on a free tier, this check will return empty results — that's expected behavior, not an error.

---

## ❌ Script is very slow or times out

**Cause:** Large tenant with many users — pagination is working through many pages of results.

**Fix:** This is normal for large tenants. Let it run. If it times out consistently:
1. Check your internet connection
2. Try running during off-peak hours
3. The Graph API has throttling limits — if you hit them, wait a few minutes and retry

---

## Still stuck?

1. Check the [Microsoft Graph API status](https://developer.microsoft.com/en-us/graph/status)
2. Open an issue on this repo with:
   - The exact error message
   - Which step you're on
   - Your Python version (`python --version`)
   - Your OS (Windows/Mac/Linux)

---

➡️ Back to start: [Step 1 — Prerequisites](./01-prerequisites.md)
