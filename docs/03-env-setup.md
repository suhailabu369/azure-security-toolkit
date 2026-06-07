# 🔑 Step 3 — Environment Setup (.env file)

The script reads your Azure credentials from a `.env` file stored **locally on your machine**.  
This keeps your secrets out of the code and out of GitHub.

---

## 3.1 What is a .env file?

A `.env` file is a plain text file that stores sensitive configuration values as key=value pairs.  
The script reads these values at runtime using the `python-dotenv` library.

```
TENANT_ID=your-tenant-id
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
```

> 🔒 This file is listed in `.gitignore` — it will **never** be uploaded to GitHub.  
> The `.env.example` file in this repo is a safe template with no real values.

---

## 3.2 Create your .env file

### Option A — Copy from the example file (recommended)

**Mac/Linux:**
```bash
cp .env.example .env
```

**Windows (Command Prompt):**
```bash
copy .env.example .env
```

**Windows (PowerShell):**
```bash
Copy-Item .env.example .env
```

Then open the `.env` file and replace the placeholder values with your real credentials from Step 2.

---

### Option B — Create manually

**Windows:**
1. Open **Notepad**
2. Type the following — replacing with your actual values:
```
TENANT_ID=paste-your-tenant-id-here
CLIENT_ID=paste-your-client-id-here
CLIENT_SECRET=paste-your-client-secret-here
```
3. Click **File** → **Save As**
4. Navigate to your project folder (`azure-security-toolkit`)
5. In the **File name** field type: `.env`
6. In **Save as type** select: **All Files** ← important, do not leave as .txt
7. Click **Save**

**Mac/Linux:**
```bash
cd azure-security-toolkit
nano .env
```
Type the 3 lines with your real values → press `Ctrl+X` → `Y` → `Enter` to save

---

## 3.3 Fill in your credentials

Open your `.env` file and it should look exactly like this with your real values:

```
TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
CLIENT_SECRET=your~actual~secret~value~here
```

These values come from your App Registration created in Step 2:

| Variable | Where to get it |
|----------|----------------|
| `TENANT_ID` | Azure Portal → App Registration → Overview → Directory (tenant) ID |
| `CLIENT_ID` | Azure Portal → App Registration → Overview → Application (client) ID |
| `CLIENT_SECRET` | Azure Portal → App Registration → Certificates & secrets → Value |

---

## 3.4 Verify the file is in the right place

Your project folder should look like this:

```
azure-security-toolkit/
├── audit.py
├── requirements.txt
├── .env            ← your credentials file (local only)
├── .env.example    ← safe template (on GitHub)
├── .gitignore
├── README.md
└── docs/
```

---

## 3.5 Confirm .gitignore is protecting your .env

Open `.gitignore` and confirm `.env` is listed:

```
.env
__pycache__/
*.pyc
*.pyo
.DS_Store
```

If `.env` is listed — your credentials will never be accidentally pushed to GitHub.

---

## ✅ Checklist Before Moving On

- [ ] `.env` file created in the project root folder
- [ ] All 3 values filled in with real credentials
- [ ] `.env` is NOT uploaded to GitHub (check your repo — it should not appear)
- [ ] `.env.example` IS on GitHub (with placeholder values only)

---

➡️ Next: [Step 4 — Installation](./04-installation.md)
