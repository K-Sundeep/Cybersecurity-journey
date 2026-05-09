# Linux — Processes

---

## 1. ps (Processes)

A **process** is a program currently running on your machine. The Linux kernel manages all processes, and each is assigned a unique **Process ID (PID)**. PIDs are assigned sequentially as new processes are created.

**Basic process snapshot:**
```bash
ps
# PID    TTY      STAT   TIME  CMD
# 41230  pts/4    Ss     0:00  bash
# 51224  pts/4    R+     0:00  ps
```

**Column meanings:**

| Column | Meaning |
|---|---|
| `PID` | Unique Process ID |
| `TTY` | The controlling terminal that launched the process |
| `STAT` | Current status/state of the process |
| `TIME` | Total CPU time the process has consumed |
| `CMD` | The command that started the process |

**More detailed views:**
```bash
ps aux          # Show ALL processes on the system (most commonly used)
ps l            # Long format — shows PPID, priority, niceness and more
ps aux | grep firefox   # Filter for a specific process by name
```

**`ps aux` column breakdown:**

| Column | Meaning |
|---|---|
| `USER` | Owner of the process (EUID) |
| `PID` | Process ID |
| `%CPU` | CPU usage percentage |
| `%MEM` | Memory usage percentage |
| `VSZ` | Virtual memory size (KB) |
| `RSS` | Resident set size — actual RAM used (KB) |
| `TTY` | Controlling terminal (`?` = no terminal / daemon) |
| `STAT` | Process state |
| `START` | Time the process started |
| `TIME` | Total CPU time used |
| `CMD` | Command with arguments |

**`top` — live real-time process viewer:**
```bash
top             # Interactive real-time process monitor
htop            # Enhanced version of top (may need installing)
```
Press `q` to quit `top`. Press `k` then enter a PID to kill a process from within top.

---

## 2. Controlling Terminal (TTY)

The **TTY** field in `ps` output indicates the **controlling terminal** that executed the command.

**TTY** stands for "Teletype" — historically a physical device for interacting with computers. In modern Linux it refers to the terminal that provides stdin/stdout for a process.

**Two types of terminals:**

| Type | Description | Example |
|---|---|---|
| **TTY (true terminal)** | A native console — type commands directly, no GUI | Virtual consoles `tty1`–`tty6` |
| **PTS (pseudo-terminal)** | A terminal emulator window in a GUI environment | `pts/0`, `pts/1`, `pts/4` |

**Accessing virtual consoles:**
```bash
# Press Ctrl+Alt+F1 through F6 to switch to TTY1–TTY6
# Press Ctrl+Alt+F7 (or F8) to return to the graphical session
```

**What `?` in the TTY column means:**
A `?` means the process has **no controlling terminal**. These are typically system daemons that started at boot and run in the background (e.g. `sshd`, `cron`, `systemd`).

```bash
ps aux | grep "?"       # Shows background daemons with no terminal
tty                     # Shows your current terminal device name
```

---

## 3. Process Details

A **process** is more than just a running program — it is a program in execution that the kernel has allocated resources to: memory, CPU time, file descriptors, and I/O.

**Multiple instances:** Running the same program twice creates two completely separate processes, each with their own unique PID and resources. Example: open `cat` in two terminals — `ps aux | grep cat` shows two distinct processes.

**What the kernel tracks for every process:**

| Detail | Description |
|---|---|
| PID | Unique process identifier |
| PPID | Parent Process ID — who created this process |
| UID / GID | Who owns the process |
| State | Current state (running, sleeping, stopped, zombie) |
| Memory | Stack, heap, code segments |
| Open files | File descriptors the process has open |
| CPU registers | Current execution state |
| Priority / Nice | Scheduling priority |

**Key process IDs:**
```bash
echo $$         # Print PID of current shell
echo $PPID      # Print PPID of current shell
ps l            # Long format — shows both PID and PPID columns
```

---

## 4. Process Creation

Every process in Linux is created from another process using the **`fork`** system call — a process clones itself to create a child.

**How it works:**

1. The parent process calls **`fork()`** — creates a near-identical copy of itself
2. The child gets a new unique **PID**; the parent's PID becomes the child's **PPID**
3. The child typically calls **`execve()`** — replaces itself with a new program to run

```
Parent (bash, PID 100)
    |
    |── fork() ──> Child (PID 101, PPID 100)
                       |
                       |── execve(ls) ──> ls is now running as PID 101
```

