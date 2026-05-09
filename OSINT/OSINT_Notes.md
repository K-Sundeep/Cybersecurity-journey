# OSINT Notes — Open Source Intelligence

---

# Chapter 1 — OSINT Fundamentals

---

## 1. What is OSINT?

Open Source Intelligence (OSINT) is the practice of collecting information about a target using only publicly available sources — no hacking, no unauthorized access. Everything is already visible on the internet.

**Why it matters for cybersecurity:**
Every penetration testing engagement starts with OSINT. Before attempting any technical attack, a pentester maps everything publicly known about the target — employees, email formats, technologies used, exposed credentials, and digital footprints.

**Rule:** The more information you gather before attacking, the more targeted and effective your attack becomes.

---

## 2. OSINT Methodology — The Process

Always follow this order. Never skip steps.

| Step | Action | Purpose |
|---|---|---|
| 1 | Identify your starting point | Name, email, image, domain, username |
| 2 | Extract all metadata | Hidden information in files and images |
| 3 | Google everything found | Find connected accounts and profiles |
| 4 | Search all major platforms | Twitter, LinkedIn, GitHub, Instagram |
| 5 | Check linked websites and blogs | More personal information, credentials |
| 6 | View page source of websites | Hidden content not visible on screen |
| 7 | Cross-reference all findings | Build complete picture of the target |

> **Rule:** One clue leads to another. Follow every thread until it dead-ends.

---

## 3. Image Metadata — exiftool

Images contain hidden metadata — information embedded invisibly inside the file. Cameras and phones automatically store this when taking photos.

**Install exiftool:**
```bash
sudo apt install exiftool
```

**Basic usage:**
```bash
exiftool filename.jpg
exiftool filename.png
exiftool *.jpg          # scan all jpg files in folder
```

**What metadata can reveal:**

| Field | What it tells you |
|---|---|
| Author / Creator | Real name of person who created file |
| GPS Coordinates | Exact location where photo was taken |
| Device Make/Model | Phone or camera used |
| Software | Application used to create or edit |
| Creation Date | When file was originally created |
| Copyright | Often contains name or organization |
| Comment | Sometimes contains usernames or passwords |

**Example output:**
```bash
exiftool WindowsXP.jpg
# Look for fields like:
# Author        : oliverwoodflint
# GPS Position  : 51° 30' 51.90" N, 0° 7' 39.87" W
# Create Date   : 2013:01:14 07:09:02
```

> **Rule:** Read every single field in exiftool output. The clue can be in any field.

---

## 4. Username Investigation

Once you find a name or username, search it everywhere.

**Search order:**

```
1. Google: "username" or "full name"
2. Twitter/X: twitter.com/username
3. LinkedIn: linkedin.com/in/username
4. GitHub: github.com/username
5. Instagram: instagram.com/username
6. WordPress blogs: username.wordpress.com
7. Facebook: facebook.com/username
```

**What to look for on each platform:**

| Platform | What to check |
|---|---|
| Twitter/X | Bio, linked website, all tweets, location |
| LinkedIn | Employer, email, connections, skills |
| GitHub | Repos, README files, commit messages, config files |
| WordPress | All posts, About page, page source |
| Instagram | Bio, location tags, tagged photos |

**Advanced Google searches:**
```bash
"oliverwoodflint"                    # exact name match
"oliverwoodflint" site:twitter.com   # find on Twitter
"oliverwoodflint" site:github.com    # find on GitHub
"oliverwoodflint" password           # find leaked credentials
```

---

## 5. Website Investigation

When you find a linked website or blog, investigate it fully.

**Check page source:**
```
Press Ctrl+U in browser
Look for hidden comments, credentials, metadata
Search for: password, email, key, secret, admin
```

**Check robots.txt:**
```
website.com/robots.txt
Lists pages the owner wants hidden from search engines
Often reveals admin panels and sensitive directories
```

**Check common paths:**
```
website.com/admin
website.com/login
website.com/wp-admin        (WordPress admin panel)
website.com/.git            (exposed git repository)
website.com/backup          (backup files)
```

**Find email format:**
```
If you find one employee email like john.doe@company.com
All other employees likely follow same format
```

---

## 6. GitHub Investigation

GitHub is a goldmine for OSINT. Developers accidentally commit sensitive information.

**What to look for:**
```bash
# Search for sensitive keywords in repos:
password
api_key
secret
token
credentials
config
.env
```

**Check commit history:**
```
Even if sensitive data was deleted, it may exist in old commits
Click on commits tab in any repo
Look through every commit message and changed files
```

**Check all repos including forked ones:**
```
Forked repos may contain original sensitive data
Look at .env files, config files, README files
```

---

## 7. Social Media OSINT

**Twitter/X tips:**
```
Check pinned tweet
Read bio carefully — email, website, location often there
Check likes and retweets for interests and connections
Advanced search: from:username — see all their tweets
```

**LinkedIn tips:**
```
Company name → find all employees
Job descriptions reveal technology stack
Education → find classmates and connections
```

**Instagram tips:**
```
Location tags reveal where person lives and works
Tagged photos reveal friends and family
Highlights contain older content
```

---

## 8. Tools Summary

| Tool | Purpose | Install |
|---|---|---|
| exiftool | Extract file metadata | `sudo apt install exiftool` |
| theHarvester | Gather emails and subdomains | `sudo apt install theharvester` |
| Maltego | Visual OSINT mapping | maltego.com |
| Shodan | Search engine for internet-connected devices | shodan.io |
| Have I Been Pwned | Check if email in data breach | haveibeenpwned.com |
| Wayback Machine | See old versions of websites | web.archive.org |

---

## 9. Completed Challenges

### OHSint — TryHackMe

**Starting point:** One image file — WindowsXP.jpg

**Step 1 — exiftool revealed:**
```bash
exiftool WindowsXP.jpg
# Author: OWoodflint (oliverwoodflint)
```

**Step 2 — Searched oliverwoodflint on Twitter:**
Found active Twitter profile with linked website and location information

**Step 3 — Found WordPress blog:**
Linked from Twitter profile — contained personal information and hidden password in page source

**Step 4 — Checked GitHub:**
Found GitHub profile with additional information

**Key learning:** One name from image metadata led to Twitter → WordPress → GitHub → complete profile of the target including password hidden in plain sight on their own website.

---

## 10. Key Takeaways

- Images contain hidden metadata that most people never think about
- People leave massive digital footprints across multiple platforms
- One piece of information always connects to another
- GitHub is one of the most information-rich OSINT sources
- Passwords and credentials are frequently visible in page source and commit history
- OSINT requires patience — follow every thread methodically
- The same methodology used in CTFs is used in real penetration testing engagements

---
