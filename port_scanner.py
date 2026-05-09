import socket
import threading
from datetime import datetime

# Target
target = input("Enter target IP or hostname: ")
print(f"\nScanning target: {target}")
print(f"Time started: {datetime.now()}")
print("-" * 50)

# Lock for thread-safe printing
print_lock = threading.Lock()

def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            try:
                banner = sock.recv(1024).decode().strip()
            except:
                banner = ""
            with print_lock:
                if banner:
                    print(f"[+] Port {port} OPEN | Banner: {banner}")
                else:
                    print(f"[+] Port {port} OPEN")
        sock.close()
    except socket.error:
        pass

# Thread list
threads = []

# Scan ports 1-1024
for port in range(1, 1025):
    thread = threading.Thread(target=scan_port, args=(port,))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

print("-" * 50)
print("Scan complete.")
