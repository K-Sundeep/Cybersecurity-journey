# Nmap — TryHackMe (Further Nmap)
### Beginner-Friendly Notes

---

## 1. What is Nmap?

**Nmap (Network Mapper)** is a free, open-source tool used by network administrators and security professionals to scan networks. Think of it as a way to "knock on doors" of a computer to see which ones are open, what's behind them, and who's home.

It was first released in 1997 and is now one of the most widely used tools in cybersecurity.

**What can Nmap tell you?**
- Which computers (hosts) are alive on a network
- Which ports are open, closed, or blocked on a target
- What software/services are running behind each open port
- What version those services are
- What operating system the target is running
- Potential security weaknesses

**⚠️ Legal warning:** Only scan networks and systems you own or have **explicit written permission** to scan. Unauthorized port scanning is illegal in many countries.

---

## 2. Understanding Ports — The Foundation

### What is a port?

Think of a computer like an office building. The building's address is the **IP address** — it gets you to the right building. But once you're there, you need to know which **room (port)** to go to for the right service.

- Port `80` → Web server (HTTP)
- Port `443` → Secure web server (HTTPS)
- Port `22` → SSH (remote terminal)
- Port `21` → FTP (file transfer)
- Port `25` → Email (SMTP)

Every networked computer has **65,535 ports**:
- Ports **0–1023** = "Well-known ports" — reserved for standard services
- Ports **1024–49151** = Registered ports — used by specific apps
- Ports **49152–65535** = Dynamic/ephemeral — used temporarily by your OS

Only **one service** can listen on a given port at a time (on the same IP address).

### What is a service?

A **service** is a program running on a computer that **listens** on a specific port waiting for connections. When Nmap finds an open port, it tries to figure out what service is listening there.

**Example:**
```
22/tcp  open  ssh    OpenSSH 7.4 (protocol 2.0)
80/tcp  open  http   Apache httpd 2.4.6
443/tcp open  https  nginx 1.18.0
```

### The 6 port states Nmap reports

| State | What it means | Why it happens |
|---|---|---|
| `open` | A service is actively listening — you can connect | Normal — something is running there |
| `closed` | Port is reachable but nothing is listening | Accessible but no service running |
| `filtered` | Nmap can't tell — a firewall is blocking it | Firewall silently drops packets |
| `open\|filtered` | Can't tell if open or filtered | No response (UDP, NULL, FIN, Xmas scans) |
| `unfiltered` | Accessible but can't determine open/closed | Only with ACK scan |
| `closed\|filtered` | Can't tell if closed or filtered | Only with Idle/IP ID scan |

---

## 3. Understanding TCP — How Connections Work

Before understanding Nmap's scan types, you need to understand how TCP connections work. This is called the **Three-Way Handshake**.

### The TCP Three-Way Handshake

Whenever two computers want to communicate over TCP, they first establish a connection using a three-step process:

```
Step 1: Your computer sends a SYN packet
        "Hey, I want to connect to you!"

Step 2: The target responds with SYN-ACK
        "Got it! I'm here and I'm ready."

Step 3: Your computer sends ACK
        "Great! Let's talk."
        ← Connection is now established, data can flow →
```

In diagram form:
```
Your PC  ──── SYN ────────────→  Target
Your PC  ←─── SYN/ACK ─────────  Target
Your PC  ──── ACK ────────────→  Target
           [Connection Open — data flows]
```

**If the port is CLOSED**, the target responds to your SYN with RST:
```
Your PC  ──── SYN ────────────→  Target
Your PC  ←─── RST/ACK ─────────  Target     ← "No service here, go away"
```

**If the port is FILTERED** (firewall blocking):
```
Your PC  ──── SYN ────────────→  Target
            [silence — no reply]             ← Firewall dropped the packet
```

Understanding this handshake is the key to understanding every Nmap scan type.

**TCP Flag meanings:**

| Flag | Meaning |
|---|---|
| `SYN` | Synchronize — "I want to start a connection" |
| `ACK` | Acknowledge — "I received your message" |
| `RST` | Reset — "Stop this connection immediately" |
| `FIN` | Finish — "I want to close the connection gracefully" |
| `PSH` | Push — "Send this data to the app immediately" |
| `URG` | Urgent — "This data is urgent" |

---

## 4. Scan Types — Explained Simply

### TCP Connect Scan — `-sT`

