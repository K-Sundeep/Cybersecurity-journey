# Linux — The Shell

---

## 1. The Shell

The **shell** is a program that accepts your typed commands and passes them to the operating system to execute. Applications like "Terminal" or "Console" are simply programs that open a shell session for you.

**Bash (Bourne Again Shell)** is the default shell for most Linux distributions and is what this course focuses on.

The shell prompt looks like this:
```
pete@icebox:~$
```
- `pete` — your username
- `icebox` — the hostname (computer name)
- `~` — your current directory (home)
- `$` — indicates a regular user. Root user shows `#`

---

## 2. pwd (Print Working Directory)

Everything in Linux is organized in a **hierarchical filesystem** starting from the root `/`.

```bash
pwd
# Output: /home/pete
```

The filesystem branches out like a tree from `/`:
```
/
|-- bin
|-- etc
|-- home
|   |-- pete
|-- var
```

---

## 3. cd (Change Directory)

```bash
cd /home/pete/Documents      # Absolute path — full path from root /
cd Documents                 # Relative path — relative to where you currently are
cd ..                        # Go up one directory
cd ~                         # Go to home directory
cd -                         # Go to the previous directory you were in
```

**Absolute vs Relative paths:**

| Type | Starts with | Example |
|---|---|---|
| Absolute | `/` | `/home/pete/Documents` |
| Relative | directory name or `.` `..` | `Documents` or `../etc` |

---

## 4. ls (List Directories)

```bash
ls                      # List files in current directory
ls /home/pete           # List files in a specific directory
ls -l                   # Long format — permissions, owner, size, date
ls -a                   # Show all files including hidden (starting with .)
ls -la                  # Long format + show all
ls -R                   # Recursively list all subdirectories
```

**Long format output breakdown:**
```
drwxr-xr-x 2 pete pete 4096 Jan 1 12:00 Documents
```
- `d` — directory (or `-` for file)
- `rwxr-xr-x` — permissions (owner / group / others)
- `2` — number of links
- `pete pete` — owner and group
- `4096` — size in bytes
- `Jan 1 12:00` — last modified date
- `Documents` — name

---

## 5. touch

```bash
touch newfile.txt           # Create a new empty file
touch existingfile.txt      # Update the timestamp of an existing file (no content change)
touch file1.txt file2.txt   # Create multiple files at once
```

- If the file **doesn't exist** — creates it as an empty file.
- If the file **already exists** — just updates its timestamp without changing content.

---

## 6. file

In Linux, **filenames don't have to represent their contents**. A file called `funny.gif` might not actually be a GIF. The `file` command inspects the actual contents and tells you what type of file it really is.

```bash
file banana.jpg         # Output: banana.jpg: JPEG image data...
file hello.txt          # Output: hello.txt: ASCII text
file myscript           # Output: myscript: Bourne-Again shell script, ASCII text executable
file /bin/ls            # Output: /bin/ls: ELF 64-bit LSB executable...
```

> Unlike Windows, Linux does not rely on file extensions to determine file type. Always use `file` if unsure.

---

## 7. cat

`cat` (concatenate) displays file contents directly to the screen. Great for short files.

```bash
cat file1.txt                   # Display contents of a file
cat file1.txt file2.txt         # Display two files one after another
cat -n file1.txt                # Display with line numbers
cat > newfile.txt               # Create a file and type contents (Ctrl+D to save)
cat file1.txt > file2.txt       # Copy contents of file1 into file2
cat file1.txt >> file2.txt      # Append contents of file1 to end of file2
```

> `cat` is best for short files. For long files, use `less` instead — `cat` will dump everything to the screen at once.

---

## 8. less

`less` displays file content in a **paged format** — one screen at a time. Perfect for large files. As the saying goes, *"less is more."*

```bash
less /home/pete/Documents/text1     # Open a file in less
```

**Navigation keys inside less:**

| Key | Action |
|---|---|
| `↑` / `↓` | Scroll up / down one line |
| `Page Up` / `Page Down` | Scroll up / down one full page |
| `g` | Jump to the **beginning** of the file |
| `G` | Jump to the **end** of the file |
| `/pattern` | Search forward for a pattern |
| `?pattern` | Search backward for a pattern |
| `n` | Jump to next search match |
| `N` | Jump to previous search match |
| `h` | Show help menu |
| `q` | Quit and return to the shell |

