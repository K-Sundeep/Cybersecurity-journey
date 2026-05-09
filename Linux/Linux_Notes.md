# Linux Notes

---

# Chapter 1 — Navigation & File System Basics

---

## 1. Core Concepts

Linux uses a **hierarchical file system** — a tree of folders branching from the root `/`.

| Symbol | Meaning |
|---|---|
| `/` | Root of the entire file system |
| `~` | Your home directory (e.g. `/home/labex`) |
| `.` | Current directory |
| `..` | Parent directory (one level up) |

**`pwd`** — "print working directory". Shows your current location in the file system.

**`echo ~`** — Displays the full path to your home directory.

---

## 2. Listing Files & Directories

| Command | Description |
|---|---|
| `ls` | List files and directories in current directory |
| `ls ~` | List contents of the home directory |
| `ls *.txt` | List all files ending with `.txt` |
| `ls -l` | Long format — shows permissions, owner, size, date |
| `ls -a` | Show all files including hidden ones (starting with `.`) |
| `ls -la` | Combines long format and show-all |
| `ls -l dir_name` | List contents of a specific directory |
| `ls -R` | Recursively list all subdirectories (uppercase `-R`) |

> **Note:** For `ls`, `-R` (uppercase) = recursive listing, `-r` (lowercase) = reverse sort. For `cp` and `rm`, recursive is `-r` (lowercase). They are completely different options.

---

## 3. Navigating Directories

| Command | Description |
|---|---|
| `cd ..` | Move up one level to the parent directory |
| `cd ~` | Move to the home directory |
| `cd /home/labex/project` | Navigate using an **absolute path** (full path from root) |

---

## 4. Creating Files

| Command | Description |
|---|---|
| `touch filename.txt` | Create an empty file. If file exists, updates its timestamp only |
| `echo "Hello" > file.txt` | Write text into a file. Creates it if it doesn't exist; **replaces** existing content |
| `echo "Hidden" > .hiddenfile` | Create a hidden file |

> In Linux, any file or folder starting with a dot (`.`) is **hidden**. Use `ls -a` to see them.

---

## 5. Creating Directories

| Command | Description |
|---|---|
| `mkdir dir_name` | Create a new directory |
| `mkdir -p project/{src,bin,lib}` | Create nested directories in one shot |

---

## 6. Copying Files & Directories

| Command | Description |
|---|---|
| `cp file1.txt file1_copy.txt` | Copy a file in the current directory |
| `cp file2.txt testdir/` | Copy a file into a directory |
| `cp -r testdir testdir_copy` | Copy a directory recursively (includes all contents) |

---

## 7. Moving & Renaming

| Command | Description |
|---|---|
| `mv file1.txt newname.txt` | Rename a file |
| `mv newname.txt testdir/` | Move a file into a directory |
| `mv testdir_copy new_testdir` | Rename a directory |
| `mv testdir/file.txt ./original.txt` | Move and rename in one step |

---

## 8. Deleting Files & Directories

| Command | Description |
|---|---|
| `rm filename.txt` | Delete a file permanently |
| `rm -i file.txt` | Prompt for confirmation before deleting (`y` = yes, `n` = no) |
| `rmdir dir_name` | Remove an **empty** directory only |
| `rm -r dir_name` | Remove a directory and everything inside it recursively |

> ⚠️ **`rm -rf` Warning:** Removes recursively (`-r`) and forces removal with no prompt (`-f`). **There is no undo.** A typo like `rm -rf /` could attempt to delete your entire system. Always double-check the path.

> Deletions made with `rm` are generally **permanent** — there is no trash bin in the terminal.

---

## 9. Wildcards

Wildcards are special characters that match multiple files at once.

| Wildcard | Meaning |
|---|---|
| `*` | Matches any number of characters |
| `?` | Matches exactly one character |
| `[abc]` | Matches any one character listed in the brackets |

**Example:** `ls *.txt` — lists all `.txt` files in the current directory.

---

## 10. Brace Expansion

Brace expansion lets you create or reference multiple files in one command.

**Range:**
```bash
touch note_{1..5}.txt
# Creates: note_1.txt, note_2.txt, note_3.txt, note_4.txt, note_5.txt
```

**List of strings:**
```bash
touch project_{docs,code,tests}.txt
# Creates: project_docs.txt, project_code.txt, project_tests.txt
```

**Nested braces:**
```bash
touch {jan,feb}_{01..02}.log
# Creates: jan_01.log, jan_02.log, feb_01.log, feb_02.log
```

**Step values:**
```bash
touch file_{1..10..2}.txt
# Creates: file_1.txt, file_3.txt, file_5.txt, file_7.txt, file_9.txt
```

---

## 11. Useful Terminal Shortcuts

| Shortcut | What it does |
|---|---|
| `↑` arrow key | Recall the last command typed |
| `Tab` | Auto-complete file or command names |
| `Ctrl+C` | Interrupt/stop a running command |
| `Ctrl+L` | Clear the terminal screen |
| `;` | Run commands in sequence: `ls; ls testdir` |
| `&&` | Run next command only if previous succeeded: `ls && ls testdir` |

---

## 12. Misc Notes

- **`~/.zshrc`** — A hidden config file in your home directory for the Zsh shell.
- **`~/Code`** — A common directory for storing source code.
- **`tail -f /dev/null`** — Waits forever doing nothing. `/dev/null` is a special empty file that returns nothing. Useful for testing `Ctrl+C`.

---

---

# Chapter 2 — User Account Management

---

## 13. Creating a New User

```bash
sudo useradd joker          # Create user (no home directory)
sudo useradd -m bob         # Create user WITH a home directory
```

- **`sudo`** — Grants temporary superuser (admin) privileges. Required to create users.
- **`useradd`** — Low-level command to create a new user.
- **`-m`** — Creates a home directory at `/home/username` for the user.

**`adduser` vs `useradd`:**

| Command | Behaviour |
|---|---|
| `sudo useradd username` | Low-level, manual. No password or home dir unless flags are added |
| `sudo adduser username` | Higher-level, interactive. Prompts for password and info automatically |

**Verify a user's home directory:**
```bash
sudo ls -ld /home/bob
# Output: drwxr-x--- 2 bob bob 57 Jan 19 13:33 /home/bob
```
- `d` — it's a directory
- `rwxr-x---` — permissions (owner / group / others)
- Two `bob` entries — user and group owner

---

## 14. The `/etc/passwd` File

A **phonebook for all user accounts**. Each line = one user, fields separated by colons (`:`).

```bash
sudo grep -w 'joker' /etc/passwd
# Output: joker:x:5001:5001::/home/joker:/bin/sh
```

| Field | Example | Meaning |
|---|---|---|
| Username | `joker` | Login name |
| Password | `x` | Actual password is stored in `/etc/shadow` |
| User ID (UID) | `5001` | Unique numeric ID for the user |
| Group ID (GID) | `5001` | Primary group ID |
| Home Directory | `/home/joker` | User's personal folder |
| Default Shell | `/bin/sh` | Shell launched when the user logs in |

---

## 15. Setting & Managing Passwords

```bash
sudo passwd joker       # Set/change another user's password (admin)
passwd                  # Change your own password
```

- Passwords are **not displayed** as you type — this is called **"Silent Feedback"** or **"Blind Typing"**. It prevents shoulder-surfers from seeing your input.
- Passwords are stored as **encrypted hashes** in `/etc/shadow`, readable only by root. You will never see the plain password stored there.

---

## 16. Password Aging with `chage`

`chage` ("Change Age") manages password expiration and aging policies. All settings are stored in `/etc/shadow`.

**View current aging info:**
```bash
sudo chage -l joker
```

**Common options:**

| Command | Effect |
|---|---|
| `sudo chage -M 90 joker` | Force password change every 90 days |
| `sudo chage -m 5 joker` | Minimum 5 days before user can change password again |
| `sudo chage -W 7 joker` | Warn user 7 days before password expires |
| `sudo chage -d 0 joker` | Force password change on very next login |

---

## 17. Modifying a User — `usermod`

```bash
sudo usermod -d /new/path joker         # Change home directory
sudo usermod -s /bin/bash joker         # Change default shell
sudo usermod -aG sudo joker             # Add user to a group (secondary)
sudo usermod -g developers joker        # Change primary group (lowercase -g)
sudo usermod -G developers joker        # Set secondary groups (OVERWRITES existing!)
sudo usermod -aG developers joker       # APPEND to secondary groups (safe)
```

> ⚠️ **`-g` vs `-G`:** Lowercase `-g` = primary group. Uppercase `-G` = secondary groups. Using `-G` without `-a` **removes all other secondary group memberships**. Always use `-aG` together when adding to groups.

**Switch to a user:**
```bash
su - joker
```
The `-` starts a full login shell, loads their environment, and changes to their home directory. Type `exit` to return.

---

## 18. Locking & Unlocking an Account

Temporarily disable an account without deleting it.

```bash
sudo passwd -l joker    # Lock the account
sudo passwd -u joker    # Unlock the account
```

When locked, the user gets an "authentication failure" on login. Unlocking restores normal access.

---

## 19. Deleting a User

```bash
sudo userdel bob          # Delete account only (files remain on system)
sudo userdel -r bob       # Delete account AND home directory + mail spool
```

> A warning about the mail spool not being found is **normal** in container environments.

---

## 20. Quick Reference — User Account Commands

| Command | Purpose |
|---|---|
| `sudo useradd username` | Create a new user |
| `sudo useradd -m username` | Create a user with a home directory |
| `sudo adduser username` | Create a user interactively (with password prompt) |
| `sudo passwd username` | Set or change a user's password |
| `sudo usermod -d /path username` | Change home directory |
| `sudo usermod -s /bin/bash username` | Change default shell |
| `sudo usermod -aG groupname username` | Append user to a secondary group |
| `sudo usermod -g groupname username` | Change primary group |
| `sudo passwd -l username` | Lock an account |
| `sudo passwd -u username` | Unlock an account |
| `sudo userdel -r username` | Delete user and their home directory |
| `su - username` | Switch to another user |
| `sudo chage -l username` | View password aging info |
| `grep -w username /etc/passwd` | Look up a user's account entry |

---

## 21. Key System Files

| File | Purpose | Access |
|---|---|---|
| `/etc/passwd` | Basic user account info | Readable by all users |
| `/etc/shadow` | Encrypted passwords + aging settings | Root only |
| `/etc/group` | Group names, GIDs, and members | Readable by all users |
| `/etc/gshadow` | Secure group info and group admins | Root only |

---

---

# Chapter 3 — Groups & File Permissions

---

## 22. Checking the Current User

```bash
whoami          # Show currently logged-in username
id username     # Show UID, primary GID, and all groups the user belongs to
```

---

## 23. Primary Group vs Secondary Groups

Every Linux user has exactly **one primary group** and can belong to **zero or more secondary groups**.

| | Primary Group | Secondary Groups |
|---|---|---|
| How many | Exactly one | Zero or more |
| Stored in | `/etc/passwd` | `/etc/group` |
| Set with | `usermod -g` (lowercase) | `usermod -aG` (uppercase with `-a`) |
| Purpose | Auto-assigned to files the user creates | Grant extra access/permissions |

**User Private Group (UPG):** When you create a user, Linux automatically creates a primary group with the same name. This is called the UPG scheme.

> ⚠️ Each user has only **one** primary group. To grant extra access to things, always use secondary groups.

---

## 24. Group Management

**Create a group:**
```bash
sudo groupadd developers
```

**Add a user to a group:**
```bash
sudo usermod -aG developers alice       # via usermod
sudo gpasswd -a alice developers        # via gpasswd (alternative)
```

**Remove a user from a group:**
```bash
sudo gpasswd -d alice developers
```

**Create a user with groups assigned at creation time:**
```bash
sudo useradd -g staff alice                     # Set primary group
sudo useradd -G developers,sudo alice           # Set secondary groups
sudo useradd -g staff -G developers,sudo alice  # Both at once
```
> Note: The group must already exist before you can assign it. Use `groupadd` first.

---

## 25. Managing Group Membership with `gpasswd`

`gpasswd` directly administers `/etc/group` and `/etc/gshadow`.

```bash
sudo gpasswd -a alice developers            # Add one user
sudo gpasswd -d alice developers            # Remove one user
sudo gpasswd -M alice,bob,charlie developers  # Set entire member list (overwrites!)
sudo gpasswd -A alice developers            # Make alice a group admin (can add/remove members without sudo)
sudo gpasswd developers                     # Set a password on the group
```

> ⚠️ `-M` **replaces** the entire member list — it does not append. Only use it when setting up a group from scratch.

---

## 26. Switching Active Group — `newgrp`

`newgrp` temporarily switches your active/primary group for the current shell session without logging out.

```bash
newgrp developers       # Switch active group to developers
newgrp                  # Switch back to your original primary group (no argument)
```

After switching, any files you create will have `developers` as the group owner instead of your usual primary group.

**When is this useful?**
- You were just added to a group and don't want to log out to activate it.
- You want files in a specific folder to belong to a team group.

> Note: `newgrp` only affects the **current shell session**. Open a new terminal and you're back to normal.

---

## 27. Viewing Group Info

```bash
groups alice              # List all groups alice belongs to
id alice                  # Show UID, primary GID, and all groups
grep alice /etc/group     # Find all groups alice appears in
cat /etc/group            # View all groups on the system
tail -5 /etc/group        # See the 5 most recently added groups
grep developers /etc/group  # Search for a specific group
```

Each line in `/etc/group` follows this format:
```
groupname:password:GID:member1,member2,...
```

> **Important:** Group membership changes take effect immediately when checked with `id username`. However, a **user's active session** won't reflect changes until they log out and back in — or use `newgrp`.

---

## 28. Renaming & Deleting Groups

**Rename a group:**
```bash
sudo groupmod -n newname oldname
```
This keeps the same GID, so all files previously owned by `oldname` automatically show `newname` since Linux tracks ownership by GID (number), not name.

**Delete a group:**
```bash
sudo groupdel developers
```

> ⚠️ You **cannot** delete a group that is a user's **primary group**. Change the user's primary group first, then delete:
```bash
sudo usermod -g staff alice     # Reassign primary group first
sudo groupdel developers        # Then delete
```

Deleting a group does **not** delete the users in it — only the group entry is removed.

---

## 29. Giving a User Sudo Privileges

```bash
sudo usermod -aG sudo alice
```

- **Security** — Users can perform admin tasks without logging in as root directly (which is risky).
- **Accountability** — All `sudo` actions are **logged**, creating an audit trail.

---

## 30. Understanding File Permissions

Every file and directory has permissions controlling who can do what. Use `ls -l` to see them:

```
-rw-rw-r-- 1 alice developers 57 Jan 19 13:33 file.txt
```

**Breaking down the permission string:**

| Position | Example | Meaning |
|---|---|---|
| 1st character | `-` or `d` | `-` = regular file, `d` = directory |
| Characters 2–4 | `rw-` | **Owner** permissions |
| Characters 5–7 | `rw-` | **Group** permissions |
| Characters 8–10 | `r--` | **Others** (everyone else) permissions |

**Permission letters:**

| Letter | Permission | For Files | For Directories |
|---|---|---|---|
| `r` | Read | View file contents | List directory contents |
| `w` | Write | Edit/delete the file | Create/delete files inside |
| `x` | Execute | Run as a program | Enter (`cd`) the directory |
| `-` | No permission | Denied | Denied |

**Example decoded — `drwxr-x---`:**
- `d` — it's a directory
- `rwx` — owner can read, write, and enter
- `r-x` — group can read and enter, but NOT write
- `---` — others have zero access

---

## 31. Changing File Ownership — `chown` & `chgrp`

```bash
sudo chown alice file.txt                 # Change owner only
sudo chown alice:developers file.txt      # Change owner AND group
sudo chown -R alice:developers mydir/     # Recursively change entire directory
sudo chgrp developers file.txt            # Change group ownership only
```

- **`-R`** — Recursive. Applies to the directory and everything inside it.

**Verify ownership:**
```bash
ls -l file.txt
```

---

## 32. Changing File Permissions — `chmod`

### Numeric (Octal) Method

Each permission has a numeric value: `r = 4`, `w = 2`, `x = 1`. Add them up for each group (Owner, Group, Others).

| Value | Permissions | Meaning |
|---|---|---|
| `7` | `rwx` | Read + Write + Execute |
| `6` | `rw-` | Read + Write |
| `5` | `r-x` | Read + Execute |
| `4` | `r--` | Read only |
| `0` | `---` | No permissions |

```bash
sudo chmod 750 file.txt
# 7 = owner gets rwx (full access)
# 5 = group gets r-x (read and execute)
# 0 = others get --- (no access)

sudo chmod 644 file.txt
# 6 = owner gets rw- (read and write)
# 4 = group gets r-- (read only)
# 4 = others get r-- (read only)
```

### Symbolic Method

Use letters to add (`+`), remove (`-`), or set (`=`) permissions:

