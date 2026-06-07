# 🚀 Step 5 — Running the Audit

Everything is set up. Let's run the audit.

---

## 5.1 Make sure your virtual environment is active

If you created a virtual environment in Step 4, activate it before running:

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

---

## 5.2 Run the script

**Windows:**
```bash
python audit.py
```

**Mac/Linux:**
```bash
python3 audit.py
```

---

## 5.3 What happens when it runs

The script will work through 5 checks sequentially:

```
Starting Azure Security Audit...
[✓] Checking MFA enrollment...
[✓] Checking Conditional Access policies...
[✓] Checking app registration permissions...
[✓] Checking guest user exposure...
[✓] Checking for stale accounts...
```

Each check calls the Microsoft Graph API and collects results.  
Depending on the size of your tenant, this may take 30 seconds to a few minutes.

---

## 5.4 Sample Output

```
============================================================
        AZURE SECURITY AUDIT REPORT
        2025-10-01 14:32:10
============================================================

[!] MFA GAPS DETECTED
------------------------------------------------------------
  - john.doe@company.com              No MFA methods registered
  - jane.smith@company.com            No MFA methods registered

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
  - guest@external.com                Member of: IT-Admins, Finance-Team

[!] STALE ACCOUNTS (90+ days inactive)
------------------------------------------------------------
  - old.account@company.com           Last sign-in: 2025-06-12T08:21:00Z

============================================================
Audit complete. Review findings and remediate accordingly.
============================================================
```

---

## 5.5 Understanding the findings

| Finding | Risk | Recommended Action |
|---------|------|--------------------|
| MFA gaps | High — accounts vulnerable to password spray attacks | Enforce MFA via Conditional Access or per-user MFA |
| No legacy auth block | High — legacy protocols bypass MFA | Create CA policy blocking `exchangeActiveSync` and `other` client apps |
| MFA not enforced for all users | High | Create CA policy targeting all users, require MFA grant control |
| Overprivileged apps | Medium-High — excessive permissions increase blast radius | Review and reduce to least-privilege permissions |
| Guest users in sensitive groups | Medium — third party access to internal resources | Review guest memberships and apply access reviews |
| Stale accounts | Medium — dormant accounts are easy targets | Disable or delete accounts inactive 90+ days |

---

## 5.6 What this script does NOT do

This tool is **read-only** — it only queries data and reports findings.  
It makes **zero changes** to your tenant. Safe to run in production environments.

---

## ✅ Audit Complete

If the script ran successfully — well done. You now have a clear picture of your Azure tenant's security posture across identity, access, and configuration.

Review the findings and prioritise remediation starting with **High** severity items first.

---

➡️ Having issues? See: [Step 6 — Troubleshooting](./06-troubleshooting.md)
