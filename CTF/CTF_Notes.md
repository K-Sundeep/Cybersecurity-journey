# CTF Notes

---

# Chapter 1 — Web Exploitation CTFs

---

## 1. What is a CTF?

Capture The Flag (CTF) is a cybersecurity competition where you find hidden flags or secret values on intentionally vulnerable systems. Each flag proves you successfully exploited a vulnerability.

**Types of flags:**
- Text strings like THM{flag_here}
- Secret ingredients, passwords, or files hidden on a server
- Database contents extracted via SQL injection

**Why CTFs matter:**
CTFs teach real attack techniques in a legal environment. Every skill used in CTFs transfers directly to real penetration testing engagements.

---

## 2. Web CTF Methodology — Always Follow This Order

| Step | Action | Command / Location |
|---|---|---|
| 1 | View page source | Ctrl+U in browser |
| 2 | Check robots.txt | targetIP/robots.txt |
| 3 | Check common directories | /login, /admin, /assets, /index.php |
| 4 | Look for login pages | Try found credentials immediately |
| 5 | Check command execution | ls, cat, sudo -l, whoami |
| 6 | Look for hidden files | ls -la, find / -name "*.txt" |

> Rule: Always check page source and robots.txt first. Credentials are hidden in plain sight more often than you think.

---

## 3. Essential Linux Commands for CTFs

Navigation and file discovery:
```bash
ls                          # list files in current directory
ls -la                      # list all files including hidden ones
cat filename                # read file contents
find / -name "*.txt"        # find all text files on system
find / -name "*ingredient*" # find files by keyword
pwd                         # show current directory
cd /directory               # change directory
```

Privilege and user commands:
```bash
whoami                      # show current user
sudo -l                     # list commands current user can run as root
sudo command                # run command as root
id                          # show user ID and group memberships
```

Reading restricted files:
```bash
sudo cat /root/filename     # read root-owned files if sudo allowed
strings filename            # extract readable strings from any file
```

---

## 4. Completed CTF Challenges

### OHSint — TryHackMe

**Type:** OSINT
**Difficulty:** Easy
**Starting point:** One image file

**Methodology used:**
```
1. exiftool WindowsXP.jpg → found author: OWoodflint
2. Searched oliverwoodflint on Twitter → found profile
3. Found linked WordPress blog → personal information
4. Viewed page source on WordPress → found hidden password
5. Checked GitHub → additional information
```

Key learning: Image metadata reveals identity, social media reveals location and personal details, page source reveals hidden credentials.

---

### Pickle Rick — TryHackMe

**Type:** Web Exploitation
**Difficulty:** Easy
**Goal:** Find 3 secret ingredients hidden on a web server

**Methodology used:**
```
1. Opened target IP in browser → read page carefully
2. Viewed page source Ctrl+U → found username in HTML comment
3. Checked robots.txt → found password string
4. Found login page at /login → logged in with found credentials
5. Discovered command execution panel → ran Linux commands
6. Used ls to list files → found first ingredient file
7. Used cat to read ingredient → first flag found
8. Used sudo -l → found what commands allowed as root
9. Used sudo to access restricted directories → found remaining ingredients
```

Commands that found the flags:
```bash
ls                                      # found first ingredient
cat "Sup3rS3cretPickl3Ingred.txt"       # read first ingredient
sudo ls /root                           # listed root directory
sudo cat /root/3rd.txt                  # read third ingredient
```

Key learning: Page source and robots.txt always contain clues. Command execution panels give direct system access. sudo -l reveals privilege escalation paths.

---

## 5. Key Takeaways

- Always check page source before anything else
- robots.txt is meant to hide pages from Google but reveals them to attackers
- Command execution on a web server = full system access
- sudo -l is one of the first commands to run after getting any shell access
- Hidden files start with . so always use ls -la not just ls
- CTF methodology is identical to real penetration testing methodology

---