**The init process:**
- When the system boots, the kernel creates **`init`** as the very first user-space process with **PID 1**
- `init` is the ultimate ancestor of **all** other processes on the system
- It runs with root privileges and cannot be killed until shutdown
- On modern systems, `init` is typically **systemd**

```bash
ps aux | grep init      # Find the init/systemd process
pstree                  # Show entire process tree (parent → child relationships)
pstree -p               # Show tree with PIDs
```

**View parent-child relationships:**
```bash
ps l
# Shows PPID column — the PID of each process's parent
```

---

## 5. Process Termination

A process ends by calling the **`_exit`** system call, signalling the kernel to reclaim its resources (memory, file descriptors etc.).

**Exit status codes:**

| Value | Meaning |
|---|---|
| `0` | Success — program completed normally |
| Non-zero | Error — something went wrong |

```bash
ls /existingdir ; echo $?       # Prints 0 (success)
ls /fakedir ; echo $?           # Prints non-zero error code
```

**`$?`** — a special variable that holds the exit status of the last command.

**The two-step termination (parent/child):**
1. Child process calls `_exit()` and sends its exit status to the kernel
2. Parent process calls `wait()` to retrieve the child's exit status and fully clean it up

Without step 2, a dead process lingers in the process table.

**Orphan processes:**
- A child whose **parent dies first** becomes an **orphan**
- The kernel automatically re-parents orphans to **init (PID 1)**
- Init regularly calls `wait()` so orphans are eventually cleaned up
- Orphans are **still running** — they just have a new parent

**Zombie processes:**
- A child that has **finished but whose parent hasn't called `wait()`** yet
- Appears as **`Z`** in the STAT column of `ps`
- Uses almost no resources (no CPU, no memory) but occupies a slot in the process table
- Cannot be killed with signals — it's already dead
- The parent calling `wait()` to clean it up is called **"reaping"**
- If the parent also dies, init adopts and reaps the zombie

```bash
ps aux | grep Z         # Find zombie processes
```

---

## 6. Signals

Signals are **software interrupts** sent to a process to notify it of an event. They are the primary way processes, users, and the kernel communicate with running processes.

**Three sources of signals:**
- **User input** — `Ctrl+C` (interrupt), `Ctrl+Z` (suspend)
- **Kernel** — notifies of hardware errors, illegal memory access
- **Other processes / admin** — using the `kill` command

**Common signals:**

| Signal | Number | Meaning | Catchable? |
|---|---|---|---|
| `SIGHUP` | 1 | Hangup — terminal closed or reload config | Yes |
| `SIGINT` | 2 | Interrupt — sent by `Ctrl+C` | Yes |
| `SIGQUIT` | 3 | Quit — sent by `Ctrl+\` | Yes |
| `SIGKILL` | 9 | Kill immediately — cannot be caught or ignored | **No** |
| `SIGTERM` | 15 | Terminate politely — default `kill` signal | Yes |
| `SIGTSTP` | 20 | Stop (suspend) — sent by `Ctrl+Z` | Yes |
| `SIGSTOP` | 19 | Stop — cannot be caught or ignored | **No** |
| `SIGCONT` | 18 | Continue a stopped process | Yes |
| `SIGSEGV` | 11 | Segmentation fault — illegal memory access | Yes |

**Key difference — SIGTERM vs SIGKILL:**
- **SIGTERM (15)** — politely asks the process to terminate. The process can catch it, do cleanup, and exit gracefully. Always try this first.
- **SIGKILL (9)** — forces the process to die immediately. Cannot be caught, blocked, or ignored. The kernel kills it directly. Use only when SIGTERM fails.

**List all signals:**
```bash
kill -l         # List all available signals and their numbers
```

---

## 7. kill (Terminate)

Despite its name, `kill` doesn't just kill processes — it **sends any signal** to any process. Its most common use is terminating processes.

```bash
kill PID                    # Send SIGTERM (15) — polite termination request
kill -9 PID                 # Send SIGKILL — force kill immediately
kill -SIGKILL PID           # Same as above (signal name instead of number)
kill -15 PID                # Send SIGTERM explicitly
kill -1 PID                 # Send SIGHUP — often used to reload config files
kill -SIGSTOP PID           # Pause/suspend a process
kill -SIGCONT PID           # Resume a paused process
```

**Kill by name instead of PID:**
```bash
killall firefox             # Send SIGTERM to all processes named "firefox"
killall -9 firefox          # Force kill all processes named "firefox"
pkill firefox               # Similar to killall — kills by name pattern
pkill -u pete               # Kill all processes owned by user pete
```

**Find a PID to kill:**
```bash
ps aux | grep firefox       # Find PID manually
pgrep firefox               # Print PID(s) of matching processes
```

**Best practice for killing a process:**
```bash
# Step 1 — try politely first
kill PID

