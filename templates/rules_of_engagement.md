# Red Team Rules of Engagement (RoE) Agreement

This document defines the formal boundaries, scope, authorization, emergency contacts, and operational protocols governing the Red Team adversary emulation exercise.

---

## 1. Exercise Objectives & Authorization
- **Primary Objective**: Evaluate corporate defensive controls, perimeter resilience, detection timelines, and internal response procedures against realistic Advanced Persistent Threat (APT) attack chains.
- **Authorization Authority**: Chief Information Security Officer (CISO) & Director of Security Operations.
- **Legal Safe Harbor**: All activities defined within Section 2 are pre-authorized and explicitly protected from prosecution or internal disciplinary action.

---

## 2. Scope Definition

### In-Scope Systems & Targets
- Corporate External IP Subnets: `198.51.100.0/24`, `203.0.113.0/24`
- In-Scope Domains: `*.corp.local`, `*.target-enterprise.com`
- User Workstation VLAN: `VLAN 20 (10.10.20.0/24)`
- Internal Server VLAN: `VLAN 10 (10.10.10.0/24)`

### Explicitly Out-of-Scope (Strictly Prohibited)
- Denial of Service (DoS / DDoS) attacks against any network link, server, or cloud service.
- Physical security breaches, lock picking, or entry into physical data centers.
- Customer-facing payment processing infrastructure (PCI-DSS Cardholder Data Environment).
- Modification or destruction of production data (read-only verification required upon compromise).

---

## 3. Trusted Agents & White Cell Coordination

The White Cell acts as the liaison between the Red Team and enterprise management, maintaining situational awareness while ensuring operational confidentiality.

| Role | Name | Title | Contact Number | Secure Email |
| :--- | :--- | :--- | :--- | :--- |
| **White Cell Lead** | Jane Doe | Director of InfoSec | +1-555-0192 | `jdoe@corp.local` |
| **SOC Liaison** | John Smith | SOC Manager | +1-555-0193 | `jsmith@corp.local` |
| **Red Team Lead** | Alex Vance | Lead Red Teamer | +1-555-0194 | `redteam-lead@partner.corp` |

---

## 4. Emergency Halt & Deconfliction Procedures

### Emergency Halt Conditions
The exercise will be halted immediately under any of the following circumstances:
1. Unplanned disruption of critical production services or customer transactions.
2. Discovery of an actual (non-simulated) external threat actor operating in the environment.
3. Formal request from the White Cell Lead or CISO.

### Deconfliction Protocol
When the SOC detects suspicious activity:
1. The SOC analyst contacts the White Cell Lead.
2. The White Cell checks the Red Team activity log (Timestamp, Source IP, Target Host, Action).
3. If activity matches the Red Team ledger: marked as **Deconflicted (Simulated Attack)**.
4. If activity does NOT match: treated immediately as an **Active Real-World Security Incident**.