**The most basic scan.** Completes a full three-way handshake with every port. Used when NOT running as root/sudo.

```bash
nmap -sT 192.168.1.1
```

**Open port:**
```
Your PC  ──── SYN ────────→  Target     "Is anyone there?"
Your PC  ←─── SYN/ACK ────  Target     "Yes! I'm here!" → PORT IS OPEN
Your PC  ──── ACK ────────→  Target     "Cool..."
Your PC  ──── RST ────────→  Target     "Actually never mind, I'm done." (Nmap closes it)
```

**Closed port:**
```
Your PC  ──── SYN ────────→  Target     "Is anyone there?"
Your PC  ←─── RST/ACK ────  Target     "Nothing here!" → PORT IS CLOSED
```

**Pros:** Works without root, reliable, works on all OS
**Cons:** Very **noisy** — web servers, SSH, firewalls all log complete connections. Easily detected.

---

### SYN Scan (Stealth / Half-Open) — `-sS`

**The most popular scan.** Default when running as root. Never completes the handshake — aborts halfway through. Called "half-open" or "stealth."

```bash
sudo nmap -sS 192.168.1.1        # Requires sudo/root
```

**Open port:**
```
Your PC  ──── SYN ────────→  Target     "Is anyone there?"
Your PC  ←─── SYN/ACK ────  Target     "Yes! I'm here!" → PORT IS OPEN
Your PC  ──── RST ────────→  Target     "Never mind!" (kills it before app is notified)
```

**Closed port:**
```
Your PC  ──── SYN ────────→  Target
Your PC  ←─── RST/ACK ────  Target     → PORT IS CLOSED
```

**Filtered port:**
```
Your PC  ──── SYN ────────→  Target
            [no response]               → PORT IS FILTERED
```

**Why stealthier than `-sT`:** Because the connection never fully opens, the **application** (e.g. Apache) is never notified — so it doesn't log it. **However,** network-level firewalls and IDS can still detect the pattern of SYN packets.

**Pros:** Fast, applications don't log it, preferred by pentesters
**Cons:** Needs root. Modern IDS can still detect it.

---

### UDP Scan — `-sU`

UDP is **connectionless** — there's no handshake. Nmap fires a packet and sees what happens.

```bash
sudo nmap -sU 192.168.1.1
```

| What Nmap receives | Port state |
|---|---|
| No response | `open\|filtered` |
| UDP response | `open` |
| ICMP "Port Unreachable" | `closed` |

**Why UDP is slow:** Closed ports return ICMP errors but OS rate-limits ICMP → Nmap must wait between probes. Top 1000 UDP ports = 15–20+ minutes.

**Tip — combine UDP and SYN:**
```bash
sudo nmap -sU -sS 192.168.1.1
```

---

### NULL, FIN, and Xmas Scans

All three exploit the same RFC 793 quirk: an open port **ignores** unexpected packets → no response. A closed port sends back RST.

**NULL Scan — `-sN`:** No flags at all
**FIN Scan — `-sF`:** Only FIN flag
**Xmas Scan — `-sX`:** FIN + PSH + URG flags (lit up like a Christmas tree 🎄)

```bash
sudo nmap -sN 192.168.1.1
sudo nmap -sF 192.168.1.1
sudo nmap -sX 192.168.1.1
```

**Response table:**

| Response | Port state |
|---|---|
| No response | `open\|filtered` |
| RST received | `closed` |

**Why use them?** To bypass firewalls that only filter SYN packets.

**⚠️ Big caveat:** Windows ignores RFC 793 — sends RST for ALL ports. These scans are **unreliable on Windows targets** — everything looks closed.

---

### ICMP Ping Sweep — `-sn`

Discovers which hosts are **alive** without scanning any ports.

```bash
nmap -sn 192.168.1.0/24         # Entire /24 subnet
nmap -sn 192.168.1.1-50         # IP range
```

Sends ICMP ping to every IP — anything that replies = live host. Always run before port scanning to find active targets first.

**Skip host discovery with `-Pn`:**
```bash
sudo nmap -Pn 192.168.1.1       # Scan even if host doesn't respond to ping
```
Useful when ICMP is blocked (many servers block ping).

---

## 5. All Nmap Switches Explained

### Scan Type Switches

