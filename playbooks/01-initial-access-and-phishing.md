# Initial Access & Perimeter Breach Playbook

This playbook covers methodologies for establishing initial footholds in enterprise environments aligned with the MITRE ATT&CK framework.

## 1. External Reconnaissance & Pre-Attack Preparation
* **Target Profiling (T1592 / T1589)**: Identify corporate email formats, organizational hierarchies, VPN portals, and Single Sign-On (SSO) endpoints via passive OSINT (LinkedIn, GitHub commits, WHOIS, DNS records).
* **Infrastructure Setup (T1583 / T1584)**:
  - Register aged domains categorized under Financial, Healthcare, or Technology classifications to bypass standard proxy reputation filters.
  - Configure forward and reverse DNS, DKIM, SPF (`v=spf1 include:... ~all`), and strict DMARC (`p=reject`) policies to ensure inbox delivery.

---

## 2. Payload Delivery & Evasion (T1566 / T1204)

### Container Formatting (ISO / VHD)
Packaging payloads inside container formats bypasses Windows Mark-of-the-Web (MOTW) NTFS alternate data streams (`Zone.Identifier`):
1. **Payload Structure**:
   - `invoice_q4.iso` containing:
     - Hidden payload binary or DLL: `app.dll`
     - Legitimate decoy document: `Q4_Financial_Report.pdf`
     - Visible Windows Shortcut: `Invoice_Summary.lnk`
2. **LNK Target Argument Obfuscation**:
   The shortcut executes a living-off-the-land binary (LOLBAS) to load the disguised DLL without invoking `powershell.exe` directly:
   ```cmd
   C:\Windows\System32\rundll32.exe app.dll,StartRoutine
   ```

### HTML Smuggling (T1027.006)
Embedding base64-encoded payload bytes directly within client-side JavaScript on a legitimate-looking landing page:
- The browser reconstructs the blob dynamically in client memory and triggers a standard download:
  ```javascript
  function downloadPayload(base64Data, filename) {
      const byteCharacters = atob(base64Data);
      const byteNumbers = new Array(byteCharacters.length);
      for (let i = 0; i < byteCharacters.length; i++) {
          byteNumbers[i] = byteCharacters.charCodeAt(i);
      }
      const byteArray = new Uint8Array(byteNumbers);
      const blob = new Blob([byteArray], { type: "application/octet-stream" });
      const link = document.createElement("a");
      link.href = window.URL.createObjectURL(blob);
      link.download = filename;
      link.click();
  }
  ```
- **Detection Evasion**: Because no executable crosses the network boundary in transit (only obfuscated JavaScript text), network-level content inspection and gateway sandboxes are bypassed.

---

## 3. Perimeter Exploitation (T1190)
When phishing is out-of-scope or restricted by the Rules of Engagement (RoE):
- Scan external boundaries for unauthenticated N-day vulnerabilities on perimeter appliances (e.g. SSL VPN concentrators, remote access gateways, exposed file transfer services).
- Verify proof-of-concept exploits locally in lab environments prior to execution against production systems to eliminate denial-of-service risks.

---

## 4. Verification & Operational Security Checklist
- [x] C2 communication routes through redirectors (CDN / Apache reverse proxies) hiding backend team server IP.
- [x] Initial payloads do not drop uncompiled `.ps1` or unsigned `.exe` files directly to `%TEMP%`.
- [x] In-memory execution verified against offline endpoint security controls prior to deployment.
