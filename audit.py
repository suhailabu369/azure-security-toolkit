"""
Azure Security Toolkit — audit.py
Description: Audits Azure tenant for common misconfigurations across
             MFA, Conditional Access, App Registrations, and Guest Users.
"""

import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
GRAPH_BETA = "https://graph.microsoft.com/beta"

# ─────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────

def get_access_token():
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "https://graph.microsoft.com/.default"
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json().get("access_token")


def graph_get(token, url):
    headers = {"Authorization": f"Bearer {token}"}
    results = []
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        results.extend(data.get("value", []))
        url = data.get("@odata.nextLink")
    return results


# ─────────────────────────────────────────────
# CHECK 1 — MFA GAPS
# ─────────────────────────────────────────────

def check_mfa_gaps(token):
    print("\n[✓] Checking MFA enrollment...")
    users = graph_get(token, f"{GRAPH_BASE}/users?$select=displayName,userPrincipalName,accountEnabled")
    gaps = []

    for user in users:
        if not user.get("accountEnabled"):
            continue
        upn = user.get("userPrincipalName", "")
        if "#EXT#" in upn:  # skip guests here
            continue
        methods_url = f"{GRAPH_BASE}/users/{user['id']}/authentication/methods"
        try:
            methods = graph_get(token, methods_url)
            # passwordAuthenticationMethod is always present — real MFA = more than 1 method
            if len(methods) <= 1:
                gaps.append(upn)
        except Exception:
            pass

    return gaps


# ─────────────────────────────────────────────
# CHECK 2 — CONDITIONAL ACCESS POLICIES
# ─────────────────────────────────────────────

def check_conditional_access(token):
    print("[✓] Checking Conditional Access policies...")
    policies = graph_get(token, f"{GRAPH_BETA}/identity/conditionalAccess/policies")
    issues = []

    has_mfa_policy = False
    has_legacy_block = False

    for policy in policies:
        if policy.get("state") != "enabled":
            continue
        grant_controls = policy.get("grantControls") or {}
        built_in = grant_controls.get("builtInControls", [])
        conditions = policy.get("conditions", {})
        client_apps = conditions.get("clientAppTypes", [])

        if "mfa" in built_in:
            users = conditions.get("users", {})
            # Check if policy applies to all users
            if not users.get("excludeUsers") and not users.get("includeGroups"):
                has_mfa_policy = True

        if "exchangeActiveSync" in client_apps or "other" in client_apps:
            has_legacy_block = True

    if not has_mfa_policy:
        issues.append(('Policy "Require MFA - All Users"', "MFA not enforced for all users"))
    if not has_legacy_block:
        issues.append(('Policy "Block Legacy Auth"', "Missing - No policy blocking legacy authentication"))

    return issues


# ─────────────────────────────────────────────
# CHECK 3 — OVERPRIVILEGED APP REGISTRATIONS
# ─────────────────────────────────────────────

HIGH_PRIVILEGE_PERMISSIONS = [
    "Directory.ReadWrite.All",
    "User.ReadWrite.All",
    "Mail.ReadWrite",
    "Files.ReadWrite.All",
    "RoleManagement.ReadWrite.Directory",
    "Application.ReadWrite.All",
    "Group.ReadWrite.All",
]

def check_app_permissions(token):
    print("[✓] Checking app registration permissions...")
    apps = graph_get(token, f"{GRAPH_BASE}/applications?$select=displayName,requiredResourceAccess,id")
    flagged = []

    # Get service principal list to resolve permission GUIDs to names
    sps = graph_get(token, f"{GRAPH_BASE}/servicePrincipals?$filter=appId eq '00000003-0000-0000-c000-000000000000'&$select=appRoles,oauth2PermissionScopes")
    perm_map = {}
    if sps:
        for role in sps[0].get("appRoles", []):
            perm_map[role["id"]] = role["value"]

    for app in apps:
        app_name = app.get("displayName", "Unknown")
        for resource in app.get("requiredResourceAccess", []):
            for perm in resource.get("resourceAccess", []):
                perm_name = perm_map.get(perm["id"], perm["id"])
                if perm_name in HIGH_PRIVILEGE_PERMISSIONS:
                    flagged.append((app_name, perm_name))

    return flagged


