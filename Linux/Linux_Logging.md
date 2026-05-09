# Linux — Logging

---

## 1. System Logging

The services, kernel, and daemons on your system are constantly active. This activity is recorded in files called **logs** — a human-readable journal of all important system events. Logs are essential for monitoring system health, troubleshooting problems, and auditing security.

**How logs get collected:**
A core service called **syslog** is responsible for gathering log messages from all over the system and routing them to the right files. On most modern Linux distributions, this service is implemented by **rsyslog** (an advanced, improved version of the original syslog daemon).

```bash
# Check if rsyslog is running
systemctl status rsyslog
```

**Log storage location:** Logs are stored in `/var/log/` — the designated directory for variable data like logs.

**Standard log entry format:**
```
Jan 27 07:41:32 icebox anacron[4650]: Job `cron.weekly' started
```

| Part | Example | Meaning |
|---|---|---|
| Timestamp | `Jan 27 07:41:32` | When the event occurred |
| Hostname | `icebox` | Machine where it happened |
| Process | `anacron[4650]` | Program name and PID |
| Message | `Job 'cron.weekly' started` | What actually happened |

---

## 2. syslog

The **syslog** service (running as `rsyslogd`) manages and routes log messages to the system logger. It reads its configuration from `/etc/rsyslog.conf` and from additional files in `/etc/rsyslog.d/`.

**View the rsyslog config:**
```bash
less /etc/rsyslog.d/50-default.conf
```

**Sample config — selector rules:**
```
auth,authpriv.*              /var/log/auth.log
*.*;auth,authpriv.none      -/var/log/syslog
kern.*                      -/var/log/kern.log
mail.*                       /var/log/mail.log
```

Each rule has two parts: **selector** (left) and **action** (right).

**Selector format:** `facility.severity`

**Facilities** — the source/category of the message:

| Facility | Source |
|---|---|
| `auth` / `authpriv` | Authentication and security |
| `kern` | Kernel messages |
| `mail` | Mail system |
| `cron` | Cron daemon |
| `daemon` | System daemons |
| `user` | User-level messages |
| `*` | All facilities |

**Severity levels** — from most to least severe:

| Level | Meaning |
|---|---|
| `emerg` | System is unusable |
| `alert` | Immediate action required |
| `crit` | Critical conditions |
| `err` | Error conditions |
| `warn` | Warning conditions |
| `notice` | Normal but significant events |
| `info` | Informational messages |
| `debug` | Debug-level messages |
| `*` | All severity levels |
| `none` | Exclude this facility |

**Actions** — where to send the log:
- `/var/log/syslog` — write to a file
- `-/var/log/syslog` — write to file (buffered, `-` means async)
- `@192.168.1.10` — forward to a remote syslog server (UDP)
- `@@192.168.1.10` — forward via TCP

**Manually send a test log message:**
```bash
logger "Hello this is a test log message"
logger -t "MyApp" "Application started successfully"
# -t sets a tag/identifier for the message
```
Then check `/var/log/syslog` — you'll see your message appear.

---

## 3. General Logging

The two most commonly checked general log files:

**`/var/log/messages`** — Contains all non-critical, non-debug messages. Includes boot messages (`dmesg`), auth, cron, daemon events, and more. First place to check for a general system overview.

**`/var/log/syslog`** — Everything except auth messages. Extremely useful for debugging errors on your machine.

```bash
# View general logs
sudo less /var/log/syslog
sudo tail -f /var/log/syslog        # Live view — watch in real time
sudo tail -n 50 /var/log/syslog     # Last 50 lines
sudo grep "error" /var/log/syslog   # Search for errors
sudo grep "$(date '+%b %e')" /var/log/syslog   # Today's entries only
```

**Other specific log files in `/var/log/`:**

| Log file | Contents |
|---|---|
| `/var/log/syslog` | General system messages (except auth) |
| `/var/log/messages` | General messages including boot info |
| `/var/log/auth.log` | Authentication events (logins, sudo, SSH) |
| `/var/log/kern.log` | Kernel messages |
| `/var/log/dmesg` | Kernel boot messages (cleared on reboot) |
| `/var/log/apt/history.log` | Package install/remove history |
| `/var/log/dpkg.log` | All dpkg operations |
| `/var/log/cron.log` | Cron job execution logs |
| `/var/log/mail.log` | Mail server activity |
| `/var/log/boot.log` | System boot messages |
| `/var/log/faillog` | Failed login attempts |
| `/var/log/wtmp` | Login/logout history (binary — use `last`) |
| `/var/log/btmp` | Failed login attempts (binary — use `lastb`) |
| `/var/log/nginx/` | Nginx web server logs |
| `/var/log/apache2/` | Apache web server logs |
| `/var/log/mysql/` | MySQL database logs |

> Many applications that don't use rsyslog manage their own log files in subdirectories of `/var/log/`. Always check the relevant subdirectory if you're troubleshooting a specific application.

---

## 4. Kernel Logging

The Linux kernel generates its own messages about hardware status, driver loading, and kernel operations. These messages are critical for diagnosing hardware issues and problems during system startup.

**The kernel ring buffer** — during boot, the kernel stores its messages in a circular memory buffer. These messages are available via:

```bash
dmesg                           # Display all kernel ring buffer messages
dmesg | less                    # View page by page
dmesg | grep -i error           # Filter for errors
dmesg | grep -i usb             # Filter for USB-related messages
dmesg | grep -i "eth\|network"  # Network-related kernel messages
dmesg -T                        # Show human-readable timestamps
dmesg --level=err,warn          # Show only errors and warnings
dmesg -w                        # Follow mode — watch for new kernel messages live
```

> `dmesg` is the **first place to check** when you have a hardware issue, a driver problem, or something went wrong during boot. If your USB device isn't being recognised, `dmesg` will show you why.

**Persistent kernel log file:**
```bash
sudo less /var/log/kern.log     # Kernel messages saved by rsyslog
sudo less /var/log/dmesg        # Snapshot from last boot (cleared on reboot)
```

**Sample dmesg output:**
```
[    0.000000] Linux version 5.15.0-91-generic
[    0.123456] ACPI: BIOS _OSI(Linux) query ignored
[    2.345678] usb 1-1.2: new full-speed USB device number 3 using xhci_hcd
[    2.567890] usb 1-1.2: New USB device found, idVendor=046d, idProduct=c52b
```

The number in brackets is the **timestamp in seconds since boot**.

---

## 5. Authentication Logging

Authentication logging records all **authorization-related events** — user logins, logout, sudo usage, SSH connections, failed login attempts, and authentication method triggers.

**Primary authentication log file:**
```bash
sudo less /var/log/auth.log         # Debian/Ubuntu
sudo less /var/log/secure           # Red Hat/CentOS/Fedora
```

**Sample `auth.log` entry:**
```
Jan 31 10:37:50 icebox pkexec: pam_unix(polkit-1:session): session opened for user root by (uid=1000)
```

Decoded:
- `Jan 31 10:37:50` — timestamp
- `icebox` — hostname
- `pkexec` — the program that triggered authentication
- `pam_unix(polkit-1:session)` — PAM module used
- `session opened for user root by (uid=1000)` — what happened

**Common things to look for in auth.log:**

```bash
# Check for failed login attempts
sudo grep "Failed password" /var/log/auth.log

