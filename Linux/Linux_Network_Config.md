# Linux — Network Config

---

## 1. Network Interfaces

A **network interface** is the connection point between the kernel's software networking stack and the physical (or virtual) network hardware. It allows your OS to send and receive data over a network.

**Interface naming conventions:**

| Name | Type |
|---|---|
| `eth0`, `eth1` | First, second Ethernet (wired) interface |
| `enp0s3`, `enp2s0` | Predictable Ethernet names (modern systems) |
| `wlan0`, `wlp3s0` | Wireless interface |
| `lo` | Loopback — virtual interface representing your own machine |
| `tun0`, `tap0` | Tunnel interfaces (VPN) |
| `docker0`, `virbr0` | Virtual bridge interfaces |

**The loopback interface (`lo`)** is special — it always has the address `127.0.0.1` and represents your own computer. Used to connect to services running locally without going through physical hardware.

**An interface can be in `up` (active) or `down` (inactive) state.**

### ifconfig — Classic tool

```bash
ifconfig                    # Show all active interfaces
ifconfig -a                 # Show all interfaces including inactive ones
ifconfig eth0               # Show specific interface
```

**Sample `ifconfig` output:**
```
eth0  Link encap:Ethernet  HWaddr 1d:3a:32:24:4d:ce
      inet addr:192.168.1.129  Bcast:192.168.1.255  Mask:255.255.255.0
      inet6 addr: fd60::21c:29ff:fe63:5cdc/64  Scope:Link
      UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
```

- `HWaddr` — MAC address
- `inet addr` — IPv4 address
- `Bcast` — broadcast address
- `Mask` — subnet mask
- `inet6 addr` — IPv6 address
- `MTU` — Maximum Transmission Unit (max packet size, bytes)
- `UP` — interface is active

### ip — Modern replacement for ifconfig

`ip` is the modern, preferred tool for managing network interfaces. More powerful and consistent than `ifconfig`.

```bash
# View interfaces
ip a                            # Show all interfaces with addresses (short for ip addr show)
ip addr show                    # Same as above
ip addr show eth0               # Show specific interface only
ip link show                    # Show link-layer info (no IP addresses)
ip link show eth0               # Show specific interface link info

# Bring interfaces up and down
sudo ip link set eth0 up        # Bring interface up
sudo ip link set eth0 down      # Bring interface down

# Assign a static IP address
sudo ip addr add 192.168.1.10/24 dev eth0       # Add IP to interface
sudo ip addr del 192.168.1.10/24 dev eth0       # Remove IP from interface
sudo ip addr flush dev eth0                     # Remove ALL addresses from interface
```

**Sample `ip a` output:**
```
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default
    link/ether 00:16:3e:0f:23:a5 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.129/24 brd 192.168.1.255 scope global dynamic eth0
       valid_lft 86391sec preferred_lft 86391sec
    inet6 fd60::21c:29ff:fe63:5cdc/64 scope link
       valid_lft forever preferred_lft forever
```

> **Note:** `ip` and `ifconfig` configure the **live state** only. Changes are lost on reboot. To make settings persistent, you must edit configuration files.

### Making network config persistent

**Debian/Ubuntu — `/etc/network/interfaces`:**
```
# Static IP
auto eth0
iface eth0 inet static
    address 192.168.1.129
    netmask 255.255.255.0
    gateway 192.168.1.1
    dns-nameservers 8.8.8.8 8.8.4.4

# DHCP
auto eth0
iface eth0 inet dhcp
```

**Ubuntu 18.04+ — Netplan (`/etc/netplan/01-netcfg.yaml`):**
```yaml
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: true
```

```bash
sudo netplan apply              # Apply netplan configuration
```

---

## 2. route

The **routing table** tells the kernel where to send packets based on their destination IP. Every packet that leaves your machine is matched against the routing table to decide which interface to use and which gateway to forward it through.

**Viewing the routing table:**

```bash
ip route                        # Show routing table (modern — preferred)
ip route show                   # Same as above
route -n                        # Classic tool (shows numeric IPs, no DNS lookups)
netstat -r                      # Alternative view of routing table
```

**Sample `ip route` output:**
```
default via 192.168.1.1 dev eth0 proto dhcp src 192.168.1.129 metric 100
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.129
```

| Entry | Meaning |
|---|---|
| `default via 192.168.1.1` | Default gateway — where to send packets with no specific route |
| `dev eth0` | Use the eth0 interface |
| `192.168.1.0/24 dev eth0` | The 192.168.1.x network is directly reachable via eth0 |
| `proto kernel` | This route was added automatically by the kernel |
| `metric 100` | Route priority — lower metric = preferred route |

### Managing routes with `ip route`

