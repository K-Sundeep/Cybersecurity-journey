# Linux — Network Basics

---

## 1. Network Basics

A **network** is two or more devices connected together so they can communicate and share resources. The internet is simply a massive global network of networks.

**Key networking concepts:**

| Term | Meaning |
|---|---|
| **Host** | Any device connected to a network (computer, phone, server, printer) |
| **Packet** | The basic unit of data transmitted over a network — data is broken into small chunks |
| **Protocol** | A set of rules defining how data is formatted, transmitted, and received |
| **IP address** | Unique logical address identifying a device on a network |
| **MAC address** | Unique physical address burned into every network interface card |
| **Port** | A numbered endpoint on a host — directs traffic to the right application |
| **Router** | Device that forwards packets between different networks |
| **Switch** | Device that connects devices within the same network |

**Two foundational models:**
- **OSI Model** — Theoretical 7-layer reference model
- **TCP/IP Model** — Practical 4-layer implementation (what the internet actually uses)

---

## 2. OSI Model

The **OSI (Open Systems Interconnection) model** is a conceptual framework that describes how network communication works. It divides networking into **7 layers**, each with a specific job. Although theoretical and never directly implemented, it is still used universally for troubleshooting and understanding networking concepts.

```
Layer 7 — Application    ← You interact here (HTTP, FTP, SMTP, DNS)
Layer 6 — Presentation   ← Data formatting, encryption, compression
Layer 5 — Session        ← Opening, managing, closing sessions between apps
Layer 4 — Transport      ← End-to-end delivery, ports, TCP/UDP
Layer 3 — Network        ← Routing and IP addressing (IP, ICMP)
Layer 2 — Data Link      ← MAC addressing, frames, error detection (Ethernet, Wi-Fi)
Layer 1 — Physical       ← Raw bits over cables, wireless signals, hardware
```

**Each layer's job:**

| Layer | Name | Data unit | Key protocols | Job |
|---|---|---|---|---|
| 7 | Application | Data | HTTP, FTP, SMTP, DNS, SSH | Interface for user applications |
| 6 | Presentation | Data | SSL/TLS, JPEG, ASCII | Translate, encrypt, compress data |
| 5 | Session | Data | NetBIOS, RPC | Start, manage, end communication sessions |
| 4 | Transport | Segment | TCP, UDP | Reliable delivery, ports, flow control |
| 3 | Network | Packet | IP, ICMP, ARP | Routing between different networks |
| 2 | Data Link | Frame | Ethernet, Wi-Fi (802.11) | Local network delivery using MAC addresses |
| 1 | Physical | Bits | Cables, NIC, Wi-Fi signals | Transmit raw bits over physical media |

**Memory trick for the layers (top to bottom):**
**A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing

**Why it matters:**
When troubleshooting a network problem, you work from the bottom up — check physical cables (Layer 1), check if the interface is up (Layer 2), check IP address (Layer 3), check port (Layer 4), check the application (Layer 7). The layer where the problem exists tells you exactly what to investigate.

---

## 3. TCP/IP Model

The **TCP/IP model** is the practical foundation the internet is built on. It condenses the OSI model's 7 layers into **4 layers**. This is the model you work with in real-world networking.

```
Layer 4 — Application    ← Combines OSI layers 5, 6, 7 (HTTP, DNS, SMTP, SSH)
Layer 3 — Transport      ← Same as OSI layer 4 (TCP, UDP)
Layer 2 — Internet       ← Same as OSI layer 3 (IP, ICMP)
Layer 1 — Link           ← Combines OSI layers 1, 2 (Ethernet, Wi-Fi, ARP)
```

**TCP/IP vs OSI comparison:**

| TCP/IP Layer | OSI Equivalent | Protocols |
|---|---|---|
| Application | Layers 5, 6, 7 | HTTP, HTTPS, FTP, SMTP, DNS, SSH, Telnet |
| Transport | Layer 4 | TCP, UDP |
| Internet (Network) | Layer 3 | IP, ICMP, ARP |
| Link | Layers 1, 2 | Ethernet, Wi-Fi, MAC |

**How a packet travels — example (Pete emails Patty):**

```
SENDING (Pete's machine — encapsulation going DOWN):
Application  → Email data formatted by SMTP
Transport    → TCP header added: source/destination ports, sequence number
Internet     → IP header added: source/destination IP addresses
Link         → Frame header added: source/destination MAC addresses → sent over wire

RECEIVING (Patty's machine — de-encapsulation going UP):
Link         → Frame received, MAC checked, header stripped
Internet     → IP checked, header stripped, passed up
Transport    → Port checked, header stripped, data reassembled
Application  → Email data presented to Patty
```

> This process of wrapping data with headers as it goes down = **encapsulation**. Unwrapping as it goes up = **de-encapsulation**.

---