> Your normal shell commands won't work while inside `less`. Use the keys above to navigate, and `q` to exit.

---

## 9. history

The shell keeps a record of every command you've typed. `history` lets you view and reuse them.

```bash
history             # Show the full list of past commands with numbers
history 10          # Show only the last 10 commands
```

**Reusing commands from history:**

| Shortcut | Action |
|---|---|
| `↑` / `↓` arrow keys | Scroll through previous commands one by one |
| `Ctrl+R` | Reverse search — type part of a command to find it |
| `!!` | Run the **last** command again |
| `!n` | Run command number `n` from history (e.g. `!42`) |
| `!string` | Run the most recent command starting with that string (e.g. `!ls`) |

```bash
!!              # Re-run last command
!42             # Re-run command #42 from history
!ls             # Re-run the most recent command that started with "ls"
```

> History is stored in `~/.bash_history`. It saves across sessions so you can find commands from days ago.

---

## 10. cp (Copy)

```bash
cp source destination
```

```bash
cp mycoolfile /home/pete/Documents/         # Copy file to a directory
cp mycoolfile /home/pete/Documents/backup   # Copy and rename in one step
cp *.jpg /home/pete/Pictures/               # Copy all .jpg files using wildcard
cp -r mydir/ /home/pete/backup/             # Copy entire directory recursively
cp -i file1 file2                           # Prompt before overwriting (-i = interactive)
cp -p file1 file2                           # Preserve file attributes (timestamps, permissions)
```

| Flag | Meaning |
|---|---|
| `-r` | Recursive — required when copying directories |
| `-i` | Interactive — prompt before overwriting |
| `-p` | Preserve — keep original timestamps and permissions |

---

## 11. mv (Move)

`mv` moves files/directories AND renames them — it's the same command for both.

```bash
mv oldname.txt newname.txt              # Rename a file
mv file.txt /home/pete/Documents/       # Move a file to another directory
mv file.txt /home/pete/Documents/new.txt  # Move AND rename in one step
mv dir1/ /home/pete/backup/             # Move a directory
mv -i file1 file2                       # Prompt before overwriting
```

> Unlike `cp`, `mv` does **not** need `-r` for directories — it moves them as-is.

---

## 12. mkdir (Make Directory)

```bash
mkdir myfolder                          # Create a single directory
mkdir dir1 dir2 dir3                    # Create multiple directories at once
mkdir -p parentdir/childdir/grandchild  # Create nested directories in one shot
```

- **`-p`** — "parents". Creates all intermediate directories that don't exist yet. Without `-p`, if `parentdir` doesn't exist, the command fails.

---

## 13. rm (Remove)

```bash
rm file.txt                 # Delete a file permanently
rm -i file.txt              # Prompt for confirmation before deleting
rm -f file.txt              # Force delete — no prompt, no error if file doesn't exist
rm -r mydir/                # Delete a directory and all its contents recursively
rm -rf mydir/               # Force delete directory recursively — NO warnings, NO undo
```

| Flag | Meaning |
|---|---|
| `-i` | Interactive — confirm before each deletion |
| `-f` | Force — skip prompts, ignore non-existent files |
| `-r` | Recursive — required to delete directories |

> ⚠️ `rm -rf` is one of the most dangerous commands in Linux. **There is no trash bin, no undo.** Always double-check what you're deleting before running it.

---

## 14. find

`find` searches for files and directories in a directory tree. Far more powerful than `ls` for locating specific files.

```bash
find /home -name "puppies.jpg"          # Find file by exact name
find /home -name "*.jpg"                # Find all .jpg files
find /home -type f -name "*.txt"        # Find only files (-type f) with .txt extension
find /home -type d                      # Find only directories (-type d)
find /home -newer file.txt              # Find files newer than file.txt
find /home -size +1M                    # Find files larger than 1MB
find . -name "*.log" -mtime -7          # Find .log files modified in the last 7 days
```

**`-type` values:**

| Value | Meaning |
|---|---|
| `f` | Regular file |
| `d` | Directory |
| `l` | Symbolic link |

**Size units for `-size`:**

| Unit | Meaning |
|---|---|
| `c` | Bytes |
| `k` | Kilobytes |
| `M` | Megabytes |
| `G` | Gigabytes |

