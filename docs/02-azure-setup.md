# ☁️ Step 2 — Azure App Registration Setup

This script uses the **Microsoft Graph API** to read your Azure tenant data.  
To do that, you need to create an **App Registration** in Azure — this gives the script a secure identity to authenticate with.

> ⚠️ You need **Global Admin** or **Privileged Role Admin** access to complete this step.

---

## 2.1 Create the App Registration

1. Go to [https://portal.azure.com](https://portal.azure.com) and sign in
2. In the top search bar, type **App registrations** and click it
3. Click **+ New registration**
4. Fill in the following:
   - **Name:** `AzureSecurityAuditTool`
   - **Supported account types:** `Accounts in this organizational directory only (Single tenant)`
   - **Redirect URI:** Leave blank
5. Click **Register**

---

## 2.2 Copy Your Credentials

Once the app is created, you'll land on the **Overview** page.  
Copy and save these two values — you'll need them for your `.env` file:

| Value | Where to find it | Used as |
|-------|-----------------|---------|
| Application (client) ID | Overview page | `CLIENT_ID` |
| Directory (tenant) ID | Overview page | `TENANT_ID` |

---

## 2.3 Create a Client Secret

1. In the left menu, click **Certificates & secrets**
2. Click **+ New client secret**
3. Fill in:
   - **Description:** `audit-tool-secret`
   - **Expires:** 12 months
4. Click **Add**
5. **Immediately copy the Value shown** — this is your `CLIENT_SECRET`

> ⚠️ This value is only shown once. If you leave the page without copying it, you'll need to create a new secret.

---

## 2.4 Add API Permissions

The script needs read-only access to your tenant data via these 5 permissions.

1. In the left menu, click **API permissions**
2. Click **+ Add a permission**
3. Select **Microsoft Graph**
4. Select **Application permissions** (not Delegated)
5. Search and add each permission below:

| Permission | What the script uses it for |
|------------|----------------------------|
| `User.Read.All` | Read all user accounts and MFA methods |
| `Policy.Read.All` | Read Conditional Access policies |
| `Application.Read.All` | Read app registrations and their permissions |
| `AuditLog.Read.All` | Read sign-in activity for stale account detection |
| `Directory.Read.All` | Read group memberships and directory objects |

6. After adding all 5, click **Grant admin consent for [your organization]**
7. Click **Yes** to confirm
8. All 5 permissions should now show a green ✅ status

---

## 2.5 Verify Setup

Your API permissions page should look like this:

```
Microsoft Graph
├── AuditLog.Read.All          ✅ Granted
├── Application.Read.All       ✅ Granted
├── Directory.Read.All         ✅ Granted
├── Policy.Read.All            ✅ Granted
└── User.Read.All              ✅ Granted
```

---

## ✅ Checklist Before Moving On

- [ ] App Registration created
- [ ] CLIENT_ID copied
- [ ] TENANT_ID copied
- [ ] CLIENT_SECRET copied (saved safely)
- [ ] All 5 permissions added and admin consent granted

---

➡️ Next: [Step 3 — Environment Setup (.env file)](./03-env-setup.md)
