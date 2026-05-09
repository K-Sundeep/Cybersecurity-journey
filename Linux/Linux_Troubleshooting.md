# Linux — Network Troubleshooting

---

## 1. ICMP

**ICMP (Internet Control Message Protocol)** is a Network Layer protocol used to send **diagnostic and error messages** between network devices. It is not used to transfer data like TCP or UDP — it's purely for reporting network conditions and testing connectivity.

**How ICMP works:**
Every IP packet has a **TTL (Time-To-Live)** field — a counter that gets decremented by 1 at every router hop. When TTL hits 0, the router discards the packet and sends an ICMP "Time Exceeded" message back to the sender. This prevents packets from looping forever on the internet.

**Key ICMP message types:**

| Type | Name | Description |
|---|---|---|
| 0 | Echo Reply | Response to a ping (Echo Request) — host is reachable |
| 3 | Destination Unreachable | Packet couldn't reach its destination — includes 16 sub-codes |
| 8 | Echo Request | Sent by `ping` to test if a host is reachable |
| 11 | Time Exceeded | TTL reached 0 before packet arrived — used by `traceroute` |

**Type 3 — Destination Unreachable sub-codes (most common):**

| Code | Meaning |
|---|---|
| 0 | Network Unreachable |
| 1 | Host Unreachable |
| 2 | Protocol Unreachable |
| 3 | Port Unreachable |
| 4 | Fragmentation Needed but DF bit set |
| 13 | Communication Administratively Prohibited (firewall) |

**ICMP in the troubleshooting toolkit:**
- `ping` uses **Type 8 (Echo Request)** and **Type 0 (Echo Reply)** to test basic connectivity
- `traceroute` uses **TTL manipulation** and **Type 11 (Time Exceeded)** responses to map the path to a host
- Routers use **Type 3 (Destination Unreachable)** to tell the source a route couldn't be found

> ⚠️ Many firewalls and routers block ICMP traffic. If `ping` fails, it doesn't always mean the host is down — it might just be blocking ICMP packets. Use other tools to confirm.

---

## 2. ping

`ping` is the most fundamental network troubleshooting command. It sends **ICMP Echo Request** packets to a target and waits for **ICMP Echo Reply** packets. It tells you if a host is reachable and measures round-trip time (latency).

```bash
ping google.com                     # Ping continuously (Ctrl+C to stop)
ping 8.8.8.8                        # Ping by IP address
ping -c 4 google.com                # Send exactly 4 packets then stop
ping -c 4 -i 0.5 google.com         # Send 4 packets, 0.5s interval
ping -s 100 google.com              # Set packet size to 100 bytes (default 56)
ping -w 5 google.com                # Deadline — stop after 5 seconds
ping -t 64 google.com               # Set TTL to 64
```

**Sample `ping` output:**
```
PING google.com (172.217.16.142) 56(84) bytes of data.
64 bytes from 172.217.16.142: icmp_seq=1 ttl=117 time=11.8 ms
64 bytes from 172.217.16.142: icmp_seq=2 ttl=117 time=11.7 ms
64 bytes from 172.217.16.142: icmp_seq=3 ttl=117 time=11.7 ms
64 bytes from 172.217.16.142: icmp_seq=4 ttl=117 time=11.7 ms

--- google.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/mdev = 11.677/11.719/11.814/0.052 ms
```

**Output field meanings:**

| Field | Meaning |
|---|---|
| `56(84) bytes` | 56 bytes data + 28 bytes ICMP/IP headers = 84 bytes total |
| `icmp_seq=1` | Sequence number — used to track which packets returned |
| `ttl=117` | TTL value in the reply packet — decrements with each hop |
| `time=11.8 ms` | Round-trip time (RTT) — lower is better |
| `0% packet loss` | All sent packets received a reply — network is healthy |
| `rtt min/avg/max/mdev` | Min, average, max, deviation of round-trip times |

**Interpreting results:**

| Result | Meaning |
|---|---|
| Replies with low RTT | Host is reachable, network is healthy |
| Replies with high RTT | Host reachable but high latency — possible congestion |
| Packet loss > 0% | Network instability or congestion |
| 100% packet loss | Host unreachable, down, or blocking ICMP |
| `Destination Host Unreachable` | No route to the host from your machine |
| `Network is unreachable` | No default gateway or routing issue |

