# Linux — DNS

---

## 1. What is DNS?

**DNS (Domain Name System)** translates human-readable hostnames like `www.google.com` into machine-readable IP addresses like `192.78.12.4`. This process is called **resolution**.

Without DNS, you'd have to memorize IP addresses for every website you visit. DNS acts like the internet's phone book — you look up a name, it gives you the number (IP).

**Why DNS is distributed:**
DNS is not a single central database. It is a massive, distributed, hierarchical system. Website owners manage their own DNS records. These individual records are distributed across thousands of servers worldwide. This decentralized structure makes the system incredibly resilient and scalable — no single point of failure.

**Name resolution priority on Linux:**
Before querying an external DNS server, Linux checks sources in this order (defined in `/etc/nsswitch.conf`):

```
hosts: files dns myhostname
```

1. **`files`** — `/etc/hosts` (local static mappings, always checked first)
2. **`dns`** — External DNS server (from `/etc/resolv.conf`)
3. **`myhostname`** — Your own hostname

This means entries in `/etc/hosts` always override DNS — useful for development and testing.

---

## 2. DNS Components

### Name Servers

**Name servers** load DNS settings and answer queries from clients. If a name server doesn't know the answer, it redirects the request to another name server.

Two types of name servers:

| Type | Description |
|---|---|
| **Authoritative** | Holds the actual DNS records for a domain. The definitive source — its answer is final |
| **Recursive (Resolver)** | Doesn't hold records itself. Queries other servers on behalf of the client until it finds an authoritative answer. Also caches results |

Most users talk to a **recursive resolver** provided by their ISP (or a public one like `8.8.8.8`). That resolver does the hard work of finding the answer by querying the DNS hierarchy.

### Zone Files

Inside every name server lives **zone files** — how the server stores information about a domain.

A zone file contains multiple **resource records (RRs)**. Each line is one record containing information about a host, name server, mail server, or other resource.

**Resource record format:**
```
Name    TTL    Class    Type    Data
```

| Field | Meaning |
|---|---|
| `Name` | Hostname or domain this record applies to |
| `TTL` | Time-To-Live — how long (seconds) other servers can cache this record |
| `Class` | Always `IN` (Internet) for standard DNS |
| `Type` | Record type (A, AAAA, MX, CNAME, NS, PTR, TXT...) |
| `Data` | The value — IP address for A records, hostname for MX etc. |

### DNS Record Types

| Record | Full name | Purpose |
|---|---|---|
| `A` | Address | Maps hostname → IPv4 address |
| `AAAA` | IPv6 Address | Maps hostname → IPv6 address |
| `CNAME` | Canonical Name | Alias — maps one hostname to another hostname |
| `MX` | Mail Exchanger | Specifies mail server for a domain |
| `NS` | Name Server | Identifies the authoritative name servers for a domain |
| `PTR` | Pointer | Reverse lookup — maps IP address → hostname |
| `TXT` | Text | Free-form text — used for SPF, DKIM, domain verification |
| `SOA` | Start of Authority | First record in zone — defines key zone parameters |
| `SRV` | Service | Specifies location of a service (host + port) |

**Example zone file entries:**
```
google.com.     300   IN   A      172.217.16.142
google.com.     300   IN   AAAA   2607:f8b0:4004:c09::8a
mail.google.com 300   IN   MX     10 smtp.google.com.
smtp.google.com 300   IN   CNAME  mail-smtp.google.com.
```

---

## 3. DNS Process

When you type `catzontheinterwebz.com` into your browser, here's exactly what happens step by step:

### Step-by-step DNS resolution

```
Browser → Local DNS cache → /etc/hosts → Recursive Resolver → DNS Hierarchy
```

**Step 1 — Local cache check:**
Your computer first checks its own DNS cache for a recently resolved answer. If found and not expired → use it immediately.

**Step 2 — /etc/hosts check:**
Your OS checks `/etc/hosts` for a static mapping. If found → use it.