```bash
# Add routes
sudo ip route add 192.168.2.0/24 via 10.0.0.1         # Add route to network via gateway
sudo ip route add 192.168.2.0/24 via 10.0.0.1 dev eth0 # Specify interface too
sudo ip route add default via 192.168.1.1               # Add/change default gateway

# Delete routes
sudo ip route delete 192.168.2.0/24 via 10.0.0.1       # Delete specific route
sudo ip route delete 192.168.2.0/24                    # Delete by destination only
sudo ip route delete default                            # Remove default gateway

# Replace (add or update if exists)
sudo ip route replace default via 192.168.1.1
```

### Legacy `route` command

```bash
sudo route add -net 192.168.2.0 netmask 255.255.255.0 gw 10.0.0.1   # Add route
sudo route del -net 192.168.2.0 netmask 255.255.255.0                 # Delete route
sudo route add default gw 192.168.1.1                                 # Add default gateway
```

> `ip route` is the modern standard. Use it in preference to the legacy `route` command.

**How routing decisions work:**
```
Packet arrives → check routing table → match most specific route
                                    → no match? → use default gateway
                                    → no default gateway? → packet dropped
```

---

## 3. dhclient

`dhclient` is the **DHCP client** that automatically obtains IP address, subnet mask, gateway, and DNS configuration from a DHCP server.

**How dhclient works:**
1. Starts up at boot
2. Reads `/etc/dhcp/dhclient.conf` for a list of network interfaces and options
3. For each listed interface, runs the DHCP DORA process to get a lease
4. Reads `/var/lib/dhcp/dhclient.leases` to check for existing leases (avoids requesting a new IP unnecessarily across reboots)

**Key files:**

| File | Purpose |
|---|---|
| `/etc/dhcp/dhclient.conf` | Configuration — which interfaces to manage, options to request |
| `/var/lib/dhcp/dhclient.leases` | Stores all current and past DHCP leases |

```bash
# Obtain a DHCP lease for an interface
sudo dhclient eth0              # Request IP from DHCP server for eth0

# Release and renew
sudo dhclient -r eth0           # Release the current DHCP lease
sudo dhclient eth0              # Get a fresh lease after releasing

# Flush existing IP first, then get new one
sudo ip addr flush dev eth0     # Remove all current IPs
sudo dhclient eth0              # Obtain fresh DHCP lease

# Verbose mode — see DORA process
sudo dhclient -v eth0
```

**Sample lease file entry (`/var/lib/dhcp/dhclient.leases`):**
```
lease {
  interface "eth0";
  fixed-address 192.168.1.129;
  option subnet-mask 255.255.255.0;
  option routers 192.168.1.1;
  option domain-name-servers 8.8.8.8, 8.8.4.4;
  renew 2 2024/01/30 06:00:00;
  rebind 2 2024/01/30 12:00:00;
  expire 2 2024/01/30 14:00:00;
}
```

> On most modern Linux systems with NetworkManager, you won't need to run `dhclient` manually — NetworkManager handles it. Use `dhclient` directly on servers or minimal systems without NetworkManager.

---

## 4. Network Manager

**NetworkManager** is a service that manages network hardware and connections. On desktop/GUI systems it appears as a network icon in the taskbar. On startup, it inventories hardware, scans for available connections, and activates them automatically.

**Check if NetworkManager is running:**
```bash
systemctl status NetworkManager
```

### nmcli — Command-line interface for NetworkManager

`nmcli` is the primary CLI tool for interacting with NetworkManager. Essential for server administration and scripting.

```bash
# View status and devices
nmcli                               # General status overview
nmcli general status                # NetworkManager overall state
nmcli device status                 # List all devices and their states
nmcli device show eth0              # Detailed info about a specific device

# View connections
nmcli connection show               # List all saved connections
nmcli connection show --active      # Active connections only
nmcli connection show "Wired connection 1"   # Details of a specific connection

# Connect / disconnect
nmcli device connect eth0           # Activate a device
nmcli device disconnect eth0        # Deactivate a device
nmcli connection up "Wired connection 1"     # Bring up a connection
nmcli connection down "Wired connection 1"   # Bring down a connection
```

**Configure a static IP using nmcli:**
```bash
# Modify an existing connection
nmcli connection modify "Wired connection 1" \
    ipv4.method manual \
    ipv4.addresses 192.168.1.100/24 \
    ipv4.gateway 192.168.1.1 \
    ipv4.dns "8.8.8.8 8.8.4.4"

nmcli connection up "Wired connection 1"    # Apply changes
```

**Configure DHCP using nmcli:**
```bash
nmcli connection modify "Wired connection 1" ipv4.method auto
nmcli connection up "Wired connection 1"
```

**Create a new connection:**
```bash
nmcli connection add type ethernet ifname eth0 con-name "MyConnection" \
    ipv4.method manual \
    ipv4.addresses 192.168.1.50/24 \
    ipv4.gateway 192.168.1.1
```

