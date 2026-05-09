# Linux — User Management

---

## 1. Users and Groups

In any multi-user operating system, managing users and groups is a fundamental concept. When a process runs, it does so **as the user who started it**. File access and ownership are dependent on permissions, preventing one user from accessing another's private documents.

**The basics:**
- Every user has a personal home directory at `/home/username`
- The system identifies users with a **User ID (UID)** — a unique number
- The system identifies groups with a **Group ID (GID)** — a unique number
- While we use human-readable usernames, the OS uses UIDs/GIDs internally for all permission tasks
- **Groups** are collections of users, making it easier to manage permissions for multiple accounts at once

**Types of users:**

| Type | Description |
|---|---|
| **Root user** | The superuser. Has unlimited power — can access any file and manage any process |
| **Regular users** | Human users with limited privileges. Can only do what they're authorized to do |
| **System users** | Special accounts created by the OS to run specific services/daemons (e.g. `daemon`, `www-data`) |

---

## 2. root

The **root** user (also called the superuser) sits above all others in the Linux hierarchy. Root has unlimited power over the entire system.

```bash
# Check if you are root
whoami          # shows current username
id              # shows UID, GID and groups
```

When logged in as root, the prompt ends with `#` instead of `$`:
```
root@hostname:~#
```

**Why you should NOT operate as root constantly:**
- A simple typo or mistake could delete critical system files
- Any process you run inherits root's unlimited power
- There is no safety net

**The `sudo` command — safer alternative to root:**

`sudo` (Super User Do) lets a regular user run a **single command** with root privileges, without fully switching to the root account.

```bash
sudo useradd bob            # Run useradd as root, just for this command
sudo cat /etc/shadow        # View root-only files
sudo -i                     # Open a root shell (use with extreme caution)
```

