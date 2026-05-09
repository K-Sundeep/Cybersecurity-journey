# Linux — Subnetting

---

## 1. IPv4

**IPv4 (Internet Protocol version 4)** is the foundational addressing system of the internet. Every device needs an IP address to communicate on a network.

**IPv4 address structure:**
- 32-bit address written as **4 octets** in decimal, separated by dots
- Each octet is 8 bits → values range from **0 to 255**

```
192  .  168  .   1  .  165
 ↑        ↑       ↑      ↑
Octet 1  Octet 2  Octet 3  Octet 4
```

**In binary:**
```
192.168.1.165 = 11000000.10101000.00000001.10100101
```

**IPv4 Address Classes:**

| Class | First octet range | Default mask | Hosts per network | Purpose |
|---|---|---|---|---|
| A | 1–126 | 255.0.0.0 (/8) | ~16.7 million | Large organizations |
| B | 128–191 | 255.255.0.0 (/16) | ~65,534 | Medium organizations |
| C | 192–223 | 255.255.255.0 (/24) | 254 | Small networks |
| D | 224–239 | — | — | Multicast |
| E | 240–255 | — | — | Reserved |

**Special addresses:**
- `127.0.0.1` — loopback (your own machine, always)
- `0.0.0.0` — unspecified / default route
- `255.255.255.255` — limited broadcast (entire local network)

**Private IP ranges (not routable on the internet):**

| Range | CIDR | Class |
|---|---|---|
| 10.0.0.0 – 10.255.255.255 | 10.0.0.0/8 | A |
| 172.16.0.0 – 172.31.255.255 | 172.16.0.0/12 | B |
| 192.168.0.0 – 192.168.255.255 | 192.168.0.0/16 | C |

---

## 2. Subnets

A **subnet** (subnetwork) is a logical division of a larger IP network into smaller segments. Hosts on the same subnet can communicate directly with each other; traffic to other subnets must go through a router.

**Think of it like mail:** sending a letter within the same postcode (subnet) is simple and direct. Sending to a different city (different subnet) requires routing through the postal system (a router).

Every IP address on a subnet has two parts:
- **Network prefix** — identifies which subnet (shared by all hosts on the subnet)
- **Host identifier** — identifies the specific device on that subnet

```
192.168.1.8   →   192.168.1 = network  |  8 = host
192.168.1.9   →   192.168.1 = network  |  9 = host
```
Both of these are on the same subnet — they can communicate directly.

**Subnet mask** — tells the system which bits are the network portion and which are the host portion:

```
IP address:    192.168.1.165  =  11000000.10101000.00000001.10100101
Subnet mask:   255.255.255.0  =  11111111.11111111.11111111.00000000
                                  ←── network prefix ───→  ←─ host ─→
```

`255` means "this octet is part of the network." `0` means "this octet is for the host."

**Special addresses within a subnet (cannot be assigned to hosts):**

| Address | Role |
|---|---|
| First address (all host bits = 0) | **Network address** — identifies the subnet itself |
| Last address (all host bits = 1) | **Broadcast address** — sends to all hosts on subnet |

For a `/24` subnet like `192.168.1.0/24`:
- Network address: `192.168.1.0`
- Broadcast address: `192.168.1.255`
- Usable hosts: `192.168.1.1` – `192.168.1.254` (254 hosts)

---

## 3. Subnet Math

**How to calculate usable hosts:**

```
Usable hosts = 2^(host bits) - 2
```

Subtract 2 to exclude the **network address** and **broadcast address**.

**Worked example — `192.168.1.0 / 255.255.255.0`:**

```
IP:   192.168.1.165  =  11000000.10101000.00000001.10100101
Mask: 255.255.255.0  =  11111111.11111111.11111111.00000000
```

The `1` bits in the mask "block out" (mask) the network portion. Only the `0` bits represent available host space.

- Host bits = 8 (the last octet is all zeros in the mask)
- Total addresses = 2⁸ = 256
- Subtract 2 (network + broadcast) = **254 usable hosts**

**Another example — `192.168.1.0 / 255.255.255.192` (a `/26`):**

```
Mask: 255.255.255.192 = 11111111.11111111.11111111.11000000
```
- Host bits = 6 (last 6 bits are 0)
- Total addresses = 2⁶ = 64
- Subtract 2 = **62 usable hosts**

