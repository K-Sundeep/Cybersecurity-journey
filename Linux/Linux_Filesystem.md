# Linux — The Filesystem

---

## 1. Filesystem Hierarchy

Linux organizes all files and directories in a single unified tree starting from the **root directory `/`**. This is called the **Filesystem Hierarchy Standard (FHS)**.

```
/
├── bin       → Essential user binaries (ls, cp, mv, cat...)
├── sbin      → System binaries for admin (fdisk, mkfs...)
├── etc       → System configuration files
├── home      → User home directories (/home/pete, /home/alice...)
├── root      → Home directory for the root user
├── var       → Variable data: logs, mail, spool (/var/log/)
├── tmp       → Temporary files (cleared on reboot)
├── usr       → User programs and data (/usr/bin, /usr/lib...)
├── lib       → Shared libraries used by /bin and /sbin
├── dev       → Device files (hard drives, USB, terminals...)
├── proc      → Virtual filesystem — running processes and kernel info
├── sys       → Virtual filesystem — hardware and kernel info
├── mnt       → Temporary mount points
├── media     → Auto-mounted removable media (USB, CD...)
├── opt       → Optional third-party software
└── boot      → Boot loader files, kernel image
```

**Key principle:** Unlike Windows, Linux has **one tree** — everything attaches to `/`. External drives, network shares, and USB sticks are all "mounted" somewhere in this tree rather than appearing as separate drive letters.

---

## 2. Filesystem Types

Linux supports many different filesystem implementations. The **Virtual File System (VFS)** — an abstraction layer in the kernel — sits between applications and filesystems, providing a single uniform interface so apps work regardless of which filesystem is underneath.

**Common Linux filesystem types:**

| Filesystem | Description |
|---|---|
| **ext4** | Fourth Extended Filesystem. Default for most Linux distros. Reliable, journaled, supports files up to 16TB |
| **xfs** | High-performance journaling filesystem. Default on RHEL/CentOS. Great for large files and high throughput |
| **btrfs** | "Better FS." Modern filesystem with snapshots, checksums, built-in RAID. Still maturing |
| **vfat / FAT32** | Windows-compatible. Used for USB drives and EFI partitions |
| **ntfs** | Windows NT filesystem. Linux can read/write with ntfs-3g driver |
| **tmpfs** | Temporary filesystem stored in RAM. `/tmp` often uses this |
| **proc** | Virtual filesystem exposing process/kernel info at `/proc` |
| **sysfs** | Virtual filesystem exposing hardware info at `/sys` |

**Journaling** — Most modern filesystems (ext4, xfs, btrfs) are **journaled**. Before writing data, the filesystem records the intended changes in a journal (log). If the system loses power mid-write, it can replay or roll back the journal on reboot — preventing corruption. Without journaling, a power cut could corrupt the filesystem and require a full `fsck` scan on a large disk.

**Check filesystem type of mounted devices:**
```bash
df -T                   # Show filesystem type of all mounted filesystems
df -T /home             # Show filesystem type of a specific mount point
lsblk -f                # List block devices with filesystem info
```

---

## 3. Anatomy of a Disk

**Physical structure:**
A hard disk (or SSD) is divided into **partitions** — logical sections that function as independent block devices.

- `/dev/sda` — the entire disk
- `/dev/sda1` — first partition on that disk
- `/dev/sda2` — second partition

**Why partition?**
- Separate data by purpose (OS, home, swap)
- Use different filesystems on different partitions
- Protect one partition from another filling up

**Partition tables — two types:**

| Table | Max partitions | Max disk size | Notes |
|---|---|---|---|
| **MBR** (Master Boot Record) | 4 primary (or 3 primary + extended with logical inside) | 2 TB | Legacy, traditional |
| **GPT** (GUID Partition Table) | 128 primary | 9.4 ZB | Modern standard, required for UEFI |

**MBR partition types:**
- **Primary** — max 4 per disk
- **Extended** — one of the 4 primary slots used to hold logical partitions (workaround for the 4 limit)
- **Logical** — created inside the extended partition; work like regular partitions