| Symbol | Who |
|---|---|
| `u` | User (owner) |
| `g` | Group |
| `o` | Others |
| `a` | All (u + g + o) |

```bash
chmod u+x file.txt       # Add execute for owner
chmod g-w file.txt       # Remove write from group
chmod o=r file.txt       # Set others to read-only
chmod a+r file.txt       # Add read for everyone
chmod g+rw file.txt      # Add read and write for group
chmod -R 770 mydir/      # Recursively set permissions on a directory
```

---

## 33. Common Permission Patterns

| Value | Pattern | Typical Use |
|---|---|---|
| `777` | `rwxrwxrwx` | Everyone has full access — avoid in production |
| `755` | `rwxr-xr-x` | Owner full, others can read/execute. Common for public directories |
| `750` | `rwxr-x---` | Owner full, group can read/execute, others blocked |
| `700` | `rwx------` | Only owner has any access |
| `644` | `rw-r--r--` | Owner can edit, everyone else read-only. Common for regular files |
| `600` | `rw-------` | Owner read/write only, nobody else. Common for private/sensitive files |
| `770` | `rwxrwx---` | Owner and group full access, others blocked. Common for team directories |

---

## 34. Practical Example — Setting Up a Team Environment

```bash
# 1. Create groups
sudo groupadd developers
sudo groupadd designers

# 2. Create users and assign groups
sudo adduser alice                              # Interactive creation
sudo useradd -m -G developers,sudo bob         # With groups at creation
sudo useradd -m -G designers carol

# 3. Add alice to developers group later
sudo usermod -aG developers alice

# 4. Create a shared project directory
sudo mkdir /home/project
sudo chown root:developers /home/project        # Group owns the folder
sudo chmod 770 /home/project                    # Owner + group full access, others blocked

# 5. Verify
groups alice
ls -ld /home/project
```

---

## 35. Quick Reference — Groups & Permissions Commands

| Command | Purpose |
|---|---|
| `whoami` | Show current logged-in user |
| `id username` | Show UID, GID, and all group memberships |
| `groups username` | List all groups a user belongs to |
| `sudo groupadd groupname` | Create a new group |
| `sudo groupmod -n newname oldname` | Rename a group |
| `sudo groupdel groupname` | Delete a group (not if it's someone's primary) |
| `sudo gpasswd -a username groupname` | Add user to a group |
| `sudo gpasswd -d username groupname` | Remove user from a group |
| `sudo gpasswd -M u1,u2,u3 groupname` | Set entire member list for a group (overwrites) |
| `sudo gpasswd -A username groupname` | Make user a group administrator |
| `newgrp groupname` | Temporarily switch active group (current session) |
| `newgrp` | Switch back to original primary group |
| `cat /etc/group` | View all groups on the system |
| `grep groupname /etc/group` | Search for a specific group |
| `tail -5 /etc/group` | View recently added groups |
| `sudo chown user:group file` | Change file owner and group |
| `sudo chown -R user:group dir/` | Recursively change ownership |
| `sudo chgrp groupname file` | Change group ownership only |
| `chmod 750 file` | Set permissions — numeric method |
| `chmod u+x file` | Set permissions — symbolic method |
| `chmod -R 770 dir/` | Recursively set permissions on a directory |
| `ls -l` | View file permissions and ownership |

---

---

# Chapter 4 — Text-Fu (Text Processing)

---

## 36. stdout (Standard Out)

Every command by default sends its results to **stdout** — your terminal screen. I/O redirection lets you change where that output goes.

**Redirect operators:**

| Operator | Behaviour |
|---|---|
| `>` | Redirect output to a file. **Creates** the file if it doesn't exist. **Overwrites** if it does |
| `>>` | Append output to the end of a file. Does NOT overwrite existing content |

```bash
echo Hello World > peanuts.txt      # Writes "Hello World" to peanuts.txt (overwrites)
echo Hello World >> peanuts.txt     # Appends "Hello World" to peanuts.txt
```

---

## 37. stdin (Standard In)

By default, a program reads its input from the **keyboard**. You can redirect it to read from a file instead using `<`.

```bash
cat < peanuts.txt       # cat reads from the file instead of waiting for keyboard input
```

Every command-line process operates with two fundamental streams: **stdin** (reads data in) and **stdout** (writes results out). Controlling both is key to effective command-line work.

---

## 38. stderr (Standard Error)

Linux has a **third** I/O stream called **stderr** — used exclusively for error messages and diagnostics. It is completely separate from stdout.

**File descriptors:**
- `0` = stdin
- `1` = stdout
- `2` = stderr

```bash
ls /fake/directory > peanuts.txt        # Error still prints to screen — NOT redirected
ls /fake/directory 2> peanuts.txt       # Redirect stderr to a file
ls /fake/directory > out.txt 2> err.txt # Redirect stdout and stderr to separate files
ls /fake/directory 2>&1                 # Merge stderr INTO stdout (both go to same place)
ls /fake/directory > out.txt 2>&1       # Redirect both stdout and stderr to one file
```

> The error message appears on screen even when you redirect with `>` because `>` only redirects stdout (file descriptor 1). To capture errors you must redirect stderr (file descriptor 2) separately using `2>`.

---

## 39. pipe and tee

**Pipe `|`** — Takes the stdout of the command on the left and feeds it as stdin to the command on the right. One of the most powerful and frequently used features in Linux.

```bash
ls -la /etc | less              # Pipe output of ls into less (scrollable view)
cat /etc/passwd | grep root     # Filter passwd file for lines containing "root"
```

**tee** — Splits the output stream in two directions: one to stdout (your screen) AND one to a file simultaneously.

```bash
ls | tee peanuts.txt            # Output appears on screen AND is saved to peanuts.txt
```

> Use `tee` when you want to see output live AND save it at the same time — great for logging.

---

## 40. env (Environment Variables)

Environment variables store information that the shell and processes can access — things like your home directory, username, and where to find programs.

```bash
echo $HOME          # Prints your home directory path
echo $USER          # Prints your current username
echo $PATH          # Prints the list of directories searched when you run a command
env                 # Lists ALL environment variables currently set in your session
```

**PATH** is the most important env variable. It's a colon-separated list of directories. When you type a command, your shell searches through each directory in PATH to find the executable. If a program is installed in a non-standard location, Linux can't find it until you add that location to PATH.

**Adding to PATH temporarily (current session only):**
```bash
export PATH=$PATH:/opt/coolapp/bin
```

**Making it permanent** — add the export line to your shell config file:
- Bash: `~/.bashrc`
- Zsh: `~/.zshrc`
- Fish: `~/.config/fish/config.fish`

---

## 41. cut

`cut` extracts portions of text from each line of a file.

**By character position (`-c`):**
```bash
cut -c5 sample.txt          # Extract the 5th character from each line
cut -c1-10 sample.txt       # Extract characters 1 through 10
```

**By field/column (`-f`):**
By default, `cut` uses TAB as the delimiter. Everything separated by a TAB is a distinct field.
```bash
cut -f2 sample.txt              # Extract the 2nd TAB-separated field
cut -d',' -f1 file.csv          # Extract 1st field using comma as delimiter
cut -d':' -f1,3 /etc/passwd     # Extract fields 1 and 3 from /etc/passwd (colon-delimited)
```

---

## 42. paste

`paste` merges lines of a file together (or merges multiple files side by side). Think of it as the opposite of `cut`.

```bash
paste sample.txt                    # Merges all lines of file into one TAB-separated line
paste -s sample.txt                 # Same as above (-s = serial, merge lines of one file)
paste -d' ' -s sample.txt          # Use space as delimiter instead of TAB
paste file1.txt file2.txt           # Combine two files side by side, separated by TAB
```

> The default delimiter for `paste` is TAB. Use `-d` to change it.

---

## 43. head

`head` shows the **beginning** of a file. Useful for quickly peeking at large files.

```bash
head /var/log/syslog            # Show first 10 lines (default)
head -n 15 /var/log/syslog      # Show first 15 lines
```

- Default is **10 lines**.
- `-n` flag sets the number of lines.

---

## 44. tail

`tail` shows the **end** of a file. Especially useful for checking the latest entries in log files.

```bash
tail /var/log/syslog            # Show last 10 lines (default)
tail -n 20 /var/log/syslog      # Show last 20 lines
tail -f /var/log/syslog         # Follow mode — shows new lines in real time as they are added
```

- Default is **10 lines**.
- `-f` (follow) is invaluable for monitoring live logs. Press `Ctrl+C` to stop.

---

## 45. expand and unexpand

Inconsistent tab/space usage makes files hard to read across different editors. These commands convert between them.

```bash
expand sample.txt               # Convert TABs to spaces (default: 8 spaces per tab)
expand -t 4 sample.txt          # Convert TABs to 4 spaces instead
unexpand -a sample.txt          # Convert spaces back to TABs
```

> `expand` outputs to stdout — it doesn't modify the file in place. Redirect to save: `expand sample.txt > fixed.txt`

---

## 46. join and split

**join** — Merges lines from two files based on a matching common field (like a SQL JOIN). Both files must be sorted on the join field.

```bash
join file1.txt file2.txt                # Join on first field (default)
join -1 2 -2 1 file1.txt file2.txt      # Join on field 2 of file1 and field 1 of file2
```

Example:
```
file1.txt      file2.txt      Result
1 John         1 Doe          1 John Doe
2 Jane         2 Doe          2 Jane Doe
3 Mary         3 Sue          3 Mary Sue
```

**split** — Breaks a large file into smaller pieces.

```bash
split largefile.txt             # Split into pieces (default 1000 lines each, named xaa, xab...)
split -l 500 largefile.txt      # Split into 500-line pieces
split -b 1M largefile.txt       # Split into 1MB pieces
```

---

## 47. sort

`sort` sorts the lines of a file alphabetically by default.

```bash
sort file.txt               # Sort alphabetically (A-Z)
sort -r file.txt            # Reverse sort (Z-A)
sort -n file.txt            # Sort numerically (treats values as numbers, not strings)
sort -u file.txt            # Sort and remove duplicates (unique)
```

> Always `sort` before using `uniq` — uniq only removes **adjacent** duplicate lines, so unsorted duplicates won't be caught.

---

## 48. tr (Translate)

`tr` translates or deletes characters from stdin. It always works with pipes — it doesn't accept filenames directly.

```bash
echo "hello world" | tr a-z A-Z         # Convert lowercase to uppercase → HELLO WORLD
echo "Hello World" | tr A-Z a-z         # Convert uppercase to lowercase → hello world
echo "hello 123" | tr -d 0-9            # Delete all digits → hello
echo "hello   world" | tr -s ' '        # Squeeze multiple spaces into one → hello world
```

- `-d` — delete specified characters
- `-s` — squeeze repeated characters into one

---

## 49. uniq (Unique)

`uniq` filters out **adjacent** duplicate lines. Because it only works on adjacent lines, you almost always pipe `sort` into it first.

```bash
uniq reading.txt                    # Remove adjacent duplicate lines
sort reading.txt | uniq             # Sort first, then remove all duplicates
sort reading.txt | uniq -c          # Count how many times each line appears
sort reading.txt | uniq -d          # Show only lines that ARE duplicated
sort reading.txt | uniq -u          # Show only lines that are NOT duplicated (unique only)
```

> The combination `sort file | uniq` is one of the most common patterns in shell scripting.

---

## 50. wc and nl

**wc (word count)** — Counts lines, words, and characters in a file.

```bash
wc sample.txt               # Shows: line count, word count, character count
wc -l sample.txt            # Count lines only
wc -w sample.txt            # Count words only
wc -c sample.txt            # Count characters (bytes) only
```

**nl (number lines)** — Adds line numbers to a file's output.

```bash
nl sample.txt               # Print file with line numbers added
```

---

## 51. grep

`grep` is arguably the most essential text-processing tool in Linux. It searches through files or streams for lines that match a pattern.

```bash
grep fox sample.txt             # Find all lines containing "fox"
grep -i fox sample.txt          # Case-insensitive search
grep -n fox sample.txt          # Show line numbers alongside matches
grep -c fox sample.txt          # Count how many lines match (don't show them)
grep -v fox sample.txt          # Invert — show lines that do NOT match
grep -e fox -e dog sample.txt   # Search for multiple patterns at once
grep "^The" sample.txt          # Lines starting with "The" (^ = start of line)
grep "dog$" sample.txt          # Lines ending with "dog" ($ = end of line)
```

**Using grep with pipes:**
```bash
env | grep USER                 # Filter env variables to find USER-related ones
ls -l | grep ".txt"             # Filter ls output to show only .txt files
cat /etc/passwd | grep root     # Find root's entry in passwd
```

> `grep` becomes extremely powerful when combined with pipes. It is the standard way to filter the output of any command.

---

## 52. Quick Reference — Text-Fu Commands

| Command | Purpose |
|---|---|
| `command > file` | Redirect stdout to file (overwrites) |
| `command >> file` | Append stdout to file |
| `command < file` | Redirect file as stdin to command |
| `command 2> file` | Redirect stderr to file |
| `command 2>&1` | Merge stderr into stdout |
| `cmd1 \| cmd2` | Pipe stdout of cmd1 into stdin of cmd2 |
| `cmd \| tee file` | Output to screen AND save to file |
| `env` | List all environment variables |
| `echo $VAR` | Print value of an environment variable |
| `export PATH=$PATH:/dir` | Add directory to PATH |
| `cut -c5 file` | Extract 5th character from each line |
| `cut -f2 file` | Extract 2nd TAB-delimited field |
| `cut -d',' -f1 file` | Extract 1st field using custom delimiter |
| `paste -s file` | Merge all lines of a file into one line |
| `head file` | Show first 10 lines of a file |
| `head -n 20 file` | Show first 20 lines |
| `tail file` | Show last 10 lines of a file |
| `tail -n 20 file` | Show last 20 lines |
| `tail -f file` | Follow file in real time (live logs) |
| `expand file` | Convert TABs to spaces |
| `unexpand -a file` | Convert spaces back to TABs |
| `join file1 file2` | Join two files on a common field |
| `split -l 500 file` | Split file into 500-line chunks |
| `sort file` | Sort lines alphabetically |
| `sort -r file` | Sort in reverse |
| `sort -n file` | Sort numerically |
| `echo "text" \| tr a-z A-Z` | Translate lowercase to uppercase |
| `echo "text" \| tr -d 0-9` | Delete digits |
| `uniq file` | Remove adjacent duplicate lines |
| `sort file \| uniq` | Remove all duplicates (sort first!) |
| `sort file \| uniq -c` | Count occurrences of each line |
| `wc file` | Count lines, words, characters |
| `wc -l file` | Count lines only |
| `nl file` | Print file with line numbers |
| `grep pattern file` | Find lines matching pattern |
| `grep -i pattern file` | Case-insensitive search |
| `grep -v pattern file` | Invert match (lines NOT matching) |
| `grep -n pattern file` | Show line numbers with matches |
| `grep -c pattern file` | Count matching lines |

---

---

# Chapter 5 — Regular Expressions (Regex)

---

## 53. What is Regex?

Regular expressions (regex) are a powerful tool for **pattern-based text selection**. They are fundamental to mastering text manipulation in Linux and are used with commands like `grep`, `sed`, `awk`, and `tr`. They use special notations, some of which are similar to wildcards like `*`.

Sample text used in examples:
```
sally sells seashells
by the seashore
```

> Always wrap regex patterns in **single quotes** `' '` to prevent the shell from misinterpreting special characters.

---

## 54. Anchors — Matching Position

Anchors don't match characters — they match a **position** in a line.

| Anchor | Meaning |
|---|---|
| `^` | Start of a line |
| `$` | End of a line |

```bash
grep "^by" file.txt             # Matches "by the seashore" — starts with "by"
grep "seashore$" file.txt       # Matches "by the seashore" — ends with "seashore"
grep "^by the seashore$" file.txt   # Exact full line match only
grep "^$" file.txt              # Matches empty lines
```

---

## 55. The Dot `.` — Match Any Single Character

The dot `.` matches **any single character** except a newline.

```bash
grep "s.lly" file.txt   # Matches "sally", "sully", "s1lly", "s lly" etc.
grep "sell." file.txt   # Matches "sells", "sella", "sell1" etc.
grep "3\.14" file.txt   # Literal dot — escape with \ to match "3.14" exactly
```

---

## 56. Character Classes `[ ]`

Square brackets define a set — exactly one character from the set matches at that position.

```bash
grep "s[ea]lls" file.txt        # Matches "sells" and "salls" but NOT "sills"
grep "[a-z]" file.txt           # Any lowercase letter
grep "[A-Z]" file.txt           # Any uppercase letter
grep "[0-9]" file.txt           # Any digit
grep "[a-zA-Z0-9]" file.txt     # Any letter or digit
grep "[^a-z]" file.txt          # Any character NOT a lowercase letter (^ inside [] = NOT)
grep "[^0-9]" file.txt          # Any character NOT a digit
```