# ─────────────────────────────────────────────
# CHECK 4 — GUEST USER AUDIT
# ─────────────────────────────────────────────

def check_guest_users(token):
    print("[✓] Checking guest user exposure...")
    guests = graph_get(token, f"{GRAPH_BASE}/users?$filter=userType eq 'Guest'&$select=displayName,userPrincipalName,id")
    guest_info = []

    for guest in guests:
        upn = guest.get("userPrincipalName", "")
        groups_url = f"{GRAPH_BASE}/users/{guest['id']}/memberOf?$select=displayName"
        try:
            groups = graph_get(token, groups_url)
            group_names = [g.get("displayName", "") for g in groups]
            guest_info.append((upn, group_names))
        except Exception:
            guest_info.append((upn, []))

    return guest_info


# ─────────────────────────────────────────────
# CHECK 5 — STALE ACCOUNTS (90+ days inactive)
# ─────────────────────────────────────────────

def check_stale_accounts(token):
    print("[✓] Checking for stale accounts...")
    cutoff = (datetime.now(timezone.utc) - timedelta(days=90)).strftime("%Y-%m-%dT%H:%M:%SZ")
    url = (
        f"{GRAPH_BETA}/users?$filter=accountEnabled eq true"
        f" and signInActivity/lastSignInDateTime le {cutoff}"
        f"&$select=displayName,userPrincipalName,signInActivity"
    )
    try:
        stale = graph_get(token, url)
        return stale
    except Exception:
        return []


# ─────────────────────────────────────────────
# REPORT
# ─────────────────────────────────────────────

def print_report(mfa_gaps, ca_issues, app_issues, guest_info, stale_accounts):
    divider = "-" * 60
    print("\n" + "=" * 60)
    print("        AZURE SECURITY AUDIT REPORT")
    print("        " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)

    # MFA
    print(f"\n{'[!] MFA GAPS DETECTED' if mfa_gaps else '[✓] MFA Coverage — No gaps found'}")
    print(divider)
    for upn in mfa_gaps:
        print(f"  - {upn:<45} No MFA methods registered")

    # Conditional Access
    print(f"\n{'[!] CONDITIONAL ACCESS ISSUES' if ca_issues else '[✓] Conditional Access — Policies look good'}")
    print(divider)
    for policy, reason in ca_issues:
        print(f"  - {policy} : {reason}")

    # App Permissions
    print(f"\n{'[!] OVERPRIVILEGED APP REGISTRATIONS' if app_issues else '[✓] App Registrations — No high-privilege apps found'}")
    print(divider)
    for app_name, perm in app_issues:
        print(f"  - App: \"{app_name}\"")
        print(f"    Permission: {perm} (High Privilege)")

    # Guests
    print(f"\n{'[!] GUEST USER EXPOSURE' if guest_info else '[✓] Guest Users — None found'}")
    print(divider)
    for upn, groups in guest_info:
        group_str = ", ".join(groups) if groups else "No group memberships"
        print(f"  - {upn:<45} Member of: {group_str}")

    # Stale Accounts
    print(f"\n{'[!] STALE ACCOUNTS (90+ days inactive)' if stale_accounts else '[✓] Stale Accounts — None found'}")
    print(divider)
    for user in stale_accounts:
        last_sign_in = user.get("signInActivity", {}).get("lastSignInDateTime", "Never")
        print(f"  - {user.get('userPrincipalName', ''):<45} Last sign-in: {last_sign_in}")

    print("\n" + "=" * 60)
    print("Audit complete. Review findings and remediate accordingly.")
    print("=" * 60 + "\n")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("Starting Azure Security Audit...")

    if not all([TENANT_ID, CLIENT_ID, CLIENT_SECRET]):
        print("[ERROR] Missing credentials. Please check your .env file.")
        exit(1)

    token = get_access_token()

    mfa_gaps       = check_mfa_gaps(token)
    ca_issues      = check_conditional_access(token)
    app_issues     = check_app_permissions(token)
    guest_info     = check_guest_users(token)
    stale_accounts = check_stale_accounts(token)

    print_report(mfa_gaps, ca_issues, app_issues, guest_info, stale_accounts)