**View partition table:**
```bash
sudo parted -l              # View all disks and their partition tables
sudo fdisk -l               # List partition info for all disks
lsblk                       # Tree view of all block devices and partitions
```

Sample `parted -l` output:
```
Model: Seagate (scsi)
Disk /dev/sda: 21.5GB
Partition Table: msdos
Number  Start    End      Size     Type      File system   Flags
 1      1049kB   6860MB   6859MB   primary   ext4          boot
 2      6861MB   21.5GB   14.6GB   extended
 5      6861MB   7380MB   519MB    logical   linux-swap
 6      7381MB   21.5GB   14.1GB   logical   xfs
```

---

## 4. Disk Partitioning

**Tools for partitioning:**

| Tool | Supports | Interface | Notes |
|---|---|---|---|
| `fdisk` | MBR only | Command-line | Classic tool, simple |
| `parted` | MBR + GPT | Command-line | More powerful |
| `gdisk` | GPT only | Command-line | Similar to fdisk but GPT |
| `gparted` | MBR + GPT | Graphical | Easy visual partitioning |

### Using fdisk (interactive)

```bash
sudo fdisk /dev/sdb         # Open fdisk for disk /dev/sdb
```

**Inside fdisk — key commands:**

| Key | Action |
|---|---|
| `p` | Print current partition table |
| `n` | Create a new partition |
| `d` | Delete a partition |
| `t` | Change partition type |
| `w` | Write changes and exit (SAVES changes) |
| `q` | Quit without saving |
| `m` | Show help menu |

> ⚠️ Changes are only written to disk when you press `w`. Press `q` to safely exit without making changes.

### Using parted (direct commands)

```bash
sudo parted /dev/sdb                        # Interactive mode
sudo parted /dev/sdb print                  # View partition table
sudo parted /dev/sdb mklabel gpt            # Create GPT partition table
sudo parted /dev/sdb mkpart primary ext4 1MiB 5GiB   # Create a partition
sudo parted /dev/sdb rm 1                   # Delete partition 1
```

---

## 5. Creating Filesystems

After partitioning, a partition is just raw space. You need to **create a filesystem** on it before you can store files. This process is also called **formatting**.

**`mkfs` — Make Filesystem**

```bash
sudo mkfs -t ext4 /dev/sdb1             # Format partition as ext4
sudo mkfs -t xfs /dev/sdb2              # Format partition as xfs
sudo mkfs -t vfat /dev/sdb3             # Format as FAT32

# Shorthand aliases (same result):
sudo mkfs.ext4 /dev/sdb1
sudo mkfs.xfs /dev/sdb2
sudo mkfs.vfat /dev/sdb3
```

> ⚠️ `mkfs` **destroys all existing data** on the partition. Make absolutely sure you're pointing at the right device before running it.

**Check UUID of a partition after formatting:**
```bash
sudo blkid                  # Show UUID and filesystem type of all partitions
sudo blkid /dev/sdb1        # Show info for a specific partition
```

Sample output:
```
/dev/sda1: UUID="130b882f-7d79-436d-a096-1e594c92bb76" TYPE="ext4"
/dev/sda5: UUID="22c3d34b-467e-467c-b44d-f03803c2c526" TYPE="swap"
/dev/sda6: UUID="78d203a0-7c18-49bd-9e07-54f44cdb5726" TYPE="xfs"
```

UUIDs are permanent unique identifiers — more reliable than device names (`/dev/sda1` can change if you add/remove drives).

---

## 6. mount and umount

Before you can access files on a storage device, you must **mount** its filesystem to a directory (called a **mount point**) in the Linux tree.

```bash
# Create a mount point directory
sudo mkdir /mydrive

# Mount a device
sudo mount /dev/sdb2 /mydrive                   # Auto-detect filesystem type
sudo mount -t ext4 /dev/sdb2 /mydrive           # Specify filesystem type
sudo mount UUID=130b882f-... /mydrive           # Mount by UUID (more reliable)

# View currently mounted filesystems
mount                                           # Show all mounts
df -h                                           # Show mounts with disk usage

# Unmount
sudo umount /mydrive                            # Unmount by mount point
sudo umount /dev/sdb2                           # Unmount by device name
```

