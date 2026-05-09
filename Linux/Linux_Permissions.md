# Linux — Permissions

---

## 1. File Permissions

Every file and directory in Linux has a set of permissions that control who can do what with it. Run `ls -l` to view them.

```bash
ls -l myfile.txt
# Output: -rwxr-xr-- 1 pete developers 1234 Jan 1 12:00 myfile.txt
```

**Breaking down the permission string:**

```
-  rwx  r-x  r--
↑   ↑    ↑    ↑
|   |    |    └── Others permissions
|   |    └─────── Group permissions
|   └──────────── Owner (user) permissions
└──────────────── File type: - = file, d = directory, l = symlink
```

**Permission letters:**

| Letter | Name | On Files | On Directories |
|---|---|---|---|
| `r` | Read | View file contents | List contents with `ls` |
| `w` | Write | Edit or delete the file | Create, delete, rename files inside |
| `x` | Execute | Run as a program | Enter with `cd` |
| `-` | None | Permission denied | Permission denied |

**Reading a full permission string — `drwxr-xr--`:**
- `d` — it's a directory
- `rwx` — owner can read, write, execute
- `r-x` — group can read and execute, NOT write
- `r--` — others can only read

**Who is "owner", "group", "others"?**

| Category | Who it means |
|---|---|
| **Owner (user)** | The user who owns the file |
| **Group** | Users who belong to the file's assigned group |
| **Others** | Everyone else on the system |

---

## 2. Modifying Permissions — chmod

`chmod` (change mode) modifies permissions on files and directories.

### Symbolic Method

Use letters to specify who and what to change:

| Who | Symbol |
|---|---|
| User (owner) | `u` |
| Group | `g` |
| Others | `o` |
| All (u+g+o) | `a` |

| Operator | Meaning |
|---|---|
| `+` | Add a permission |
| `-` | Remove a permission |
| `=` | Set exact permissions (replaces existing) |

```bash
chmod u+x myfile        # Add execute for owner
chmod g-w myfile        # Remove write from group
chmod o= myfile         # Remove ALL permissions from others
chmod a+r myfile        # Add read for everyone
chmod u+x,g-w myfile    # Multiple changes at once
chmod u=rwx,g=rx,o=r myfile  # Set exact permissions for each
```

### Numeric (Octal) Method

Each permission has a value: `r=4`, `w=2`, `x=1`. Add them for each category.

| Value | Permissions |
|---|---|
| `7` | `rwx` |
| `6` | `rw-` |
| `5` | `r-x` |
| `4` | `r--` |
| `3` | `-wx` |
| `2` | `-w-` |
| `1` | `--x` |
| `0` | `---` |

The three digits represent **owner**, **group**, **others** in that order.

```bash
chmod 755 myfile        # rwxr-xr-x — owner full, group/others read+execute
chmod 644 myfile        # rw-r--r-- — owner read/write, everyone else read only
chmod 700 myfile        # rwx------ — only owner has any access
chmod 777 myfile        # rwxrwxrwx — everyone full access (avoid in production)
chmod -R 755 mydir/     # Recursively apply to all files in directory
```

**Common patterns:**

| Value | Pattern | Typical use |
|---|---|---|
| `777` | `rwxrwxrwx` | Everyone full — dangerous in production |
| `755` | `rwxr-xr-x` | Public directories, scripts |
| `750` | `rwxr-x---` | Group access, others blocked |
| `700` | `rwx------` | Private — owner only |
| `644` | `rw-r--r--` | Regular files — owner edits, others read |
| `600` | `rw-------` | Private files (SSH keys, configs) |
| `770` | `rwxrwx---` | Shared team directory |

---

## 3. Ownership Permissions — chown and chgrp

Every file has an **owner** (a user) and an **associated group**. These are set at creation and can be changed with `chown` and `chgrp`.

```bash
# chown — change owner
sudo chown alice myfile.txt             # Change owner to alice
sudo chown alice:developers myfile.txt  # Change owner AND group
sudo chown :developers myfile.txt       # Change group only (colon with no user)
sudo chown -R alice:devs mydir/         # Recursively change entire directory

# chgrp — change group (simpler than chown when only group changes)
sudo chgrp developers myfile.txt
sudo chgrp -R developers mydir/
```