# Step 2 — if it doesn't respond after a few seconds, force it
kill -9 PID
```

> ⚠️ `kill -9` gives the process no chance to clean up — open files may not be saved properly, temp files may remain. Always try SIGTERM first.

---

## 8. Niceness

Processes compete for CPU time. You can **influence** how much CPU a process gets by adjusting its **niceness value** — you can't directly control CPU time, but you can influence the kernel's scheduling decisions.

**Niceness scale: `-20` to `19`**

| Value | Priority | Meaning |
|---|---|---|
| `-20` | Highest | Very demanding — takes CPU from others |
| `0` | Default | Normal priority |
| `19` | Lowest | Very "nice" — gives up CPU to others |

> The higher the niceness number, the **lower** the priority. Think of it as how "nice" the process is to others — very nice processes step back and let others have more CPU.

**View niceness:**
```bash
top             # NI column shows niceness value for each process
ps aux -o pid,ni,cmd    # Show PID, niceness, and command
```

**Start a new process with a specific niceness:**
```bash
nice -n 10 myprogram        # Start with niceness 10 (lower priority)
nice -n -5 myprogram        # Start with niceness -5 (higher priority — needs sudo)
sudo nice -n -20 myprogram  # Highest possible priority
```

**Change niceness of an already running process:**
```bash
renice 10 -p 3245           # Change PID 3245 to niceness 10
renice -5 -p 3245           # Change to niceness -5 (needs sudo)
sudo renice -20 -p 3245     # Set maximum priority
renice 10 -u pete           # Change niceness of all processes owned by pete
```

> Only root can set negative niceness values (higher than default priority). Regular users can only increase niceness (lower priority).

---

## 9. Process States

Every process is always in one of several **states** that describe what it's currently doing. The state appears in the **STAT** column of `ps` output.

**Main process states:**

| STAT code | State | Meaning |
|---|---|---|
| `R` | Running / Runnable | Actively using CPU, or ready and waiting in the run queue |
| `S` | Interruptible Sleep | Waiting for an event (e.g. keyboard input, network data). Most common state |
| `D` | Uninterruptible Sleep | Waiting for I/O (usually disk). Cannot be interrupted even by signals |
| `T` | Stopped | Suspended by `Ctrl+Z` or a debugger. Can be resumed with SIGCONT |
| `Z` | Zombie | Process finished but parent hasn't called `wait()` yet |

**Additional modifier characters (after main state):**

| Modifier | Meaning |
|---|---|
| `s` | Session leader |
| `+` | In the foreground process group |
| `l` | Multi-threaded process |
| `<` | High priority (negative niceness) |
| `N` | Low priority (positive niceness) |

```bash
ps aux          # STAT column shows state + modifiers
# Examples:
# Ss    = sleeping, session leader
# R+    = running in foreground
# Sl    = sleeping, multi-threaded (common for GUI apps)
# Z     = zombie
```

---

## 10. /proc Filesystem

`/proc` is a **virtual filesystem** — it doesn't exist on disk. The kernel generates its contents on the fly when you read from it. It exposes the kernel's internal view of the system and every running process as readable files.

```bash
ls /proc        # Shows numbered directories (one per PID) + system files
```

**Per-process directories — `/proc/PID/`:**

Every running process has a directory named after its PID inside `/proc`:

```bash
cat /proc/1234/status       # Detailed status of process 1234 (state, memory, UIDs)
cat /proc/1234/cmdline      # Full command line that started the process
ls /proc/1234/fd/           # Open file descriptors of the process
cat /proc/1234/maps         # Memory map of the process
```

**System-wide files in `/proc`:**

| File | Contents |
|---|---|
| `/proc/cpuinfo` | CPU model, cores, speed, flags |
| `/proc/meminfo` | RAM and swap usage details |
| `/proc/uptime` | How long the system has been running |
| `/proc/loadavg` | System load averages (1, 5, 15 min) |
| `/proc/version` | Kernel version string |
| `/proc/mounts` | Currently mounted filesystems |

```bash
cat /proc/cpuinfo           # CPU details
cat /proc/meminfo           # Memory details
cat /proc/uptime            # System uptime in seconds
cat /proc/loadavg           # Load averages
```

> Tools like `ps`, `top`, and `htop` all read from `/proc` to get their data. You can read it directly for more detail or to build custom monitoring scripts.

---

## 11. Job Control

**Job control** lets you run and manage multiple processes within a single shell session — running long tasks in the background while keeping your terminal free.

**Running a process in the background:**
```bash
sleep 1000 &            # The & at the end sends it to background immediately
# Output: [1] 51000     → job number 1, PID 51000
```

**View all background jobs:**
```bash
jobs
# [1]   Running     sleep 1000 &
# [2]-  Running     sleep 1001 &
# [3]+  Running     sleep 1002 &
```

- `+` = most recently started background job (default for `fg`/`bg`)
- `-` = second most recently started

**Suspend a foreground process:**
```bash
# While a command is running in foreground:
Ctrl+Z          # Suspends (pauses) it — shows: [4]+ Stopped sleep 1003
```

**Send a suspended job to the background:**
```bash
bg              # Resume most recent suspended job in background
bg %4           # Resume job number 4 in background
```

**Bring a background job to the foreground:**
```bash
fg              # Bring most recent background job to foreground
fg %1           # Bring job number 1 to foreground
```

**Kill a background job:**
```bash
kill %1         # Send SIGTERM to job number 1
kill -9 %1      # Force kill job number 1
```

**Typical job control workflow:**
```bash
sleep 1000 &        # Start in background
jobs                # Check what's running
fg %1               # Bring to foreground
Ctrl+Z              # Suspend it
bg                  # Send back to background
kill %1             # Kill when done
```

**`nohup` — keep process running after logout:**
```bash
nohup myprogram &       # Runs in background, survives terminal close
                        # Output goes to nohup.out by default