**Delete a connection:**
```bash
nmcli connection delete "MyConnection"
```

### NetworkManager config files

NetworkManager stores connection profiles in:
```
/etc/NetworkManager/system-connections/
```

Each connection is a `.nmconnection` file. You can view and edit them directly, though `nmcli` or `nmtui` is preferred.

### nmtui — Text-based UI (easier alternative)

```bash
nmtui                   # Opens a simple text menu for managing connections
```
A friendly menu-driven interface — easier for beginners than `nmcli`.

---

## 5. arp

**ARP (Address Resolution Protocol)** resolves IP addresses to MAC addresses on the local network. When sending a packet to another device on the same subnet, your computer needs the destination's MAC address to build the Ethernet frame — ARP finds it.

### The ARP cache

Before sending an ARP request over the network, the system always checks its **local ARP cache** first — a table of known IP→MAC mappings stored in memory.

```bash
arp                             # Show ARP cache (classic)
arp -n                          # Show without DNS resolution (numeric IPs)
ip neigh                        # Modern equivalent — show neighbour table
ip neigh show                   # Same as above
```

**Sample `arp` output:**
```
Address          HWtype  HWaddress          Flags  Mask  Iface
192.168.22.1     ether   00:12:24:fc:12:cc  C            eth0
192.168.22.254   ether   00:12:45:f2:84:64  C            eth0
```

- `Address` — IP address
- `HWaddress` — resolved MAC address
- `Flags` — `C` = complete (valid entry)
- `Iface` — interface it was learned on

> The ARP cache **starts empty** on boot and fills up as your machine sends packets to other hosts.

### The ARP process (when IP is not in cache)

```
1. Source creates an Ethernet frame with an ARP request packet
2. Source broadcasts the frame to the entire local network
   "Who has IP 192.168.1.1? Tell 192.168.1.100"
3. Device with that IP replies with its MAC address
   "192.168.1.1 is at 00:12:24:fc:12:cc"
4. Source adds the IP→MAC mapping to its ARP cache
5. Source sends the original packet to that MAC address
```

### Managing the ARP cache

```bash
# Add a static ARP entry (permanent mapping)
sudo arp -s 192.168.1.50 00:11:22:33:44:55
sudo ip neigh add 192.168.1.50 lladdr 00:11:22:33:44:55 dev eth0 nud permanent

# Delete an ARP entry
sudo arp -d 192.168.1.50
sudo ip neigh del 192.168.1.50 dev eth0

# Flush the entire ARP cache
sudo ip neigh flush all
sudo ip neigh flush dev eth0            # Flush only for one interface
```

### Practical example — populate and view ARP cache

```bash
# 1. Find your default gateway
ip route | grep default
# → default via 192.168.1.1 dev eth0

# 2. Ping the gateway to generate traffic (populates ARP cache)
ping -c 1 192.168.1.1

# 3. View the ARP cache
arp -n
# → 192.168.1.1  ether  00:12:24:fc:12:cc  C  eth0
```

---

## 6. Quick Reference — Network Config

**View interface info:**
```bash
ip a                            # All interfaces (modern)
ip a show eth0                  # Specific interface
ifconfig                        # Classic
ifconfig -a                     # All including inactive
ip link show                    # Link-layer info only
```

**Configure interfaces:**
```bash
sudo ip link set eth0 up/down               # Bring up/down
sudo ip addr add 192.168.1.10/24 dev eth0   # Add static IP
sudo ip addr del 192.168.1.10/24 dev eth0   # Remove IP
sudo ip addr flush dev eth0                 # Remove all IPs
```

**Routing:**
```bash
ip route                                    # View routing table
sudo ip route add default via 192.168.1.1   # Set default gateway
sudo ip route add 10.0.0.0/8 via 172.16.1.1 # Add specific route
sudo ip route delete 10.0.0.0/8             # Delete route
```

**DHCP:**
```bash
sudo dhclient eth0              # Get IP from DHCP
sudo dhclient -r eth0           # Release DHCP lease
sudo dhclient -v eth0           # Verbose DHCP request
sudo ip addr flush dev eth0 && sudo dhclient eth0   # Full refresh
```

**NetworkManager:**
```bash
nmcli                           # General status
nmcli device status             # List devices and states
nmcli connection show           # Saved connections
nmcli device connect eth0       # Activate device
nmcli device disconnect eth0    # Deactivate device
nmtui                           # Text UI (easier)
systemctl status NetworkManager # Check service status
```

**ARP:**
```bash
arp -n                          # View ARP cache (numeric)
ip neigh                        # Modern ARP cache view
ip neigh flush all              # Clear ARP cache
sudo arp -s IP MAC              # Add static ARP entry
sudo arp -d IP                  # Delete ARP entry
ping -c 1 192.168.1.1 && arp -n # Ping then check ARP cache
```