**Verify ownership:**
```bash
ls -l myfile.txt
# -rw-r--r-- 1 alice developers 1234 Jan 1 myfile.txt
#              ↑     ↑
#           owner   group
```

> Only **root** or the **file owner** can change ownership. Regular users can change the group only to a group they belong to.

---

## 4. Umask

When you create a new file or directory, it gets a set of **default permissions**. The `umask` (user file-creation mask) controls what permissions are **removed** from those defaults.

**Default maximum permissions before umask:**
- New **files**: `666` (rw-rw-rw-) — execute is never given by default
- New **directories**: `777` (rwxrwxrwx)

**How umask works:** It subtracts from the default. The umask value represents permissions to **remove**.

```bash
umask           # Show current umask value
umask 022       # Set umask to 022
```

**Most common umask — `022`:**

| | Files | Directories |
|---|---|---|
| Default | `666` | `777` |
| Umask | `022` | `022` |
| Result | `644` (rw-r--r--) | `755` (rwxr-xr-x) |

**Other common umask values:**

| Umask | New files | New directories |
|---|---|---|
| `022` | `644` | `755` |
| `027` | `640` | `750` |
| `077` | `600` | `700` |
| `002` | `664` | `775` |

**Make umask permanent** — add to your shell config:
```bash
# In ~/.bashrc or ~/.zshrc:
umask 027       # More restrictive — group no write, others nothing
```

> The umask is applied every time a file or directory is created. It is not applied retroactively to existing files.

---

## 5. Setuid (SUID)

The **setuid** bit is a special permission that changes how executable files run. Normally, when you run a program, it runs **as you** (with your permissions). With setuid set, the program runs **as the file's owner** instead — regardless of who executes it.

**Why this exists — the `passwd` example:**
The `/usr/bin/passwd` command needs to write to `/etc/shadow`, which is owned by root and unreadable by regular users. If `passwd` ran as you, it couldn't write to `/etc/shadow`. Because it has the setuid bit and is owned by root, it temporarily runs with root's permissions.

```bash
ls -l /usr/bin/passwd
# -rwsr-xr-x 1 root root ... /usr/bin/passwd
#     ↑
#     s in place of x means setuid is set
```

**Setting and removing setuid:**
```bash
sudo chmod u+s myprogram       # Add setuid using symbolic method
sudo chmod 4755 myprogram      # Add setuid using numeric (4 prefix)
sudo chmod u-s myprogram       # Remove setuid
```

**How to identify setuid files:**
```bash
ls -l myprogram         # Look for 's' in owner execute position: -rwsr-xr-x
find / -perm -4000      # Find all setuid files on the system
```

> ⚠️ setuid files are a **security concern** — if a setuid-root program has a vulnerability, an attacker could use it to gain root access. Never set the setuid bit on scripts, only on trusted compiled programs.

---

## 6. Setgid (SGID)

The **setgid** bit works similarly to setuid but for **groups**. It has two different effects depending on whether it's set on a file or a directory.

**On executable files:**
The program runs with the **file's group permissions** instead of the user's primary group. Less common than setuid.

**On directories (most useful case):**
Any new files created inside the directory **automatically inherit the directory's group** — regardless of the creating user's primary group. Essential for shared team folders.

```bash
# Create a shared team directory
sudo mkdir /home/team
sudo chgrp developers /home/team
sudo chmod g+s /home/team       # Set setgid on directory

# Now any file created inside /home/team automatically belongs to "developers"
```

```bash
ls -l /home/team
# drwxrwsr-x 2 root developers ... /home/team
#        ↑
#        s in group execute position = setgid set
```

**Setting and removing setgid:**
```bash
sudo chmod g+s mydir/       # Add setgid using symbolic
sudo chmod 2775 mydir/      # Add setgid using numeric (2 prefix)
sudo chmod g-s mydir/       # Remove setgid
```

**Find all setgid files/dirs:**
```bash
find / -perm -2000
```

---

## 7. Process Permissions

When a process runs, it carries **two User IDs** — not just one:

| ID | Name | Meaning |
|---|---|---|
| **Real UID (RUID)** | Real User ID | Who actually launched the process (the logged-in user) |
| **Effective UID (EUID)** | Effective User ID | The UID the process uses for permission checks — what it actually runs as |

**Normally** — RUID and EUID are the same. You run a program, it runs as you.

**With setuid** — RUID is still you (the real user), but EUID becomes the file owner (e.g. root). The OS checks EUID for permissions, so the program can access things you normally can't.

```bash
# Example — when you run passwd:
# RUID = pete (you)
# EUID = root (because passwd has setuid and is owned by root)
# The OS lets passwd write to /etc/shadow because EUID = root
```

**View process info:**
```bash
ps aux          # Show running processes — USER column shows the EUID
id              # Show your own real UID and effective UID
```

> This distinction is important for security. Programs that use setuid must be very carefully written — they have elevated privileges and must not be exploitable.

---

## 8. The Sticky Bit

The **sticky bit** is a special permission for **directories**. When set on a directory, it restricts file deletion — users can only delete **their own files** inside that directory, even if they have write permission on the directory itself.

**Without sticky bit:**
If a directory is world-writable (`rwxrwxrwx`), any user can delete any file in it — even files they don't own.

**With sticky bit:**
Only the **file's owner**, the **directory's owner**, or **root** can delete files in that directory.

**Classic example — `/tmp`:**
```bash
ls -ld /tmp
# drwxrwxrwt 1 root root ... /tmp
#          ↑
#          t in others execute position = sticky bit set
```
`/tmp` is world-writable so every user can create temp files there. The sticky bit prevents users from deleting each other's temp files.

**Setting and removing the sticky bit:**
```bash
sudo chmod +t mydir/            # Add sticky bit using symbolic
sudo chmod 1777 mydir/          # Add sticky bit using numeric (1 prefix)
sudo chmod -t mydir/            # Remove sticky bit
```

**Identifying sticky bit:**
- `t` (lowercase) in the others execute position = sticky bit set and others have execute
- `T` (uppercase) = sticky bit set but others do NOT have execute

```bash
ls -ld /tmp             # drwxrwxrwt — t = sticky bit
find / -perm -1000      # Find all directories with sticky bit
```

---

## 9. Quick Reference — Permissions

**chmod — change permissions:**

```bash
chmod u+x file          # Add execute for owner (symbolic)
chmod g-w file          # Remove write from group
chmod o= file           # Remove all from others
chmod 755 file          # Set rwxr-xr-x (numeric)
chmod 644 file          # Set rw-r--r--
chmod -R 755 dir/       # Recursive
```

**chown / chgrp — change ownership:**

```bash
sudo chown user file                # Change owner
sudo chown user:group file          # Change owner and group
sudo chown -R user:group dir/       # Recursive
sudo chgrp group file               # Change group only
```

**Special permissions:**

| Permission | Numeric | Symbolic | Effect |
|---|---|---|---|
| Setuid | `4xxx` | `u+s` | Program runs as file owner |
| Setgid | `2xxx` | `g+s` | Program runs as file group / new files inherit group |
| Sticky bit | `1xxx` | `+t` | Only file owner can delete files in directory |

**Combined examples:**
```bash
sudo chmod 4755 program     # setuid + rwxr-xr-x
sudo chmod 2775 shareddir/  # setgid + rwxrwxr-x
sudo chmod 1777 /tmp        # sticky + rwxrwxrwx
```

**umask:**
```bash
umask               # View current umask
umask 022           # Files → 644, Directories → 755
umask 027           # Files → 640, Directories → 750
umask 077           # Files → 600, Directories → 700
```

**Finding special permission files:**
```bash
find / -perm -4000      # All setuid files
find / -perm -2000      # All setgid files
find / -perm -1000      # All sticky bit directories
find / -perm -777 -type f  # All world-writable files (audit)
```

**Reading special bits in ls -l:**

| Position | Letter | Meaning |
|---|---|---|
| Owner execute | `s` | setuid set |
| Group execute | `s` | setgid set |
| Others execute | `t` | sticky bit set |
| Others execute | `T` | sticky bit set, no execute for others |
