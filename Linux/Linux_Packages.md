# Linux — Packages

---

## 1. Software Distribution

A Linux **package** is a compressed archive that contains all the files needed to run a piece of software — the application itself, supporting libraries, configuration files, and metadata. A **package manager** is the tool that handles the installation, updating, and removal process for you automatically.

**What is inside a package?**
- The compiled application binary
- Supporting files (icons, documentation, configs)
- Metadata (version, description, author)
- A list of **dependencies** — other packages this one needs to work

**Why not just download a `.zip` from a website?**

| Manual download | Package manager |
|---|---|
| You manage updates yourself | Updates handled automatically |
| No dependency resolution | Dependencies installed automatically |
| No central tracking | Clean install/removal tracking |
| Security risk — unverified source | Packages verified and signed |

**The two major package ecosystems in Linux:**

| Ecosystem | Based on | Package format | Package managers |
|---|---|---|---|
| **Debian-based** | Ubuntu, Debian, Linux Mint | `.deb` | `apt`, `dpkg` |
| **Red Hat-based** | RHEL, Fedora, CentOS | `.rpm` | `yum`, `dnf`, `rpm` |

---

## 2. Package Repositories

A **package repository** is a central storage server that hosts curated, verified collections of software packages. Instead of hunting down individual downloads, your package manager connects to these repositories to find, install, and update software.

Your system comes pre-configured with default repositories for all base packages. You can add third-party repositories to get software not in the defaults.

### Debian/Ubuntu — Sources List

The package manager reads repository locations from:
- `/etc/apt/sources.list` — main file (traditional)
- `/etc/apt/sources.list.d/` — directory for additional sources (cleaner approach, used by default on Ubuntu 22.04+)

**Format of a source entry:**
```
deb http://archive.ubuntu.com/ubuntu jammy main restricted
```
- `deb` — binary packages (use `deb-src` for source packages)
- URL — repository server address
- `jammy` — the distribution codename (Ubuntu 22.04)
- `main restricted` — repository sections/components

**Adding a repository:**
```bash
sudo add-apt-repository ppa:some/ppa       # Add a PPA (Personal Package Archive)
sudo apt update                             # Refresh package list after adding repo
```

**After editing sources, always update:**
```bash
sudo apt update         # Fetch updated package lists from all repos
```

### Red Hat/Fedora — repo files

Repository configs are stored in `/etc/yum.repos.d/` as `.repo` files.

```bash
sudo yum repolist               # List all enabled repositories
sudo dnf repolist               # Same for newer Fedora/RHEL (dnf replaces yum)
```

---

## 3. tar and gzip

Before installing from repositories was standard, software was distributed as compressed archives. You still encounter these regularly — especially when downloading source code or tools not in repos.

**Key distinction:**

| Tool | Purpose |
|---|---|
| `tar` | **Archiving** — combines multiple files/dirs into one single file |
| `gzip` | **Compression** — reduces the size of a file |

They are often **used together**: `tar` bundles, `gzip` compresses the bundle → resulting in a `.tar.gz` (also called a "tarball").

### gzip — Compress/Decompress Files

```bash
gzip file.txt               # Compress — replaces file.txt with file.txt.gz
gzip -d file.txt.gz         # Decompress — restores file.txt (removes .gz)
gunzip file.txt.gz          # Same as gzip -d
gzip -k file.txt            # Compress but KEEP the original file
gzip -l file.txt.gz         # List compression info (ratio, sizes)
```

> `gzip` replaces the original file by default. Use `-k` to keep the original.

### tar — Archive Files

```bash
# Create archives
tar -cvf archive.tar mydir/             # Create archive from directory
tar -czvf archive.tar.gz mydir/         # Create AND compress with gzip
tar -cjvf archive.tar.bz2 mydir/        # Create AND compress with bzip2

# Extract archives
tar -xvf archive.tar                    # Extract a .tar archive
tar -xzvf archive.tar.gz               # Extract a .tar.gz archive
tar -xjvf archive.tar.bz2              # Extract a .tar.bz2 archive
tar -xvf archive.tar -C /target/dir/   # Extract to a specific directory

# Inspect without extracting
tar -tvf archive.tar                    # List contents of archive
tar -tzvf archive.tar.gz               # List contents of .tar.gz
```

**tar flags:**

| Flag | Meaning |
|---|---|
| `c` | Create a new archive |
| `x` | Extract files from archive |
| `t` | List (table of) contents |
| `v` | Verbose — show filenames as processed |
| `f` | Specifies the filename (always needed, must come last) |
| `z` | Filter through gzip (`.tar.gz` / `.tgz`) |
| `j` | Filter through bzip2 (`.tar.bz2`) |
| `J` | Filter through xz (`.tar.xz`) |
| `C` | Extract to a specific directory |

**Other compression formats:**

