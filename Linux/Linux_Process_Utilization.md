# Linux — Process Utilization

---

## 1. Tracking Processes: top

`top` gives you a **dynamic, real-time view** of all running processes and system resource usage. It updates automatically every few seconds.

```bash
top                     # Launch top
top -p 1234             # Monitor a specific process by PID
```

**Sample top output:**
```
top - 18:06:26 up 6 days, 4:07, 2 users, load average: 0.92, 0.62, 0.59
Tasks: 389 total, 1 running, 387 sleeping, 0 stopped, 1 zombie
%Cpu(s): 1.8 us, 0.4 sy, 0.0 ni, 97.6 id, 0.1 wa, 0.0 hi, 0.0 si, 0.0 st
KiB Mem: 32870888 total, 27467976 used, 5402912 free, 518808 buffers
KiB Swap: 33480700 total, 39892 used, 33440808 free, 19454152 cached Mem

PID   USER  PR  NI   VIRT    RES   SHR  S  %CPU %MEM   TIME+   COMMAND
6675  patty 20   0 1731472 520960 30876  S   8.3  1.6 160:24.79 chrome
```

**Header lines explained:**

| Line | Meaning |
|---|---|
| Line 1 (`top -`) | Current time, uptime, number of users, load average over 1/5/15 minutes |
| Line 2 (`Tasks`) | Total processes: running, sleeping, stopped, zombie |
| Line 3 (`%Cpu`) | CPU time breakdown — `us`=user, `sy`=system, `id`=idle, `wa`=waiting for I/O |
| Line 4 (`KiB Mem`) | Physical RAM — total, used, free, buffers |
| Line 5 (`KiB Swap`) | Swap space — total, used, free, cached |

**Process columns explained:**

| Column | Meaning |
|---|---|
| `PID` | Process ID |
| `USER` | User who owns the process |
| `PR` | Priority |
| `NI` | Nice value (negative = higher priority) |
| `VIRT` | Total virtual memory used |
| `RES` | Physical RAM used (resident memory) |
| `SHR` | Shared memory used |
| `S` | Status: `S`=sleeping, `R`=running, `Z`=zombie, `D`=uninterruptible sleep, `T`=stopped |
| `%CPU` | CPU usage since last update |
| `%MEM` | Percentage of physical RAM used |
| `TIME+` | Total CPU time used since process started |
| `COMMAND` | Command that started the process |

**Keyboard shortcuts inside top:**

| Key | Action |
|---|---|
| `q` | Quit top |
| `M` | Sort by memory usage |
| `P` | Sort by CPU usage (default) |
| `T` | Sort by running time |
| `k` | Kill a process (prompts for PID) |
| `r` | Renice a process (change priority) |
| `1` | Toggle per-CPU breakdown |
| `h` | Show help |

---

## 2. lsof and fuser

In Linux, **almost everything is treated as a file** — disks, pipes, network sockets, devices. When you get a "Device or Resource Busy" error (e.g. trying to unmount a USB drive), these two tools help you find which process is holding the resource.

### lsof — List Open Files

`lsof` shows a detailed list of all open files and the processes using them.

```bash
lsof                        # List ALL open files (very long output)
lsof .                      # Show processes using the current directory
lsof /home/pete             # Show processes using a specific path
lsof -p 1234                # Show all files opened by process with PID 1234
lsof -u pete                # Show all files opened by user pete
lsof -i                     # Show all network connections (open sockets)
lsof -i :80                 # Show processes using port 80
lsof /dev/sdb1              # Show what's using a specific device (e.g. USB drive)
```

**Sample output:**
```
COMMAND   PID  USER  FD   TYPE  DEVICE SIZE/OFF  NODE NAME
bash      2207 pete  cwd   DIR   8,6    4096      131  .
chrome    6675 patty mem   REG   8,6    100       200  /lib/x86_64/libc.so
```

| Column | Meaning |
|---|---|
| `COMMAND` | Name of the process |
| `PID` | Process ID |
| `USER` | User who owns the process |
| `FD` | File descriptor (cwd=current dir, txt=program text, mem=memory-mapped) |
| `TYPE` | Type: DIR, REG (regular file), CHR (character device), IPv4/IPv6 |
| `NAME` | File or path name |

### fuser — Find Processes Using a File