**General formula:**

| Host bits | Total addresses | Usable hosts |
|---|---|---|
| 1 | 2 | 0 |
| 2 | 4 | 2 |
| 3 | 8 | 6 |
| 4 | 16 | 14 |
| 5 | 32 | 30 |
| 6 | 64 | 62 |
| 7 | 128 | 126 |
| 8 | 256 | 254 |

**Finding the network and broadcast for any IP:**

Given `192.168.1.165 / 255.255.255.0`:
- Network address = IP AND subnet mask → `192.168.1.0`
- Broadcast = Network address with all host bits set to 1 → `192.168.1.255`
- First host = Network address + 1 → `192.168.1.1`
- Last host = Broadcast - 1 → `192.168.1.254`

---

## 4. Subnetting Cheats

In the real world, tools automate subnet math. But understanding manual binary conversion is essential for networking certifications, interviews, and truly understanding how IP addressing works.

### Powers of 2 — Memorize These

```
2^1  =   2
2^2  =   4
2^3  =   8
2^4  =  16
2^5  =  32
2^6  =  64
2^7  = 128
2^8  = 256
```

### The Binary Conversion Chart

Each octet is 8 bits. Each bit position has a fixed value:

```
Bit position:  8    7    6    5    4    3    2    1
Bit value:    128   64   32   16    8    4    2    1
```

Sum of all bits = 128+64+32+16+8+4+2+1 = **255** (maximum octet value).

**Converting decimal to binary — example: `192`**

Start from the left (128) and check if the value fits:

| Bit value | 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |
|---|---|---|---|---|---|---|---|---|
| 192 ≥ 128? | ✓ (192-128=64) | | | | | | | |
| 64 ≥ 64? | 1 | ✓ (64-64=0) | | | | | | |
| 0 ≥ 32? | 1 | 1 | ✗ | | | | | |
| Result | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |

`192` in binary = `11000000`

**Full example — convert `192.168.23.43`:**

| Octet | Decimal | Binary |
|---|---|---|
| 1 | 192 | 11000000 |
| 2 | 168 | 10101000 |
| 3 | 23 | 00010111 |
| 4 | 43 | 00101011 |

**Converting binary to decimal:**
Add up the values for each `1` bit.
`10101000` = 128+0+32+0+8+0+0+0 = **168**

### Common Subnet Mask Values — Quick Cheat Sheet

| CIDR | Subnet mask | Host bits | Usable hosts |
|---|---|---|---|
| /24 | 255.255.255.0 | 8 | 254 |
| /25 | 255.255.255.128 | 7 | 126 |
| /26 | 255.255.255.192 | 6 | 62 |
| /27 | 255.255.255.224 | 5 | 30 |
| /28 | 255.255.255.240 | 4 | 14 |
| /29 | 255.255.255.248 | 3 | 6 |
| /30 | 255.255.255.252 | 2 | 2 |
| /23 | 255.255.254.0 | 9 | 510 |
| /22 | 255.255.252.0 | 10 | 1022 |
| /20 | 255.255.240.0 | 12 | 4094 |
| /16 | 255.255.0.0 | 16 | 65,534 |
| /8 | 255.0.0.0 | 24 | 16,777,214 |

---

## 5. CIDR

**CIDR (Classless Inter-Domain Routing)** is a compact method for writing subnet masks as a **prefix length** — the number of network bits — instead of writing the full dotted decimal mask.

```
10.42.3.0 with mask 255.255.255.0   →   10.42.3.0/24
```

The `/24` means the first 24 bits are the network prefix. The remaining bits (32-24=8) are for hosts.

**Why "classless"?**
Before CIDR, networks were divided strictly by class (A=8 bits, B=16 bits, C=24 bits). This wasted huge amounts of address space. A company needing 300 hosts would get a Class B with 65,534 addresses — 65,234 wasted. CIDR allows any prefix length, so you can allocate exactly (or close to) the space needed.

**Calculating hosts from CIDR:**

```
hosts = 2^(32 - prefix) - 2
```

Example: `123.12.24.0/23`
- Host bits = 32 - 23 = 9
- Total addresses = 2⁹ = 512
- Usable hosts = 512 - 2 = **510**

