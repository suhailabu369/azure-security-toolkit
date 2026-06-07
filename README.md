# 🔐 Azure Security Toolkit

A Python-based toolkit to audit Azure tenant misconfigurations — identifying security gaps across MFA enrollment, Conditional Access policies, overprivileged app registrations, and guest user exposure.

Built from real-world experience securing enterprise Azure environments.

---

## 🎯 What This Toolkit Covers

| Check | Description | MITRE ATT&CK |
|-------|-------------|--------------|
| MFA Coverage | Identifies users with no MFA methods registered | T1078 – Valid Accounts |
| Conditional Access | Flags policies not enforcing MFA or compliant devices | T1078 – Valid Accounts |
| Overprivileged Apps | Detects app registrations with high-privilege API permissions | T1098 – Account Manipulation |
| Guest User Audit | Lists guest accounts and their group memberships | T1136 – Create Account |
| Stale Accounts | Finds accounts inactive for 90+ days | T1078 – Valid Accounts |

---

## 🛠️ Prerequisites

- Python 3.8+
- An Azure AD tenant with admin access
- An App Registration with the following **Microsoft Graph API** permissions (Application type):
  - `User.Read.All`
  - `Policy.Read.All`
  - `Application.Read.All`
  - `AuditLog.Read.All`
  - `Directory.Read.All`

---

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/suhailabu369/azure-security-toolkit.git
cd azure-security-toolkit
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure credentials
Create a `.env` file in the root directory:
```
TENANT_ID=your-tenant-id
CLIENT_ID=your-app-client-id
CLIENT_SECRET=your-client-secret
```

> ⚠️ Never commit your `.env` file. It is already included in `.gitignore`.

### 4. Run the audit
```bash
python audit.py
```

---

## 📊 Sample Output

```
============================================================
        AZURE SECURITY AUDIT REPORT
============================================================

[!] MFA GAPS DETECTED
------------------------------------------------------------
  - john.doe@company.com         No MFA methods registered
  - jane.smith@company.com       No MFA methods registered

[!] CONDITIONAL ACCESS ISSUES
------------------------------------------------------------
  - Policy "Block Legacy Auth" : Missing - No policy blocking legacy authentication
  - Policy "Require MFA - All Users" : MFA not enforced for all users

[!] OVERPRIVILEGED APP REGISTRATIONS
------------------------------------------------------------
  - App: "InternalSyncApp"
    Permission: Directory.ReadWrite.All (High Privilege)

[!] GUEST USER EXPOSURE
------------------------------------------------------------
  - guest_user@external.com      Member of: IT-Admins, Finance-Team

[✓] Stale Account Check
------------------------------------------------------------
  - 3 accounts inactive for 90+ days

============================================================
Audit complete. Review findings and remediate accordingly.
============================================================
```

---

## 📁 Project Structure

```
azure-security-toolkit/
├── audit.py              # Main script — runs all checks
├── checks/
│   ├── mfa_check.py      # MFA enrollment audit
│   ├── ca_check.py       # Conditional Access policy audit
│   ├── app_check.py      # App registration permission audit
│   └── guest_check.py    # Guest user audit
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🔒 Security Note

This tool is read-only — it only uses `Read` permissions and makes no changes to your tenant. Safe to run in production environments.

---

## 📌 Roadmap

- [ ] Export findings to CSV / JSON report
- [ ] Add Azure role assignment audit (detect Global Admin overuse)
- [ ] Add HTML report generation
- [ ] Integrate with Microsoft Sentinel for automated alerting

---

## 👤 Author

**Suhail T A** — Cloud & Infrastructure Security Engineer  
[LinkedIn](https://www.linkedin.com/in/suhailta) · [GitHub](https://github.com/suhailabu369)