> ⚠️ Ranges are **case-sensitive**. `[a-c]` does NOT match A, B, or C.

---

## 57. Quantifiers — How Many Times?

| Quantifier | Meaning | Mode |
|---|---|---|
| `*` | 0 or more times | BRE (default) |
| `+` | 1 or more times | ERE (`grep -E`) |
| `?` | 0 or 1 — optional | ERE (`grep -E`) |
| `{n}` | Exactly n times | ERE (`grep -E`) |
| `{n,}` | At least n times | ERE (`grep -E`) |
| `{n,m}` | Between n and m times | ERE (`grep -E`) |

```bash
grep "ab*c" file.txt            # "ac", "abc", "abbc" (0 or more b's)
grep -E "ab+c" file.txt         # "abc", "abbc" — NOT "ac" (at least 1 b)
grep -E "colou?r" file.txt      # "color" or "colour" (u is optional)
grep -E "[0-9]{4}" file.txt     # Exactly 4 digits in a row
grep -E "co{1,2}l" file.txt     # "col" or "cool"
```

---

## 58. Alternation `|` and Grouping `( )`

```bash
grep -E "cat|dog" file.txt          # Lines with "cat" OR "dog"
grep -E "sells|shores" file.txt     # Lines with "sells" OR "shores"
grep -E "(ha)+" file.txt            # "ha", "haha", "hahaha"
grep -E "(cat|dog)s?" file.txt      # "cat", "cats", "dog", "dogs"
grep -E "^(sally|by) " file.txt     # Lines starting with "sally " or "by "
```

> Both `|` and `()` require `grep -E`. In BRE, escape them: `\|` and `\(\)`.

---

## 59. BRE vs ERE

| Feature | BRE (default) | ERE (`grep -E`) |
|---|---|---|
| One or more | `\+` | `+` |
| Zero or one | `\?` | `?` |
| Grouping | `\(\)` | `()` |
| Alternation | `\|` | `\|` |
| Repetition | `\{n\}` | `{n}` |

---

## 60. Quick Reference — Regex & grep Flags

**Anchors & Characters:**