- You are prompted for **your own password** (not root's)
- The action is **logged** in `/var/log/auth.log` — creating an audit trail
- Only users in the `sudo` group can use it

**Switch to root (when necessary):**
```bash
su              # Switch to root (prompts for root password)
su -            # Switch to root with full login environment
su - username   # Switch to another user
exit            # Return to your original account
```

> ⚠️ Use `sudo` for individual commands. Only use `su` to root when you have multiple admin tasks to do, and exit root as soon as you're done.

---

## 3. /etc/passwd

The `/etc/passwd` file is the **main user database** — a plain text phonebook for all user accounts on the system. Every user, including system accounts, has one entry here.

```bash
cat /etc/passwd             # View all user entries
grep -w 'pete' /etc/passwd  # Look up a specific user
```

**Format — each line has 7 fields separated by colons `:`:**
```
pete:x:1000:1000:Pete Smith,,,:/home/pete:/bin/bash
```

| Field | Example | Meaning |
|---|---|---|
| Username | `pete` | Login name |
| Password | `x` | Password stored in `/etc/shadow` (always `x` here) |
| UID | `1000` | User ID number |
| GID | `1000` | Primary Group ID number |
| GECOS | `Pete Smith,,,` | Full name and optional info (comment field) |
| Home directory | `/home/pete` | Path to user's home directory |
| Default shell | `/bin/bash` | Shell launched at login |

**UID ranges (typical):**

| UID range | Type |
|---|---|
| `0` | root |
| `1–999` | System/service accounts |
| `1000+` | Regular human users |

> ⚠️ Never edit `/etc/passwd` directly with a text editor. Always use `useradd`, `usermod`, `userdel`. A syntax error in this file can lock everyone out of the system. If you must edit it directly, use `vipw` — it locks the file and validates syntax before saving.

**System accounts** — You'll notice many accounts that don't belong to human users (e.g. `daemon`, `bin`, `sys`). These run specific services with limited permissions to improve security.

---

## 4. /etc/shadow

The `/etc/shadow` file stores **encrypted passwords and password aging policies**. It is kept separate from `/etc/passwd` for security — if a non-privileged user could read password hashes, they could attempt to crack them offline.

```bash
sudo cat /etc/shadow            # Requires root/sudo to read
sudo grep 'pete' /etc/shadow    # Look up a specific user
```

**Permissions on the file:**
```
-rw-r----- 1 root shadow 1134 Dec 1 11:45 /etc/shadow
```
Only root and members of the `shadow` group can read it.

**Format — each line has 9 fields separated by colons `:`:**
```
pete:$6$xyz...hashedpassword...:19000:0:99999:7:::
```

| Field | Example | Meaning |
|---|---|---|
| Username | `pete` | Login name |
| Encrypted password | `$6$xyz...` | Hashed password. `*` or `!` = account locked |
| Last password change | `19000` | Days since Jan 1, 1970 the password was last changed |
| Minimum age | `0` | Min days before user can change password again |
| Maximum age | `99999` | Max days before password must be changed |
| Warning period | `7` | Days before expiry to warn the user |
| Inactivity period | (empty) | Days after expiry before account is disabled |
| Expiration date | (empty) | Date the account expires |
| Reserved | (empty) | Reserved for future use |

**Locked accounts:**
When an account is locked with `passwd -l`, the password hash gets prefixed with `!`:
```
pete:!$6$xyz...hashedpassword...:19000:0:99999:7:::
```
The `!` makes the hash invalid — no password will ever match it, so the user cannot log in.

---

## 5. /etc/group

The `/etc/group` file stores all **group information** on the system — group names, GIDs, and which users belong to each group.

```bash
cat /etc/group                  # View all groups
grep 'developers' /etc/group    # Look up a specific group
groups pete                     # List all groups pete belongs to
id pete                         # Show UID, GID and all group memberships
```

**Format — each line has 4 fields separated by colons `:`:**
```
developers:x:1001:pete,alice,bob
```

| Field | Example | Meaning |
|---|---|---|
| Group name | `developers` | Name of the group |
| Password | `x` | Group password (rarely used, stored in `/etc/gshadow`) |
| GID | `1001` | Group ID number |
| Members | `pete,alice,bob` | Comma-separated list of group members |

**GID ranges (typical):**

| GID range | Type |
|---|---|
| `0` | root group |
| `1–999` | System groups |
| `1000+` | User-created groups |

**Related file — `/etc/gshadow`:**
Stores secure group information (group passwords and administrators). Rarely used in practice but exists for completeness.

---

## 6. User Management Tools

The core commands for managing user accounts:

### useradd — Create a user

```bash
sudo useradd bob                        # Create user (no home directory)
sudo useradd -m bob                     # Create user WITH home directory
sudo useradd -m -s /bin/bash bob        # With home dir and bash shell
sudo useradd -m -g developers bob       # With specific primary group
sudo useradd -m -G sudo,developers bob  # With secondary groups
```

When `useradd` runs, it automatically creates entries in `/etc/passwd`, `/etc/shadow`, and `/etc/group`.

### userdel — Delete a user

```bash
sudo userdel bob            # Delete account only (home directory remains)
sudo userdel -r bob         # Delete account AND home directory + mail spool
```

> After `userdel` without `-r`, the home directory stays but its owner shows as a number (old UID) since the username no longer exists.

### passwd — Set or change passwords

```bash
sudo passwd bob             # Set/change bob's password (admin)
passwd                      # Change your own password
sudo passwd -l bob          # Lock bob's account
sudo passwd -u bob          # Unlock bob's account
sudo passwd -e bob          # Force bob to change password at next login
```

### usermod — Modify an existing user

```bash
sudo usermod -d /new/home bob           # Change home directory
sudo usermod -s /bin/bash bob           # Change default shell
sudo usermod -l newname bob             # Rename the user
sudo usermod -g developers bob          # Change primary group (lowercase -g)
sudo usermod -aG sudo bob               # Add to secondary group (always use -aG)
sudo usermod -L bob                     # Lock account (alternative to passwd -l)
sudo usermod -U bob                     # Unlock account
```

> ⚠️ Always use `-aG` (append + group) when adding to secondary groups. Using `-G` alone **overwrites** all existing secondary group memberships.

### Verify users and groups

```bash
id bob                          # Show UID, GID, and all groups
groups bob                      # List all groups bob belongs to
grep 'bob' /etc/passwd          # Check passwd entry
sudo grep 'bob' /etc/shadow     # Check shadow entry (needs sudo)
grep 'bob' /etc/group           # Find all groups bob is in
who                             # Show who is currently logged in
w                               # Show logged-in users and what they're doing
last                            # Show login history
```

---

## 7. Quick Reference — User Management

| Command | Purpose |
|---|---|
| `whoami` | Show current username |
| `id username` | Show UID, GID, all groups |
| `who` | Show who is logged in |
| `sudo useradd -m username` | Create user with home directory |
| `sudo userdel -r username` | Delete user and home directory |
| `sudo passwd username` | Set/change user password |
| `sudo passwd -l username` | Lock account |
| `sudo passwd -u username` | Unlock account |
| `sudo usermod -aG group user` | Add user to secondary group |
| `sudo usermod -s /bin/bash user` | Change shell |
| `sudo usermod -d /path user` | Change home directory |
| `cat /etc/passwd` | View all user accounts |
| `cat /etc/shadow` | View encrypted passwords (needs sudo) |
| `cat /etc/group` | View all groups |
| `grep username /etc/passwd` | Look up a specific user |
| `groups username` | List user's groups |
| `su - username` | Switch to another user |
| `sudo -i` | Open root shell |
| `exit` | Exit current user / shell |

**Key system files:**

| File | Contents | Who can read |
|---|---|---|
| `/etc/passwd` | User accounts (no passwords) | Everyone |
| `/etc/shadow` | Encrypted passwords + aging | Root only |
| `/etc/group` | Group info and membership | Everyone |
| `/etc/gshadow` | Secure group info | Root only |
