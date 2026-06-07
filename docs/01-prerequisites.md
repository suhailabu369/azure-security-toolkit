# 📋 Step 1 — Prerequisites

Before running the Azure Security Toolkit, make sure you have the following ready on your machine.

---

## 1.1 Python 3.8 or Higher

### Check if Python is already installed

**Windows:**
```bash
python --version
```

**Mac/Linux:**
```bash
python3 --version
```

You should see something like `Python 3.10.x` or higher.  
If you get an error or see Python 2.x — install Python first.

### Install Python (if not installed)

- Download from: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- During installation on Windows — **check the box that says "Add Python to PATH"** before clicking Install
- Verify again after installation using the command above

---

## 1.2 pip (Python Package Manager)

pip comes bundled with Python 3.8+. Verify it's available:

**Windows:**
```bash
pip --version
```

**Mac/Linux:**
```bash
pip3 --version
```

If pip is missing, run:
```bash
python -m ensurepip --upgrade
```

---

## 1.3 Git (to clone the repo)

### Check if Git is installed
```bash
git --version
```

### Install Git (if not installed)
- Download from: [https://git-scm.com/downloads](https://git-scm.com/downloads)
- Default installation settings are fine

---

## 1.4 Azure Requirements

You will need:

| Requirement | Details |
|-------------|---------|
| Azure AD Tenant | An active Azure subscription or free trial |
| Admin Access | Global Admin or Privileged Role Admin to create App Registration and grant consent |

> Don't have an Azure tenant? You can create a **free Azure trial** at [https://azure.microsoft.com/free](https://azure.microsoft.com/free) — includes Azure AD access.

---

## ✅ Checklist Before Moving On

- [ ] Python 3.8+ installed and showing correct version
- [ ] pip working
- [ ] Git installed
- [ ] Azure admin access available

---

➡️ Next: [Step 2 — Azure App Registration Setup](./02-azure-setup.md)