> ⚠️ You cannot unmount a filesystem that is currently in use. Make sure no terminal is `cd`'d into it and no files are open. Use `lsof /mydrive` to find what's using it.

**Mount is temporary** — it only persists until reboot. To auto-mount at startup, add an entry to `/etc/fstab`.

---

## 7. /etc/fstab

`/etc/fstab` (filesystem table) is a configuration file that tells Linux **which filesystems to mount automatically at boot** and where to mount them.

```bash
cat /etc/fstab              # View current fstab
```

**Sample `/etc/fstab`:**
```
UUID=130b882f-7d79-436d-a096-1e594c92bb76  /       ext4   relatime,errors=remount-ro  0  1
UUID=78d203a0-7c18-49bd-9e07-54f44cdb5726  /home   xfs    relatime                    0  2
UUID=22c3d34b-467e-467c-b44d-f03803c2c526  none    swap   sw                          0  0
```

**6-field format:**

| Field | Example | Meaning |
|---|---|---|
| Device | `UUID=130b882f...` | What to mount — UUID (recommended) or `/dev/sdXn` |
| Mount point | `/home` | Where to mount it in the filesystem tree |
| Filesystem type | `ext4` | Type of filesystem |
| Options | `relatime,errors=remount-ro` | Mount options (see below) |
| Dump | `0` | Whether to include in `dump` backups (0=no, 1=yes) |
| Pass (fsck order) | `1` | Order for `fsck` checks at boot (0=skip, 1=root first, 2=others) |

**Common mount options:**

| Option | Meaning |
|---|---|
| `defaults` | Use default options (rw, suid, exec, auto, nouser, async) |
| `ro` | Mount read-only |
| `rw` | Mount read-write |
| `noexec` | Prevent execution of binaries on this filesystem |
| `noatime` | Don't update access timestamps (performance boost) |
| `relatime` | Update atime only if newer than mtime (compromise) |
| `errors=remount-ro` | On error, remount as read-only instead of crashing |
| `sw` | Used for swap partitions |

**Test fstab without rebooting:**
```bash
sudo mount -a               # Mount everything in fstab that isn't already mounted
```

> ⚠️ A syntax error in `/etc/fstab` can prevent your system from booting. Always test with `sudo mount -a` after editing. Use `sudo nano /etc/fstab` to edit it.

---

## 8. swap

**Swap** is a dedicated area of disk used as **virtual memory**. When the system runs low on RAM, it moves idle processes' memory pages to swap, freeing up RAM for active processes.

**Two types of swap:**
- **Swap partition** — a dedicated disk partition for swap
- **Swap file** — a regular file on an existing filesystem used as swap (more flexible)

**Rule of thumb for swap size:**
- With less than 2GB RAM — use 2× RAM
- With 2–8GB RAM — equal to RAM
- With more than 8GB RAM — at least 4GB (modern systems rarely need more)

### Setting up a swap partition

```bash
sudo mkswap /dev/sdb2           # Initialize the partition as swap space
sudo swapon /dev/sdb2           # Activate the swap partition
sudo swapoff /dev/sdb2          # Deactivate swap
swapon -s                       # Show all active swap spaces
free -h                         # View swap usage under the "Swap" line
```

**Make swap persistent — add to `/etc/fstab`:**
```
UUID=22c3d34b-467e-467c-b44d-f03803c2c526   none   swap   sw   0   0
```

### Creating a swap file (alternative)

```bash
sudo fallocate -l 2G /swapfile          # Create a 2GB file
sudo chmod 600 /swapfile               # Restrict permissions (security)
sudo mkswap /swapfile                  # Set up as swap
sudo swapon /swapfile                  # Activate it
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab  # Make persistent
```

---

## 9. Disk Usage

### df — Disk Free (filesystem-level view)

`df` reports disk space used and available on all **mounted filesystems**.

```bash
df                      # Show all filesystems in kilobytes
df -h                   # Human-readable (MB, GB)
df -T                   # Include filesystem type
df -i                   # Show inode usage instead of block usage
df -h /home             # Show only the filesystem containing /home
```

