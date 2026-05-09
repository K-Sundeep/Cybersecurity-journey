# Linux — Routing

---

## 1. What is a Router?

A **router** is a networking device whose primary job is to **forward packets between different networks**. You almost certainly have one in your home — it connects your local devices to the internet.

**Think of it like a post office:** When you send a letter, the post office looks at the destination address, decides which route will get it there, and forwards it along. A router does the same thing for network packets.

**How a router is physically connected:**
- **LAN ports** — connects to your local devices (computers, phones, printers) via Ethernet or Wi-Fi
- **WAN port** — connects to the wider internet (your ISP's network)

**Every packet passes through the router.** Whether you're loading a webpage, sending an email, or streaming video — every piece of data you send or receive travels through the router. The router inspects each packet's destination IP address and decides where to send it next.

### How a router makes decisions

Routers use a **routing table** — a set of rules that tells it: "to reach network X, send packets to router Y." If there's no specific rule for a destination, it uses the **default route**, which typically points to the internet.

### Hops

As packets travel across networks, their journey is measured in **hops**. A hop is one step where a packet passes through a router. If a packet goes through two routers to get from Host A to Host B, the path is **2 hops** long.

### Flooding vs Routing

**Flooding** — an older, inefficient method. If a router doesn't know where to send a packet, it sends copies out on every port except the one it arrived on, hoping one path reaches the destination. Generates massive unnecessary traffic.

**Routing** — the modern approach. Routers maintain routing tables and make intelligent forwarding decisions based on rules. Much more efficient.

---

## 2. Routing Table

The **routing table** contains rules that determine where network packets are sent. Every time your system needs to send a packet, it checks the routing table first to find the right path.

**Viewing the routing table:**

```bash
sudo route -n                   # Classic command (numeric, no DNS lookup)
ip route                        # Modern command (preferred)
ip route show                   # Same as above
```

**Sample `route -n` output:**
```
Kernel IP routing table
Destination     Gateway         Genmask         Flags  Metric  Ref  Use  Iface
0.0.0.0         192.168.224.2   0.0.0.0         UG     0       0    0    eth0
192.168.224.0   0.0.0.0         255.255.255.0   U      1       0    0    eth0
```

### Routing table columns explained

| Column | Meaning |
|---|---|
| **Destination** | The target network or host. `0.0.0.0` = default route (unknown destination) |
| **Gateway** | The router to send the packet to. `0.0.0.0` = directly connected (no gateway needed) |
| **Genmask** | The subnet mask for the destination network |
| **Flags** | Status of the route (see below) |
| **Metric** | Cost of the route — lower is preferred when multiple routes exist |
| **Iface** | Network interface to send the packet out of |

**Flags:**

| Flag | Meaning |
|---|---|
| `U` | Route is **U**p and active |
| `G` | Route uses a **G**ateway (router) |
| `UG` | Route is active and points to a gateway |
| `H` | Route is to a single **H**ost, not a network |

### Reading the example output

**Row 1:** `0.0.0.0` destination with Gateway `192.168.224.2`
- This is the **default route** — for any destination Nmap doesn't have a specific rule for
- All unknown traffic goes to the gateway `192.168.224.2` (your router) via `eth0`

**Row 2:** `192.168.224.0` destination with no gateway (`0.0.0.0`)
- Any packet going to the `192.168.224.x` network goes **directly** via `eth0`
- No router needed — it's the local network

**In practice:** If you're `192.168.224.5` and want to reach `192.168.224.7` → use eth0 directly (same network). If you want to reach `151.123.43.6` → no specific rule → use default route → send to gateway `192.168.224.2`.

### Managing the routing table

```bash
# Add a route
sudo ip route add 192.168.2.0/24 via 10.0.0.1           # Route to network via gateway
sudo ip route add default via 192.168.1.1                # Add default gateway

# Delete a route
sudo ip route delete 192.168.2.0/24                      # Delete specific route
sudo ip route delete default                             # Remove default gateway

# View with ip route
ip route
# Output: default via 192.168.1.1 dev eth0
#         192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.5
```

---

## 3. Path of a Packet

Understanding how a packet actually travels from source to destination is fundamental to networking. The path involves different processes depending on whether the destination is on the **same local network** or an **external network**.

### Scenario 1 — Same local network

When two devices on the same subnet communicate, they don't need a router.

**Step-by-step:**
1. Host A wants to send a packet to Host B (both on `192.168.1.0/24`)
2. Host A checks: is `192.168.1.50` on my subnet? → Yes → no router needed
3. Host A needs Host B's **MAC address** (for the Ethernet frame) but only knows the IP
4. Host A sends an **ARP broadcast**: "Who has 192.168.1.50? Tell me your MAC!"
5. Host B replies with its MAC address
6. Host A builds the frame with Host B's MAC and sends it directly
7. Host B receives the packet

```
Host A ──── ARP broadcast ──────────────→ All hosts
Host A ←─── ARP reply (B's MAC) ──────── Host B
Host A ──── Packet (src:A MAC, dst:B MAC) → Host B (direct delivery)
```

**Key point:** Source and destination **IP addresses never change** throughout the journey. Only MAC addresses change at each hop.

### Scenario 2 — Different network (external destination)

When the destination is outside the local network, routers must be involved.

**Step-by-step:**
1. Host A wants to send a packet to `8.8.8.8` (external — Google's DNS)
2. Host A checks: is `8.8.8.8` on my subnet (`192.168.1.0/24`)? → No → need a router
3. Host A checks its routing table → no specific route → use **default gateway** (`192.168.1.1`)
4. Host A uses ARP to get the **gateway's MAC address** (if not already cached)
5. Host A sends the packet:
   - Source IP: Host A's IP (stays the same all journey)
   - Destination IP: `8.8.8.8` (stays the same all journey)
   - Source MAC: Host A's MAC
   - Destination MAC: **Router's MAC** (changes at every hop)
6. Router receives the packet, checks its own routing table, finds the next hop
7. Router **rewrites the MAC addresses**: source MAC = router's MAC, destination MAC = next router's MAC
8. This repeats at every router along the path
9. Final router delivers to the destination host via ARP

```
Host A ──── Packet (srcIP:A, dstIP:8.8.8.8, srcMAC:A, dstMAC:Router1) ──→ Router1
Router1 ──── Packet (srcIP:A, dstIP:8.8.8.8, srcMAC:R1, dstMAC:Router2) ──→ Router2
Router2 ──── Packet (srcIP:A, dstIP:8.8.8.8, srcMAC:R2, dstMAC:Dest) ────→ Destination
```

**Key rule: IP addresses are permanent end-to-end. MAC addresses change at every hop.**

---

## 4. Routing Protocols

Routers need to know about other networks to forward packets correctly. There are two ways this information can be populated:

**Static routing** — An administrator manually enters every route. Simple but doesn't scale — impractical for large networks. Doesn't adapt to failures automatically.

**Dynamic routing** — Routers automatically discover and share information about networks using **routing protocols**. They talk to each other, exchange routing information, and build their routing tables automatically. They also adapt when links fail.

### Two categories of routing protocols

| Category | Abbreviation | Used for | Examples |
|---|---|---|---|
| **Interior Gateway Protocols** | IGP | Routing **within** an Autonomous System (single organization) | RIP, OSPF, EIGRP |
| **Exterior Gateway Protocols** | EGP | Routing **between** Autonomous Systems (between organizations/ISPs) | BGP |

### What is an Autonomous System (AS)?

An **Autonomous System (AS)** is a collection of IP networks under the control of a single organization (like a company, university, or ISP) that presents a unified routing policy to the internet. Each AS is identified by an **ASN (Autonomous System Number)**.

- Your university's campus network = one AS
- Your ISP's network = one AS
- Google's global network = one AS

IGP protocols handle routing **inside** an AS. BGP handles routing **between** ASes.

### Convergence

**Convergence** is when all routers in a network agree on the same routing information. When a link goes down or a new network is added, routers must update and share new information until they all have a consistent view. The time it takes to reach this consistent state = **convergence time**. Faster convergence = network recovers from failures more quickly.

---

## 5. Distance Vector Protocols

**Distance vector protocols** make routing decisions based on **distance** (usually measured in hops) and **direction** (which interface/neighbor to send to). Each router only knows what its directly connected neighbors have told it — like navigating by asking each person you meet which way to go.

**How it works:**
- Each router maintains a routing table with distances to all known networks
- Periodically (e.g., every 30 seconds), each router sends its **entire routing table** to its directly connected neighbors
- Neighbors update their own tables based on received information
- This process repeats until all routers converge

**Analogy:** Imagine you're in a city you don't know. You ask the nearest person: "How far to the airport?" They say "3 km east." You don't know the actual road — you just know the direction and distance from your neighbor's perspective.

### RIP — Routing Information Protocol

**RIP** is the classic, simplest distance vector protocol.

| Feature | RIP |
|---|---|
| Metric | **Hop count** — number of routers between source and destination |
| Maximum hops | **15** — a hop count of 16 = infinity (unreachable). Limits RIP to small networks |
| Update interval | Every **30 seconds** — sends full routing table to neighbors |
| Version | RIPv1 (classful, no subnet info) / RIPv2 (classless, includes subnet masks) |
| Convergence | **Slow** — can take minutes |

**Why hop count is a crude metric:**
RIP always picks the route with fewest hops, even if a 2-hop path uses slow 56Kbps links and a 3-hop path uses fast gigabit links. It has no concept of link speed or bandwidth.

**The count-to-infinity problem:**
A known weakness of distance vector. If a network goes down, routers may keep incrementing hop counts and sending bad routes to each other, slowly counting up to 15 (infinity) before realizing the network is unreachable. This causes slow convergence.

**RIPv1 vs RIPv2:**

| | RIPv1 | RIPv2 |
|---|---|---|
| Subnet support | Classful only (no subnet masks) | ✅ Classless (includes subnet mask) |
| Authentication | None | ✅ Supports authentication |
| Multicast | Broadcasts updates | ✅ Multicasts to 224.0.0.9 |

### EIGRP — Enhanced Interior Gateway Routing Protocol

A Cisco-proprietary protocol that is considered a "hybrid" — has features of both distance vector and link state protocols.

- Uses **bandwidth** and **delay** as its metric (much smarter than hop count)
- Sends **partial updates** (only changes, not full table) — more efficient
- Forms neighbor adjacencies like link-state protocols
- **Fast convergence** using DUAL (Diffusing Update Algorithm)

---

## 6. Link State Protocols

**Link state protocols** take a completely different approach — each router builds a **complete map of the entire network topology** and calculates the best path itself using Dijkstra's shortest path algorithm.

**How it works:**
- Each router discovers its directly connected neighbors and the cost of each link
- Each router creates a **Link State Advertisement (LSA)** — a packet containing its connections and link costs
- Routers **flood** LSAs to every router in the network (not just neighbors)
- Every router receives every other router's LSA and builds a complete **topology database**
- Each router independently runs **Dijkstra's algorithm** (SPF — Shortest Path First) on the topology database to calculate the best path to every network
- Results are placed in the routing table

**Analogy:** Instead of asking each person directions, you obtain a complete map of the city and calculate the best route yourself.

**Key advantages over distance vector:**
- Much **faster convergence** — updates are triggered by changes (not periodic)
- No routing loops — each router has the complete picture
- Scales better to large networks

**Key disadvantage:**
- More **memory and CPU** required — storing the topology database and running SPF

### OSPF — Open Shortest Path First

**OSPF** is the most widely used link state IGP. It's an open standard (not vendor-specific).

| Feature | OSPF |
|---|---|
| Algorithm | **Dijkstra / SPF** (Shortest Path First) |
| Metric | **Cost** — based on link bandwidth (lower cost = faster link = preferred) |
| Updates | **Triggered** — only when something changes (no periodic full table dumps) |
| Convergence | **Fast** |
| Scalability | Uses **areas** to organize large networks |
| Standard | Open (works on all vendors) |

**OSPF Areas:**
OSPF networks are divided into **areas** to limit the scope of flooding and reduce the size of the topology database. All areas must connect to **Area 0** (the backbone area).

```
Area 0 (Backbone) ──── Area 1
                  ──── Area 2
                  ──── Area 3
```

**OSPF cost calculation:**
```
Cost = Reference bandwidth / Interface bandwidth
Default reference bandwidth = 100 Mbps
Fast Ethernet (100 Mbps): cost = 100/100 = 1
Ethernet (10 Mbps): cost = 100/10 = 10
Serial link (1.544 Mbps): cost = 100/1.544 ≈ 64
```

Lower cost = better path. OSPF automatically prefers faster links.

**OSPF router types:**
- **Internal router** — all interfaces in the same area
- **ABR (Area Border Router)** — connects two or more areas
- **ASBR (Autonomous System Border Router)** — connects OSPF to other routing domains (e.g. BGP)
- **Backbone router** — at least one interface in Area 0

### IS-IS — Intermediate System to Intermediate System

Another link state protocol, similar to OSPF. Also uses Dijkstra/SPF. Preferred by large ISPs and service providers. Uses a two-level hierarchy (Level 1 = intra-area, Level 2 = inter-area).

---

## 7. Border Gateway Protocol

**BGP (Border Gateway Protocol)** is the routing protocol that powers the entire internet. It handles routing between Autonomous Systems — when your traffic needs to travel from your ISP's network across the globe to reach a destination.

BGP is classified as a **path vector protocol** — a variant of distance vector that uses the complete **AS path** (list of all ASes the route passes through) as its metric instead of simple hop count.

### Why BGP is different from IGPs

| Feature | IGPs (RIP, OSPF) | BGP |
|---|---|---|
| Scope | Within one AS | Between ASes |
| Goal | Best path by metric | Policy-based routing |
| Transport | Own protocol | **TCP port 179** |
| Speed | Fast convergence | Slow — path exploration takes time |
| Focus | Performance | **Policy and business relationships** |

### BGP path selection

BGP doesn't just pick the shortest path — it chooses paths based on **policies** and **path attributes**. ISPs use these to implement business agreements (e.g., "prefer sending traffic through our partner network over competitors").

**Key BGP path attributes:**

| Attribute | Description |
|---|---|
| **AS-PATH** | List of all AS numbers the route has passed through. Shorter = preferred (loop prevention — if your own AS is in the path, reject it) |
| **NEXT-HOP** | IP address of the next router to reach the destination |
| **LOCAL-PREF** | Used within an AS to prefer one exit point over another (higher = preferred) |
| **MED** | Multi-Exit Discriminator — hints to external peers which path to use into your AS |
| **ORIGIN** | How the route was learned (IGP, EGP, or incomplete) |

### BGP types

| Type | Description |
|---|---|
| **iBGP** (internal BGP) | BGP sessions between routers **within the same AS** |
| **eBGP** (external BGP) | BGP sessions between routers **in different ASes** — this is how the internet works |

### BGP and the internet

Every major ISP, cloud provider (AWS, Google Cloud, Azure), and large organization has its own AS number. BGP is how they all connect and share routing information with each other. When you type a URL, your packet may traverse dozens of different ASes — each handoff is guided by BGP.

```
Your PC → Your ISP (AS 12345)
            ↓ eBGP
         Transit ISP (AS 3356)
            ↓ eBGP
         Google's AS (AS 15169)
            ↓ iBGP internally
         Google's server
```

### BGP on Linux

```bash
# BGP is typically implemented with routing daemons like FRRouting (FRR) or Quagga
sudo apt install frr                    # Install FRRouting
sudo systemctl status frr               # Check status
vtysh                                   # Enter the routing CLI (like Cisco IOS)
```

---

## 8. Quick Reference — Routing

**View and manage routing table:**
```bash
ip route                                    # View routing table (modern)
sudo route -n                              # Classic (numeric)
sudo ip route add 192.168.2.0/24 via 10.0.0.1   # Add route
sudo ip route add default via 192.168.1.1         # Set default gateway
sudo ip route delete 192.168.2.0/24              # Delete route
```

**Routing protocol summary:**

| Protocol | Type | Metric | Scope | Convergence |
|---|---|---|---|---|
| **RIP** | Distance Vector | Hop count (max 15) | IGP — small networks | Slow |
| **RIPv2** | Distance Vector | Hop count + VLSM | IGP — small networks | Slow |
| **EIGRP** | Hybrid | Bandwidth + Delay | IGP — Cisco | Fast |
| **OSPF** | Link State | Cost (bandwidth) | IGP — any size | Fast |
| **IS-IS** | Link State | Cost | IGP — ISPs | Fast |
| **BGP** | Path Vector | AS-PATH + policy | EGP — internet | Slow |

**Routing types:**

| Type | How configured | Adapts to failures |
|---|---|---|
| **Static** | Manually by admin | ❌ No |
| **Dynamic** | Automatically via protocols | ✅ Yes |

**Key concepts:**

| Term | Meaning |
|---|---|
| **Hop** | One router traversal on the path |
| **AS** | Autonomous System — network under one organization |
| **IGP** | Interior — routing within one AS |
| **EGP** | Exterior — routing between ASes |
| **Convergence** | When all routers agree on routing information |
| **Default route** | Where to send packets with no specific match |
| **Metric** | Cost used to compare routes — lower usually preferred |