**Systematic troubleshooting with ping:**
```bash
ping 127.0.0.1              # Step 1: Test loopback — is TCP/IP stack working?
ping 192.168.1.1            # Step 2: Test gateway — is local network working?
ping 8.8.8.8                # Step 3: Test internet by IP — is routing working?
ping google.com             # Step 4: Test by name — is DNS working?
```

---

## 3. traceroute

`traceroute` maps the **exact path packets take** from your machine to a destination, showing every router (hop) along the way and the time taken at each hop. It is the go-to tool for pinpointing exactly where in the network path a problem exists.

```bash
traceroute google.com           # Trace route to google.com
traceroute 8.8.8.8              # Trace to IP address
traceroute -n google.com        # No DNS resolution — faster, shows IPs only
traceroute -m 30 google.com     # Max 30 hops (default)
traceroute -I google.com        # Use ICMP instead of UDP probes
```

**How traceroute works:**
1. Sends a packet with **TTL=1** → first router decrements to 0, sends back ICMP "Time Exceeded" — we learn the first hop's IP and RTT
2. Sends packet with **TTL=2** → second router sends back ICMP "Time Exceeded" — second hop discovered
3. Continues incrementing TTL until the destination is reached
4. Each hop is probed **3 times** — three RTT values are shown per hop

**Sample `traceroute` output:**
```
traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 60 byte packets
 1  _gateway (10.0.2.2)       0.113 ms  0.087 ms  0.083 ms
 2  * * *
 3  * * *
 4  8.8.8.8                  14.080 ms 13.849 ms 14.399 ms
```

**Output explained:**

| Column | Meaning |
|---|---|
| Number | Hop number (1 = closest, increasing towards destination) |
| Hostname (IP) | Router at that hop |
| Three RTT values | Round-trip time for each of the 3 probes sent |
| `* * *` | Router at this hop doesn't respond to traceroute probes (filtered by firewall) |

**Reading traceroute results:**
- **Increasing RTT** as hops increase is normal
- **Sudden spike** in RTT at a specific hop = that hop may be the bottleneck
- **All `* * *` after a point** = a firewall is blocking further probes (not necessarily a problem — destination may still be reachable)
- **Long RTT at early hops** = problem is local (your network or ISP)
- **Long RTT at later hops** = problem is further along the path

**`mtr` — combined ping + traceroute (real-time):**
```bash
sudo apt install mtr
mtr google.com              # Real-time continuous path analysis
mtr -n google.com           # No DNS lookup
mtr -r -c 100 google.com    # Report mode — send 100 packets then show stats
```

`mtr` combines the continuous updates of `ping` with the path mapping of `traceroute`. Shows packet loss and latency **per hop** in real time. Very useful for spotting intermittent issues.

---

## 4. netstat

`netstat` displays network connections, routing tables, interface statistics, and more. It is the **Swiss army knife** of network status commands, giving you a full picture of what's happening on your system's network layer.

> **Note:** `netstat` is from the older `net-tools` package. The modern replacement is `ss` (socket statistics), which is faster and shows more detail.

```bash
# Connections
netstat -a                  # All connections (listening + established)
netstat -t                  # TCP connections only
netstat -u                  # UDP connections only
netstat -l                  # Listening sockets only
netstat -lt                 # Listening TCP sockets
netstat -lu                 # Listening UDP sockets

# Options
netstat -n                  # Numeric — don't resolve hostnames or port names
netstat -p                  # Show PID and process name for each connection
netstat -e                  # Extended info

# Useful combinations
netstat -tulnp              # Most useful: TCP+UDP listening, numeric, with process
netstat -anp | grep :80     # Show what's using port 80
netstat -anp | grep ESTABLISHED  # Show active connections only

# Other views
netstat -r                  # Routing table
netstat -i                  # Interface statistics
netstat -s                  # Statistics by protocol (total packets, errors)
```

**Sample `netstat -tulnp` output:**
```
Proto  Recv-Q Send-Q  Local Address    Foreign Address  State    PID/Program
tcp        0      0  0.0.0.0:22       0.0.0.0:*        LISTEN   1234/sshd
tcp        0      0  127.0.0.1:3306   0.0.0.0:*        LISTEN   5678/mysqld
tcp        0      0  192.168.1.5:22   192.168.1.10:52420 ESTABLISHED 9012/sshd
udp        0      0  0.0.0.0:68       0.0.0.0:*                 890/dhclient
```