| Format | Extension | Flag |
|---|---|---|
| gzip | `.tar.gz` or `.tgz` | `z` |
| bzip2 | `.tar.bz2` | `j` |
| xz | `.tar.xz` | `J` |
| zip | `.zip` | use `zip`/`unzip` separately |

```bash
zip archive.zip file1 file2 dir/        # Create zip archive
zip -r archive.zip dir/                 # Zip directory recursively
unzip archive.zip                       # Extract zip
unzip -l archive.zip                    # List zip contents
```

---

## 4. Package Dependencies

Packages almost never work alone. They rely on **dependencies** — other packages or shared libraries they need to function.

**Shared libraries** are collections of pre-compiled code that multiple programs can use simultaneously. Instead of every program shipping its own copy of common code, they all share one. Think of it like restaurants all sourcing ingredients from the same central farm.

**Dependency chain example:**
```
Firefox → requires → libgtk, libssl, libcairo...
libssl  → requires → libcrypto...
```

**Library naming conventions:**

| Type | Description | Example |
|---|---|---|
| Shared library | Used at runtime, shared by multiple programs | `libssl.so.1.1` |
| Static library | Compiled into the program at build time | `libssl.a` |

**Where shared libraries live:**
```bash
/lib/                   # Essential system libraries
/usr/lib/               # Most shared libraries
/usr/local/lib/         # Locally installed libraries
```

**Finding library dependencies of a program:**
```bash
ldd /usr/bin/firefox        # List shared libraries used by firefox
ldd /bin/ls                 # List libraries used by ls
```

**The dependency problem with direct packages (rpm/dpkg):**
If you manually install a `.deb` or `.rpm` file, you are responsible for finding and installing every dependency yourself — and their dependencies, recursively. This is why full package managers (apt, yum) exist: they resolve and install the entire dependency tree automatically.

---

## 5. rpm and dpkg

These are the **low-level** package management tools — they install individual `.rpm` or `.deb` files directly. Unlike `apt` and `yum`, they do **NOT** automatically resolve or install dependencies.

### dpkg — Debian Package Manager

```bash
# Install
sudo dpkg -i package.deb            # Install a .deb package file

# Remove
sudo dpkg -r package_name           # Remove package (keep config files)
sudo dpkg -P package_name           # Purge — remove package AND config files

# Query / inspect
dpkg -l                             # List all installed packages
dpkg -l | grep firefox              # Search installed packages
dpkg -s package_name                # Show package status and info
dpkg -L package_name                # List all files installed by a package
dpkg -S /path/to/file               # Find which package owns a file
dpkg --get-selections               # List all installed packages (alternative)
```

### rpm — Red Hat Package Manager

```bash
# Install / Update / Remove
sudo rpm -i package.rpm             # Install a .rpm package
sudo rpm -U package.rpm             # Upgrade (install or update)
sudo rpm -e package_name            # Remove (erase) a package

# Query
rpm -qa                             # List all installed packages
rpm -qa | grep firefox              # Search installed packages
rpm -qi package_name                # Show detailed package info
rpm -ql package_name                # List files installed by a package
rpm -qf /path/to/file               # Find which package owns a file
rpm -qR package_name                # List dependencies of a package

# Verify
rpm -V package_name                 # Verify package integrity
```