| Pattern | Meaning |
|---|---|
| `^` | Start of line |
| `$` | End of line |
| `.` | Any single character |
| `[abc]` | Any one of: a, b, c |
| `[^abc]` | NOT a, b, or c |
| `[a-z]` | Any lowercase letter |
| `[0-9]` | Any digit |
| `\` | Escape next character literally |

**Quantifiers:**

| Pattern | Meaning | Mode |
|---|---|---|
| `*` | 0 or more | BRE + ERE |
| `+` | 1 or more | ERE (`-E`) |
| `?` | 0 or 1 | ERE (`-E`) |
| `{n}` | Exactly n | ERE (`-E`) |
| `{n,m}` | n to m times | ERE (`-E`) |

**grep Flags:**

| Flag | Meaning |
|---|---|
| `-E` | Extended regex (ERE) |
| `-i` | Case-insensitive |
| `-v` | Invert match |
| `-n` | Show line numbers |
| `-c` | Count matches |
| `-w` | Whole word only |
| `-r` | Recursive search |
| `-l` | Filenames only |
| `-C n` | n lines of context |
| `-e` | Multiple patterns |

---

---

# Chapter 5 — Advanced Text-Fu

---

# Part 1 — Regular Expressions (Regex)

---

## 53. What is Regex?

Regular expressions (regex) are **patterns** used to match character combinations in strings. Used heavily with `grep`, `sed`, `awk`, and `tr`.

Sample text used in examples:
```
sally sells seashells
by the seashore
```

**Three regex modes in grep:**

| Mode | Flag | Description |
|---|---|---|
| Basic (BRE) | default | `?`, `+`, `{`, `\|` must be escaped with `\` |
| Extended (ERE) | `grep -E` | Meta-characters work without escaping |
| Perl-Compatible (PCRE) | `grep -P` | Most powerful — supports lookaheads etc. |

> Always wrap regex patterns in **single quotes** `' '` to prevent the shell misinterpreting special characters.

---

## 54. Anchors — Matching Position

| Anchor | Meaning |
|---|---|
| `^` | Start of line |
| `$` | End of line |
| `\b` | Word boundary |

```bash
grep "^by" file.txt         # Matches "by the seashore" (starts with "by")
grep "seashore$" file.txt   # Matches line ending with "seashore"
grep "^$" file.txt          # Matches empty lines
grep '\bsells\b' file.txt   # Matches whole word "sells" only
```

---

## 55. The Dot and Character Classes

`.` matches **any single character** except a newline.

```bash
grep "s.lly" file.txt       # Matches "sally", "s1lly" etc.
grep "\." file.txt          # Matches a literal dot
```

**Character classes `[ ]`:**

| Pattern | Matches |
|---|---|
| `[abc]` | Any one of: a, b, or c |
| `[a-z]` | Any lowercase letter |
| `[0-9]` | Any digit |
| `[^abc]` | Any character NOT a, b, or c |

**POSIX classes:**

| Class | Matches |
|---|---|
| `[:alpha:]` | Any letter |
| `[:digit:]` | Any digit |
| `[:alnum:]` | Any letter or digit |
| `[:upper:]` | Uppercase letters |
| `[:lower:]` | Lowercase letters |

---

## 56. Quantifiers

| Quantifier | Meaning |
|---|---|
| `*` | 0 or more |
| `+` | 1 or more (ERE) |
| `?` | 0 or 1 — optional (ERE) |
| `{n}` | Exactly n times |
| `{n,m}` | Between n and m times |

```bash
grep -E "se+" file.txt          # "se", "see" etc.
grep -E "colou?r" file.txt      # "color" or "colour"
grep -E "se{1,3}" file.txt      # "se", "see", or "seee"
```

---

## 57. Alternation and Grouping

```bash
grep -E "sells|seashells" file.txt      # OR matching
grep -E "^(sally|by)" file.txt          # Lines starting with "sally" or "by"
grep -E "(sea)(shell|shore)" file.txt   # "seashell" or "seashore"
```

---

## 58. Regex Quick Reference

| Pattern | Meaning |
|---|---|
| `^` / `$` | Start / end of line |
| `.` | Any character |
| `[abc]` | Any of a, b, c |
| `[^abc]` | NOT a, b, c |
| `*` / `+` / `?` | 0+ / 1+ / 0 or 1 |
| `{n,m}` | Between n and m times |
| `\|` | OR (ERE: no backslash needed) |
| `( )` | Group |
| `\` | Escape special character |

| grep flag | Meaning |
|---|---|
| `-E` | Extended regex |
| `-i` | Case-insensitive |
| `-v` | Invert match |
| `-n` | Show line numbers |
| `-c` | Count matches |
| `-w` | Whole word only |
| `-r` | Recursive |

---

---

# Part 2 — Text Editors

---

## 59. Text Editors Overview

| Editor | Best for | Learning curve |
|---|---|---|
| **Vim** | Fast, lightweight; pre-installed on every server | Moderate |
| **Emacs** | Extensible, all-in-one environment | Steeper |

---

---

# Part 3 — Vim

---

## 60. Vim (Vi Improved)

Pre-installed on nearly every Linux distribution. Lightweight, fast, handles large files instantly.

```bash
vim                     # Open blank buffer
vim filename.txt        # Open/create a file
```

**Vim modes:**

| Mode | How to enter | Purpose |
|---|---|---|
| **Normal** | Default / `Esc` | Navigate and run commands |
| **Insert** | `i` | Type and edit text |
| **Visual** | `v` | Select text |
| **Command-line** | `:` | Save, quit, search & replace |

> ⚠️ Press `Esc` whenever unsure — always safely returns to Normal mode.

---

## 61. Vim Navigation (Normal mode)

| Key | Movement |
|---|---|
| `h j k l` | Left / Down / Up / Right |
| `w` / `b` | Next / previous word |
| `0` / `$` | Start / end of line |
| `gg` / `G` | First / last line of file |
| `:n` | Jump to line number n |
| `Ctrl+f / b` | Page down / up |

---

## 62. Vim Search Patterns

```bash
/pattern        # Search forward
?pattern        # Search backward
n               # Next match
N               # Previous match

:s/old/new/g        # Replace all on current line
:%s/old/new/g       # Replace all in entire file
:%s/old/new/gc      # Replace all with confirmation
```

---

## 63. Vim Inserting and Appending Text

| Key | Action |
|---|---|
| `i` | Insert before cursor |
| `a` | Append after cursor |
| `I` | Insert at beginning of line |
| `A` | Append at end of line |
| `o` | New line below and insert |
| `O` | New line above and insert |

Press **`Esc`** to return to Normal mode.

---

## 64. Vim Editing (Normal mode)

| Command | Action |
|---|---|
| `x` | Delete character |
| `dd` | Delete line |
| `2dd` | Delete 2 lines |
| `d$` | Delete to end of line |
| `yy` | Copy (yank) line |
| `3yy` | Copy 3 lines |
| `p` | Paste below |
| `P` | Paste above |
| `u` | Undo |
| `Ctrl+r` | Redo |
| `r` | Replace single character |

---

## 65. Vim Saving and Exiting (Command-line mode)

| Command | Action |
|---|---|
| `:w` | Save |
| `:w filename` | Save as |
| `:q` | Quit |
| `:wq` | Save and quit |
| `:q!` | Force quit WITHOUT saving |

**Typical Vim workflow:**
```
vim filename.txt → i → type → Esc → :wq
```

---

---

# Part 4 — Emacs

---

## 66. Emacs

Extremely powerful, extensible editor. `C-` = Ctrl, `M-` = Alt/Meta.

```bash
emacs                   # Open Emacs
emacs filename.txt      # Open a file
```

**Buffers** — text lives in buffers. Multiple files = multiple buffers open simultaneously.

---

## 67. Emacs Manipulate Files

| Command | Action |
|---|---|
| `C-x C-f` | Open / create file |
| `C-x C-s` | Save |
| `C-x C-w` | Save as |
| `C-x s` | Save all |

---

## 68. Emacs Buffer Navigation

| Command | Action |
|---|---|
| `C-← / C-→` | Word left / right |
| `C-↑ / C-↓` | Paragraph up / down |
| `M-<` / `M->` | Start / end of buffer |
| `C-x 2` | Split screen horizontally |
| `C-x o` | Switch to other window |
| `C-x 1` | Close all other windows |
| `C-x k` | Close buffer |
| `C-x b` | Switch buffer |

---

## 69. Emacs Editing

In Emacs: cutting = **killing**, pasting = **yanking**.

| Command | Action |
|---|---|
| `C-Space` | Start selection (set mark) |
| `C-w` | Cut (kill) selection |
| `M-w` | Copy selection |
| `C-y` | Paste (yank) |
| `C-k` | Cut to end of line |
| `C-x u` | Undo |

---

## 70. Emacs Exiting and Help

| Command | Action |
|---|---|
| `C-x C-c` | Exit Emacs |
| `C-h C-h` | Help menu |
| `C-h k` | Describe what a key does |
| `C-h f` | Describe a function |

---

---

# Chapter 6 — The Shell

---

## 71. The Shell

The **shell** is a program that accepts your typed commands and passes them to the OS to execute. "Terminal" and "Console" apps are simply programs that open a shell session. **Bash** is the default shell for most Linux distributions.

The prompt looks like: `pete@icebox:~$`
- `pete` = username | `icebox` = hostname | `~` = current dir | `$` = regular user (`#` = root)

---

## 72. pwd (Print Working Directory)

```bash
pwd             # Output: /home/pete
```

The filesystem starts at root `/` and branches into subdirectories like a tree.

---

## 73. cd (Change Directory)

```bash
cd /home/pete/Documents     # Absolute path (starts from /)
cd Documents                # Relative path (from current location)
cd ..                       # Go up one directory
cd ~                        # Go to home directory
cd -                        # Go back to previous directory
```

---

## 74. ls (List Directories)

```bash
ls                  # List current directory
ls -l               # Long format — permissions, owner, size, date
ls -a               # Show hidden files (starting with .)
ls -la              # Long format + hidden files
ls -R               # Recursively list all subdirectories
```

---

## 75. touch

```bash
touch newfile.txt           # Create empty file
touch existingfile.txt      # Update timestamp only (no content change)
touch file1.txt file2.txt   # Create multiple files at once
```

---

## 76. file

In Linux filenames don't need to match their contents. `file` inspects actual content and tells you the real file type.

```bash
file banana.jpg         # banana.jpg: JPEG image data...
file myscript           # myscript: Bourne-Again shell script...
file /bin/ls            # /bin/ls: ELF 64-bit LSB executable...
```

---

## 77. cat

```bash
cat file.txt                    # Display file contents
cat file1.txt file2.txt         # Display two files sequentially
cat -n file.txt                 # Display with line numbers
cat > newfile.txt               # Create file and type contents (Ctrl+D to save)
cat file1.txt >> file2.txt      # Append file1 contents to file2
```

> For large files use `less` — `cat` dumps everything to screen at once.

---

## 78. less

Displays file contents **page by page**. Best for large files.

```bash
less filename.txt
```

**Navigation inside less:**

| Key | Action |
|---|---|
| `↑` / `↓` | Scroll line by line |
| `Page Up/Down` | Scroll page by page |
| `g` / `G` | Jump to start / end of file |
| `/pattern` | Search forward |
| `n` / `N` | Next / previous match |
| `q` | Quit |

---

## 79. history

```bash
history             # Show full command history with numbers
history 10          # Show last 10 commands
!!                  # Re-run last command
!42                 # Re-run command number 42
!ls                 # Re-run most recent command starting with "ls"
Ctrl+R              # Reverse search through history
```

> History is stored in `~/.bash_history` and persists across sessions.

---

## 80. cp (Copy)

```bash
cp source destination
cp mycoolfile /home/pete/Documents/         # Copy to directory
cp mycoolfile /home/pete/Documents/backup   # Copy and rename
cp *.jpg /home/pete/Pictures/               # Copy using wildcard
cp -r mydir/ /home/pete/backup/             # Copy directory recursively
cp -i file1 file2                           # Prompt before overwriting
cp -p file1 file2                           # Preserve timestamps and permissions
```

---

## 81. mv (Move)

```bash
mv oldname.txt newname.txt              # Rename
mv file.txt /home/pete/Documents/       # Move to directory
mv file.txt /home/pete/Documents/new.txt  # Move and rename
mv -i file1 file2                       # Prompt before overwriting
```

> Unlike `cp`, `mv` does NOT need `-r` for directories.

---

## 82. mkdir (Make Directory)

```bash
mkdir myfolder                          # Create single directory
mkdir dir1 dir2 dir3                    # Create multiple at once
mkdir -p parentdir/childdir/grandchild  # Create nested directories (-p = parents)
```

---

## 83. rm (Remove)

```bash
rm file.txt             # Delete file permanently
rm -i file.txt          # Prompt before deleting
rm -f file.txt          # Force delete, no prompts
rm -r mydir/            # Delete directory recursively
rm -rf mydir/           # Force delete directory — NO warnings, NO undo
```

> ⚠️ `rm -rf` has no undo. Always double-check before running.

---

## 84. find

```bash
find /home -name "puppies.jpg"          # Find by exact name
find /home -name "*.jpg"                # Find by pattern
find /home -type f -name "*.txt"        # Files only
find /home -type d                      # Directories only
find /home -newer file.txt              # Files newer than file.txt
find /home -size +1M                    # Files larger than 1MB
find . -name "*.log" -mtime -7          # Modified in last 7 days
```

| `-type` value | Meaning |
|---|---|
| `f` | Regular file |
| `d` | Directory |
| `l` | Symbolic link |

---

## 85. help, man, whatis

```bash
help echo               # Help for Bash built-in commands (cd, echo, pwd etc.)
ls --help               # Help for external programs (use --help flag)

man ls                  # Full manual page for any command
man cp                  # Press q to quit, /pattern to search inside

whatis cat              # One-line description: "cat - concatenate files..."
whatis ls               # Quick reminder without reading full man page
```

> `help` = built-ins only | `--help` = external programs | `man` = full docs | `whatis` = one-liner

---

## 86. alias

```bash
alias ll='ls -la'           # Create shortcut (current session only)
alias c='clear'
alias                       # List all active aliases
unalias ll                  # Remove an alias

# Make permanent — add to ~/.bashrc or ~/.zshrc:
alias ll='ls -la'
source ~/.bashrc            # Reload config to apply
```

---

## 87. exit

```bash
exit                # End the current shell session
logout              # End a login shell (e.g. after SSH)
```

---

## 88. Quick Reference — The Shell

| Command | Purpose |
|---|---|
| `pwd` | Print current directory |
| `cd /path` | Change directory (absolute) |
| `cd -` | Go back to previous directory |
| `ls -la` | List all files with details |
| `touch file` | Create empty file |
| `file filename` | Show actual file type |
| `cat file` | Display file contents |
| `less file` | View large files page by page |
| `history` | Show command history |
| `!!` | Re-run last command |
| `Ctrl+R` | Search history |
| `cp -r src dest` | Copy directory |
| `cp -p src dest` | Copy preserving attributes |
| `mv old new` | Move or rename |
| `mkdir -p a/b/c` | Create nested directories |
| `rm -rf dir/` | Force delete directory (no undo!) |
| `find /path -name "*.txt"` | Find files by name |
| `find /path -type d` | Find directories |
| `help cmd` | Help for Bash built-ins |
| `cmd --help` | Help for external programs |
| `man cmd` | Full manual page |
| `whatis cmd` | One-line description |
| `alias name='cmd'` | Create shortcut |
| `unalias name` | Remove alias |
| `source ~/.bashrc` | Reload shell config |
| `exit` | End shell session |

---

---

# Chapter 7 — User Management

---

## 89. Users and Groups

Every process runs **as the user who started it**. File access depends on permissions, preventing users from accessing each other's private files.

- Every user has a home directory at `/home/username`
- Users are identified by a **UID** (User ID) — a unique number
- Groups are identified by a **GID** (Group ID) — a unique number
- The OS uses UIDs/GIDs internally for all permission tasks

**Types of users:**

| Type | Description |
|---|---|
| **Root** | Superuser — unlimited power over everything |
| **Regular users** | Human users with limited privileges |
| **System users** | OS-created accounts for running services (e.g. `daemon`, `www-data`) |

---

## 90. root

The **root** user has unlimited power — can access any file, manage any process. Root prompt ends in `#` instead of `$`.

```bash
whoami          # Show current username
id              # Show UID, GID and groups
```

**Why not to operate as root constantly** — a typo or mistake could break the system. No safety net.

**`sudo` — safer alternative:**
```bash
sudo useradd bob        # Run single command as root
sudo cat /etc/shadow    # Access root-only files
sudo -i                 # Open a root shell (use sparingly)
```
- Prompts for **your** password, not root's
- All actions are **logged** in `/var/log/auth.log`
- Only users in the `sudo` group can use it

**Switch users:**
```bash
su              # Switch to root
su - username   # Switch to another user
exit            # Return to original account
```

---

## 91. /etc/passwd

The **main user database** — a plain text file with one entry per user.

```bash
cat /etc/passwd
grep -w 'pete' /etc/passwd
```

**7-field format (colon-separated):**
```
pete:x:1000:1000:Pete Smith,,,:/home/pete:/bin/bash
```

| Field | Meaning |
|---|---|
| Username | Login name |
| Password | Always `x` — actual password is in `/etc/shadow` |
| UID | User ID number |
| GID | Primary Group ID |
| GECOS | Full name / comment |
| Home directory | Path to home folder |
| Default shell | Shell launched at login |

**UID ranges:**

| Range | Type |
|---|---|
| `0` | root |
| `1–999` | System accounts |
| `1000+` | Regular human users |

> ⚠️ Never edit `/etc/passwd` directly. Use `useradd`, `usermod`, `userdel`. If you must edit directly, use `vipw` — it validates syntax before saving.

---

## 92. /etc/shadow

Stores **encrypted passwords and aging policies**. Kept separate from `/etc/passwd` so unprivileged users can't attempt to crack password hashes.

```bash
sudo cat /etc/shadow
sudo grep 'pete' /etc/shadow
```

**9-field format:**
```
pete:$6$xyz...hash...:19000:0:99999:7:::
```

| Field | Meaning |
|---|---|
| Username | Login name |
| Encrypted password | Hashed password. `*` or `!` = account locked |
| Last change | Days since Jan 1 1970 password was last changed |
| Minimum age | Min days before user can change password |
| Maximum age | Max days before password must be changed |
| Warning period | Days before expiry to warn user |
| Inactivity / Expiration | (usually empty) |

**Locked accounts** — password field is prefixed with `!`:
```
pete:!$6$xyz...hash...:19000:0:99999:7:::
```
The `!` invalidates the hash — no password will ever match, user cannot log in.

---

## 93. /etc/group

Stores all **group information** — names, GIDs, and members.

```bash
cat /etc/group
grep 'developers' /etc/group
groups pete
```

**4-field format:**
```
developers:x:1001:pete,alice,bob
```

| Field | Meaning |
|---|---|
| Group name | Name of the group |
| Password | `x` — stored in `/etc/gshadow` (rarely used) |
| GID | Group ID number |
| Members | Comma-separated list of members |

---

## 94. User Management Tools

```bash
# Create a user
sudo useradd -m bob                         # With home directory
sudo useradd -m -s /bin/bash bob            # With home dir and bash shell
sudo useradd -m -G sudo,developers bob      # With secondary groups

# Delete a user
sudo userdel bob                            # Delete account only (home dir remains)
sudo userdel -r bob                         # Delete account AND home directory

# Set/change passwords
sudo passwd bob                             # Set bob's password
passwd                                      # Change your own password
sudo passwd -l bob                          # Lock account
sudo passwd -u bob                          # Unlock account
sudo passwd -e bob                          # Force change at next login

# Modify a user
sudo usermod -d /new/home bob               # Change home directory
sudo usermod -s /bin/bash bob               # Change shell
sudo usermod -l newname bob                 # Rename user
sudo usermod -g developers bob              # Change primary group
sudo usermod -aG sudo bob                   # Add to secondary group (safe)

# Verify
id bob                                      # Show UID, GID, groups
groups bob                                  # List all groups
who                                         # Show logged-in users
last                                        # Show login history
```

---

## 95. Quick Reference — User Management

| Command | Purpose |
|---|---|
| `whoami` | Show current username |
| `id username` | Show UID, GID, all groups |
| `who` / `w` | Show logged-in users |
| `sudo useradd -m username` | Create user with home directory |
| `sudo userdel -r username` | Delete user and home directory |
| `sudo passwd username` | Set/change password |
| `sudo passwd -l username` | Lock account |
| `sudo passwd -u username` | Unlock account |
| `sudo usermod -aG group user` | Add to secondary group |
| `sudo usermod -s /bin/bash user` | Change shell |
| `cat /etc/passwd` | View all user accounts |
| `sudo cat /etc/shadow` | View encrypted passwords |
| `cat /etc/group` | View all groups |
| `su - username` | Switch to another user |
| `sudo -i` | Open root shell |

**Key system files:**

| File | Contents | Readable by |
|---|---|---|
| `/etc/passwd` | User accounts | Everyone |
| `/etc/shadow` | Encrypted passwords | Root only |
| `/etc/group` | Group info | Everyone |
| `/etc/gshadow` | Secure group info | Root only |

---

---

# Chapter 8 — Permissions

---

## 96. File Permissions

Every file and directory has permissions controlling who can do what. View with `ls -l`.

```
-  rwx  r-x  r--
↑   ↑    ↑    ↑
|   |    |    └── Others
|   |    └─────── Group
|   └──────────── Owner
└──────────────── Type: - = file, d = dir, l = symlink
```

| Letter | Files | Directories |
|---|---|---|
| `r` | View contents | List with `ls` |
| `w` | Edit/delete | Create/delete files inside |
| `x` | Run as program | Enter with `cd` |
| `-` | No permission | No permission |

---

## 97. Modifying Permissions — chmod

**Symbolic:**
```bash
chmod u+x file          # Add execute for owner
chmod g-w file          # Remove write from group
chmod o= file           # Remove ALL from others
chmod a+r file          # Add read for everyone
chmod u=rwx,g=rx,o=r file  # Set exact permissions
```

**Numeric (r=4, w=2, x=1):**
```bash
chmod 755 file          # rwxr-xr-x
chmod 644 file          # rw-r--r--
chmod 700 file          # rwx------
chmod -R 755 dir/       # Recursive
```

| Value | Pattern | Use |
|---|---|---|
| `777` | `rwxrwxrwx` | Avoid in production |
| `755` | `rwxr-xr-x` | Public dirs, scripts |
| `644` | `rw-r--r--` | Regular files |
| `600` | `rw-------` | Private files |
| `770` | `rwxrwx---` | Shared team dir |

---

## 98. Ownership — chown and chgrp

```bash
sudo chown alice file               # Change owner
sudo chown alice:developers file    # Change owner AND group
sudo chown :developers file         # Change group only
sudo chown -R alice:devs dir/       # Recursive
sudo chgrp developers file          # Change group only
```

---

## 99. Umask

Controls which permissions are **removed** from newly created files/directories.

- New files default: `666` | New directories default: `777`
- Umask value is **subtracted** from default

```bash
umask               # View current umask
umask 022           # Files → 644, Directories → 755
```

| Umask | New files | New dirs |
|---|---|---|
| `022` | `644` | `755` |
| `027` | `640` | `750` |
| `077` | `600` | `700` |
| `002` | `664` | `775` |

Permanent — add `umask 027` to `~/.bashrc` or `~/.zshrc`.

---

## 100. Setuid (SUID)

Program runs **as the file's owner** instead of the user who runs it.

Classic example — `/usr/bin/passwd` is owned by root with setuid set, so it can write to `/etc/shadow` even when run by a regular user.

```bash
ls -l /usr/bin/passwd
# -rwsr-xr-x ... root root ... /usr/bin/passwd
#     ↑ s = setuid set

sudo chmod u+s program      # Add setuid (symbolic)
sudo chmod 4755 program     # Add setuid (numeric — 4 prefix)
sudo chmod u-s program      # Remove setuid
find / -perm -4000          # Find all setuid files
```

> ⚠️ Setuid files are a security risk. Never set it on scripts.

---

## 101. Setgid (SGID)

**On files** — program runs with the file's group permissions.

**On directories (most useful)** — new files created inside **inherit the directory's group** automatically. Essential for shared team folders.

```bash
sudo chmod g+s dir/         # Add setgid (symbolic)
sudo chmod 2775 dir/        # Add setgid (numeric — 2 prefix)
find / -perm -2000          # Find all setgid files/dirs

# ls -l shows 's' in group execute position: drwxrwsr-x
```

---

## 102. Process Permissions

Every running process carries two UIDs:

| ID | Meaning |
|---|---|
| **Real UID (RUID)** | Who actually launched the process |
| **Effective UID (EUID)** | What UID the OS uses for permission checks |

Normally RUID = EUID. With setuid, EUID becomes the file owner — the process gets elevated permissions even though you (RUID) are a regular user.

```bash
ps aux      # USER column shows EUID of each process
id          # Show your real and effective UID
```

---

## 103. The Sticky Bit

Set on **directories** — users can only delete **their own files** inside, even if they have write permission on the directory.

Classic example — `/tmp` is world-writable but has the sticky bit so users can't delete each other's temp files.

```bash
ls -ld /tmp
# drwxrwxrwt ... /tmp
#          ↑ t = sticky bit

sudo chmod +t dir/          # Add sticky bit (symbolic)
sudo chmod 1777 dir/        # Add sticky bit (numeric — 1 prefix)
find / -perm -1000          # Find all sticky bit dirs
```

- `t` (lowercase) = sticky bit + others have execute
- `T` (uppercase) = sticky bit + others have NO execute

---

## 104. Quick Reference — Special Permissions

| Permission | Numeric | Symbolic | Effect |
|---|---|---|---|
| Setuid | `4xxx` | `u+s` | Runs as file owner |
| Setgid | `2xxx` | `g+s` | New files inherit group |
| Sticky bit | `1xxx` | `+t` | Only owner can delete |

```bash
sudo chmod 4755 program     # setuid + rwxr-xr-x
sudo chmod 2775 shareddir/  # setgid + rwxrwxr-x
sudo chmod 1777 /tmp        # sticky + rwxrwxrwx
```

**In ls -l output:**

| Position | Letter | Meaning |
|---|---|---|
| Owner execute | `s` | setuid set |
| Group execute | `s` | setgid set |
| Others execute | `t` / `T` | sticky bit (with/without execute) |

---

---

# Chapter 9 — Processes

---

## 105. ps (Processes)

A **process** is a running program assigned a unique **PID** (Process ID) by the kernel.

```bash
ps                      # Snapshot of current terminal's processes
ps aux                  # ALL processes on the system
ps l                    # Long format — shows PPID, priority, niceness
ps aux | grep firefox   # Filter for a specific process
top                     # Live real-time process monitor (q to quit)
```

**ps aux columns:**

| Column | Meaning |
|---|---|
| `USER` | Owner (EUID) |
| `PID` | Process ID |
| `%CPU` / `%MEM` | CPU and memory usage |
| `TTY` | Controlling terminal (`?` = no terminal) |
| `STAT` | Process state |
| `CMD` | Command and arguments |

---

## 106. Controlling Terminal (TTY)

The **TTY** field shows which terminal controls the process.

| Type | Description | Example |
|---|---|---|
| **TTY** | Native console — no GUI | `tty1`–`tty6` |
| **PTS** | Terminal emulator window | `pts/0`, `pts/4` |

- `?` in TTY column = no controlling terminal = background daemon
- `Ctrl+Alt+F1–F6` switches to virtual consoles; `Ctrl+Alt+F7` returns to GUI

```bash
tty             # Show your current terminal device name
```

---

## 107. Process Details

A process is a program the kernel has allocated resources to (memory, CPU, file descriptors).

**What the kernel tracks per process:**

| Detail | Description |
|---|---|
| PID / PPID | Process ID / Parent Process ID |
| UID / GID | Who owns it |
| State | Running, sleeping, stopped, zombie |
| Memory | Stack, heap, code |
| Open files | File descriptors |

```bash
echo $$         # PID of current shell
echo $PPID      # PPID of current shell
pstree -p       # Show full process tree with PIDs
```

---

## 108. Process Creation

Every process is created by another process via **`fork()`** — a clone of the parent.

1. Parent calls `fork()` → creates child with new PID, parent's PID becomes child's PPID
2. Child calls `execve()` → replaces itself with a new program

**`init` (PID 1)** — the first process started by the kernel at boot. Ultimate ancestor of all processes. On modern systems this is `systemd`.

```bash
pstree          # View full parent → child process tree
ps l            # Shows PPID column
```

---

## 109. Process Termination

Process exits via `_exit()` system call. Exit status `0` = success, non-zero = error.

```bash
echo $?         # Exit status of last command (0 = success)
```

**Orphan** — child whose parent died. Adopted by init. Still running.

**Zombie** — finished process whose parent hasn't called `wait()`. Shows as `Z` in STAT. No CPU/memory used but occupies process table slot. Cannot be killed — already dead.

```bash
ps aux | grep Z         # Find zombie processes
```

---

## 110. Signals

Signals are software interrupts sent to processes to notify them of events.

| Signal | Number | Shortcut | Catchable | Use |
|---|---|---|---|---|
| `SIGHUP` | 1 | `kill -1` | Yes | Hangup / reload config |
| `SIGINT` | 2 | `Ctrl+C` | Yes | Interrupt |
| `SIGKILL` | 9 | `kill -9` | **No** | Force kill immediately |
| `SIGTERM` | 15 | `kill` | Yes | Polite terminate (default) |
| `SIGTSTP` | 20 | `Ctrl+Z` | Yes | Suspend |
| `SIGSTOP` | 19 | — | **No** | Pause (uncatchable) |
| `SIGCONT` | 18 | — | Yes | Resume stopped process |

- **SIGTERM** — asks process to terminate, allows cleanup. Always try first.
- **SIGKILL** — forces immediate death. No cleanup. Cannot be caught or ignored.

```bash
kill -l         # List all signals and numbers
```

---

## 111. kill (Terminate)

```bash
kill PID                # SIGTERM — polite terminate
kill -9 PID             # SIGKILL — force kill
kill -1 PID             # SIGHUP — reload config
kill -SIGSTOP PID       # Pause process
kill -SIGCONT PID       # Resume process
killall firefox         # Kill all processes named firefox
pkill firefox           # Kill by name pattern
pgrep firefox           # Find PID by name
```

> Always try `kill PID` first. Only use `kill -9` if the process won't respond.

---

## 112. Niceness

Niceness influences how much CPU a process gets from the scheduler.

**Scale: `-20` (highest priority) → `19` (lowest priority)**

```bash
top                         # NI column shows niceness
nice -n 10 myprogram        # Start at niceness 10 (low priority)
sudo nice -n -5 myprogram   # Start at niceness -5 (higher priority)
renice 10 -p 3245           # Change niceness of running PID
sudo renice -20 -p 3245     # Set maximum priority
renice 10 -u pete           # Change all processes owned by pete
```

> Only root can set negative niceness values.

---

## 113. Process States

| STAT | State | Meaning |
|---|---|---|
| `R` | Running | Using CPU or ready in run queue |
| `S` | Sleeping | Waiting for event (most common) |
| `D` | Uninterruptible sleep | Waiting for I/O — cannot be interrupted |
| `T` | Stopped | Suspended by `Ctrl+Z` or debugger |
| `Z` | Zombie | Dead but parent hasn't called `wait()` |

**Modifiers after state:**

| Modifier | Meaning |
|---|---|
| `+` | Foreground process |
| `s` | Session leader |
| `l` | Multi-threaded |
| `<` | High priority |
| `N` | Low priority |

---

## 114. /proc Filesystem

A **virtual filesystem** generated by the kernel on the fly — not stored on disk. Every running process has a directory `/proc/PID/`.

```bash
cat /proc/1234/status       # Status, memory, UIDs of process 1234
cat /proc/1234/cmdline      # Full command line of process 1234
ls /proc/1234/fd/           # Open file descriptors
```

**System-wide files:**

| File | Contents |
|---|---|
| `/proc/cpuinfo` | CPU details |
| `/proc/meminfo` | RAM and swap usage |
| `/proc/uptime` | System uptime |
| `/proc/loadavg` | Load averages (1, 5, 15 min) |
| `/proc/version` | Kernel version |

> `ps`, `top`, and `htop` all read from `/proc` internally.

---

## 115. Job Control

Run and manage multiple processes in one terminal session.

```bash
sleep 1000 &        # Start in background (& = background)
jobs                # List all background jobs
Ctrl+Z              # Suspend the current foreground process
bg                  # Resume suspended job in background
bg %2               # Resume job number 2 in background
fg                  # Bring most recent background job to foreground
fg %1               # Bring job number 1 to foreground
kill %1             # Kill job number 1
nohup cmd &         # Run in background, survives terminal close
```

**jobs output:**
```
[1]   Running     sleep 1000 &
[2]-  Running     sleep 1001 &
[3]+  Running     sleep 1002 &   ← + = most recent (default for fg/bg)
```

---

## 116. Quick Reference — Processes

| Command | Purpose |
|---|---|
| `ps aux` | All system processes |
| `ps aux \| grep name` | Find process by name |
| `top` | Live process monitor |
| `pgrep name` | Find PID by name |
| `pstree` | Show process tree |
| `kill PID` | Polite terminate (SIGTERM) |
| `kill -9 PID` | Force kill (SIGKILL) |
| `killall name` | Kill all by name |
| `nice -n 10 cmd` | Start with low priority |
| `renice 10 -p PID` | Change priority of running process |
| `echo $?` | Last command exit status |
| `jobs` | List background jobs |
| `cmd &` | Run in background |
| `Ctrl+Z` | Suspend foreground process |
| `bg` / `fg` | Send to background / foreground |
| `kill %n` | Kill job number n |
| `nohup cmd &` | Survive terminal close |
| `cat /proc/cpuinfo` | CPU info |
| `cat /proc/meminfo` | Memory info |

---

---

# Chapter 9 — Process Utilization

---

## 105. Tracking Processes: top

`top` gives a **dynamic real-time view** of all running processes and resource usage.

```bash
top                 # Launch top
top -p 1234         # Monitor a specific process by PID
```

**Header lines:**

| Line | Meaning |
|---|---|
| Line 1 | Time, uptime, users, load average (1/5/15 min) |
| Line 2 (Tasks) | Total, running, sleeping, stopped, zombie |
| Line 3 (%Cpu) | `us`=user, `sy`=system, `id`=idle, `wa`=I/O wait |
| Line 4 (Mem) | Total, used, free, buffers |
| Line 5 (Swap) | Total, used, free, cached |

**Process columns:**

| Column | Meaning |
|---|---|
| `PID` | Process ID |
| `USER` | Owner |
| `VIRT` | Total virtual memory |
| `RES` | Physical RAM used |
| `S` | Status: S=sleep R=run Z=zombie D=uninterruptible T=stopped |
| `%CPU` | CPU usage since last update |
| `%MEM` | % of RAM used |
| `TIME+` | Total CPU time since start |

**Keys inside top:** `q`=quit, `M`=sort memory, `P`=sort CPU, `k`=kill, `r`=renice, `1`=per-CPU view

---

## 106. lsof and fuser

Linux treats almost everything as a file. These tools find what's holding a resource when you get "Device or Resource Busy."

```bash
lsof .                  # Processes using current directory
lsof -p 1234            # Files opened by PID 1234
lsof -u pete            # Files opened by user pete
lsof -i                 # All network connections
lsof -i :80             # Processes using port 80
lsof /dev/sdb1          # What's using a USB drive

fuser /dev/sdb1         # Show PIDs using the device
fuser -v /dev/sdb1      # Verbose output
fuser -k /dev/sdb1      # Kill all processes using the device
fuser -ki /dev/sdb1     # Kill with confirmation
```

> `lsof` = detailed investigation | `fuser` = quick find-and-kill for "Device Busy" errors

---

## 107. Process Threads

Threads are units of execution within a process — "lightweight processes."

- Processes have **isolated** resources (separate memory)
- Threads within the same process **share** resources — faster communication
- Every process has at least one thread
- **Single-threaded** = one thread | **Multi-threaded** = multiple concurrent threads

```bash
ps -L -p 1234       # Show threads of process 1234
ps -eLf             # Show all processes with thread info
top -H              # Thread view in top
top -H -p 1234      # Threads of a specific process
```

---

## 108. CPU Monitoring

```bash
uptime              # Load average over 1, 5, 15 minutes
nproc               # Number of CPU cores
mpstat              # CPU statistics summary
mpstat -P ALL       # Per-core CPU breakdown
mpstat 1 5          # Live, update every 1s, 5 times
```

**Load average interpretation:**
- Less than core count = CPU has spare capacity
- Equal to core count = fully utilized
- Greater than core count = overloaded, processes queuing

---

## 109. I/O Monitoring — iostat

```bash
iostat              # Summary since boot
iostat 2            # Live, update every 2 seconds
iostat -x           # Extended disk stats
```

**CPU section:** `%user`, `%system`, `%iowait` (high = disk bottleneck), `%idle`

**Disk section:** `tps` (transfers/sec), `kB_read/s`, `kB_wrtn/s`

---

## 110. Memory Monitoring

```bash
free -h             # Memory in human-readable format
free -s 2           # Update every 2 seconds

vmstat              # One-shot system stats
vmstat 2            # Live, update every 2 seconds
vmstat 2 5          # 5 updates then stop
vmstat -s           # Detailed stats table
```

**free columns:** `total`, `used`, `free`, `buff/cache`, `available`

> Watch `available` not `free` — Linux uses spare RAM for cache (reclaimed instantly when needed).

**vmstat key fields:**

| Field | Meaning |
|---|---|
| `r` | Processes in run queue |
| `b` | Processes blocked on I/O |
| `si` / `so` | Swap in / swap out per second |
| `wa` | CPU waiting for I/O |
| `us/sy/id` | User / system / idle CPU % |

> High `si`/`so` = system is swapping heavily = RAM pressure = performance degrades.

---

## 111. Continuous Monitoring — sar

`sar` records and reports **historical** system activity. Part of the `sysstat` package.

```bash
sudo apt install sysstat        # Install
```

Enable data collection if needed:
```bash
sudo nano /etc/default/sysstat  # Set ENABLED="true"
```

```bash
sar                             # Today's CPU history
sar -q                          # Load average history
sar -r                          # Memory usage history
sar -b                          # I/O history
sar -u                          # CPU utilization history
sar 1 5                         # Live — 5 updates, 1s interval
sar -f /var/log/sysstat/sa15    # View data from the 15th
```

> Essential for diagnosing intermittent problems — look back in time to find when a spike happened.

---

## 112. Cron Jobs

**Cron** schedules tasks to run automatically at specified times. Tasks are called **cron jobs**.

```bash
crontab -e          # Edit your cron jobs
crontab -l          # List current cron jobs
crontab -r          # Remove ALL cron jobs
sudo crontab -e     # Edit root's cron jobs
```

**Cron syntax:**
```
MIN  HOUR  DOM  MON  DOW  command
 *    *     *    *    *   /path/to/script.sh
 │    │     │    │    └── Day of week  (0-7, Sun=0 or 7)
 │    │     │    └─────── Month        (1-12)
 │    │     └──────────── Day of month (1-31)
 │    └────────────────── Hour         (0-23)
 └─────────────────────── Minute       (0-59)
```

`*` = wildcard = "every"

**Examples:**
```bash
30 08 * * *     /scripts/task.sh        # Every day at 8:30 AM
0 0 * * *       /scripts/backup.sh      # Every day at midnight
0 2 * * 0       /scripts/cleanup.sh     # Every Sunday at 2 AM
*/15 * * * *    /scripts/check.sh       # Every 15 minutes
0 9 * * 1-5     /scripts/work.sh        # Weekdays at 9 AM
```

**Shorthand:**
```bash
@reboot     /scripts/startup.sh         # Run at boot
@daily      /scripts/backup.sh          # Every day at midnight
@weekly     /scripts/weekly.sh          # Every Sunday at midnight
@monthly    /scripts/monthly.sh         # 1st of every month
```

**Log cron output:**
```bash
30 08 * * * /scripts/task.sh >> /home/pete/cron.log 2>&1
```

---

---

# Chapter 10 — Packages

---

## 113. Software Distribution

A Linux **package** contains all files needed to run a piece of software — the binary, libraries, configs, and a list of dependencies. A **package manager** handles install, update, and removal automatically.

**Two major ecosystems:**

| Ecosystem | Distros | Format | Tools |
|---|---|---|---|
| Debian-based | Ubuntu, Debian, Mint | `.deb` | `apt`, `dpkg` |
| Red Hat-based | RHEL, Fedora, CentOS | `.rpm` | `yum`, `dnf`, `rpm` |

---

## 114. Package Repositories

A **repository** is a central server hosting verified, curated packages. Your package manager connects to repos to find and install software.

**Debian/Ubuntu — sources list:**
- `/etc/apt/sources.list` — main repo config
- `/etc/apt/sources.list.d/` — additional repos (Ubuntu 22.04+ default)

```bash
sudo add-apt-repository ppa:some/ppa       # Add a PPA
sudo apt update                            # Refresh after adding repo
sudo yum repolist                          # List enabled repos (Red Hat)
```

---

## 115. tar and gzip

**Archiving** = combining many files into one | **Compression** = reducing file size.

- `tar` = archiving tool
- `gzip` = compression tool
- Together: `.tar.gz` (tarball)

```bash
# gzip
gzip file.txt               # Compress (replaces original)
gzip -d file.txt.gz         # Decompress
gzip -k file.txt            # Compress, keep original

# tar — create
tar -czvf archive.tar.gz dir/       # Create compressed archive
tar -cjvf archive.tar.bz2 dir/      # Create bzip2 archive

# tar — extract
tar -xzvf archive.tar.gz            # Extract .tar.gz
tar -xvf archive.tar -C /dest/      # Extract to specific directory

# tar — inspect
tar -tzvf archive.tar.gz            # List contents without extracting
```

**tar flags:** `c`=create, `x`=extract, `t`=list, `v`=verbose, `f`=filename, `z`=gzip, `j`=bzip2, `J`=xz

```bash
zip -r archive.zip dir/     # Create zip
unzip archive.zip           # Extract zip
```

---

## 116. Package Dependencies

Packages rely on **dependencies** — other packages or shared libraries they need. Think of restaurants all sourcing ingredients from the same central farm.

**Shared libraries** = pre-compiled code reused by multiple programs simultaneously.

```bash
ldd /usr/bin/firefox        # List shared libraries used by a program
```

> `dpkg` and `rpm` do NOT auto-resolve dependencies. `apt` and `yum` do — this is why full package managers exist.

---

## 117. rpm and dpkg

Low-level tools for installing individual package files. **No automatic dependency resolution.**

```bash
# dpkg (Debian .deb)
sudo dpkg -i package.deb            # Install
sudo dpkg -r package_name           # Remove
sudo dpkg -P package_name           # Purge (remove + configs)
dpkg -l                             # List all installed
dpkg -L package_name                # List files from package
dpkg -S /path/to/file               # Find which package owns a file

# rpm (Red Hat .rpm)
sudo rpm -i package.rpm             # Install
sudo rpm -U package.rpm             # Upgrade
sudo rpm -e package_name            # Remove
rpm -qa                             # List all installed
rpm -ql package_name                # List files from package
rpm -qR package_name                # List dependencies
rpm -V package_name                 # Verify package integrity
```

---

## 118. yum and apt

Full package managers — connect to repos, resolve dependencies, handle everything automatically.

```bash
# apt (Debian/Ubuntu)
sudo apt update                     # Refresh package index (do this first!)
sudo apt install package            # Install
sudo apt remove package             # Remove (keep configs)
sudo apt purge package              # Remove + config files
sudo apt autoremove                 # Remove unused dependencies
sudo apt upgrade                    # Upgrade all packages
apt search keyword                  # Search
apt show package                    # Show package info
apt list --installed                # List installed packages

# yum (Red Hat/CentOS)
sudo yum install package            # Install
sudo yum remove package             # Remove
sudo yum update                     # Update all packages
yum search keyword                  # Search
yum info package                    # Show info
yum list installed                  # List installed
```

> `apt update` only refreshes the package list — it does NOT install anything. Always run it before installing.

---

## 119. Compile Source Code

When a package isn't in any repo, compile from source:

```bash
# 1. Install build tools
sudo apt install build-essential

# 2. Extract source
tar -xzvf package.tar.gz
cd package_directory/

# 3. Read instructions
cat README
cat INSTALL

# 4. Configure — checks for dependencies
./configure

# 5. Compile
make

# 6. Install (use checkinstall — integrates with package manager)
sudo apt install checkinstall
sudo checkinstall
```

> **Always use `checkinstall` over `make install`** — it creates a `.deb`/`.rpm` so you can remove the software cleanly with `apt remove` later.

---

---

# Chapter 11 — The Filesystem

---

## 120. Filesystem Hierarchy

Linux organizes everything in one unified tree from root `/`:

```
/bin   → Essential binaries       /home  → User home directories
/etc   → System config files      /var   → Logs, mail, variable data
/dev   → Device files             /tmp   → Temporary files (cleared on reboot)
/proc  → Running process info     /mnt   → Temporary mount points
/sys   → Hardware/kernel info     /usr   → User programs and libraries
/root  → Root user's home         /boot  → Kernel and bootloader files
```

> Unlike Windows, everything attaches to `/`. External drives and USB sticks are "mounted" into the tree.

---

## 121. Filesystem Types

The **VFS (Virtual File System)** is a kernel abstraction layer providing a uniform interface across different filesystem types.

| Filesystem | Description |
|---|---|
| `ext4` | Default for most Linux distros. Journaled, reliable |
| `xfs` | High-performance. Default on RHEL/CentOS. Great for large files |
| `btrfs` | Modern — snapshots, checksums, built-in RAID |
| `vfat` | FAT32 — Windows-compatible, used for USB/EFI |
| `tmpfs` | RAM-based — used for `/tmp` |

**Journaling** — records intended changes before writing. Prevents corruption on power loss. Most modern filesystems (ext4, xfs, btrfs) are journaled.

```bash
df -T               # Show filesystem type of all mounts
lsblk -f            # List block devices with filesystem info
```

---

## 122. Anatomy of a Disk

Disks are divided into **partitions** — independent block devices:
- `/dev/sda` = whole disk | `/dev/sda1` = first partition

**Partition tables:**

| Table | Max partitions | Max disk size |
|---|---|---|
| **MBR** | 4 primary (or 3 + extended with logical) | 2 TB |
| **GPT** | 128 primary | 9.4 ZB |

```bash
sudo parted -l          # View all disks and partition tables
sudo fdisk -l           # List partition info
lsblk                   # Tree view of all block devices
```

---

## 123. Disk Partitioning

| Tool | Supports | Type |
|---|---|---|
| `fdisk` | MBR only | CLI |
| `parted` | MBR + GPT | CLI |
| `gdisk` | GPT only | CLI |
| `gparted` | MBR + GPT | GUI |

```bash
sudo fdisk /dev/sdb         # Interactive MBR partitioning
# Inside fdisk: p=print, n=new, d=delete, w=write, q=quit
sudo parted /dev/sdb print  # View partition table with parted
```

> ⚠️ Changes only save when you press `w` in fdisk. Press `q` to exit safely.

---

## 124. Creating Filesystems

After partitioning, **format** the partition with a filesystem before storing files.

```bash
sudo mkfs -t ext4 /dev/sdb1     # Format as ext4
sudo mkfs.ext4 /dev/sdb1        # Shorthand
sudo mkfs.xfs /dev/sdb2         # Format as xfs
sudo mkfs.vfat /dev/sdb3        # Format as FAT32
sudo blkid                      # Show UUID and type of all partitions
sudo blkid /dev/sdb1            # Specific partition UUID
```

> ⚠️ `mkfs` destroys all existing data. Double-check the device name first.

---

## 125. mount and umount

**Mounting** attaches a filesystem to a directory (mount point) in the Linux tree.

```bash
sudo mkdir /mydrive                         # Create mount point
sudo mount /dev/sdb2 /mydrive               # Mount device
sudo mount -t ext4 /dev/sdb2 /mydrive       # Specify type
sudo mount UUID=130b882f-... /mydrive       # Mount by UUID (reliable)
mount                                       # Show all mounts
sudo umount /mydrive                        # Unmount
```

> Mount is **temporary** — lost on reboot. Use `/etc/fstab` for persistent mounts.

---

## 126. /etc/fstab

Configures **automatic mounts at boot**. 6-field format:

```
UUID=130b882f-...   /       ext4   relatime,errors=remount-ro   0  1
UUID=78d203a0-...   /home   xfs    relatime                     0  2
UUID=22c3d34b-...   none    swap   sw                           0  0
```

| Field | Meaning |
|---|---|
| Device | UUID or `/dev/sdXn` |
| Mount point | Where to mount (or `none` for swap) |
| Type | `ext4`, `xfs`, `swap`, etc. |
| Options | `defaults`, `ro`, `noexec`, `relatime`... |
| Dump | 0=no backup, 1=yes |
| Pass | fsck order: 0=skip, 1=root, 2=others |

```bash
sudo mount -a               # Test fstab — mount everything not yet mounted
```

> ⚠️ A syntax error in fstab can prevent booting. Always test with `sudo mount -a` after editing.

---

## 127. swap

Swap is disk space used as **virtual memory** when RAM is full — idle process memory is moved to disk.

```bash
sudo mkswap /dev/sdb2           # Initialize swap partition
sudo swapon /dev/sdb2           # Activate
sudo swapoff /dev/sdb2          # Deactivate
swapon -s                       # Show active swap
free -h                         # View swap usage
```

**Create a swap file:**
```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## 128. Disk Usage

```bash
df -h                           # Filesystem-level usage (human-readable)
df -T                           # Include filesystem type
df -i                           # Inode usage

du -h                           # Directory/file usage
du -sh /home/pete               # Summary of one directory
du -sh *                        # Size of each item in current dir
du -h --max-depth=1 /home       # One level deep
du -h | sort -h | tail -20      # Top 20 largest items
```

> `df` = big picture | `du` = find what's consuming space. Use `df` first, then `du` to drill down.

---

## 129. Filesystem Repair

```bash
sudo fsck /dev/sda1             # Check and repair
sudo fsck -n /dev/sda1          # Dry run — check only, no repairs
sudo fsck -y /dev/sda1          # Auto-yes to all repair questions
```

> ⚠️ Never run `fsck` on a **mounted** filesystem. For root `/`, boot from live CD or let it run automatically at startup.

---

## 130. Inodes

Every file and directory has an **inode** — an entry in the inode table storing all metadata:

- File type, owner, group, permissions
- Timestamps: `atime` (access), `mtime` (modified), `ctime` (changed)
- File size, block count
- Pointers to actual data blocks on disk

**Filename is NOT stored in the inode** — it's stored in the directory.

```bash
ls -li                  # Show inode numbers
stat filename           # Full inode metadata
df -i                   # Inode usage per filesystem
```

> You can run out of inodes even with free disk space (millions of tiny files). If "No space left" but `df -h` shows free space — check `df -i`.

---

## 131. symlinks

**Hard link** — another directory entry pointing to the **same inode**.
**Symbolic link** — a file that stores the **path** to another file (like a shortcut).

```bash
ln target.txt hardlink.txt          # Create hard link
ln -s /path/to/target linkname      # Create symbolic link
ln -sf /new/target existinglink     # Force overwrite existing symlink
ls -l                               # Symlinks shown as: name -> target
readlink -f linkname                # Resolve full path
rm linkname                         # Remove symlink (NOT the target)
```

**Hard vs Symbolic:**

| | Hard Link | Symlink |
|---|---|---|
| Same inode | ✓ Yes | ✗ No |
| Survives original deletion | ✓ Yes | ✗ No (dangling) |
| Cross filesystem | ✗ No | ✓ Yes |
| Link to directory | ✗ No | ✓ Yes |

---

---

# Chapter 12 — Logging

---

## 132. System Logging

Services, the kernel, and daemons record their activity in **logs** — human-readable journals stored in `/var/log/`. The **rsyslog** daemon (improved syslog) collects and routes all log messages to the right files.

**Standard log entry format:**
```
Jan 27 07:41:32 icebox anacron[4650]: Job `cron.weekly' started
```
Timestamp → Hostname → Process[PID] → Message

---

## 133. syslog

`rsyslogd` reads rules from `/etc/rsyslog.d/50-default.conf` — each rule has a **selector** (what to log) and **action** (where to send it).

```
auth,authpriv.*          /var/log/auth.log
*.*;auth,authpriv.none  -/var/log/syslog
kern.*                  -/var/log/kern.log
```

**Selector format:** `facility.severity`

**Facilities:** `auth`, `kern`, `mail`, `cron`, `daemon`, `user`, `*` (all)

**Severity levels (most → least severe):**
`emerg` → `alert` → `crit` → `err` → `warn` → `notice` → `info` → `debug`

**Manually log a test message:**
```bash
logger "Hello this is a test"
logger -t "MyApp" "Application started"
# Then check: sudo tail /var/log/syslog
```

---

## 134. General Logging

```bash
sudo less /var/log/syslog               # All messages except auth
sudo less /var/log/messages             # All non-critical messages + boot info
sudo tail -f /var/log/syslog            # Live view
sudo tail -n 50 /var/log/syslog         # Last 50 lines
sudo grep "error" /var/log/syslog       # Search for errors
```

**Key log files:**

| File | Contents |
|---|---|
| `/var/log/syslog` | General system (except auth) |
| `/var/log/messages` | General + boot info |
| `/var/log/auth.log` | Logins, sudo, SSH |
| `/var/log/kern.log` | Kernel messages |
| `/var/log/dmesg` | Boot kernel messages (cleared on reboot) |
| `/var/log/apt/history.log` | Package install/remove history |
| `/var/log/cron.log` | Cron job executions |
| `/var/log/faillog` | Failed login counts |
| `/var/log/wtmp` | Login history (use `last`) |
| `/var/log/btmp` | Failed logins (use `lastb`) |

---

## 135. Kernel Logging

Kernel messages live in the **ring buffer** — viewable with `dmesg`. First place to check for hardware or driver problems.

```bash
dmesg                           # All kernel messages
dmesg | less                    # Page by page
dmesg -T                        # Human-readable timestamps
dmesg | grep -i error           # Filter errors
dmesg | grep -i usb             # USB messages
dmesg --level=err,warn          # Errors and warnings only
dmesg -w                        # Live follow mode

sudo less /var/log/kern.log     # Kernel log saved by rsyslog
```

---

## 136. Authentication Logging

Records all auth events: logins, sudo, SSH, failed attempts.

```bash
sudo less /var/log/auth.log             # Debian/Ubuntu
sudo less /var/log/secure               # Red Hat/CentOS

sudo grep "Failed password" /var/log/auth.log    # Failed logins
sudo grep "Accepted password" /var/log/auth.log  # Successful logins
sudo grep "sudo" /var/log/auth.log               # Sudo usage
sudo grep "Invalid user" /var/log/auth.log       # Unknown users

last                    # Login history
last -n 10              # Last 10 logins
lastb                   # Failed login attempts (needs sudo)
who                     # Currently logged in users
w                       # Logged in + what they're doing
```

> A flood of "Failed password" from an unknown IP = brute-force attack.

---

## 137. Managing Log Files — logrotate

`logrotate` automatically rotates, compresses, and archives logs. Runs daily via cron.

**Config files:**
- `/etc/logrotate.conf` — global defaults
- `/etc/logrotate.d/` — per-application configs

**Key directives:**

| Directive | Meaning |
|---|---|
| `daily` / `weekly` / `monthly` | Rotation schedule |
| `size 100M` | Rotate when file exceeds 100MB |
| `rotate 7` | Keep 7 rotated copies |
| `compress` | Compress rotated files |
| `delaycompress` | Don't compress the most recent rotated file |
| `missingok` | Don't error if log is missing |
| `notifempty` | Don't rotate if file is empty |
| `create 640 user group` | Create new log file after rotation |
| `sharedscripts` | Run scripts once, not once per file |

**Sample `/etc/logrotate.d/myapp`:**
```
/var/log/myapp/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 640 myappuser myappuser
    sharedscripts
    postrotate
        systemctl reload myapp > /dev/null 2>&1 || true
    endscript
}
```

**logrotate commands:**
```bash
sudo logrotate -d /etc/logrotate.d/myapp    # Dry run (no changes)
sudo logrotate -v /etc/logrotate.conf       # Verbose
sudo logrotate -f /etc/logrotate.conf       # Force rotate now
cat /var/lib/logrotate/status               # View last rotation times
```

---

---

# Chapter 13 — Network Basics

---

## 138. Network Basics

A **network** is devices connected to communicate and share resources. The internet is a massive network of networks.

| Term | Meaning |
|---|---|
| **Host** | Any device on a network |
| **Packet** | Basic unit of transmitted data |
| **Protocol** | Rules for formatting and transmitting data |
| **Port** | Numbered endpoint directing traffic to the right application |
| **Router** | Forwards packets between different networks |
| **Switch** | Connects devices within the same local network |

Two foundational models: **OSI** (7-layer theory) and **TCP/IP** (4-layer practice).

---

## 139. OSI Model

Theoretical 7-layer framework. Used for troubleshooting and understanding networking.

```
Layer 7 — Application    HTTP, FTP, SMTP, DNS
Layer 6 — Presentation   Encryption, compression, formatting
Layer 5 — Session        Manages sessions between apps
Layer 4 — Transport      TCP/UDP, ports, end-to-end delivery
Layer 3 — Network        IP routing between networks
Layer 2 — Data Link      MAC addresses, frames, Ethernet/Wi-Fi
Layer 1 — Physical       Raw bits, cables, hardware
```

| Layer | Data unit | Key protocols |
|---|---|---|
| 7 Application | Data | HTTP, SSH, FTP, SMTP, DNS |
| 4 Transport | Segment | TCP, UDP |
| 3 Network | Packet | IP, ICMP, ARP |
| 2 Data Link | Frame | Ethernet, Wi-Fi |
| 1 Physical | Bits | Cables, NIC |

**Memory trick (top→bottom):** All People Seem To Need Data Processing

---

## 140. TCP/IP Model

Practical 4-layer model the internet actually runs on.

| TCP/IP Layer | OSI Equivalent | Protocols |
|---|---|---|
| Application | Layers 5, 6, 7 | HTTP, DNS, SSH, SMTP |
| Transport | Layer 4 | TCP, UDP |
| Internet | Layer 3 | IP, ICMP, ARP |
| Link | Layers 1, 2 | Ethernet, Wi-Fi, MAC |

**Packet journey (Pete emails Patty):**
- **Sending (down):** Application → Transport adds ports → Internet adds IPs → Link adds MACs → sent
- **Receiving (up):** MAC checked → IP checked → port checked → data presented

Wrapping data with headers going down = **encapsulation**. Unwrapping going up = **de-encapsulation**.

---

## 141. Network Addressing

**IPv4** — 32-bit, 4 octets (0–255): `192.168.1.129` (~4.3 billion addresses)

**IPv6** — 128-bit, 8 hex groups: `fd60::21c:29ff:fe63:5cdc` (effectively unlimited)

**IPv4 Classes:**

| Class | First octet | Default mask | Hosts |
|---|---|---|---|
| A | 1–126 | 255.0.0.0 (/8) | ~16M |
| B | 128–191 | 255.255.0.0 (/16) | ~65K |
| C | 192–223 | 255.255.255.0 (/24) | 254 |

**Private IP ranges (not internet-routable):**

| Range | CIDR |
|---|---|
| 10.0.0.0 – 10.255.255.255 | /8 |
| 172.16.0.0 – 172.31.255.255 | /12 |
| 192.168.0.0 – 192.168.255.255 | /16 |

**Subnet mask** — separates network portion from host portion:
`192.168.1.129` with mask `255.255.255.0` → network=`192.168.1`, host=`129`

**CIDR** — compact notation for subnet mask:
`192.168.1.0/24` = first 24 bits are network, 8 bits for hosts = 254 usable hosts

| CIDR | Subnet mask | Usable hosts |
|---|---|---|
| /24 | 255.255.255.0 | 254 |
| /25 | 255.255.255.128 | 126 |
| /16 | 255.255.0.0 | 65,534 |

**MAC address** — 48-bit physical address burned into NIC: `1d:3a:32:24:4d:ce`
- First 3 pairs = manufacturer (OUI) | Last 3 pairs = device ID
- Used within local network | IP used between different networks

```bash
ip a                    # Show all interfaces, IPs, MACs
ifconfig                # Classic interface info
```

---

## 142. Application Layer

Top TCP/IP layer — interface between applications and the network.

**Common protocols and ports:**

| Protocol | Port | Use |
|---|---|---|
| HTTP | 80 | Web (unencrypted) |
| HTTPS | 443 | Web (encrypted) |
| SSH | 22 | Secure remote access |
| FTP | 20/21 | File transfer |
| SMTP | 25 | Send email |
| DNS | 53 | Domain name resolution |
| DHCP | 67/68 | Auto IP assignment |
| IMAP | 143/993 | Receive email |
| NTP | 123 | Time sync |

---

## 143. Transport Layer

Handles **end-to-end communication** using port numbers to direct data to the correct application.

**Port ranges:**

| Range | Type |
|---|---|
| 0–1023 | Well-known (HTTP=80, SSH=22) |
| 1024–49151 | Registered (apps) |
| 49152–65535 | Ephemeral (dynamic, outbound) |

**TCP — Transmission Control Protocol:**
Reliable, ordered, connection-oriented. Uses **3-way handshake**:
```
Client ──SYN──────────> Server   "I want to connect"
Client <──SYN-ACK────── Server   "OK, I'm ready"
Client ──ACK──────────> Server   "Connection established"
```
Use for: HTTP, SSH, FTP, email — when all data must arrive correctly.

**UDP — User Datagram Protocol:**
Fast, connectionless, unreliable. No handshake, no guarantees.
Use for: DNS, video streaming, gaming, VoIP — when speed > perfect delivery.

| | TCP | UDP |
|---|---|---|
| Reliable | ✓ | ✗ |
| Ordered | ✓ | ✗ |
| Speed | Slower | Faster |
| Use | HTTP, SSH, email | DNS, video, gaming |

---

## 144. Network Layer

Routes packets from source to destination host across networks. Adds **IP addresses** to packets.

```bash
ping 8.8.8.8                    # Test reachability (ICMP)
ping -c 4 google.com            # Send 4 pings
traceroute google.com           # Show every hop to destination
arp -n                          # Show ARP cache (IP → MAC)
ip neigh                        # Modern neighbour table
ip route                        # Show routing table
```

**ARP** — resolves an IP address to a MAC address on the local network (broadcasts "Who has this IP?").

**ICMP** — diagnostic protocol used by `ping` and `traceroute`.

---

## 145. Link Layer

Bottom layer — handles communication on the **local network segment**. Encapsulates IP packets into **frames** with MAC addresses.

```
Data units: Application=Data → Transport=Segment → Network=Packet → Link=Frame → Physical=Bits
```

```bash
ip link show                    # Show all interfaces and link info
ip link show eth0               # Show specific interface
```

**ARP process:** "I need the MAC for IP x.x.x.x" → broadcasts → target replies with MAC → frame built and sent.

---

## 146. DHCP Overview

**DHCP** automatically assigns IP addresses and network configuration to devices.

**What DHCP assigns:** IP address, subnet mask, default gateway, DNS servers, lease duration

**DORA — 4-step process:**

| Step | Who sends | Message | Purpose |
|---|---|---|---|
| **D**iscover | Client | Broadcast | "Any DHCP servers out there?" |
| **O**ffer | Server | Unicast | "Here's an IP offer" |
| **R**equest | Client | Broadcast | "I accept that offer" |
| **A**CK | Server | Unicast | "Confirmed, lease started" |

```bash
ip a                    # View assigned IP
dhclient eth0           # Request IP from DHCP
dhclient -r eth0        # Release DHCP lease
```

> On home networks, your router is the DHCP server — every device gets automatically configured when it connects.

---

---

# Chapter 14 — Subnetting

---

## 147. IPv4

32-bit address written as 4 octets (0–255), e.g. `192.168.1.165`

In binary: `192.168.1.165 = 11000000.10101000.00000001.10100101`

**IPv4 Classes:**

| Class | First octet | Mask | Hosts |
|---|---|---|---|
| A | 1–126 | 255.0.0.0 (/8) | ~16.7M |
| B | 128–191 | 255.255.0.0 (/16) | ~65K |
| C | 192–223 | 255.255.255.0 (/24) | 254 |
| D | 224–239 | — | Multicast |

Special: `127.0.0.1` = loopback | `255.255.255.255` = broadcast

**Private ranges (not internet-routable):**

| Range | CIDR |
|---|---|
| 10.0.0.0 – 10.255.255.255 | /8 |
| 172.16.0.0 – 172.31.255.255 | /12 |
| 192.168.0.0 – 192.168.255.255 | /16 |

---

## 148. Subnets

A **subnet** divides a larger network into smaller segments. Hosts on the same subnet communicate directly; traffic to other subnets goes through a router.

Every IP = **network prefix** (which subnet) + **host identifier** (which device)

**Subnet mask** — defines which bits are network vs host:
```
IP:    192.168.1.165  =  11000000.10101000.00000001.10100101
Mask:  255.255.255.0  =  11111111.11111111.11111111.00000000
                          ←─── network prefix ───→  ←─ host ─→
```

**Reserved addresses in every subnet:**
- First address (all host bits = 0) = **Network address**
- Last address (all host bits = 1) = **Broadcast address**

For `192.168.1.0/24`: Network=`192.168.1.0`, Broadcast=`192.168.1.255`, Usable=`.1`–`.254`

---

## 149. Subnet Math

```
Usable hosts = 2^(host bits) - 2
```
(Subtract 2 for network address + broadcast address)

**Example: `192.168.1.0 / 255.255.255.0`**
- Host bits = 8 (last octet all zeros in mask)
- Total = 2⁸ = 256 → Usable = **254**

**Example: `192.168.1.0 / 255.255.255.192` (/26)**
- Host bits = 6 → 2⁶ = 64 → Usable = **62**

**For any IP/mask — find these 4 values:**
- Network = IP AND mask → `192.168.1.0`
- Broadcast = network + all host bits to 1 → `192.168.1.255`
- First host = network + 1 → `192.168.1.1`
- Last host = broadcast - 1 → `192.168.1.254`

---

## 150. Subnetting Cheats

**Powers of 2 — memorize:**
```
2^1=2  2^2=4  2^3=8  2^4=16  2^5=32  2^6=64  2^7=128  2^8=256
```

**Binary conversion chart (one octet):**
```
Bit value:  128  64  32  16   8   4   2   1
```
Sum = 255 (max octet value)

**Decimal → Binary: `192`**
- 192 ≥ 128? ✓ (remainder 64) → bit=1
- 64 ≥ 64? ✓ (remainder 0) → bit=1
- 0 < 32? → all remaining bits=0
- Result: `11000000`

**Binary → Decimal: `10101000`**
= 128+0+32+0+8+0+0+0 = **168**

**CIDR cheat sheet:**

| CIDR | Subnet mask | Usable hosts |
|---|---|---|
| /30 | 255.255.255.252 | 2 |
| /29 | 255.255.255.248 | 6 |
| /28 | 255.255.255.240 | 14 |
| /27 | 255.255.255.224 | 30 |
| /26 | 255.255.255.192 | 62 |
| /25 | 255.255.255.128 | 126 |
| /24 | 255.255.255.0 | 254 |
| /23 | 255.255.254.0 | 510 |
| /16 | 255.255.0.0 | 65,534 |
| /8 | 255.0.0.0 | 16,777,214 |

---

## 151. CIDR

**CIDR** writes the subnet mask as a prefix length: `10.42.3.0/24`
- `/24` = first 24 bits are network, remaining 8 bits for hosts

```
Usable hosts = 2^(32 - prefix) - 2
Example: /23 → 2^(32-23) - 2 = 2^9 - 2 = 510 hosts
```

**Why classless?** Before CIDR, classes wasted huge amounts of address space. CIDR allows any prefix length for precise allocation.

**Route aggregation (supernetting):** Multiple networks combined into one route:
```
192.168.0.0/24 + 192.168.1.0/24 = 192.168.0.0/23
```

```bash
ip a            # Shows CIDR notation: inet 192.168.1.5/24
ip route        # Shows CIDR routes: 192.168.1.0/24 dev eth0
```

---

## 152. NAT

**NAT** lets devices with private IPs share one public IP to reach the internet. The router rewrites source/destination IPs as packets pass through.

**How it works:**
```
Your PC (192.168.1.100) → Router → rewrites source to public IP (203.0.113.5) → Internet
Internet replies to 203.0.113.5 → Router → looks up NAT table → delivers to 192.168.1.100
```

**NAT types:**

| Type | Description |
|---|---|
| **Static NAT** | 1:1 — one private IP ↔ one public IP (permanent) |
| **Dynamic NAT** | Pool of public IPs assigned temporarily |
| **PAT / Masquerade** | Many private IPs share one public IP using port numbers |
| **SNAT** | Modifies source IP — used for outgoing traffic |
| **DNAT** | Modifies destination IP — used for port forwarding |

**PAT** is what every home router uses — all devices share one public IP, distinguished by unique port numbers.

**iptables NAT commands:**
```bash
# Masquerade — share internet via eth0
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# DNAT — forward external port 80 to internal server
sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j DNAT --to-destination 192.168.1.10:80

# View NAT table
sudo iptables -t nat -L -n -v
```

> NAT breaks end-to-end connectivity. IPv6 doesn't need NAT — it has enough addresses for every device.

---

## 153. IPv6

**128-bit** address in 8 hex groups: `fd60:0000:0000:0000:021c:29ff:fe63:5cdc`

**Shortening rules:**
- Remove leading zeros: `0000` → `0`
- Replace one consecutive block of zeros with `::` (only once)
- `fd60::21c:29ff:fe63:5cdc`

**IPv6 address types:**

| Type | Prefix | Scope |
|---|---|---|
| Loopback | `::1/128` | Host only (like 127.0.0.1) |
| Link-local | `fe80::/10` | Local link only — NOT routable |
| Unique local | `fc00::/7` | Private network (like 192.168.x.x) |
| Global unicast | `2000::/3` | Internet-routable |
| Multicast | `ff00::/8` | One-to-many (replaces broadcast) |

**SLAAC (auto-configuration):** Device generates own IPv6 address from network prefix + MAC address. No DHCP server needed.

**IPv4 vs IPv6:**

| | IPv4 | IPv6 |
|---|---|---|
| Size | 32 bits | 128 bits |
| Total addresses | ~4.3 billion | ~340 undecillion |
| NAT | Required | Not needed |
| Broadcast | Yes | No (multicast) |
| Auto-config | DHCP | SLAAC or DHCPv6 |

```bash
ip -6 a                     # Show IPv6 addresses
ip -6 route                 # IPv6 routing table
ping6 ::1                   # Ping IPv6 loopback
ping6 fe80::1%eth0          # Ping link-local (must specify interface with %)
sudo ip addr add 2001:db8::10/64 dev eth0   # Assign static IPv6
```

---

---

# Chapter 15 — Network Config

---

## 154. Network Interfaces

A **network interface** is the connection point between the kernel's networking stack and hardware. Interfaces can be physical (NIC) or virtual (loopback, tunnel, bridge).

**Common interface names:**

| Name | Type |
|---|---|
| `eth0`, `enp0s3` | Ethernet (wired) |
| `wlan0`, `wlp3s0` | Wireless |
| `lo` | Loopback — always `127.0.0.1`, represents your own machine |
| `tun0` / `tap0` | VPN tunnels |
| `docker0` | Virtual bridge |

**`ip` — modern tool (preferred over `ifconfig`):**
```bash
ip a                                        # Show all interfaces and IPs
ip a show eth0                              # Specific interface
ip link show                                # Link-layer info
sudo ip link set eth0 up/down               # Bring interface up/down
sudo ip addr add 192.168.1.10/24 dev eth0   # Assign static IP
sudo ip addr del 192.168.1.10/24 dev eth0   # Remove IP
sudo ip addr flush dev eth0                 # Remove all IPs from interface
```

**`ifconfig` — classic (still works):**
```bash
ifconfig                # Show active interfaces
ifconfig -a             # All including inactive
ifconfig eth0           # Specific interface
```

> `ip` and `ifconfig` changes are **temporary** — lost on reboot. For persistence use `/etc/network/interfaces` (Debian/Ubuntu) or Netplan (`/etc/netplan/`).

**Persistent static IP (`/etc/network/interfaces`):**
```
auto eth0
iface eth0 inet static
    address 192.168.1.129
    netmask 255.255.255.0
    gateway 192.168.1.1
    dns-nameservers 8.8.8.8
```

---

## 155. route

The **routing table** tells the kernel where to send packets. Every outgoing packet is matched against it to find the right interface and gateway.

```bash
ip route                            # View routing table (modern)
route -n                            # Classic (numeric IPs)
```

**Sample output:**
```
default via 192.168.1.1 dev eth0    ← default gateway for all internet traffic
192.168.1.0/24 dev eth0             ← local network, reachable directly
```

**Manage routes:**
```bash
sudo ip route add 192.168.2.0/24 via 10.0.0.1      # Add route to network
sudo ip route add default via 192.168.1.1           # Set/change default gateway
sudo ip route delete 192.168.2.0/24                 # Delete route
sudo ip route delete default                        # Remove default gateway
sudo ip route replace default via 192.168.1.1       # Replace default gateway
```

**Routing decision:**
```
Packet arrives → check routing table → match specific route → forward
                                     → no match → use default gateway
                                     → no gateway → packet dropped
```

---

## 156. dhclient

**dhclient** is the DHCP client that automatically obtains network config (IP, mask, gateway, DNS) from a DHCP server.

**How it works:**
- Reads `/etc/dhcp/dhclient.conf` for interface list and options
- Reads `/var/lib/dhcp/dhclient.leases` for existing leases (avoids unnecessary requests after reboot)
- Runs DHCP DORA for each interface

```bash
sudo dhclient eth0              # Request DHCP lease for eth0
sudo dhclient -r eth0           # Release current lease
sudo dhclient -v eth0           # Verbose — see DORA process
sudo ip addr flush dev eth0 && sudo dhclient eth0   # Full refresh
```

**Key files:**

| File | Purpose |
|---|---|
| `/etc/dhcp/dhclient.conf` | Configuration — interfaces, options to request |
| `/var/lib/dhcp/dhclient.leases` | Stored DHCP leases (survives reboot) |

---

## 157. Network Manager

**NetworkManager** manages network hardware and connections automatically. On GUI systems it's the network icon in the taskbar. On boot it scans hardware, finds connections, and activates them.

```bash
systemctl status NetworkManager     # Check service status
nmtui                               # Text menu UI — easy, beginner-friendly
```

**`nmcli` — CLI for NetworkManager:**
```bash
nmcli                               # General status
nmcli device status                 # List devices and states
nmcli connection show               # All saved connections
nmcli connection show --active      # Active connections only
nmcli device show eth0              # Detailed device info
nmcli device connect eth0           # Activate device
nmcli device disconnect eth0        # Deactivate device
```

**Set static IP:**
```bash
nmcli connection modify "Wired connection 1" \
    ipv4.method manual \
    ipv4.addresses 192.168.1.100/24 \
    ipv4.gateway 192.168.1.1 \
    ipv4.dns "8.8.8.8 8.8.4.4"
nmcli connection up "Wired connection 1"
```

**Set DHCP:**
```bash
nmcli connection modify "Wired connection 1" ipv4.method auto
nmcli connection up "Wired connection 1"
```

Connection profiles stored in: `/etc/NetworkManager/system-connections/`

---

## 158. arp

**ARP** resolves IP addresses to MAC addresses on the local network. Before sending to another device on the same subnet, your system needs its MAC address to build the Ethernet frame.

**ARP cache** — a local table of known IP→MAC mappings (starts empty at boot, fills as traffic is sent):

```bash
arp -n                          # View ARP cache (numeric)
ip neigh                        # Modern equivalent
ip neigh show                   # Same
```

**Sample output:**
```
Address          HWtype  HWaddress          Flags  Iface
192.168.22.1     ether   00:12:24:fc:12:cc  C      eth0
192.168.22.254   ether   00:12:45:f2:84:64  C      eth0
```

**ARP process (IP not in cache):**
1. Source broadcasts: "Who has 192.168.1.1?"
2. Target replies: "I'm at 00:12:24:fc:12:cc"
3. Source caches the mapping and sends the packet

**Manage ARP cache:**
```bash
sudo arp -s 192.168.1.50 00:11:22:33:44:55  # Add static entry
sudo arp -d 192.168.1.50                    # Delete entry
sudo ip neigh flush all                     # Clear entire ARP cache
sudo ip neigh flush dev eth0                # Clear for one interface
```

**Populate and view ARP cache:**
```bash
ip route | grep default         # Find gateway IP
ping -c 1 192.168.1.1           # Ping it to populate ARP cache
arp -n                          # Now see the MAC in cache
```

---

---

# Chapter 16 — Network Troubleshooting

---

## 159. ICMP

**ICMP** (Internet Control Message Protocol) is a Network Layer protocol for **diagnostic and error messages** — not data transfer. Every IP packet has a **TTL (Time-To-Live)** that decrements at each router hop. When TTL hits 0, the router discards it and sends back an ICMP "Time Exceeded" message.

**Key ICMP message types:**

| Type | Name | Used by |
|---|---|---|
| 8 | Echo Request | `ping` — test connectivity |
| 0 | Echo Reply | Response to ping |
| 3 | Destination Unreachable | Router can't deliver packet (16 sub-codes) |
| 11 | Time Exceeded | TTL hit 0 — used by `traceroute` |

**Type 3 sub-codes:** 0=Network unreachable, 1=Host unreachable, 3=Port unreachable, 13=Blocked by firewall

> ⚠️ Many firewalls block ICMP. Ping failure ≠ host is down — confirm with other tools.

---

## 160. ping

Sends ICMP Echo Requests and waits for Echo Replies — tests reachability and measures latency.

```bash
ping google.com                     # Continuous ping (Ctrl+C to stop)
ping -c 4 google.com                # Send exactly 4 packets
ping -c 4 -i 0.5 google.com         # 4 packets, 0.5s interval
ping -s 100 google.com              # Packet size 100 bytes (default 56)
ping -w 5 google.com                # Stop after 5 seconds
```

**Reading output:**
```
64 bytes from 172.217.16.142: icmp_seq=1 ttl=117 time=11.8 ms
--- google.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss
rtt min/avg/max/mdev = 11.677/11.719/11.814/0.052 ms
```

| Field | Meaning |
|---|---|
| `icmp_seq` | Sequence number — tracks which packets returned |
| `ttl=117` | TTL in reply — decrements per hop |
| `time=11.8ms` | Round-trip time — lower is better |
| `0% packet loss` | All packets returned — network healthy |

**Systematic troubleshooting with ping:**
```bash
ping 127.0.0.1          # 1. Is TCP/IP stack working?
ping 192.168.1.1         # 2. Is local network/gateway working?
ping 8.8.8.8             # 3. Is internet routing working?
ping google.com          # 4. Is DNS working?
```

---

## 161. traceroute

Maps the exact **path packets take** to a destination, showing every router (hop) and RTT at each step. Go-to tool for finding *where* a network problem is occurring.

```bash
traceroute google.com           # Trace path
traceroute -n google.com        # No DNS — faster, shows IPs only
traceroute -I google.com        # Use ICMP instead of UDP
```

**How it works:** Sends packets with TTL=1, 2, 3... — each router returns ICMP "Time Exceeded" when TTL hits 0, revealing its IP and RTT.

**Sample output:**
```
 1  _gateway (10.0.2.2)       0.113 ms  0.087 ms  0.083 ms
 2  * * *
 3  * * *
 4  8.8.8.8                  14.080 ms 13.849 ms 14.399 ms
```

- `* * *` = router doesn't respond to traceroute (firewall) — not necessarily a problem
- Sudden RTT spike at a hop = potential bottleneck there
- Long RTT at early hops = local/ISP problem

**`mtr` — real-time ping + traceroute combined:**
```bash
mtr google.com              # Live continuous path + loss/latency per hop
mtr -r -c 100 google.com    # Report after 100 packets
```

---

## 162. netstat

Shows network connections, listening ports, routing tables, and interface statistics.

```bash
netstat -tulnp              # Most useful: TCP+UDP listening, numeric, with PID
netstat -anp | grep :80     # What's using port 80
netstat -r                  # Routing table
netstat -s                  # Protocol statistics
netstat -i                  # Interface statistics
```

**Common flags:** `-t`=TCP, `-u`=UDP, `-l`=listening, `-n`=numeric, `-p`=show PID

**Sample `netstat -tulnp`:**
```
Proto  Local Address    Foreign Address  State    PID/Program
tcp    0.0.0.0:22       0.0.0.0:*        LISTEN   1234/sshd
tcp    127.0.0.1:3306   0.0.0.0:*        LISTEN   5678/mysqld
```

**Connection states:** `LISTEN` | `ESTABLISHED` | `TIME_WAIT` | `CLOSE_WAIT` | `SYN_SENT`

**`ss` — modern replacement (faster, more detail):**
```bash
ss -tulnp                       # Same as netstat -tulnp
ss -t state established         # Only established connections
ss -s                           # Summary statistics
```

---

## 163. Packet Analysis

Captures and inspects raw packets on the wire — deepest level of network troubleshooting.

| Tool | Interface | Best for |
|---|---|---|
| **tcpdump** | CLI | Remote servers, quick captures, scripts |
| **Wireshark** | GUI | Deep analysis, visual protocol decoding |

**Common workflow:** Capture with `tcpdump -w file.pcap` on remote server → copy `.pcap` → open in Wireshark locally.

### tcpdump

```bash
sudo apt install tcpdump

# Basic capture
sudo tcpdump -i eth0                    # Capture on eth0
sudo tcpdump -i any                     # All interfaces
sudo tcpdump -i eth0 -c 20             # Stop after 20 packets
sudo tcpdump -i eth0 -nn               # No DNS or port name resolution
sudo tcpdump -i eth0 -v                # Verbose output

# Save and read
sudo tcpdump -i eth0 -w capture.pcap   # Save to file
sudo tcpdump -r capture.pcap           # Read saved file
```

**Filters (BPF):**
```bash
sudo tcpdump -i eth0 host 192.168.1.10      # By host (any direction)
sudo tcpdump -i eth0 src 192.168.1.10       # From this IP only
sudo tcpdump -i eth0 dst 192.168.1.10       # To this IP only
sudo tcpdump -i eth0 port 80               # By port
sudo tcpdump -i eth0 icmp                  # ICMP only
sudo tcpdump -i eth0 tcp                   # TCP only
sudo tcpdump -i eth0 not port 22           # Exclude SSH
sudo tcpdump -i eth0 host 192.168.1.10 and port 80   # Combine with and/or/not
```

**Reading a packet line:**
```
08:41:13.729687 IP 192.168.1.5.22 > 192.168.1.10.52420: Flags [P.], seq 196:568, length 372
↑ timestamp     ↑ src.port         ↑ dst.port           ↑ flags          ↑ seq     ↑ data size
```

**TCP Flags:** `S`=SYN, `F`=FIN, `R`=RST, `P`=PSH, `A`=ACK, `.`=ACK only

### Wireshark display filters

```
ip.addr == 192.168.1.10         Traffic involving this IP
tcp.port == 80                  HTTP traffic
http                            HTTP protocol
icmp                            Ping packets
dns                             DNS queries
tcp.flags.syn == 1              New TCP connections
```

---

## 164. Troubleshooting Workflow

```
1. ping 127.0.0.1              → TCP/IP stack working?
2. ping <gateway>               → Local network working?
3. ping 8.8.8.8                 → Internet routing working?
4. ping google.com              → DNS working?
5. traceroute destination       → Where exactly does it fail?
6. netstat -tulnp               → Is the service listening on the right port?
7. tcpdump -i eth0 port X       → What's actually on the wire?
```

---

---

# Chapter 17 — DNS

---

## 165. What is DNS?

**DNS (Domain Name System)** translates human-readable hostnames (`www.google.com`) into IP addresses (`192.78.12.4`). This is called **resolution**. Without DNS you'd memorize IPs for every website.

DNS is a massive **distributed, hierarchical** system — website owners manage their own records, spread across thousands of servers worldwide. No single point of failure.

**Linux name resolution order** (`/etc/nsswitch.conf` — `hosts: files dns myhostname`):
1. `/etc/hosts` — local static mappings (always first)
2. External DNS server (`/etc/resolv.conf`)
3. Your own hostname

> `/etc/hosts` always overrides external DNS.

---

## 166. DNS Components

**Name servers** — answer DNS queries. Two types:

| Type | Description |
|---|---|
| **Authoritative** | Holds the actual DNS records. The final definitive answer |
| **Recursive (Resolver)** | Queries other servers on your behalf. Also caches results |

**Zone files** — stored inside name servers. Contain **resource records (RRs)** — one per line.

**DNS Record Types:**

| Record | Purpose |
|---|---|
| `A` | Hostname → IPv4 address |
| `AAAA` | Hostname → IPv6 address |
| `CNAME` | Alias → another hostname |
| `MX` | Mail server for a domain |
| `NS` | Authoritative name servers for domain |
| `PTR` | Reverse lookup: IP → hostname |
| `TXT` | Free text (SPF, DKIM, domain verification) |
| `SOA` | Start of Authority — zone parameters |

**TTL (Time-To-Live)** — how long other servers can cache a record. Short TTL = faster propagation, more load. Long TTL = less load, slower changes.

---

## 167. DNS Process

When you type `catzontheinterwebz.com`:

```
1. Check local DNS cache                     → hit? done.
2. Check /etc/hosts                          → match? done.
3. Query Recursive Resolver (ISP / 8.8.8.8) → has cache? done.
4. Resolver queries Root Server (13 worldwide)
   → "Go ask the .com TLD server"
5. Resolver queries .com TLD Server
   → "Go ask catzontheinterwebz.com's NS"
6. Resolver queries Authoritative NS for catzontheinterwebz.com
   → returns the IP address
7. Resolver caches result (for TTL duration) and returns IP to you
8. Browser connects to the IP
```

---

## 168. /etc/hosts

Local static DNS table — checked **before** any external DNS query.

```bash
cat /etc/hosts
sudo nano /etc/hosts        # Edit (needs sudo)
```

**Format:**
```
IP_address    hostname    [alias1] [alias2]
127.0.0.1     localhost
127.0.1.1     icebox
192.168.1.50  myserver    server
```

**Common uses:**
- Block sites by pointing to `127.0.0.1`
- Shortcut hostnames for servers
- Override DNS for testing (point domain to staging server)
- Development: `myapp.local → 127.0.0.1`

**`/etc/resolv.conf`** — DNS server configuration:
```
nameserver 8.8.8.8
nameserver 8.8.4.4
search localdomain
```

> ⚠️ On modern systems with `systemd-resolved`, this file is auto-generated. Configure DNS via `nmcli` instead of editing directly.

---

## 169. DNS Setup

**DNS server options:**

| Software | Description | Best for |
|---|---|---|
| **BIND** (named) | Oldest, most deployed, full-featured | Large orgs, public DNS |
| **DNSmasq** | Lightweight, includes DHCP, easy setup | Small networks, home labs |
| **PowerDNS** | Flexible, reads from databases (MySQL etc.) | Medium orgs |
| **Unbound** | Validating caching resolver, DNSSEC focused | Caching, privacy |

**Install BIND on Ubuntu:**
```bash
sudo apt install bind9 bind9utils
sudo systemctl enable --now bind9
```

**Key BIND files:**
```
/etc/bind/named.conf.options    # Global options (forwarders, ACLs)
/etc/bind/named.conf.local      # Zone definitions
/var/cache/bind/                # Zone data files
```

**BIND management:**
```bash
sudo named-checkconf                    # Check config for syntax errors
sudo named-checkzone domain /path/zone  # Check zone file
sudo rndc reload                        # Reload zones without restart
sudo rndc flush                         # Flush DNS cache
```

---

## 170. DNS Tools

### nslookup — simple lookup

```bash
nslookup www.google.com                     # Forward lookup
nslookup 8.8.8.8                            # Reverse lookup
nslookup -type=MX gmail.com                # Specific record type
nslookup www.google.com 8.8.8.8            # Query specific DNS server
```

**Output:** `Server` = which DNS answered | `Non-authoritative` = from cache (normal) | `Address` = resolved IP

### dig — detailed lookup (preferred)

```bash
dig www.google.com                      # A record (default)
dig www.google.com MX                   # Mail records
dig www.google.com NS                   # Name servers
dig www.google.com TXT                  # TXT records
dig @8.8.8.8 www.google.com            # Query specific DNS server
dig +short www.google.com              # IP only (minimal output)
dig -x 8.8.8.8                         # Reverse lookup (PTR)
dig +trace www.google.com              # Full trace from root servers
```

**dig output sections:** `QUESTION` (what you asked) | `ANSWER` (records returned) | `AUTHORITY` (authoritative NS) | Query time | SERVER (who answered)

### host — quick and simple

```bash
host www.google.com                     # Quick lookup
host -t MX gmail.com                    # Specific record type
host 8.8.8.8                            # Reverse lookup
```

### systemd-resolved (modern Ubuntu)

```bash
resolvectl status                       # DNS config and status
resolvectl query www.google.com         # DNS query
resolvectl flush-caches                 # Flush DNS cache
```

---

## 171. Quick Reference — DNS

| File | Purpose |
|---|---|
| `/etc/hosts` | Local static hostname mappings |
| `/etc/resolv.conf` | DNS server IPs |
| `/etc/nsswitch.conf` | Resolution order |

```bash
# nslookup
nslookup domain                         # Basic lookup
nslookup -type=MX domain               # Record type

# dig
dig domain                             # A record
dig @server domain                     # Specific DNS server
dig +short domain                      # IP only
dig +trace domain                      # Full resolution path
dig -x IP                              # Reverse lookup

# systemd
resolvectl flush-caches                # Flush DNS cache
```

---

---

# Chapter 18 — Routing

---

## 172. What is a Router?

A **router** forwards packets between different networks. Think of it as a post office — it looks at the destination address and decides the best path to send it.

- **LAN ports** — connects your local devices
- **WAN port** — connects to the internet (ISP)

Every packet passes through the router. It inspects the destination IP and uses a **routing table** to decide where to send it next.

**Hops** — one hop = one router traversal. A path through two routers = 2 hops.

**Flooding vs Routing:** Flooding sends copies on every port (old, inefficient). Routing uses a table to make smart forwarding decisions.

---

## 173. Routing Table

Contains rules that determine where to send packets. Checked every time a packet needs to be forwarded.

```bash
ip route                    # View routing table (modern)
sudo route -n               # Classic view (numeric)
```

**Sample output:**
```
Destination     Gateway         Genmask         Flags  Metric  Iface
0.0.0.0         192.168.224.2   0.0.0.0         UG     0       eth0
192.168.224.0   0.0.0.0         255.255.255.0   U      1       eth0
```

**Column meanings:**

| Column | Meaning |
|---|---|
| Destination | Target network. `0.0.0.0` = default route |
| Gateway | Next router. `0.0.0.0` = directly connected |
| Genmask | Subnet mask for destination |
| Flags | U=up, G=gateway, UG=up+gateway, H=host |
| Metric | Cost — lower is preferred |
| Iface | Which network interface to send out of |

**Reading it:** Packet for `192.168.224.7` → matches row 2 → send directly via eth0. Packet for `8.8.8.8` → no specific match → use default route → send to gateway `192.168.224.2`.

```bash
sudo ip route add 192.168.2.0/24 via 10.0.0.1      # Add route
sudo ip route add default via 192.168.1.1           # Set default gateway
sudo ip route delete 192.168.2.0/24                 # Delete route
```

---

## 174. Path of a Packet

### Same local network

1. Host A checks: is destination IP on my subnet? → Yes
2. Uses ARP to get destination MAC address
3. Sends packet directly via ethernet — no router needed

### Different network (external)

1. Host A checks: is `8.8.8.8` on my subnet? → No
2. Checks routing table → no specific route → use default gateway
3. Uses ARP to get gateway's MAC address
4. Sends packet to gateway (router):
   - Source IP + Destination IP: **never change** throughout the entire journey
   - Source MAC + Destination MAC: **change at every hop**
5. Each router reads destination IP, checks its routing table, rewrites MACs, forwards
6. Final router delivers to destination via ARP

```
Host A ──(srcIP:A, dstIP:8.8.8.8, srcMAC:A, dstMAC:Router1)──→ Router1
Router1 ──(srcIP:A, dstIP:8.8.8.8, srcMAC:R1, dstMAC:Router2)──→ Router2
Router2 ──(srcIP:A, dstIP:8.8.8.8, srcMAC:R2, dstMAC:Dest)────→ Destination
```

**Rule: IPs stay the same end-to-end. MACs change at every hop.**

---

## 175. Routing Protocols

**Static routing** — admin manually enters routes. Simple, doesn't scale, no failover.

**Dynamic routing** — routers automatically share info using protocols and adapt to changes.

**Two categories:**

| Category | For | Examples |
|---|---|---|
| **IGP** (Interior Gateway Protocol) | Routing within one AS | RIP, OSPF, EIGRP |
| **EGP** (Exterior Gateway Protocol) | Routing between ASes | BGP |

**Autonomous System (AS)** — a collection of networks under one organization's control (one company, one ISP). Each has an ASN.

**Convergence** — when all routers agree on the same routing information. Time to reach this state after a change = convergence time.

---

## 176. Distance Vector Protocols

Each router only knows what neighbors tell it. Periodically sends **entire routing table** to neighbors. Routers choose the route with the lowest "distance" (usually hop count).

**Analogy:** Ask the nearest person "how far to the airport?" — you trust their answer without seeing the whole map yourself.

### RIP (Routing Information Protocol)

| Feature | Value |
|---|---|
| Metric | Hop count |
| Max hops | 15 (16 = unreachable) |
| Updates | Every 30 seconds (full table) |
| Convergence | Slow |
| Weakness | Count-to-infinity problem, no bandwidth awareness |

**RIPv1** = classful (no subnet info) | **RIPv2** = classless + authentication + multicast

**Count-to-infinity:** When a network goes down, routers slowly increment the hop count to 15 before agreeing it's unreachable — causes very slow convergence.

**EIGRP** — Cisco hybrid protocol. Uses bandwidth + delay as metric. Partial updates only (not full table). Fast convergence.

---

## 177. Link State Protocols

Each router builds a **complete map of the entire network** and calculates best paths itself using Dijkstra's SPF (Shortest Path First) algorithm.

**How it works:**
- Routers share **Link State Advertisements (LSAs)** with every router in the network
- Each router builds the same topology database
- Each independently runs SPF to find best paths
- Updates are **triggered** (only on changes — not periodic)

**Analogy:** Get a complete city map and calculate the best route yourself.

**Advantages over distance vector:** Faster convergence, no loops, scales better.
**Disadvantage:** More memory and CPU needed.

### OSPF (Open Shortest Path First)

| Feature | Value |
|---|---|
| Algorithm | Dijkstra / SPF |
| Metric | Cost (based on bandwidth — lower cost = faster link = preferred) |
| Updates | Triggered (only on changes) |
| Convergence | Fast |
| Standard | Open (all vendors) |

**Cost formula:** `Cost = 100Mbps / Interface bandwidth`
- Fast Ethernet (100Mbps) → cost 1 | Ethernet (10Mbps) → cost 10

**OSPF areas** — networks divided into areas connected via **Area 0** (backbone). Reduces topology database size.

**Router types:** Internal → ABR (Area Border) → ASBR (AS Border) → Backbone

**IS-IS** — another link state IGP. Similar to OSPF. Preferred by large ISPs.

---

## 178. Border Gateway Protocol

**BGP** is the routing protocol that runs the internet — routes packets between Autonomous Systems.

**Path vector protocol** — uses the complete AS path as its metric (not just hop count).

| | IGPs | BGP |
|---|---|---|
| Scope | Within one AS | Between ASes |
| Transport | Own protocol | TCP port 179 |
| Convergence | Fast | Slow |
| Focus | Performance | **Policy-based** |

**BGP types:** **iBGP** = within same AS | **eBGP** = between different ASes (internet)

**Key path attributes:**

| Attribute | Meaning |
|---|---|
| **AS-PATH** | List of ASes the route passed through — shorter = preferred, loop prevention |
| **NEXT-HOP** | Next router IP |
| **LOCAL-PREF** | Preferred exit within an AS (higher = preferred) |
| **MED** | Hints to external peers which entry path to use |

**Internet path example:**
```
Your PC → Your ISP (AS 12345) ──eBGP──→ Transit ISP (AS 3356) ──eBGP──→ Google (AS 15169)
```

---

## 179. Quick Reference — Routing

**Routing table:**
```bash
ip route                                            # View (modern)
sudo route -n                                       # Classic view
sudo ip route add 192.168.2.0/24 via 10.0.0.1      # Add route
sudo ip route add default via 192.168.1.1           # Default gateway
sudo ip route delete 192.168.2.0/24                 # Delete route
```

**Protocol summary:**

| Protocol | Type | Metric | Convergence |
|---|---|---|---|
| RIP | Distance Vector | Hop count (max 15) | Slow |
| RIPv2 | Distance Vector | Hop count + VLSM | Slow |
| EIGRP | Hybrid | Bandwidth + Delay | Fast |
| OSPF | Link State | Cost (bandwidth) | Fast |
| IS-IS | Link State | Cost | Fast |
| BGP | Path Vector | AS-PATH + policy | Slow |

**Key terms:**

| Term | Meaning |
|---|---|
| Hop | One router traversal |
| AS | Autonomous System — network under one org |
| IGP | Routing within one AS |
| EGP | Routing between ASes |
| Convergence | All routers agree on routing info |
| Default route | Where packets go with no specific match |