`fuser` is more direct — quickly identifies (and optionally kills) processes using a specific file or mount point.

```bash
fuser /home/pete            # Show PIDs of processes using /home/pete
fuser /dev/sdb1             # Show what's using a USB drive
fuser -v /dev/sdb1          # Verbose — show more detail
fuser -k /dev/sdb1          # Kill ALL processes using the device
fuser -ki /dev/sdb1         # Kill with confirmation (-i = interactive)
```

> **lsof vs fuser:** `lsof` is better for detailed investigation. `fuser` is faster for quickly finding and killing processes to resolve "Device Busy" errors.

---

## 3. Process Threads

**Threads** are units of execution within a process — often called "lightweight processes."

- Processes have **isolated** system resources (separate memory space)
- Threads within the **same process share** resources (memory, file handles)
- Shared resources make thread communication much faster than inter-process communication
- Every process has **at least one thread**
  - **Single-threaded** — one thread only
  - **Multi-threaded** — more than one thread running concurrently

**Example:** A text editor may run as one process with multiple threads — one thread handles keyboard input, another runs spell-check in the background, another handles auto-save.

**View threads:**
```bash
ps -L -p 1234           # List threads of process 1234 (-L = show threads)
ps -eLf                 # Show all processes with thread info
top -H                  # Show individual threads in top (H = threads mode)
top -H -p 1234          # Show threads of a specific process
```

---

## 4. CPU Monitoring

### uptime — Quick Load Check

```bash
uptime
# Output: 17:23:35 up 1 day, 5:59, 2 users, load average: 0.00, 0.02, 0.05
```

**Load average** — the three numbers show average CPU load over the last **1, 5, and 15 minutes**. It represents the average number of processes in the run queue (running or waiting to run).

**Interpreting load average:**

| Load average vs CPU cores | Meaning |
|---|---|
| Equal to number of cores | CPU is fully utilized — no bottleneck |
| Less than number of cores | System is fine — CPU has spare capacity |
| Greater than number of cores | CPU is overloaded — processes are waiting |

Example: if you have 4 CPU cores and load average is `2.00` — CPUs are at 50% utilization. If load is `4.00` — fully loaded. If `8.00` — overloaded, processes are queuing.

```bash
nproc               # Show number of CPU cores on the system
```

### mpstat — Per-CPU Statistics

```bash
sudo apt install sysstat    # Install if not present
mpstat                      # Show CPU statistics summary
mpstat -P ALL               # Show stats for each CPU core individually
mpstat 1                    # Update every 1 second (live view)
mpstat 1 5                  # Update every 1 second, 5 times then stop
```

---

## 5. I/O Monitoring

### iostat — Disk and CPU I/O Statistics

`iostat` provides a snapshot of **CPU usage and disk I/O activity**.

```bash
sudo apt install sysstat    # Install if not present
iostat                      # Show summary since boot
iostat 2                    # Update every 2 seconds (live)
iostat 2 5                  # Update every 2 seconds, 5 times
iostat -x                   # Extended stats — more detailed disk info
iostat -d                   # Disk stats only (no CPU section)
```

**Sample output:**
```
avg-cpu: %user  %nice  %system  %iowait  %steal  %idle
           0.13   0.03     0.50     0.01    0.00  99.33

Device:   tps   kB_read/s  kB_wrtn/s  kB_read  kB_wrtn
sda      0.17        3.49       1.92   385106   212417
```

**CPU section fields:**

| Field | Meaning |
|---|---|
| `%user` | CPU time spent on user-level processes |
| `%nice` | CPU time on user processes with modified priority |
| `%system` | CPU time spent on kernel (system) code |
| `%iowait` | CPU time waiting for I/O to complete — high value = disk bottleneck |
| `%steal` | CPU time stolen by hypervisor (virtual machines only) |
| `%idle` | CPU time doing nothing |

**Disk section fields:**

| Field | Meaning |
|---|---|
| `tps` | Transfers per second (I/O requests) |
| `kB_read/s` | Kilobytes read from device per second |
| `kB_wrtn/s` | Kilobytes written to device per second |
| `kB_read` | Total kilobytes read |
| `kB_wrtn` | Total kilobytes written |

> A consistently high `%iowait` means your CPU is often waiting for disk — the disk is the bottleneck, not the CPU.

---

## 6. Memory Monitoring

### free — Memory Usage Snapshot