| Switch | Scan | Needs sudo | Notes |
|---|---|---|---|
| `-sS` | SYN/Stealth | ✅ Yes | Default with sudo. Fast and semi-stealthy |
| `-sT` | TCP Connect | ❌ No | Default without sudo. Full handshake, noisy |
| `-sU` | UDP | ✅ Yes | Slow but finds UDP services |
| `-sN` | NULL | ✅ Yes | No flags. Bypasses SYN firewalls. Fails on Windows |
| `-sF` | FIN | ✅ Yes | FIN flag only. Same limitations as NULL |
| `-sX` | Xmas | ✅ Yes | FIN+PSH+URG. Same limitations |
| `-sn` | Ping sweep | ❌ No | Host discovery only, no port scan |
| `-Pn` | Skip ping | ❌ No | Assume host is up, skip host discovery |

---

### Detection Switches

**`-sV` — Service/Version Detection**
```bash
sudo nmap -sV 192.168.1.1
```
Without `-sV`, Nmap guesses from port number (`22 = ssh`). With `-sV`, it actually connects and interrogates the service to get the real name and version.

Output: `22/tcp open ssh OpenSSH 7.4p1 Debian 10`

**`-O` — OS Detection** (needs sudo)
```bash
sudo nmap -O 192.168.1.1
```
Fingerprints the OS by analyzing how it responds to various probes.
Output: `OS details: Linux 3.2 - 4.9`

**`-A` — Aggressive Mode** (runs everything at once)
```bash
sudo nmap -A 192.168.1.1
```
Enables: OS detection + version detection + default scripts + traceroute.
Very noisy but gives a complete picture. Perfect for CTFs.

---

### Output Switches

Always save scan output — you don't want to re-run a long scan.

| Switch | Format | Use case |
|---|---|---|
| `-oN file` | Normal (readable) | Human reading |
| `-oX file` | XML | Importing into other tools |
| `-oG file` | Grepable | Searching with grep |
| `-oA file` | All three at once | ✅ Always use this |

```bash
sudo nmap -oA scan_results 192.168.1.1
# Creates: scan_results.nmap, scan_results.xml, scan_results.gnmap

grep "open" scan_results.gnmap          # Find open ports quickly
```

**Verbosity — see results as they happen:**
```bash
sudo nmap -vv 192.168.1.1              # Very verbose — recommended
```
Without `-v`, Nmap runs silently until done. With `-vv`, open ports appear in real time.

---

### Port Specification

| Switch | What it scans |
|---|---|
| `-p 80` | Only port 80 |
| `-p 22,80,443` | Specific ports |
| `-p 1000-1500` | Range |
| `-p-` | All 65,535 ports |
| `-F` | Top 100 only (fast mode) |
| `--top-ports 500` | Top 500 most common |

> **For CTFs — always use `-p-`!** Services are often deliberately placed on unusual ports. You'll miss them with the default top-1000 scan.

---

### Timing Templates

| Switch | Name | Speed | Use when |
|---|---|---|---|
| `-T0` | Paranoid | Extremely slow | Maximum IDS evasion (5 min between packets) |
| `-T1` | Sneaky | Very slow | IDS evasion |
| `-T2` | Polite | Slow | Reduce network load |
| `-T3` | Normal | Default | Standard |
| `-T4` | Aggressive | Fast | ✅ CTFs and fast networks |
| `-T5` | Insane | Fastest | May miss results |

---

### Firewall Evasion Switches

| Switch | What it does |
|---|---|
| `-f` | Fragment packets into 8-byte chunks — harder for deep packet inspection |
| `--mtu <size>` | Custom fragment size (must be multiple of 8) |
| `--scan-delay <ms>` | Add delay between packets — evades rate-based IDS |
| `--badsum` | Invalid checksums — helps identify presence of firewalls |
| `--data-length <n>` | Append random data to disguise scan signature |
| `-D IP1,IP2,ME` | Decoy scan — traffic appears to come from multiple sources |

**Decoy example:**
```bash
sudo nmap -D 10.0.0.1,10.0.0.2,ME 192.168.1.100
# Target sees scan from 3 IPs — can't tell which is real
```

---

## 6. NSE — Nmap Scripting Engine

NSE lets you run **Lua scripts** that automate extra tasks beyond basic scanning — checking vulnerabilities, trying default logins, extracting info, and more.

### Script categories

