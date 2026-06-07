# ⚙️ Step 4 — Installation

Now that your credentials are set up, let's clone the repo and install the dependencies.

---

## 4.1 Clone the Repository

Open your terminal (Command Prompt / PowerShell on Windows, Terminal on Mac/Linux) and run:

```bash
git clone https://github.com/suhailabu369/azure-security-toolkit.git
cd azure-security-toolkit
```

This downloads the project to your machine and navigates into the folder.

---

## 4.2 (Recommended) Create a Virtual Environment

A virtual environment keeps this project's dependencies isolated from your other Python projects.  
This is best practice and avoids version conflicts.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You'll see `(venv)` appear at the start of your terminal line — that means it's active.

> To deactivate the virtual environment later, simply type: `deactivate`

---

## 4.3 Install Dependencies

With your virtual environment active, run:

```bash
pip install -r requirements.txt
```

This installs the 2 required libraries:
- `requests` — makes HTTP calls to Microsoft Graph API
- `python-dotenv` — reads your `.env` credentials file

You should see output like:
```
Collecting requests==2.31.0
  Downloading requests-2.31.0...
Collecting python-dotenv==1.0.0
  Downloading python_dotenv-1.0.0...
Successfully installed python-dotenv-1.0.0 requests-2.31.0
```

---

## 4.4 Copy your .env file into the project folder

If you created your `.env` file elsewhere, make sure it's in the root of the project:

```
azure-security-toolkit/
├── audit.py
├── .env          ← must be here
├── requirements.txt
...
```

---

## 4.5 Verify everything is in place

Run this quick check to confirm Python can find your credentials:

**Windows:**
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('TENANT_ID:', os.getenv('TENANT_ID')[:8] + '...' if os.getenv('TENANT_ID') else 'NOT FOUND')"
```

**Mac/Linux:**
```bash
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print('TENANT_ID:', os.getenv('TENANT_ID')[:8] + '...' if os.getenv('TENANT_ID') else 'NOT FOUND')"
```

You should see your TENANT_ID partially printed — confirming the `.env` is being read correctly.

---

## ✅ Checklist Before Moving On

- [ ] Repo cloned successfully
- [ ] Virtual environment created and activated (venv)
- [ ] `pip install -r requirements.txt` completed without errors
- [ ] `.env` file is in the project root folder
- [ ] Credential verification check passed

---

➡️ Next: [Step 5 — Running the Audit](./05-running-the-audit.md)