```bash
free                    # Show memory in kilobytes
free -h                 # Human-readable (MB/GB)
free -m                 # Show in megabytes
free -s 2               # Update every 2 seconds
```

**Sample output:**
```
              total    used    free   shared  buff/cache  available
Mem:          7.7Gi   3.2Gi   1.1Gi   312Mi       3.4Gi      4.0Gi
Swap:         2.0Gi      0B   2.0Gi
```

| Column | Meaning |
|---|---|
| `total` | Total installed RAM |
| `used` | RAM currently in use |
| `free` | RAM not used at all |
| `shared` | Memory used by tmpfs (shared memory) |
| `buff/cache` | Memory used for disk buffers and cache |
| `available` | RAM available for new processes (free + reclaimable cache) |

> **Don't panic if `free` is low.** Linux uses spare RAM for disk caching to improve performance. That cached memory is reclaimed instantly when an application needs it. Watch `available` instead — that's the real indicator of free memory.

### vmstat — Virtual Memory Statistics

`vmstat` gives a comprehensive real-time view of processes, memory, swap, I/O, and CPU all in one line.

```bash
vmstat                  # One report averaged since boot
vmstat 2                # Update every 2 seconds (live)
vmstat 2 5              # Update every 2 seconds, 5 times then stop
vmstat -s               # Detailed stats table (not repeating)
vmstat -a               # Show active/inactive memory instead of buff/cache
```

**Sample output:**
```
procs --------memory------- --swap-- ---io-- -system-- ----cpu----
r  b  swpd   free   buff  cache  si  so   bi   bo  in  cs  us sy id wa
1  0     0 401160 100252 1307468  0   0    5   17  49  70   0  0 100  0
```

**All fields decoded:**

*Procs:*

| Field | Meaning |
|---|---|
| `r` | Processes waiting to run (run queue length) |
| `b` | Processes in uninterruptible sleep (blocked on I/O) |

*Memory:*

| Field | Meaning |
|---|---|
| `swpd` | Virtual memory (swap) used |
| `free` | Idle (free) memory |
| `buff` | Memory used as buffers |
| `cache` | Memory used as cache |

*Swap:*

| Field | Meaning |
|---|---|
| `si` | Memory swapped **in** from disk per second |
| `so` | Memory swapped **out** to disk per second |

*I/O:*

| Field | Meaning |
|---|---|
| `bi` | Blocks received from block device (reads) per second |
| `bo` | Blocks sent to block device (writes) per second |

*System:*

| Field | Meaning |
|---|---|
| `in` | Interrupts per second |
| `cs` | Context switches per second |

*CPU (% of total time):*

| Field | Meaning |
|---|---|
| `us` | User-level code |
| `sy` | Kernel code |
| `id` | Idle |
| `wa` | Waiting for I/O |
| `st` | Stolen by hypervisor |

> ⚠️ Watch `si` and `so` — if swap is being used heavily (non-zero `so`), your system is running out of RAM and performance will degrade.

---

## 7. Continuous Monitoring

The tools above are great for checking your system **right now**. But what about problems that happen at 3am when you're not looking? That's where **continuous monitoring** comes in.

### sar — System Activity Reporter

`sar` collects, reports, and saves historical system activity data. It's part of the `sysstat` package.

```bash
sudo apt install sysstat        # Install sysstat
```

After installation, `sysstat` automatically starts collecting data. If it doesn't, enable it:
```bash
sudo nano /etc/default/sysstat
# Change: ENABLED="false"  →  ENABLED="true"
```

**Using sar:**
```bash
sar                     # Show CPU usage report for today
sar -q                  # Show load average and run queue history for today
sar -r                  # Show memory usage history for today
sar -b                  # Show I/O activity history for today
sar -u                  # Show CPU utilization history
sar -n DEV              # Show network activity history
sar 1 5                 # Live report — update every 1 second, 5 times
```

**View a different day's data:**
```bash
sar -f /var/log/sysstat/sa15    # View data from the 15th of the month
# or on some systems:
sar -f /var/log/sa/sa15
```

Historical data is stored in `/var/log/sysstat/` (or `/var/log/sa/`) as files named `saXX` where `XX` is the day of the month.

> `sar` is essential for diagnosing intermittent problems — you can look back in time to find exactly when a spike happened and what caused it.