```

---

## 12. Quick Reference — Processes

| Command | Purpose |
|---|---|
| `ps` | Snapshot of current terminal's processes |
| `ps aux` | All processes on the system |
| `ps l` | Long format with PPID, priority etc. |
| `ps aux \| grep name` | Find a specific process |
| `top` | Live real-time process viewer |
| `pgrep name` | Find PID(s) by process name |
| `pstree` | Show process tree (parent → child) |
| `kill PID` | Send SIGTERM (polite terminate) |
| `kill -9 PID` | Send SIGKILL (force kill) |
| `kill -l` | List all signals |
| `killall name` | Kill all processes by name |
| `pkill name` | Kill processes matching name pattern |
| `nice -n 10 cmd` | Start command with niceness 10 |
| `renice 10 -p PID` | Change niceness of running process |
| `jobs` | List background jobs in current shell |
| `command &` | Run command in background |
| `Ctrl+Z` | Suspend foreground process |
| `bg` | Resume suspended job in background |
| `fg` | Bring background job to foreground |
| `fg %n` | Bring job number n to foreground |
| `kill %n` | Kill job number n |
| `nohup cmd &` | Run command, survives terminal close |
| `echo $?` | Show exit status of last command |
| `cat /proc/PID/status` | Detailed info on a specific process |
| `cat /proc/cpuinfo` | CPU information |
| `cat /proc/meminfo` | Memory information |

**Signal quick reference:**

| Signal | Number | Shortcut | Use |
|---|---|---|---|
| SIGINT | 2 | `Ctrl+C` | Interrupt foreground process |
| SIGTSTP | 20 | `Ctrl+Z` | Suspend foreground process |
| SIGTERM | 15 | `kill PID` | Polite terminate (default) |
| SIGKILL | 9 | `kill -9 PID` | Force kill (uncatchable) |
| SIGHUP | 1 | `kill -1 PID` | Reload config / hangup |
| SIGCONT | 18 | `kill -CONT PID` | Resume stopped process |

**Process states:**

| STAT | State |
|---|---|
| `R` | Running / ready |
| `S` | Sleeping (waiting for event) |
| `D` | Uninterruptible sleep (I/O wait) |
| `T` | Stopped / suspended |
| `Z` | Zombie (dead, waiting for parent) |