**Sample output:**
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       6.2G  2.3G  3.6G  40% /
/dev/sda6        14G  460M   13G   4% /home
```

### du — Disk Usage (directory/file level)

`du` shows how much space **files and directories** are using. Used to find what's consuming space.

```bash
du                              # Show disk usage of all subdirs in current dir
du -h                           # Human-readable
du -h /home/pete                # Show usage for a specific directory
du -sh /home/pete               # Summary only — one line total (-s)
du -sh *                        # Usage of each item in current directory
du -h --max-depth=1 /home       # Show one level deep only
du -h | sort -h | tail -20      # Find top 20 largest items
```

> **df vs du:** `df` shows filesystem-level free/used space. `du` drills into directories to find which files are consuming space. Use `df` first to spot the problem, then `du` to find the cause.

---

## 10. Filesystem Repair

Unexpected shutdowns or power failures can leave a filesystem in an **inconsistent state** — partially written data, corrupted metadata. This is where `fsck` comes in.

**`fsck` (filesystem check)** — checks and repairs filesystem consistency.

```bash
sudo fsck /dev/sda1             # Check and repair
sudo fsck -n /dev/sda1          # Dry run — check only, make NO repairs
sudo fsck -y /dev/sda1          # Auto-answer yes to all repair questions
sudo fsck -t ext4 /dev/sda1     # Specify filesystem type
```

> ⚠️ **CRITICAL:** Never run `fsck` on a **mounted** filesystem — it can cause data corruption. The filesystem must be **unmounted** first. For the root filesystem (`/`), boot from a live CD/rescue disk or let `fsck` run automatically at boot.

**When `fsck` runs automatically:**
- Linux checks the filesystem at boot if it detects it wasn't cleanly unmounted
- After a certain number of mounts or time interval (configurable with `tune2fs`)
- If the dirty bit is set (indicates unclean unmount)

**Checking if filesystem needs repair:**
```bash
sudo tune2fs -l /dev/sda1 | grep "Mount count"
sudo tune2fs -l /dev/sda1 | grep "Last checked"
```

---

## 11. Inodes

The filesystem is made of two things: **data blocks** (the actual file contents) and the **inode table** (a database describing every file).

An **inode** (index node) is an entry in the inode table. Every file and directory has exactly one inode. The inode stores **everything about the file except its name and actual data:**

| What's stored in an inode |
|---|
| File type (regular file, directory, symlink...) |
| Owner (UID) and Group (GID) |
| Access permissions (rwxrwxrwx) |
| Timestamps: `atime` (last access), `mtime` (last modified), `ctime` (last attribute change) |
| File size |
| Number of hard links pointing to this inode |
| Number of disk blocks allocated |
| Pointers to the actual data blocks on disk |

**What is NOT in an inode:**
- The filename (stored in the directory that contains the file)
- The actual file data (stored in data blocks)

**View inode number:**
```bash
ls -li                          # -i flag shows inode number at the start of each line
ls -li /home/pete
# 140 drwxr-xr-x 2 pete pete 6 Jan 20 Desktop
# ↑ inode number
```

**View detailed inode info:**
```bash
stat filename                   # Show all inode metadata for a file
stat /home/pete/Desktop/
```

**Check inode usage on filesystem:**
```bash
df -i                           # Show inode total, used, free for each filesystem
```

> You can run out of inodes even if you have free disk space — this happens when you have millions of tiny files. If you see "No space left on device" but `df -h` shows free space, check `df -i`.

**How inodes point to data:**
Each inode contains 15 pointers:
- Pointers 1–12: **Direct** — point straight to data blocks
- Pointer 13: **Indirect** — points to a block containing more pointers
- Pointer 14: **Double indirect** — points to a block of blocks of pointers
- Pointer 15: **Triple indirect** — one more level deep

This structure lets inodes stay a fixed small size while supporting files of any size.

---

## 12. symlinks

**Links** in Linux let multiple filenames point to the same file data. There are two types: **hard links** and **symbolic (soft) links**.

### Hard Links

A hard link creates **another directory entry pointing to the same inode** — the same underlying data. Both names are completely equal; neither is the "original."

```bash
ln target.txt hardlink.txt      # Create a hard link (no -s flag)
```

**Properties:**
- Shares the **same inode number** as the original
- Deleting the original does NOT remove the data — data survives until ALL hard links are deleted
- **Cannot** span across different filesystems/partitions
- **Cannot** link to directories (in most cases)

### Symbolic Links (Symlinks / Soft Links)

A symbolic link is a **special file that stores the path** to another file or directory. It's like a shortcut — the OS follows the symlink to reach the real file.

```bash
ln -s /path/to/target linkname          # Create a symlink
ln -s /home/pete/Documents ~/docs       # Symlink to a directory
ln -sf /new/target existinglink         # Force overwrite existing link
```

**View symlinks:**
```bash
ls -l                       # Symlinks shown as: linkname -> target
ls -la                      # Include hidden symlinks
readlink linkname           # Show what the symlink points to
readlink -f linkname        # Resolve the full absolute path (follow chain)
```

**Remove a symlink:**
```bash
rm linkname                 # Remove the symlink (NOT the target)
unlink linkname             # Same as rm for symlinks
```

> ⚠️ Don't use `rm -r linkname/` with a trailing slash on a directory symlink — it may delete the contents of the target directory instead of just the link.

**Hard link vs Symbolic link — comparison:**

| | Hard Link | Symbolic Link |
|---|---|---|
| Inode | Same inode as original | Has its own separate inode |
| If original deleted | Data still accessible via hard link | Link breaks (dangling symlink) |
| Cross filesystem | ✗ No | ✓ Yes |
| Link to directory | ✗ Usually not | ✓ Yes |
| Visible as link in ls | No (looks like regular file) | Yes (`->` shown) |
| Created with | `ln target link` | `ln -s target link` |

**Common uses for symlinks:**
- `/usr/bin/python` → `/usr/bin/python3.11` (version management)
- Config files shared between locations
- Shortcuts to deeply nested directories
- Linking libraries to the version expected by a program

---

## 13. Quick Reference — The Filesystem

**Disk inspection:**
```bash
lsblk                           # Block devices tree view
lsblk -f                        # Include filesystem types and UUIDs
sudo fdisk -l                   # List all partition tables
sudo parted -l                  # List all disks and partitions
sudo blkid                      # Show UUID and type of all partitions
df -h                           # Disk usage of mounted filesystems
df -T                           # Include filesystem type
df -i                           # Inode usage
```

**Partitioning:**
```bash
sudo fdisk /dev/sdb             # Interactive MBR partitioning
sudo parted /dev/sdb            # Interactive MBR/GPT partitioning
```

**Formatting:**
```bash
sudo mkfs.ext4 /dev/sdb1        # Format as ext4
sudo mkfs.xfs /dev/sdb2         # Format as xfs
sudo mkswap /dev/sdb3           # Initialize swap partition
```

**Mounting:**
```bash
sudo mount /dev/sdb1 /mnt       # Mount device
sudo mount -t ext4 /dev/sdb1 /mnt  # Mount with type specified
sudo mount UUID=xxx /mnt        # Mount by UUID
sudo umount /mnt                # Unmount
sudo mount -a                   # Mount everything in fstab
```

**Swap:**
```bash
sudo swapon /dev/sdb2           # Activate swap
sudo swapoff /dev/sdb2          # Deactivate swap
swapon -s                       # Show active swap
```

**Disk usage:**
```bash
df -h                           # Filesystem-level free/used
du -sh *                        # Size of each item in current dir
du -h --max-depth=1 /home       # One level deep
du -h | sort -h | tail -20      # Top 20 largest items
```

**Filesystem repair:**
```bash
sudo fsck /dev/sda1             # Check and repair (must be unmounted!)
sudo fsck -n /dev/sda1          # Dry run only
```

**Inodes:**
```bash
ls -li                          # Show inode numbers
stat filename                   # Show full inode metadata
df -i                           # Inode usage per filesystem
```

**Symlinks:**
```bash
ln target link                  # Hard link
ln -s target link               # Symbolic link
ls -l                           # View symlinks (shown with ->)
readlink -f link                # Resolve full path
rm linkname                     # Remove symlink (not target)
```