**Step 3 — Recursive Resolver:**
Your computer sends a query to your configured DNS server (usually your ISP's or `8.8.8.8`). This is the **recursive resolver** — it does the work for you.

**Step 4 — Root Servers:**
The recursive resolver doesn't know `catzontheinterwebz.com`, so it queries one of the **13 Root Servers** (mirrored worldwide to hundreds of physical servers). Root servers don't know the domain either, but they know who handles `.com` TLD domains → "Ask the .com TLD server at this IP."

**Step 5 — TLD Name Server:**
The recursive resolver queries the `.com` **TLD (Top-Level Domain) name server**. It doesn't know the specific domain but knows which server is authoritative for `catzontheinterwebz.com` → "Ask that server."

**Step 6 — Authoritative Name Server:**
The recursive resolver queries the **authoritative name server** for `catzontheinterwebz.com`. This server holds the actual DNS records → returns the IP address.

**Step 7 — Response + Caching:**
The recursive resolver returns the IP to your computer. Both the resolver and your computer **cache** the result for the duration of the record's **TTL** to speed up future queries.

**Step 8 — Connection:**
Your browser connects to the returned IP address.

### Visual summary:

```
Your PC
  │
  └─► Local cache (miss) → /etc/hosts (miss)
         │
         └─► Recursive Resolver (your ISP / 8.8.8.8)
                │
                └─► Root Server (13 worldwide)
                       │ "Go ask .com TLD server"
                       └─► .com TLD Server
                              │ "Go ask catzontheinterwebz.com's NS"
                              └─► Authoritative NS for catzontheinterwebz.com
                                     │ "Here's the IP: 72.14.207.99"
                                     └─► Answer cached + returned to your PC
```

### DNS Caching

Caching is what makes DNS practical — without it, every single request would have to traverse this entire chain, creating impossible load on root servers.

- **TTL (Time-To-Live)** — each DNS record has a TTL in seconds. While cached, queries are answered instantly without traversing the hierarchy.
- A short TTL (like 60s) means changes propagate quickly but creates more load.
- A long TTL (like 86400s = 24h) reduces load but means changes take longer to spread worldwide.

---

## 4. /etc/hosts

`/etc/hosts` is a **local static DNS table** — a plain text file mapping hostnames to IP addresses that is always checked **before** querying any external DNS server.

```bash
cat /etc/hosts
```

**Default `/etc/hosts`:**
```
127.0.0.1    localhost
127.0.1.1    icebox
::1          localhost ip6-localhost ip6-loopback
```

**Format — 3 fields per line:**
```
IP_address    canonical_hostname    [alias1]    [alias2]...
```

| Field | Example | Meaning |
|---|---|---|
| IP address | `127.0.0.1` | The IP to resolve to |
| Canonical hostname | `localhost` | Primary name for this IP |
| Aliases | `myserver staging` | Optional alternative names (all resolve to same IP) |

`#` starts a comment line and is ignored.

**Adding your own entries:**
```bash
sudo nano /etc/hosts
```

```
# Custom entries
127.0.0.1    localhost
127.0.1.1    icebox
192.168.1.50    myserver
192.168.1.51    staging.myapp.com    staging
10.0.0.1        company-vpn    vpn
```

**Common uses:**
- Block websites by pointing them to `127.0.0.1` or `0.0.0.0`
- Create shortcuts for frequently accessed servers (no need to type IP)
- Override DNS for testing (e.g. point a domain to a staging server before DNS propagation)
- Development — e.g. point `myapp.local` to `127.0.0.1`

```bash
# Test that your /etc/hosts entry is working
ping myserver              # Should resolve to the IP you set
```

> `/etc/hosts` entries always override external DNS. This is why it's checked first in the resolution chain.

### /etc/resolv.conf — DNS server configuration

This file tells your system which DNS servers to query:

```bash
cat /etc/resolv.conf
```

```
# Generated by resolvconf — DO NOT EDIT MANUALLY
nameserver 8.8.8.8
nameserver 8.8.4.4
search localdomain
```

| Directive | Meaning |
|---|---|
| `nameserver` | IP of the DNS server to query (up to 3 allowed) |
| `search` | Default domain appended when resolving short hostnames |
| `domain` | Local domain name |

> ⚠️ On modern Linux systems with `systemd-resolved` or `resolvconf`, this file is **auto-generated** and overwritten. Edit DNS settings via NetworkManager or `nmcli` instead of directly editing `resolv.conf`.

---

## 5. DNS Setup

When you need to run your own DNS server — for a local network, lab environment, or hosting your own domain — Linux has several options:

### DNS server software options

| Software | Description | Best for |
|---|---|---|
| **BIND** (named) | The oldest, most widely deployed DNS server. Feature-rich and battle-tested. The de facto standard on the internet | Large organizations, complex setups, public DNS |
| **DNSmasq** | Lightweight — easy to configure. Comes with DHCP too | Small networks, home labs, embedded devices |
| **PowerDNS** | Full-featured like BIND but more flexible. Can read from databases (MySQL, PostgreSQL) | Medium to large networks needing DB integration |
| **Unbound** | Validating, recursive, caching resolver. Focused on security (DNSSEC) | Caching resolvers, privacy-focused setups |

### Installing BIND (bind9) on Debian/Ubuntu

```bash
sudo apt install bind9 bind9utils bind9-doc
sudo systemctl status bind9             # Check if running
sudo systemctl enable bind9             # Start on boot
```

**BIND config files:**
```
/etc/bind/named.conf                    # Main config (includes others)
/etc/bind/named.conf.options            # Global options (forwarders, ACLs)
/etc/bind/named.conf.local              # Your zone definitions
/etc/bind/db.local                      # Template zone file
/var/cache/bind/                        # Zone data files
```

**Basic named.conf.options (forward queries to Google DNS):**
```
options {
    directory "/var/cache/bind";
    forwarders {
        8.8.8.8;
        8.8.4.4;
    };
    dnssec-validation auto;
    listen-on { any; };
};
```

**BIND commands:**
```bash
sudo systemctl restart bind9            # Restart BIND
sudo named-checkconf                    # Check config file for syntax errors
sudo named-checkzone example.com /etc/bind/db.example.com  # Check zone file
sudo rndc reload                        # Reload zones without restarting
sudo rndc flush                         # Flush DNS cache
```

### Installing DNSmasq (simpler alternative)

```bash
sudo apt install dnsmasq
sudo nano /etc/dnsmasq.conf             # Edit config
sudo systemctl restart dnsmasq
```

**Basic dnsmasq.conf:**
```
interface=eth0              # Listen on this interface
domain-needed               # Don't forward plain names without dots
bogus-priv                  # Don't forward private IP reverse lookups
no-resolv                   # Don't read /etc/resolv.conf
server=8.8.8.8              # Forward to Google DNS
server=8.8.4.4
```

---

## 6. DNS Tools

### nslookup — Simple DNS lookup

`nslookup` queries a DNS server to find the IP for a domain, or find the hostname for an IP.

```bash
nslookup www.google.com                     # Forward lookup — domain → IP
nslookup 8.8.8.8                            # Reverse lookup — IP → hostname
nslookup www.google.com 8.8.8.8             # Query a specific DNS server
nslookup -type=MX gmail.com                 # Query a specific record type
nslookup -type=NS google.com                # Find name servers for a domain
nslookup -type=TXT google.com               # Query TXT records
```

**Sample `nslookup` output:**
```
Server:    127.0.1.1
Address:   127.0.1.1#53

Non-authoritative answer:
Name:      www.google.com
Address:   216.58.192.4
```

| Field | Meaning |
|---|---|
| `Server` | DNS server that answered the query |
| `Address` | IP of that DNS server (port 53 is DNS) |
| `Non-authoritative answer` | Server returned a **cached** result, not from the authoritative source |
| `Name` / `Address` | The resolved hostname and IP |

> `Non-authoritative answer` just means the answer came from a recursive resolver's cache — this is completely normal. An `Authoritative answer` would come from the domain's own NS.

### dig — Detailed DNS lookup (preferred over nslookup)

`dig` (Domain Information Groper) provides much more detailed DNS output. It is the standard tool for DNS troubleshooting and is preferred over `nslookup`.

```bash
# Basic queries
dig www.google.com                          # Forward lookup (A record)
dig www.google.com A                        # Explicitly query A record
dig www.google.com AAAA                     # IPv6 address
dig www.google.com MX                       # Mail exchange records
dig www.google.com NS                       # Name server records
dig www.google.com TXT                      # TXT records
dig www.google.com ANY                      # All records

# Query specific DNS server
dig @8.8.8.8 www.google.com                 # Query Google's DNS
dig @192.168.1.1 www.google.com             # Query your local router

# Reverse lookup
dig -x 8.8.8.8                              # IP → hostname (PTR record)

# Control output
dig +short www.google.com                   # Short output — IP only
dig +noall +answer www.google.com           # Show only the answer section
dig +trace www.google.com                   # Trace full resolution from root servers

# Multiple queries at once
dig www.google.com www.facebook.com
```

**Sample `dig` output:**
```
; <<>> DiG 9.10.6 <<>> www.google.com
;; QUESTION SECTION:
;www.google.com.        IN    A

;; ANSWER SECTION:
www.google.com.    300  IN    A    172.217.16.142

;; Query time: 4 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Mon Jan 20 10:30:00 UTC 2024
;; MSG SIZE rcvd: 55
```

**dig output sections:**

| Section | Contents |
|---|---|
| `QUESTION SECTION` | What you asked for |
| `ANSWER SECTION` | The DNS records returned |
| `AUTHORITY SECTION` | Name servers authoritative for this domain |
| `ADDITIONAL SECTION` | Extra helpful records (e.g. IPs of name servers) |
| Query time | How long the query took (ms) |
| SERVER | Which DNS server answered |

**The most powerful dig feature — `+trace`:**
```bash
dig +trace www.google.com
```
This shows the complete resolution path from root servers → TLD → authoritative server. Invaluable for debugging DNS propagation issues.

### host — Simple and quick

```bash
host www.google.com                     # Quick lookup
host 8.8.8.8                            # Reverse lookup
host -t MX gmail.com                    # Specific record type
```

### systemd-resolved — Modern DNS on Ubuntu

```bash
systemd-resolve www.google.com          # Lookup via systemd resolver
resolvectl status                       # Show DNS configuration
resolvectl query www.google.com         # Query (modern syntax)
resolvectl flush-caches                 # Flush DNS cache
```

---

## 7. Quick Reference — DNS

**Resolution order:**
```
/etc/hosts → /etc/resolv.conf DNS → answer
```

**DNS record types:**

| Record | Purpose |
|---|---|
| `A` | Hostname → IPv4 |
| `AAAA` | Hostname → IPv6 |
| `CNAME` | Alias → hostname |
| `MX` | Mail server |
| `NS` | Name servers for domain |
| `PTR` | IP → hostname (reverse) |
| `TXT` | Free text (SPF, DKIM) |
| `SOA` | Zone authority info |

**nslookup:**
```bash
nslookup www.google.com                 # Basic lookup
nslookup -type=MX gmail.com            # Specific record type
nslookup www.google.com 8.8.8.8        # Query specific server
```

**dig:**
```bash
dig www.google.com                      # A record
dig www.google.com MX                   # Mail records
dig @8.8.8.8 www.google.com            # Query specific DNS server
dig +short www.google.com              # IP only output
dig -x 8.8.8.8                         # Reverse lookup
dig +trace www.google.com              # Full resolution trace from root
```

**Configuration files:**

| File | Purpose |
|---|---|
| `/etc/hosts` | Local static hostname → IP mappings |
| `/etc/resolv.conf` | DNS server IPs (nameserver directive) |
| `/etc/nsswitch.conf` | Resolution order (files dns myhostname) |

**DNS server management (BIND):**
```bash
sudo named-checkconf                    # Check config syntax
sudo named-checkzone domain /path/zone  # Check zone file
sudo rndc reload                        # Reload zones
sudo rndc flush                         # Clear DNS cache
```