> **dpkg vs rpm — when to use them:**
> Use `dpkg`/`rpm` only when you have a direct `.deb`/`.rpm` file to install (e.g. downloaded from a vendor's website like VS Code, Chrome, Slack). For everything else, use `apt` or `yum` which handle dependencies automatically.

---

## 6. yum and apt

These are the **full package management systems** — they connect to repositories, resolve dependencies, and handle everything automatically. Use these for day-to-day package management.

### apt — Advanced Package Tool (Debian/Ubuntu)

```bash
# Update package lists (always do this before installing)
sudo apt update                         # Refresh index from all repos

# Install
sudo apt install firefox                # Install a package
sudo apt install firefox -y             # Install without confirmation prompt
sudo apt install package1 package2      # Install multiple packages at once

# Remove
sudo apt remove firefox                 # Remove package (keep config files)
sudo apt purge firefox                  # Remove package AND config files
sudo apt autoremove                     # Remove unused dependency packages

# Upgrade
sudo apt upgrade                        # Upgrade all installed packages
sudo apt full-upgrade                   # Upgrade + remove/install as needed

# Search and info
apt search firefox                      # Search for packages
apt show firefox                        # Show detailed package info
apt list --installed                    # List all installed packages
apt list --upgradable                   # List packages with available updates

# Clean up
sudo apt clean                          # Delete downloaded package files
sudo apt autoclean                      # Delete old package files only
```

> `apt update` only refreshes the list of available packages — it does **not** install or upgrade anything. Always run it before installing to get the latest package versions.

### yum — Yellowdog Updater Modified (Red Hat/CentOS)

`yum` is being replaced by `dnf` on modern Fedora/RHEL systems, but commands are nearly identical.

```bash
# Install
sudo yum install firefox                # Install a package
sudo yum install firefox -y             # Install without prompt

# Remove
sudo yum remove firefox                 # Remove a package

# Update
sudo yum update                         # Update all packages
sudo yum update firefox                 # Update a specific package

# Search and info
yum search firefox                      # Search available packages
yum info firefox                        # Detailed package info
yum list installed                      # List all installed packages
yum list available                      # List all available packages

# Groups
yum grouplist                           # List package groups
sudo yum groupinstall "Development Tools"  # Install a group of packages
```

**apt vs yum — side by side:**

| Task | apt (Debian/Ubuntu) | yum (Red Hat/CentOS) |
|---|---|---|
| Update package index | `apt update` | `yum check-update` |
| Install package | `apt install pkg` | `yum install pkg` |
| Remove package | `apt remove pkg` | `yum remove pkg` |
| Search | `apt search pkg` | `yum search pkg` |
| Show info | `apt show pkg` | `yum info pkg` |
| Upgrade all | `apt upgrade` | `yum update` |
| List installed | `apt list --installed` | `yum list installed` |

---

## 7. Compile Source Code

Sometimes a package you need **isn't available** in any repository — only the raw source code is available. In that case you need to compile it yourself.

**Step 1 — Install build tools:**
```bash
# Debian/Ubuntu:
sudo apt install build-essential        # Installs GCC compiler, make, and essentials

# Red Hat/CentOS:
sudo yum groupinstall "Development Tools"
```

**Step 2 — Download and extract the source:**
```bash
tar -xzvf package.tar.gz               # Extract the tarball
cd package_directory/                   # Enter the extracted directory
```

**Step 3 — Read the README/INSTALL file:**
```bash
cat README                              # Always read this first!
cat INSTALL                             # May have specific instructions or requirements
```

**Step 4 — Configure:**
```bash
./configure                             # Check system for dependencies and set up build
```
The `configure` script scans your system for required libraries and tools. If it reports missing dependencies, install them before continuing. The `./` prefix means "run this script from the current directory."

**Step 5 — Compile:**
```bash
make                                    # Compile the source code into binaries
```
This can take a while depending on the size of the software. `make` reads the `Makefile` generated by `configure` and builds everything.

**Step 6 — Install:**
```bash
# Option A — checkinstall (RECOMMENDED):
sudo apt install checkinstall           # Install checkinstall first
sudo checkinstall                       # Installs AND creates a .deb package for easy removal

# Option B — make install (less recommended):
sudo make install                       # Copies files to /usr/local/
```

> **Always prefer `checkinstall` over `make install`.** `checkinstall` integrates the compiled software into your package manager so you can remove it cleanly later with `apt remove`. With `make install`, removing is unreliable — you'd have to `sudo make uninstall` from the source directory, which doesn't always work.

**Full workflow summary:**
```bash
sudo apt install build-essential
tar -xzvf package.tar.gz
cd package_directory/
./configure
make
sudo checkinstall
```

---

## 8. Quick Reference — Packages

**tar and gzip:**

```bash
tar -czvf archive.tar.gz dir/      # Create compressed archive
tar -xzvf archive.tar.gz           # Extract compressed archive
tar -tzvf archive.tar.gz           # List contents
gzip file.txt                      # Compress file
gzip -d file.txt.gz                # Decompress file
```

**dpkg (Debian .deb files):**

```bash
sudo dpkg -i package.deb           # Install
sudo dpkg -r package_name          # Remove
dpkg -l                            # List installed
dpkg -L package_name               # List files from package
dpkg -S /path/to/file              # Find which package owns a file
```

**rpm (Red Hat .rpm files):**

```bash
sudo rpm -i package.rpm            # Install
sudo rpm -e package_name           # Remove
rpm -qa                            # List all installed
rpm -ql package_name               # List files from package
rpm -qR package_name               # List dependencies
```

**apt (Debian/Ubuntu):**

```bash
sudo apt update                    # Refresh package index
sudo apt install package           # Install
sudo apt remove package            # Remove
sudo apt purge package             # Remove + config files
sudo apt upgrade                   # Upgrade all
sudo apt autoremove                # Remove unused deps
apt search keyword                 # Search
apt show package                   # Show info
```

**yum (Red Hat/CentOS):**

```bash
sudo yum install package           # Install
sudo yum remove package            # Remove
sudo yum update                    # Update all
yum search keyword                 # Search
yum info package                   # Show info
yum list installed                 # List installed
```

**Compile from source:**

```bash
sudo apt install build-essential   # Install build tools
tar -xzvf package.tar.gz           # Extract source
cd package_dir/
./configure                        # Check dependencies
make                               # Compile
sudo checkinstall                  # Install via package manager
```
