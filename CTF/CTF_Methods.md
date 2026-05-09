# CTF — Attack Methods

---

## 1. Core Concept

CTF (Capture The Flag) challenges teach real attack techniques on intentionally vulnerable systems. The methodology used in CTFs is identical to real penetration testing.

| CTF | Real Pentest |
|---|---|
| Find flags on practice systems | Find vulnerabilities on client systems |
| Legal and safe | Requires written permission |
| Same tools and techniques | Same tools and techniques |

Rule: Treat every CTF like a real engagement. Follow methodology, document everything.

---

## 2. Method 1 — Web Reconnaissance

When to use: Any web-based CTF challenge or real web pentest

### Step 1 — View page source
```
Press Ctrl+U in browser
Look for: HTML comments, usernames, passwords, hidden fields
Search for: password, user, admin, key, secret, flag
```

### Step 2 — Check robots.txt
```
targetIP/robots.txt
Lists directories hidden from search engines
Often contains passwords or sensitive directory names
```

### Step 3 — Check common directories
```
targetIP/login
targetIP/admin
targetIP/dashboard
targetIP/index.php
targetIP/assets
targetIP/uploads
targetIP/.git
targetIP/backup
```

### Step 4 — Try found credentials immediately
```
Any username or password found = try it on every login page
Common defaults: admin/admin, admin/password, root/root
```

> Rule: Page source → robots.txt → directories → login. Always in this order.

---

## 3. Method 2 — Command Execution Exploitation

When to use: Any command panel, search box executing system commands

### Step 1 — Confirm command execution
```bash
whoami          # confirms execution works, shows current user
id              # shows user ID and groups
hostname        # shows machine name
```

### Step 2 — Explore the filesystem
```bash
ls              # list current directory
ls -la          # list all including hidden files
pwd             # show current location
cat filename    # read any file
```

### Step 3 — Find the flags
```bash
find / -name "*.txt" 2>/dev/null        # find all text files
find / -name "*flag*" 2>/dev/null       # find flag files
find / -name "*secret*" 2>/dev/null     # find secret files
ls /home                                # check user home directories
ls /var/www/html                        # check web root
ls /root                                # check root directory
```

### Step 4 — Check privilege escalation
```bash
sudo -l                     # list commands you can run as root
sudo cat /root/flag.txt     # read root files if sudo allowed
sudo /bin/bash              # get root shell if bash allowed
```

> Rule: whoami → ls → find flags → sudo -l → escalate. Every shell follows this order.

---

## 4. Method 3 — OSINT in CTFs

When to use: Any CTF giving you a name, image, email, or username

### Step 1 — Extract image metadata
```bash
exiftool image.jpg
```

### Step 2 — Search all platforms
```
Google the name or username
Twitter, GitHub, LinkedIn, WordPress, Instagram
```

### Step 3 — Investigate websites
```
View page source Ctrl+U
Check robots.txt
Look for hidden comments and credentials
```

> Rule: Image → metadata → username → social media → website → page source → flag

---

## 5. Quick Reference — Web CTF Checklist

```
View page source (Ctrl+U)
Check robots.txt
Check /login, /admin, /assets
Try default credentials
Run whoami if command execution found
Run ls -la in current directory
Run sudo -l to check privileges
Run find / -name "*.txt" to find flags
Check /home directories
Check /root if accessible
Check /var/www/html for web files
```

---

## 6. Common Credential Hiding Spots

| Location | How to find it |
|---|---|
| HTML page source | Ctrl+U, search for username or password |
| robots.txt | targetIP/robots.txt |
| URL parameters | Look at the URL bar carefully |
| HTTP response headers | Browser dev tools Network tab |
| Config files | cat config.php, cat .env |
| Git repository | cat .git/config, git log |
| Database files | find / -name "*.db" |

> Rule: Credentials are always somewhere. Be systematic and check every location.

---