# Check for successful logins
sudo grep "Accepted password" /var/log/auth.log
sudo grep "Accepted publickey" /var/log/auth.log

# Check for sudo usage
sudo grep "sudo" /var/log/auth.log

# Check for invalid users (potential intrusion attempts)
sudo grep "Invalid user" /var/log/auth.log

# See login/logout history
last                    # Login history from /var/log/wtmp
last -n 10              # Last 10 logins
lastb                   # Failed login attempts from /var/log/btmp (needs sudo)
who                     # Currently logged in users
w                       # Logged in users and what they're doing
```

> Regularly reviewing `auth.log` is a key part of **Linux security monitoring**. A flood of "Failed password" entries from an unknown IP is a sign of a brute-force attack.

---

## 6. Managing Log Files

Log files grow continuously. If left unmanaged, they can fill up a partition and cause system instability or application failures. The solution is **log rotation**.

### logrotate

`logrotate` is the standard Linux utility for automatically rotating, compressing, and archiving log files. It is run as a **daily cron job** automatically.

**Configuration files:**
- `/etc/logrotate.conf` — global default settings
- `/etc/logrotate.d/` — per-application overrides (one file per application)

**View default config:**
```bash
cat /etc/logrotate.conf
```

**Sample `/etc/logrotate.conf`:**
```
weekly              # Rotate logs weekly by default
rotate 4            # Keep 4 weeks of backups
create              # Create new empty log file after rotation
compress            # Compress rotated files
include /etc/logrotate.d    # Include all app-specific configs
```

**Sample `/etc/logrotate.d/rsyslog`:**
```
/var/log/syslog {
    rotate 7
    daily
    missingok
    notifempty
    delaycompress
    compress
    postrotate
        reload rsyslog >/dev/null 2>&1 || true
    endscript
}
```

### logrotate directives

**Rotation schedule:**

| Directive | Meaning |
|---|---|
| `daily` | Rotate every day |
| `weekly` | Rotate every week |
| `monthly` | Rotate on first day of month |
| `yearly` | Rotate once a year |
| `size 100M` | Rotate when file exceeds 100MB |

**Retention:**

| Directive | Meaning |
|---|---|
| `rotate 7` | Keep 7 rotated copies before deleting oldest |
| `rotate 4` | Keep 4 copies |

**Compression:**

| Directive | Meaning |
|---|---|
| `compress` | Compress rotated files with gzip |
| `nocompress` | Don't compress |
| `delaycompress` | Don't compress the most recent rotated file (yesterday's). Useful if the app might still write to it |

**File handling:**

| Directive | Meaning |
|---|---|
| `missingok` | Don't error if log file is missing |
| `notifempty` | Don't rotate if the log file is empty |
| `create` | Create new empty log file after rotation |
| `create 640 root adm` | Create with specific permissions and owner |
| `dateext` | Append date to rotated filenames instead of numbers |

**Scripts:**

| Directive | Meaning |
|---|---|
| `postrotate ... endscript` | Commands to run after rotation (e.g. reload app) |
| `prerotate ... endscript` | Commands to run before rotation |
| `sharedscripts` | Run scripts once for all files in the block (not once per file) |

**Writing a custom logrotate config for your app:**
```bash
sudo nano /etc/logrotate.d/myapp
```

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

**Test your logrotate config without actually rotating:**
```bash
sudo logrotate -d /etc/logrotate.d/myapp    # Dry run — shows what would happen
sudo logrotate -v /etc/logrotate.conf       # Verbose — show what it's doing
sudo logrotate -f /etc/logrotate.conf       # Force rotation now (even if not due)
```

**View rotation state (when files were last rotated):**
```bash
cat /var/lib/logrotate/status
```

---

## 7. Quick Reference — Logging

**Viewing logs:**
```bash
sudo less /var/log/syslog           # General system logs
sudo less /var/log/auth.log         # Authentication logs
sudo less /var/log/kern.log         # Kernel logs
sudo tail -f /var/log/syslog        # Live tail
sudo tail -n 50 /var/log/syslog     # Last 50 lines
sudo grep "error" /var/log/syslog   # Search for errors
dmesg                               # Kernel ring buffer messages
dmesg -T                            # With human-readable timestamps
dmesg | grep -i error               # Filter kernel errors
```

**Login/user activity:**
```bash
last                    # Login history
last -n 10              # Last 10 logins
lastb                   # Failed login attempts
who                     # Currently logged in
w                       # Logged in users + activity
```

**Manual logging:**
```bash
logger "my test message"            # Log to syslog manually
logger -t "MyApp" "message"         # Log with a tag
```

**logrotate:**
```bash
sudo logrotate -d /etc/logrotate.d/myapp    # Dry run
sudo logrotate -v /etc/logrotate.conf       # Verbose
sudo logrotate -f /etc/logrotate.conf       # Force rotate now
cat /var/lib/logrotate/status               # View last rotation times
```

**Key log files:**

| File | Contents |
|---|---|
| `/var/log/syslog` | General system (except auth) |
| `/var/log/messages` | General + boot info |
| `/var/log/auth.log` | Auth, logins, sudo |
| `/var/log/kern.log` | Kernel messages |
| `/var/log/dmesg` | Boot-time kernel messages |
| `/var/log/faillog` | Failed login count |
| `/var/log/wtmp` | Login history (use `last`) |
| `/var/log/btmp` | Failed logins (use `lastb`) |
