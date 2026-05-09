# Linux Text-Fu

---

---

## 1. stdout (Standard Out)

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

## 2. stdin (Standard In)

By default, a program reads its input from the **keyboard**. You can redirect it to read from a file instead using `<`.

```bash
cat < peanuts.txt       # cat reads from the file instead of waiting for keyboard input
```

Every command-line process operates with two fundamental streams: **stdin** (reads data in) and **stdout** (writes results out). Controlling both is key to effective command-line work.

---

## 3. stderr (Standard Error)

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

## 4. pipe and tee

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

## 5. env (Environment Variables)

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

## 6. cut

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

## 7. paste

`paste` merges lines of a file together (or merges multiple files side by side). Think of it as the opposite of `cut`.

```bash
paste sample.txt                    # Merges all lines of file into one TAB-separated line
paste -s sample.txt                 # Same as above (-s = serial, merge lines of one file)
paste -d' ' -s sample.txt          # Use space as delimiter instead of TAB
paste file1.txt file2.txt           # Combine two files side by side, separated by TAB
```

> The default delimiter for `paste` is TAB. Use `-d` to change it.

---

## 8. head

`head` shows the **beginning** of a file. Useful for quickly peeking at large files.

```bash
head /var/log/syslog            # Show first 10 lines (default)
head -n 15 /var/log/syslog      # Show first 15 lines
```

- Default is **10 lines**.
- `-n` flag sets the number of lines.

---

## 9. tail

`tail` shows the **end** of a file. Especially useful for checking the latest entries in log files.

```bash
tail /var/log/syslog            # Show last 10 lines (default)
tail -n 20 /var/log/syslog      # Show last 20 lines
tail -f /var/log/syslog         # Follow mode — shows new lines in real time as they are added
```

- Default is **10 lines**.
- `-f` (follow) is invaluable for monitoring live logs. Press `Ctrl+C` to stop.

---

## 10. expand and unexpand

Inconsistent tab/space usage makes files hard to read across different editors. These commands convert between them.

```bash
expand sample.txt               # Convert TABs to spaces (default: 8 spaces per tab)
expand -t 4 sample.txt          # Convert TABs to 4 spaces instead
unexpand -a sample.txt          # Convert spaces back to TABs
```

> `expand` outputs to stdout — it doesn't modify the file in place. Redirect to save: `expand sample.txt > fixed.txt`

---

## 11. join and split

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

## 12. sort

`sort` sorts the lines of a file alphabetically by default.

```bash
sort file.txt               # Sort alphabetically (A-Z)
sort -r file.txt            # Reverse sort (Z-A)
sort -n file.txt            # Sort numerically (treats values as numbers, not strings)
sort -u file.txt            # Sort and remove duplicates (unique)
```

> Always `sort` before using `uniq` — uniq only removes **adjacent** duplicate lines, so unsorted duplicates won't be caught.

---

## 13. tr (Translate)

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

## 14. uniq (Unique)

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

## 15. wc and nl

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

## 16. grep

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

## 17. Quick Reference — Text-Fu Commands

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