**Field meanings:**

| Field | Meaning |
|---|---|
| `Proto` | Protocol: tcp, udp, tcp6, udp6 |
| `Recv-Q` | Data received but not yet read by application |
| `Send-Q` | Data sent but not yet acknowledged |
| `Local Address` | IP and port on this machine (`0.0.0.0` = all interfaces) |
| `Foreign Address` | Remote IP and port (`*` = any) |
| `State` | Connection state |
| `PID/Program` | Which process owns this socket |

**Connection states:**

| State | Meaning |
|---|---|
| `LISTEN` | Waiting for incoming connections |
| `ESTABLISHED` | Active connection — data is flowing |
| `TIME_WAIT` | Connection closed, waiting for stragglers |
| `CLOSE_WAIT` | Remote end closed, waiting for local app to close |
| `SYN_SENT` | Actively trying to connect |

**`ss` — modern replacement for netstat:**
```bash
ss -tulnp                   # Same as netstat -tulnp but faster
ss -an                      # All sockets, numeric
ss -t state established     # Only established TCP connections
ss -s                       # Summary statistics
```

---

## 5. Packet Analysis

**Packet analysis** is the practice of capturing and inspecting the raw data travelling across a network interface. It reveals exactly what is being transmitted — protocol details, flags, payloads — at a much deeper level than connection-level tools like `netstat`.

**The two main tools:**

| Tool | Interface | Best for |
|---|---|---|
| **tcpdump** | Command-line | Remote servers, scripts, quick captures |
| **Wireshark** | Graphical (GUI) | Deep analysis, visual protocol decoding |

> A common workflow: capture with `tcpdump` on a remote server (saving to a `.pcap` file), then open the file in Wireshark locally for in-depth analysis.

### tcpdump — Command-line packet capture

```bash
# Install
sudo apt install tcpdump

# Basic capture
sudo tcpdump -i eth0                    # Capture on eth0 interface
sudo tcpdump -i any                     # Capture on ALL interfaces
sudo tcpdump -i wlan0 -v               # Verbose — more detail per packet
sudo tcpdump -i wlan0 -vv              # Very verbose — maximum detail

# Control how many packets to capture
sudo tcpdump -i eth0 -c 10             # Capture only 10 packets then stop

# Suppress DNS lookups (faster, cleaner output)
sudo tcpdump -i eth0 -n                # No hostname resolution
sudo tcpdump -i eth0 -nn               # No hostname or port name resolution

# Save to file and read from file
sudo tcpdump -i eth0 -w capture.pcap           # Save to file
sudo tcpdump -r capture.pcap                   # Read and display a saved file
sudo tcpdump -i eth0 -w capture.pcap -c 100   # Capture 100 packets to file
```

**Sample tcpdump output:**
```
11:28:23.958840 IP icebox.lan > nuq04s29-in-f4.1e100.net: ICMP echo request, id 1901, seq 2, length 64
11:28:23.970928 IP nuq04s29-in-f4.1e100.net > icebox.lan: ICMP echo reply, id 1901, seq 2, length 64
```

**Reading a packet line:**
```
08:41:13.729687 IP 192.168.1.5.22 > 192.168.1.10.52420: Flags [P.], seq 196:568, ack 1, win 309, length 372
↑               ↑  ↑              ↑                      ↑              ↑         ↑        ↑        ↑
Timestamp       L3  Source IP.port  Dest IP.port           TCP flags      Seq range  ACK      Window   Data length
```

**TCP Flags:**

| Flag | Meaning |
|---|---|
| `S` | SYN — start connection |
| `F` | FIN — close connection |
| `R` | RST — reset connection |
| `P` | PSH — push data to app immediately |
| `A` | ACK — acknowledge received data |
| `.` | ACK only (no other flags) |

### Filtering with tcpdump — BPF (Berkeley Packet Filter)

Filtering is the most important skill in packet analysis — without it, traffic volume is overwhelming.