## 4. Network Addressing

### IP Addresses

An **IP address** (Internet Protocol address) is a logical address assigned to every device on a network. It has two parts: a **network portion** (which network) and a **host portion** (which device on that network).

**IPv4** — 32-bit address written as 4 octets in decimal, separated by dots:
```
192.168.1.129
```
Each octet is 8 bits, so ranges from 0–255. Total: ~4.3 billion possible addresses.

**IPv6** — 128-bit address written as 8 groups of 4 hex digits:
```
fd60:0000:0000:0000:021c:29ff:fe63:5cdc
fd60::21c:29ff:fe63:5cdc    (shortened — consecutive zeros replaced with ::)
```
Total: 2¹²⁸ addresses — effectively unlimited.

### IPv4 Address Classes (Classful)

| Class | First octet range | Default mask | Hosts per network | Usage |
|---|---|---|---|---|
| A | 1–126 | 255.0.0.0 (/8) | ~16 million | Large organizations |
| B | 128–191 | 255.255.0.0 (/16) | ~65,000 | Medium organizations |
| C | 192–223 | 255.255.255.0 (/24) | 254 | Small networks |
| D | 224–239 | — | — | Multicast |
| E | 240–255 | — | — | Reserved/experimental |

> Note: `127.x.x.x` is reserved for **loopback** (your own machine). `127.0.0.1` always means "this computer."

### Private IP Ranges

Private IPs are NOT routable on the internet — used inside local networks only.

| Range | CIDR | Class |
|---|---|---|
| `10.0.0.0` – `10.255.255.255` | 10.0.0.0/8 | A |
| `172.16.0.0` – `172.31.255.255` | 172.16.0.0/12 | B |
| `192.168.0.0` – `192.168.255.255` | 192.168.0.0/16 | C |

### Subnet Mask

The **subnet mask** determines which part of an IP address is the **network** portion and which is the **host** portion.

```
IP address:   192.168.1.129
Subnet mask:  255.255.255.0
              ↑↑↑ network ↑↑↑  ↑host↑
```

The `255`s "mask out" the network portion. So in this example, `192.168.1` is the network and `129` is the host.

### CIDR Notation

**CIDR (Classless Inter-Domain Routing)** is a compact way to write the subnet mask as a number of bits:

```
192.168.1.0/24      means subnet mask 255.255.255.0
192.168.1.0/16      means subnet mask 255.255.0.0
10.0.0.0/8          means subnet mask 255.0.0.0
```

The `/24` means the first 24 bits are the network prefix. The remaining bits (32-24=8) are for hosts.

**Hosts in a subnet:** `2^(host bits) - 2` (subtract 2 for network address and broadcast)

| CIDR | Subnet mask | Usable hosts |
|---|---|---|
| /24 | 255.255.255.0 | 254 |
| /25 | 255.255.255.128 | 126 |
| /26 | 255.255.255.192 | 62 |
| /27 | 255.255.255.224 | 30 |
| /16 | 255.255.0.0 | 65,534 |
| /8 | 255.0.0.0 | 16,777,214 |

### MAC Address

A **MAC (Media Access Control) address** is a unique physical address burned into every network interface card (NIC) by the manufacturer. It's 48 bits, written as 6 pairs of hex digits:

```
1d:3a:32:24:4d:ce
```

- First 3 pairs (`1d:3a:32`) = **OUI** (manufacturer identifier)
- Last 3 pairs (`24:4d:ce`) = **device identifier**

MAC addresses are used for communication **within the same local network**. IP addresses are used for routing **between different networks**.

**View your IP and MAC addresses:**
```bash
ip a                        # Modern Linux — show all interfaces
ifconfig                    # Classic tool (may need net-tools installed)
ip a show eth0              # Show specific interface
```

---

## 5. Application Layer

The **Application Layer** is the top layer of the TCP/IP model — the one you interact with directly. It provides network services to user-facing applications like web browsers, email clients, and file transfer tools.

**Responsibilities:**
- Provides network services to applications
- Prepares user data for transmission
- Presents incoming data in a user-friendly format
- Uses specific protocols for each type of service

**Common Application Layer protocols:**

| Protocol | Full name | Port | Use |
|---|---|---|---|
| HTTP | HyperText Transfer Protocol | 80 | Web browsing (unencrypted) |
| HTTPS | HTTP Secure | 443 | Web browsing (encrypted with TLS) |
| FTP | File Transfer Protocol | 20/21 | File transfers |
| SFTP | SSH File Transfer Protocol | 22 | Secure file transfers |
| SSH | Secure Shell | 22 | Secure remote terminal access |
| Telnet | — | 23 | Remote terminal (unencrypted — avoid) |
| SMTP | Simple Mail Transfer Protocol | 25 | Sending email |
| IMAP | Internet Message Access Protocol | 143/993 | Receiving email (server-side) |
| POP3 | Post Office Protocol v3 | 110/995 | Receiving email (download) |
| DNS | Domain Name System | 53 | Translates domain names to IPs |
| DHCP | Dynamic Host Configuration Protocol | 67/68 | Auto-assigns IP addresses |
| NTP | Network Time Protocol | 123 | Clock synchronization |
| SNMP | Simple Network Management Protocol | 161 | Network device monitoring |