**CIDR in practice:**
```bash
ip a                        # Shows addresses in CIDR notation: inet 192.168.1.5/24
ip route                    # Shows routes in CIDR: 192.168.1.0/24 dev eth0
```

**Route aggregation (supernetting):**
CIDR also allows combining multiple small networks into one route entry:
```
192.168.0.0/24
192.168.1.0/24     →   can be summarized as 192.168.0.0/23
192.168.2.0/24         (covers all three)
192.168.3.0/24     →   192.168.0.0/22 (covers all four)
```
This reduces the size of routing tables, making routing more efficient.

---

## 6. NAT

**NAT (Network Address Translation)** is a method where a router rewrites the source or destination IP address of packets as they pass through. It allows multiple devices using private IP addresses to share a single public IP address when communicating with the internet.

**Why NAT exists:**
IPv4 only has ~4.3 billion addresses — far fewer than the number of internet-connected devices. Private IP ranges (10.x.x.x, 172.16-31.x.x, 192.168.x.x) can be reused on millions of private networks. NAT allows these private addresses to reach the internet by swapping them with the router's single public IP.

**How NAT works in your home:**

```
Your laptop (192.168.1.100) → Packet sent to google.com
Router receives packet → replaces source IP 192.168.1.100 with public IP (e.g. 203.0.113.5)
                       → records mapping in NAT table
Packet reaches google.com with source 203.0.113.5
Google replies to 203.0.113.5
Router receives reply → looks up NAT table → translates back to 192.168.1.100
Your laptop receives reply
```

**Three types of NAT:**

| Type | Also called | How it works |
|---|---|---|
| **Static NAT** | 1-to-1 NAT | One private IP permanently maps to one public IP |
| **Dynamic NAT** | Pooled NAT | Private IPs map to a pool of public IPs (assigned temporarily) |
| **PAT** | MASQUERADE / NAT Overload / Hide NAT | Many private IPs share one public IP using **port numbers** to distinguish connections |

**PAT (Port Address Translation)** — the most common type, used in virtually all home routers:
- Multiple devices share one public IP
- Differentiated by source port numbers
- Router tracks all active connections in a **NAT translation table**

```
192.168.1.100:5001 → 203.0.113.5:45001  (your laptop)
192.168.1.101:5001 → 203.0.113.5:45002  (your phone)
192.168.1.102:5001 → 203.0.113.5:45003  (your tablet)
```

**SNAT vs DNAT:**

| NAT type | Modifies | Used for |
|---|---|---|
| **SNAT** (Source NAT) | Source IP address | Outgoing traffic — internal to internet |
| **DNAT** (Destination NAT) | Destination IP address | Incoming traffic — port forwarding, exposing servers |
| **Masquerade** | Source IP (dynamic) | Special SNAT for dynamic public IPs (DHCP) |

**NAT on Linux with iptables:**
```bash
# Masquerade (SNAT) — share internet via eth0
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# Port forward (DNAT) — forward port 80 to internal server
sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j DNAT --to-destination 192.168.1.10:80

# View NAT table
sudo iptables -t nat -L -n -v
```

> NAT breaks **end-to-end connectivity** — external hosts cannot initiate connections to devices behind NAT without port forwarding. This is why NAT is not used with IPv6 (IPv6 restores end-to-end connectivity).

---

## 7. IPv6

**IPv6** is the successor to IPv4, designed to solve the address exhaustion problem. It provides a vastly larger address space and other improvements.

**IPv6 address structure:**
- **128 bits** written as 8 groups of 4 hex digits, separated by colons
- Total addresses: 2¹²⁸ ≈ 340 undecillion — effectively unlimited

```
fd60:0000:0000:0000:021c:29ff:fe63:5cdc
```

**Shortening rules:**
1. Leading zeros in each group can be omitted: `0000` → `0`
2. One consecutive sequence of all-zero groups can be replaced with `::` (only once)

```
fd60:0000:0000:0000:021c:29ff:fe63:5cdc
   → fd60:0:0:0:21c:29ff:fe63:5cdc        (leading zeros removed)
   → fd60::21c:29ff:fe63:5cdc             (consecutive zeros compressed)
```

**IPv6 address types:**