---

## 8. Cron Jobs

**Cron** is a background service (daemon) that runs scheduled tasks automatically at specified times or intervals. Scheduled tasks are called **cron jobs**.

**Common uses:**
- Run a backup script every night at midnight
- Clear temporary files every Sunday
- Send a system status email every morning
- Rotate log files weekly

### Crontab — Managing Cron Jobs

```bash
crontab -e          # Edit your cron jobs (opens in default editor)
crontab -l          # List your current cron jobs
crontab -r          # Remove ALL your cron jobs (careful!)
sudo crontab -e     # Edit root's cron jobs
```

### Cron Job Syntax

```
* * * * * command_to_run
│ │ │ │ │
│ │ │ │ └── Day of week  (0-7, Sunday=0 or 7)
│ │ │ └──── Month        (1-12)
│ │ └────── Day of month (1-31)
│ └──────── Hour         (0-23)
└────────── Minute       (0-59)
```

`*` (asterisk) = wildcard meaning "every" — every minute, every hour, every day, etc.

**Examples:**

```bash
# Run at 8:30 AM every day
30 08 * * * /home/pete/scripts/change_wallpaper

# Run every day at midnight
0 0 * * * /home/pete/scripts/backup.sh

# Run every Sunday at 2:00 AM
0 2 * * 0 /home/pete/scripts/cleanup.sh

# Run every 15 minutes
*/15 * * * * /home/pete/scripts/check_status.sh

# Run at 6:00 AM on the 1st of every month
0 6 1 * * /home/pete/scripts/monthly_report.sh

# Run every weekday (Mon-Fri) at 9:00 AM
0 9 * * 1-5 /home/pete/scripts/work_task.sh

# Run every hour
0 * * * * /home/pete/scripts/hourly.sh
```

**Special shorthand keywords:**

| Shorthand | Equivalent | Meaning |
|---|---|---|
| `@reboot` | — | Run once at system startup |
| `@hourly` | `0 * * * *` | Run every hour |
| `@daily` | `0 0 * * *` | Run every day at midnight |
| `@weekly` | `0 0 * * 0` | Run every Sunday at midnight |
| `@monthly` | `0 0 1 * *` | Run on 1st of every month |
| `@yearly` | `0 0 1 1 *` | Run on Jan 1st at midnight |

```bash
@reboot /home/pete/scripts/startup.sh
@daily  /home/pete/scripts/backup.sh
```

**Redirect cron output to a log file (recommended):**
```bash
30 08 * * * /home/pete/scripts/task.sh >> /home/pete/cron.log 2>&1
# >> appends stdout to log file
# 2>&1 also redirects stderr to the same log file
```

> By default, cron emails output to the user. Redirect to a file to keep logs instead.

---

## 9. Quick Reference — Process Utilization

**top:**

| Key | Action |
|---|---|
| `q` | Quit |
| `M` | Sort by memory |
| `P` | Sort by CPU |
| `k` | Kill a process |
| `1` | Toggle per-CPU view |

**lsof / fuser:**

```bash
lsof .                      # What's using current directory
lsof -p PID                 # Files opened by a process
lsof -i :80                 # What's using port 80
fuser /dev/sdb1             # What's using a device
fuser -k /dev/sdb1          # Kill processes using a device
```

**CPU / I/O / Memory:**

```bash
uptime                      # Load average (1, 5, 15 min)
nproc                       # Number of CPU cores
mpstat -P ALL               # Per-core CPU stats
iostat                      # Disk I/O + CPU summary
iostat -x                   # Extended disk stats
free -h                     # Memory usage (human-readable)
vmstat 2                    # Live system stats every 2s
vmstat -s                   # Detailed stats table
```

**Threads:**

```bash
ps -L -p PID                # Show threads of a process
top -H                      # Thread view in top
```

**sar:**

```bash
sar                         # Today's CPU history
sar -q                      # Load average history
sar -r                      # Memory history
sar -b                      # I/O history
sar -f /var/log/sysstat/saXX   # View specific day
```

**crontab:**

```bash
crontab -e                  # Edit cron jobs
crontab -l                  # List cron jobs
crontab -r                  # Remove all cron jobs
```

**Cron syntax:**
```
MIN  HOUR  DOM  MON  DOW  command
 30    08    *    *    *   /path/to/script.sh
```