> When a user browses a website, data is formatted by HTTP and handed to the Transport layer through port 80 (or 443 for HTTPS). This is the handoff point between user applications and the network stack.

---

## 6. Transport Layer

The **Transport Layer** is responsible for **end-to-end communication** between two hosts. It ensures data is delivered to the correct application on the destination host using **port numbers**, and manages how that data is transmitted.

### Ports

A **port** is a number (0–65535) that identifies a specific application or service on a host. IP addresses get you to the right machine; ports get you to the right application on that machine.

| Port range | Type | Usage |
|---|---|---|
| 0–1023 | Well-known ports | Reserved for standard services (HTTP=80, SSH=22) |
| 1024–49151 | Registered ports | Used by specific applications (databases, games) |
| 49152–65535 | Dynamic/ephemeral | Temporarily assigned by OS for outbound connections |

### TCP — Transmission Control Protocol

TCP provides **reliable, ordered, connection-oriented** data delivery. Before any data is sent, a formal connection is established via the **three-way handshake**:

```
Client                          Server
  |  ──── SYN ────────────────> |   "I want to connect"
  |  <─── SYN-ACK ─────────── |   "OK, acknowledged, I'm ready"
  |  ──── ACK ────────────────> |   "Great, connection established"
  |                             |
  |  ═══ DATA FLOWS ══════════> |
```

**TCP features:**
- **Connection-oriented** — establishes connection before data
- **Reliable** — every packet acknowledged; missing ones retransmitted
- **Ordered** — sequence numbers ensure data arrives in the correct order
- **Flow control** — prevents sender from overwhelming receiver
- **Error checking** — checksums verify data integrity

**Use TCP when:** data must arrive completely and in order — web browsing, email, file transfers, SSH.

### UDP — User Datagram Protocol

UDP provides **fast, connectionless, unreliable** data delivery. No handshake, no acknowledgment, no guaranteed delivery.

**UDP features:**
- **Connectionless** — just sends data, no setup
- **Unreliable** — no guarantee packets arrive or arrive in order
- **Fast** — lower overhead than TCP
- **Good for** — streaming video/audio, gaming, DNS, VoIP

**Use UDP when:** speed matters more than perfect delivery — dropped frames in video are acceptable, but latency is not.

**TCP vs UDP comparison:**

| Feature | TCP | UDP |
|---|---|---|
| Connection | Required (3-way handshake) | Not required |
| Reliability | Guaranteed delivery | Not guaranteed |
| Order | In order | Not guaranteed |
| Speed | Slower | Faster |
| Use case | HTTP, SSH, FTP, email | DNS, video stream, gaming, VoIP |

---

## 7. Network Layer

The **Network Layer** (also called the Internet Layer in TCP/IP) is responsible for **routing packets** from the source host to the destination host across one or more networks.

**Main responsibilities:**
- Adds source and destination **IP addresses** to each packet
- Determines the best **route** for packets to reach their destination
- Handles communication between different networks (subnets)

### How routing works

The internet is made up of many smaller networks (subnets) connected together. When a packet needs to leave your local network, it is sent to your **default gateway** (usually your router). The router examines the destination IP and forwards the packet towards the destination, possibly through many hops.

```
Your PC → Router (gateway) → ISP network → ... → Destination server
```

### Key Network Layer protocols

**IP (Internet Protocol)** — The core protocol of the internet. Assigns addresses and routes packets.

**ICMP (Internet Control Message Protocol)** — Used for diagnostic and error messages. The `ping` command uses ICMP.

```bash
ping google.com             # Test reachability (ICMP echo request/reply)
ping -c 4 192.168.1.1       # Send 4 pings
traceroute google.com       # Trace the route packets take (shows each hop)
```

**ARP (Address Resolution Protocol)** — Resolves an IP address to a MAC address on the local network. When your computer knows the destination IP but needs the MAC address to build the link layer frame, it broadcasts an ARP request asking "Who has IP x.x.x.x?"

```bash
arp -n                      # Show ARP table (cached IP→MAC mappings)
ip neigh                    # Modern equivalent — show neighbour table
```

---

## 8. Link Layer

The **Link Layer** (Network Interface Layer) is the bottom layer of the TCP/IP model. It handles communication on the **local network segment** — the physical network your device is directly connected to.