| Type | Prefix | Scope | Description |
|---|---|---|---|
| **Loopback** | `::1/128` | Host only | Equivalent to `127.0.0.1` in IPv4 |
| **Link-local** | `fe80::/10` | Local link only | Auto-assigned to every IPv6 interface. Used for local communication only. NOT routable |
| **Unique Local** | `fc00::/7` | Organization | IPv6 equivalent of private IPs (like 192.168.x.x). Not internet-routable |
| **Global Unicast** | `2000::/3` | Internet | Globally routable — the IPv6 equivalent of public IPs |
| **Multicast** | `ff00::/8` | Varies | One-to-many (replaces IPv4 broadcast) |

**Auto-configuration (SLAAC):**
IPv6 devices can automatically generate their own address using **SLAAC (Stateless Address Autoconfiguration)**:
1. Router advertises the network prefix (e.g. `2001:db8::/64`)
2. Device generates the host portion from its **MAC address** (using EUI-64 process)
3. Result: a unique global address — no DHCP server needed (though DHCPv6 also exists)

**Key differences from IPv4:**

| | IPv4 | IPv6 |
|---|---|---|
| Address size | 32 bits | 128 bits |
| Total addresses | ~4.3 billion | ~340 undecillion |
| Address notation | Decimal dotted | Hexadecimal colon |
| NAT required | Yes (due to shortage) | No (enough addresses for all) |
| Broadcast | Yes | No (replaced by multicast) |
| Auto-configuration | DHCP | SLAAC or DHCPv6 |
| Header size | 20-60 bytes | Fixed 40 bytes (simpler) |

**Working with IPv6 in Linux:**
```bash
ip -6 a                                     # Show IPv6 addresses
ip -6 route                                 # Show IPv6 routing table
ping6 ::1                                   # Ping IPv6 loopback
ping6 fe80::1%eth0                          # Ping link-local (must specify interface with %)
ping6 2001:db8::1                           # Ping global IPv6 address

# Manually assign IPv6 address
sudo ip addr add 2001:db8::10/64 dev eth0

# View IPv6 with ip a
ip a
# Look for: inet6 fe80::... scope link    (link-local)
#           inet6 fd60::... scope global  (global unicast)
```

---

## 8. Quick Reference — Subnetting

**Subnet calculations:**
```
Usable hosts  = 2^(host bits) - 2
Host bits     = 32 - CIDR prefix
```

**Binary conversion chart (one octet):**
```
128  64  32  16   8   4   2   1
```

**Powers of 2:**
```
2^1=2  2^2=4  2^3=8  2^4=16  2^5=32  2^6=64  2^7=128  2^8=256
```

**CIDR quick reference:**

| CIDR | Subnet Mask | Hosts |
|---|---|---|
| /30 | 255.255.255.252 | 2 |
| /29 | 255.255.255.248 | 6 |
| /28 | 255.255.255.240 | 14 |
| /27 | 255.255.255.224 | 30 |
| /26 | 255.255.255.192 | 62 |
| /25 | 255.255.255.128 | 126 |
| /24 | 255.255.255.0 | 254 |
| /23 | 255.255.254.0 | 510 |
| /22 | 255.255.252.0 | 1022 |
| /16 | 255.255.0.0 | 65,534 |
| /8 | 255.0.0.0 | 16,777,214 |

**NAT types:**

| Type | Description |
|---|---|
| Static NAT | 1:1 private→public mapping |
| Dynamic NAT | Pool of public IPs |
| PAT/Masquerade | Many:1 using port numbers (most common) |
| SNAT | Modifies source IP (outbound) |
| DNAT | Modifies destination IP (port forwarding) |

**IPv6 address types:**

| Type | Prefix | Use |
|---|---|---|
| Loopback | `::1/128` | Self (like 127.0.0.1) |
| Link-local | `fe80::/10` | Local network only |
| Unique local | `fc00::/7` | Private (like 192.168.x.x) |
| Global unicast | `2000::/3` | Internet-routable |
| Multicast | `ff00::/8` | One-to-many |

**IPv6 Linux commands:**
```bash
ip -6 a                     # Show IPv6 addresses
ip -6 route                 # IPv6 routing table
ping6 ::1                   # Ping IPv6 loopback
ping6 fe80::1%eth0          # Ping link-local (% + interface required)
```
