# EDR Evasion & In-Memory Execution Playbook

This playbook outlines post-exploitation execution techniques designed to operate within monitored enterprise environments running modern Endpoint Detection and Response (EDR) solutions.

---

## 1. User-Mode Hooking & API Unhooking (T1562.001)

### Mechanism of EDR User-Mode Detection
EDR agents inject a monitoring DLL into newly spawned processes and place `JMP` instructions (hooks) at the entry points of critical Windows Native APIs (such as `NtCreateThreadEx`, `NtAllocateVirtualMemory`, `NtWriteVirtualMemory`) inside `ntdll.dll`.

```
Application Calls NtAllocateVirtualMemory()
                    │
                    ▼
       [ ntdll.dll in memory ]
   ┌───────────────────────────────┐
   │ JMP edr_sensor.dll            │ ──► [ EDR Telemetry & Behavioral Engine ]
   │ (Hook placed by security agent│
   └───────────────────────────────┘
```

### Remediation via Clean NTDLL Mapping
To bypass user-mode hooks, the loader reads a fresh copy of `ntdll.dll` from the disk or `\KnownDlls\ntdll.dll` into memory and restores the original `.text` section bytes of the hooked functions:
1. Locate base address of loaded `ntdll.dll` via the Process Environment Block (`PEB`).
2. Map `\SystemRoot\System32\ntdll.dll` from disk using `CreateFileMapping` and `MapViewOfFile`.
3. Compare the `.text` sections.
4. Overwrite modified instructions with original bytes using `VirtualProtect` (temporarily set to `PAGE_EXECUTE_READWRITE`, write original bytes, restore to `PAGE_EXECUTE_READ`).

---

## 2. Indirect Syscalls (Hell's Gate / Halo's Gate)

Rather than jumping directly into `ntdll.dll` where hooks might remain, indirect syscalls locate the syscall number (SSN) dynamically and jump to a generic `syscall` instruction within the legitimate `ntdll.dll` memory space:
- **Call Stack Spoofing**: The return address on the thread stack points back inside legitimate `ntdll.dll` code rather than untrusted, newly allocated shellcode memory.
- Bypasses kernel-level telemetry rules that inspect call stack integrity (e.g. Microsoft Threat Intelligence ETW / Defender for Endpoint stack walks).

---

## 3. AMSI & ETW Memory Patching (T1562.001)

### Antimalware Scan Interface (AMSI) Bypass
AMSI analyzes scripts (PowerShell, VBScript, Office Macros) in memory before execution:
- To disable AMSI within the current process, patch the `AmsiScanBuffer` function export in `amsi.dll` to return `E_INVALIDARG` (`0x80070057`):
```c
// Example logic in C/C++:
DWORD oldProtect;
void* pAmsiScan = GetProcAddress(GetModuleHandleA("amsi.dll"), "AmsiScanBuffer");
VirtualProtect(pAmsiScan, 6, PAGE_EXECUTE_READWRITE, &oldProtect);

// x64 patch bytes: mov eax, 0x80070057; ret
unsigned char patch[] = { 0xB8, 0x57, 0x00, 0x07, 0x80, 0xC3 };
memcpy(pAmsiScan, patch, sizeof(patch));
VirtualProtect(pAmsiScan, 6, oldProtect, &oldProtect);
```

### Event Tracing for Windows (ETW) Patching
ETW logs security events directly to the OS telemetry pipeline. Patching `EtwEventWrite` inside `ntdll.dll` with a simple `ret` instruction (`0xC3`) prevents telemetry from leaving the process.

---

## 4. Process Injection & Masquerading (T1055 / T1036)

### Parent Process ID (PPID) Spoofing
When spawning helper processes, spawning them as children of `powershell.exe` or `cmd.exe` alerts behavioral analytics:
- Red team loaders initialize `STARTUPINFOEX` with `PROC_THREAD_ATTRIBUTE_PARENT_PROCESS`.
- Assign `explorer.exe` or `svchost.exe` as the parent PID.

### Block Non-Microsoft DLL Policy
Prevent EDR DLLs from injecting into child processes:
```c
DWORD64 policy = PROCESS_CREATION_MITIGATION_POLICY_BLOCK_NON_MICROSOFT_BINARIES_ALWAYS_ON;
UpdateProcThreadAttribute(lpAttributeList, 0, PROC_THREAD_ATTRIBUTE_MITIGATION_POLICY, &policy, sizeof(policy), NULL, NULL);
```

---

## 5. C2 Network Profile Hardening (T1071 / T1001)
- **Sleep & Jitter**: Configure beacon sleep timers to 60 seconds with 25-35% jitter to defeat automated beaconing detection algorithms.
- **Header Masking**: Mimic legitimate telemetry traffic (e.g. `Host: telemetry.microsoft.com`, standard HTTP headers, legitimate TLS 1.3 ciphers).