```bash
# Filter by host
sudo tcpdump -i eth0 host 192.168.1.10          # Traffic to/from this IP
sudo tcpdump -i eth0 src 192.168.1.10           # Traffic FROM this IP only
sudo tcpdump -i eth0 dst 192.168.1.10           # Traffic TO this IP only

# Filter by port
sudo tcpdump -i eth0 port 80                    # HTTP traffic
sudo tcpdump -i eth0 port 22                    # SSH traffic
sudo tcpdump -i eth0 portrange 8000-9000        # Port range

# Filter by protocol
sudo tcpdump -i eth0 tcp                        # TCP only
sudo tcpdump -i eth0 udp                        # UDP only
sudo tcpdump -i eth0 icmp                       # ICMP only (ping)

# Combine filters with and/or/not
sudo tcpdump -i eth0 host 192.168.1.10 and port 80      # Host AND port
sudo tcpdump -i eth0 port 80 or port 443                 # HTTP or HTTPS
sudo tcpdump -i eth0 not port 22                         # Exclude SSH traffic

# Practical examples
sudo tcpdump -i eth0 -nn host 8.8.8.8               # What am I sending to 8.8.8.8?
sudo tcpdump -i eth0 -nn port 80 -c 20              # First 20 HTTP packets
sudo tcpdump -i any -c5 icmp                         # Capture 5 ping packets
sudo tcpdump -i eth0 -w debug.pcap host 10.0.0.1    # Save traffic with a host to file
```

### Wireshark

Wireshark provides a graphical interface for packet capture and analysis. Features colour-coded protocols, clickable packet dissection, and hundreds of built-in protocol decoders.

```bash
sudo apt install wireshark          # Install Wireshark
wireshark &                         # Launch GUI
wireshark capture.pcap              # Open a saved pcap file
```

**Wireshark display filters (different from tcpdump BPF):**

| Filter | What it shows |
|---|---|
| `ip.addr == 192.168.1.10` | Traffic involving this IP |
| `tcp.port == 80` | HTTP traffic |
| `http` | HTTP protocol |
| `icmp` | ICMP (ping) packets |
| `dns` | DNS queries and responses |
| `tcp.flags.syn == 1` | TCP SYN packets (new connections) |

> Tip: Use `tcpdump -w file.pcap` to capture on a remote server (no GUI), then copy the `.pcap` file to your local machine and open it in Wireshark for analysis.

---

## 6. Quick Reference — Troubleshooting

**ICMP types:**

| Type | Name | Used by |
|---|---|---|
| 0 | Echo Reply | `ping` response |
| 3 | Destination Unreachable | Routers/firewalls |
| 8 | Echo Request | `ping` |
| 11 | Time Exceeded | `traceroute` |

**ping:**
```bash
ping -c 4 google.com                # 4 packets
ping -c 4 -i 0.5 google.com         # 4 packets, 0.5s interval
ping -s 100 google.com              # Custom packet size
# Systematic: 127.0.0.1 → gateway → 8.8.8.8 → google.com
```

**traceroute / mtr:**
```bash
traceroute google.com               # Trace path to destination
traceroute -n google.com            # No DNS (faster)
mtr google.com                      # Real-time continuous path + latency
mtr -r -c 100 google.com            # Report mode
```

**netstat / ss:**
```bash
netstat -tulnp                      # Listening ports + process
netstat -anp | grep :80             # What's using port 80
netstat -r                          # Routing table
netstat -s                          # Protocol statistics
ss -tulnp                           # Modern replacement for netstat
ss -t state established             # Only established connections
```

**tcpdump:**
```bash
sudo tcpdump -i eth0                            # Capture all traffic
sudo tcpdump -i eth0 -nn -c 20                 # 20 packets, no DNS
sudo tcpdump -i eth0 host 192.168.1.10         # Filter by host
sudo tcpdump -i eth0 port 80                   # Filter by port
sudo tcpdump -i eth0 icmp                      # ICMP only
sudo tcpdump -i eth0 not port 22               # Exclude SSH
sudo tcpdump -i eth0 -w capture.pcap           # Save to file
sudo tcpdump -r capture.pcap                   # Read saved file
```

**Troubleshooting workflow:**
```
1. ping 127.0.0.1          → Is TCP/IP stack working?
2. ping <gateway>           → Is local network working?
3. ping 8.8.8.8             → Is internet routing working?
4. ping google.com          → Is DNS working?
5. traceroute destination   → Where exactly does it fail?
6. netstat -tulnp           → Is the target service listening?
7. tcpdump                  → What's actually on the wire?
```