| Category | What it does | Risk |
|---|---|---|
| `safe` | Non-intrusive info gathering | Low |
| `default` | Well-tested useful scripts (run with `-sC`) | Low |
| `discovery` | Enumerate services/network | Low |
| `version` | Enhanced version detection | Low |
| `auth` | Test authentication (anonymous login, blank passwords) | Medium |
| `vuln` | Check for known vulnerabilities (doesn't exploit) | Medium |
| `external` | Queries third-party services | Medium |
| `brute` | Brute-force credentials | High |
| `exploit` | Actively exploits vulnerabilities | High |
| `malware` | Check for backdoors | High |
| `intrusive` | May crash services | Very High |
| `dos` | **Will take down services** | Extreme |

### Using scripts

```bash
sudo nmap -sC 192.168.1.1                           # Run default scripts
sudo nmap --script=http-title 192.168.1.1           # Specific script
sudo nmap --script=smb-enum-shares,smb-enum-users 192.168.1.1  # Multiple
sudo nmap --script=vuln 192.168.1.1                 # All vuln scripts
sudo nmap --script=smb* 192.168.1.1                 # Wildcard — all SMB scripts
sudo nmap --script=ftp-anon --script-args ftp-anon.maxlist=50 192.168.1.1
```

### Finding scripts

```bash
ls /usr/share/nmap/scripts/                     # List all
ls /usr/share/nmap/scripts/ | grep smb          # Find SMB scripts
ls /usr/share/nmap/scripts/ | grep http         # Find HTTP scripts
```

---

## 7. Reading Nmap Output

**Sample output — `sudo nmap -A -T4 192.168.1.100`:**

```
PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 7.4p1 Debian 10 (protocol 2.0)
80/tcp   open  http     Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Welcome!
3306/tcp open  mysql    MySQL 5.7.28

OS details: Linux 3.2 - 4.9
```

**What this tells you:**
- Port 22 → SSH is running — could try to log in remotely
- Port 80 → Apache web server — there's a website
- Port 3306 → MySQL database is exposed — **major security issue!**
- OS is Linux (Ubuntu-based from the SSH/Apache headers)

---

## 8. Practical CTF Workflow

```bash
# Step 1: Quick scan of top 1000 ports
sudo nmap -sV 192.168.1.100

# Step 2: Full port scan (finds hidden services)
sudo nmap -p- -T4 192.168.1.100

# Step 3: Deep scan on discovered open ports
sudo nmap -sV -sC -O -p 22,80,3306 192.168.1.100

# Step 4: Run vuln scripts on interesting ports
sudo nmap --script=vuln -p 80,3306 192.168.1.100
```

**One-liner CTF scan:**
```bash
sudo nmap -sV -sC -p- -T4 -oA ctf_scan 192.168.1.100
```

---

## 9. Quick Reference

**Scan types:** `-sS` SYN | `-sT` TCP | `-sU` UDP | `-sN` NULL | `-sF` FIN | `-sX` Xmas | `-sn` ping | `-Pn` skip ping

**Detection:** `-sV` versions | `-O` OS | `-sC` scripts | `-A` all

**Ports:** `-p 80` | `-p 1-1000` | `-p-` all | `-F` top 100

**Output:** `-oA file` (all formats) | `-vv` verbose

**Timing:** `-T0` paranoid → `-T4` aggressive → `-T5` insane

**Scripts:** `-sC` defaults | `--script=name` | `--script=vuln`

---

## 10. Common Ports Reference

| Port | Service | Notes |
|---|---|---|
| 21 | FTP | File transfer — check anonymous login |
| 22 | SSH | Secure remote terminal |
| 23 | Telnet | Insecure remote — credentials sent in plaintext |
| 25 | SMTP | Email sending |
| 53 | DNS | Domain resolution |
| 80 | HTTP | Web server |
| 110 | POP3 | Email receiving |
| 139/445 | SMB/NetBIOS | Windows file sharing — often exploitable |
| 143 | IMAP | Email |
| 443 | HTTPS | Secure web |
| 1433 | MSSQL | Microsoft SQL database |
| 3306 | MySQL | MySQL database — shouldn't be public! |
| 3389 | RDP | Windows Remote Desktop |
| 5432 | PostgreSQL | PostgreSQL database |
| 5900 | VNC | Remote desktop (insecure) |
| 8080 | HTTP-alt | Web server on non-standard port |