> `find` searches recursively by default — it looks through all subdirectories from the starting point.

---

## 15. help

**`help`** is a Bash built-in command that provides information about other **built-in** commands (like `cd`, `echo`, `pwd`).

```bash
help echo           # Show help for the echo built-in
help cd             # Show help for cd
```

For programs that are **not** shell built-ins, use the `--help` flag instead:

```bash
ls --help           # Show usage summary for ls
cp --help           # Show usage summary for cp
```

> `help` only works for Bash built-ins. For everything else, use `--help` or `man`.

---

## 16. man

`man` opens the full **manual page** for any command. Man pages are the built-in documentation for Linux — detailed, accurate, and always available offline.

```bash
man ls              # Open the manual for ls
man cp              # Open the manual for cp
man man             # Open the manual for man itself
```

**Navigating inside man:**

| Key | Action |
|---|---|
| `↑` / `↓` | Scroll line by line |
| `Page Up` / `Page Down` | Scroll page by page |
| `/pattern` | Search for a term |
| `n` | Jump to next search result |
| `q` | Quit the man page |

> Man pages are the **definitive reference** for any command. If you want to know what every flag does, `man` is the answer.

---

## 17. whatis

`whatis` gives a **one-line description** of any command — like a quick dictionary for the terminal. Useful when you just need a quick reminder without reading an entire man page.

```bash
whatis cat          # Output: cat - concatenate files and print on the standard output
whatis ls           # Output: ls - list directory contents
whatis pwd          # Output: pwd - print name of current/working directory
whatis cp           # Output: cp - copy files and directories
```

> The description comes directly from the `NAME` section of the command's man page — so it's always accurate.

---

## 18. alias

`alias` lets you create a **custom shortcut** for any command or combination of commands.

**Create a temporary alias (current session only):**
```bash
alias ll='ls -la'               # Now "ll" runs "ls -la"
alias c='clear'                 # Now "c" clears the screen
alias rm='rm -i'                # Make rm always ask for confirmation
```

**List all active aliases:**
```bash
alias
```

**Remove an alias:**
```bash
unalias ll                      # Remove the "ll" alias for this session
```

**Make an alias permanent** — add it to your shell config file:
```bash
# Add to ~/.bashrc (Bash) or ~/.zshrc (Zsh):
alias ll='ls -la'

# Then reload the config:
source ~/.bashrc
```

> Temporary aliases disappear when you close the terminal. To keep them permanently, they must be in your `~/.bashrc` or `~/.zshrc`.

---

## 19. exit

```bash
exit                # End the current shell session
logout              # End a login shell session (alternative to exit)
```

- `exit` is universal — works in any shell environment.
- `logout` is specifically for **login shells** (e.g. when you SSH into a server).
- In a GUI, you can also simply close the terminal window.

---

## 20. Quick Reference — The Shell

| Command | Purpose |
|---|---|
| `pwd` | Print current working directory |
| `cd /path` | Change to absolute path |
| `cd ..` | Go up one directory |
| `cd -` | Go back to previous directory |
| `ls` | List files in current directory |
| `ls -la` | Long format + show hidden files |
| `touch file` | Create empty file / update timestamp |
| `file filename` | Show what type of file it actually is |
| `cat file` | Display file contents |
| `cat -n file` | Display with line numbers |
| `less file` | View large files page by page |
| `history` | Show command history |
| `!!` | Re-run last command |
| `!n` | Re-run command number n |
| `Ctrl+R` | Search command history |
| `cp src dest` | Copy file |
| `cp -r dir/ dest/` | Copy directory recursively |
| `mv old new` | Move or rename file/directory |
| `mkdir dir` | Create directory |
| `mkdir -p a/b/c` | Create nested directories |
| `rm file` | Delete file |
| `rm -rf dir/` | Force delete directory (no undo!) |
| `find /path -name "*.txt"` | Find files by name |
| `find /path -type d` | Find directories only |
| `help command` | Help for Bash built-ins |
| `command --help` | Help for external programs |
| `man command` | Full manual page for a command |
| `whatis command` | One-line description of a command |
| `alias name='cmd'` | Create a command shortcut |
| `unalias name` | Remove an alias |
| `source ~/.bashrc` | Reload shell config file |
| `exit` | End the shell session |
