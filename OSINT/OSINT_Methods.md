# OSINT — Attack Methods

---

## 1. Core Concept

Open Source Intelligence (OSINT) is collecting information about a target using only publicly available sources. No hacking, no unauthorized access — everything is already visible on the internet.

| Passive OSINT | Active OSINT |
|---|---|
| Google searches, social media, public records | Directly interacting with target systems |
| No risk of detection | May trigger alerts |
| Always start here | Only after passive exhausted |

**Rule:** One clue always leads to another. Follow every thread until it dead-ends.

---

## 2. Method 1 — Image Metadata Extraction

Extract hidden information embedded inside image files.

**When to use:** Any image file given as a starting point

### Step 1 — Install exiftool
```bash
sudo apt install exiftool
```

### Step 2 — Extract metadata
```bash
exiftool filename.jpg
```

### Step 3 — Read every field carefully
```
Look for: Author, Creator, GPS Coordinates, Comment, Copyright
Any name, username, or location is a clue
```

### What metadata reveals

| Field | What it tells you |
|---|---|
| Author / Creator | Real name or username |
| GPS Coordinates | Exact location photo was taken |
| Device Make/Model | Phone or camera used |
| Comment | Sometimes contains usernames or passwords |
| Software | Application used to create file |

> **Rule:** Read every single field. The clue can be anywhere in the output.

---

## 3. Method 2 — Username Investigation

Search a username or real name across all platforms.

**When to use:** Any name or username found from metadata or other sources

### Step 1 — Google the name
```
"username"
"username" site:twitter.com
"username" site:github.com
"username" password
```

### Step 2 — Check platforms in order
```
Twitter/X     → twitter.com/username
GitHub        → github.com/username
LinkedIn      → linkedin.com/in/username
WordPress     → username.wordpress.com
Instagram     → instagram.com/username
Facebook      → facebook.com/username
```

### Step 3 — On each profile look for
```
Bio           → email, website, location
Linked sites  → follow every external link
Posts         → personal information, locations
Photos        → location tags, faces, backgrounds
```

> **Rule:** Every profile leads to more profiles. Map everything before drawing conclusions.

---

## 4. Method 3 — Website Investigation

Investigate any website found during OSINT.

**When to use:** Any website or blog linked from a social media profile

### Step 1 — View page source
```
Press Ctrl+U in browser
Search for: password, email, key, secret, admin, token
```

### Step 2 — Check robots.txt
```
website.com/robots.txt
Lists pages the owner wants hidden from Google
Often reveals admin panels and sensitive directories
```

### Step 3 — Check common paths
```
website.com/admin
website.com/login
website.com/wp-admin        WordPress admin
website.com/.git            Exposed git repository
website.com/backup          Backup files
website.com/.env            Environment variables with credentials
```

> **Rule:** What is hidden from the public is usually the most valuable. Check robots.txt first.

---

## 5. Method 4 — GitHub Investigation

GitHub is the richest OSINT source — developers accidentally expose sensitive data constantly.

**When to use:** Any GitHub profile found during investigation

### Step 1 — Check all repositories
```
Look through every repo including forked ones
Read every README.md
Check config files, .env files, settings files
```

### Step 2 — Search for sensitive keywords
```
password
api_key
secret
token
credentials
private_key
```

### Step 3 — Check commit history
```
Click Commits tab in any repo
Even deleted data exists in old commits
Read every commit message
```

> **Rule:** Deleted code is not gone — it lives in commit history forever.

---

## 6. Quick Reference — OSINT Tools

| Tool | Purpose | How to access |
|---|---|---|
| exiftool | Extract image metadata | `sudo apt install exiftool` |
| Google | Search everything | google.com |
| Wayback Machine | Old versions of websites | web.archive.org |
| Have I Been Pwned | Check email in breaches | haveibeenpwned.com |
| Shodan | Internet-connected devices | shodan.io |
| theHarvester | Emails and subdomains | `sudo apt install theharvester` |

---

## 7. Complete OSINT Workflow

```
START
  ↓
Image / Name / Email / Domain given
  ↓
Run exiftool on any images
  ↓
Google everything found
  ↓
Find social media profiles
  ↓
Check Twitter → GitHub → LinkedIn → WordPress
  ↓
Investigate every linked website
  ↓
View page source, check robots.txt, check common paths
  ↓
Search GitHub repos and commit history
  ↓
Cross-reference all findings
  ↓
Document complete profile of target
```

> **Rule:** Never stop at one source. The complete picture only appears when you connect everything together.

---
