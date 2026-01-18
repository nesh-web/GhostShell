import socket
import time

target_ip = "127.0.0.1"
target_port = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_ip, target_port))

# 1. Read Banner
print(client.recv(4096).decode(), end="")

# 2. Send Fake Credentials
client.send(b"admin\n")
time.sleep(0.1)
client.send(b"password123\n")

# 3. Read Login Success Message
print(client.recv(4096).decode(), end="")
print(client.recv(4096).decode(), end="") # Prompt

# 4. Run 'ls' command
print("\n[+] Sending malicious command: ls")
client.send(b"ls\n")
print(client.recv(4096).decode()) # Output

client.close()