**Responsibilities:**
- Encapsulates the IP packet into a **frame**
- Adds source and destination **MAC addresses** to the frame header
- Handles error detection via checksums
- Sends the frame over the physical medium (cable, Wi-Fi)

**How the Link Layer works:**
When a device needs to send a packet on the local network, the link layer needs to know the **destination MAC address**. It uses **ARP** to find it:

1. "I need to send to IP 192.168.1.50 — what's its MAC?"
2. ARP broadcasts: "Who has 192.168.1.50? Tell me your MAC!"
3. Device with that IP replies with its MAC address
4. Frame is built with source + destination MAC and sent

**Data units at each layer:**
```
Application  →  Data
Transport    →  Segment (TCP) or Datagram (UDP)
Network      →  Packet
Link         →  Frame
Physical     →  Bits
```

**Common Link Layer protocols:**
- **Ethernet** — wired local networks (most common)
- **Wi-Fi (802.11)** — wireless local networks
- **PPP** — point-to-point links (DSL, WAN links)

```bash
ip link show                # Show all network interfaces and link-layer info
ip link show eth0           # Show specific interface
ethtool eth0                # Show Ethernet interface details (speed, duplex)
```

---

## 9. DHCP Overview

**DHCP (Dynamic Host Configuration Protocol)** automatically assigns IP addresses and network configuration to devices when they join a network — eliminating the need to manually configure each device.

Think of DHCP as a phone company: when you get a new phone, you need a number. You contact your carrier and they assign you one. When a device connects to a network, it needs an IP. DHCP is the service that provides it.

**What DHCP assigns:**
- IP address
- Subnet mask
- Default gateway (router)
- DNS server addresses
- Lease duration (how long the IP is valid)

**The DHCP DORA process** — 4 steps to get an IP address:

```
Client                              DHCP Server
  |                                      |
  |  ─── DISCOVER (broadcast) ───────>  |   "Anyone there? I need an IP!"
  |  <── OFFER ──────────────────────── |   "Here, take 192.168.1.50 for 24h"
  |  ─── REQUEST (broadcast) ────────>  |   "I'll take that offer, please!"
  |  <── ACK ──────────────────────────  |   "Confirmed! It's yours for 24h"
  |                                      |
  Lease granted — device is configured
```

| Step | Full name | Description |
|---|---|---|
| **D**iscover | DHCP Discover | Client broadcasts to find available DHCP servers |
| **O**ffer | DHCP Offer | Server responds with a proposed IP + config |
| **R**equest | DHCP Request | Client accepts the offer and broadcasts its choice |
| **A**cknowledge | DHCP ACK | Server confirms and the lease begins |

**Lease renewal:**
Before the lease expires, the client sends a new REQUEST directly to the server to renew. If the server is unavailable, the client tries again when 87.5% of the lease time has passed.

**Viewing DHCP-assigned address:**
```bash
ip a                        # View current IP addresses
dhclient eth0               # Request new IP from DHCP server
dhclient -r eth0            # Release current DHCP lease
```

**In a typical home network:**
Your **router** acts as the DHCP server. Every device (phone, laptop, TV) that connects gets automatically assigned an IP from the router's pool.

---

## 10. Quick Reference — Network Basics

**View network info:**
```bash
ip a                        # Show all interfaces, IPs, MACs
ip a show eth0              # Show specific interface
ifconfig                    # Classic interface info
ip route                    # Show routing table
arp -n                      # Show ARP cache (IP→MAC)
ip neigh                    # Modern ARP/neighbour table
```

**Test connectivity:**
```bash
ping 8.8.8.8                # Test internet connectivity
ping -c 4 hostname          # Send 4 pings to a host
traceroute google.com       # Show each hop to destination
```

**OSI Layers (7→1):**
Application → Presentation → Session → Transport → Network → Data Link → Physical

**TCP/IP Layers (4→1):**
Application → Transport → Internet → Link

**TCP vs UDP:**

| | TCP | UDP |
|---|---|---|
| Reliable | ✓ | ✗ |
| Ordered | ✓ | ✗ |
| Fast | Slower | Faster |
| Use | HTTP, SSH, FTP | DNS, Video, Gaming |

**DHCP DORA:** Discover → Offer → Request → ACK

**Common ports:**

| Port | Protocol |
|---|---|
| 22 | SSH / SFTP |
| 25 | SMTP |
| 53 | DNS |
| 67/68 | DHCP |
| 80 | HTTP |
| 443 | HTTPS |
| 21 | FTP |
| 110 | POP3 |
| 143 | IMAP |

**Private IP ranges:**

| Range | CIDR |
|---|---|
| 10.0.0.0 – 10.255.255.255 | 10.0.0.0/8 |
| 172.16.0.0 – 172.31.255.255 | 172.16.0.0/12 |
| 192.168.0.0 – 192.168.255.255 | 192.168.0.0/16 |
