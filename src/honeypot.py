import socket
import logging
import threading
from datetime import datetime

# --- CONFIGURATION ---
HOST = '0.0.0.0'  
PORT = 9999       
LOG_FILE = 'logs/intrusions.log'

# --- 1. SETUP LOGGING ---
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- 2. FAKE FILE SYSTEM ---
FAKE_FILES = "sys_config.conf  passwords.txt  database.db\n"

def handle_intruder(conn, addr):
    print(f"[!] ALERT: Connection from {addr}")
    logging.info(f"CONNECTION: New session from {addr}")

    try:
        # --- PHASE A: THE TRAP (Login Simulation) ---
        conn.sendall(b"Ubuntu 22.04 LTS (GNU/Linux 5.15.0-91-generic x86_64)\n")
        conn.sendall(b"server-01 login: ")
        
        username = conn.recv(1024).decode().strip()
        
        conn.sendall(b"Password: ")
        password = conn.recv(1024).decode().strip()
        
        # LOG CREDENTIALS
        print(f"[*] CAPTURED: User={username} | Pass={password}")
        logging.info(f"CREDENTIALS: User={username} | Pass={password}")

        # --- PHASE B: THE ILLUSION (Fake Shell) ---
        conn.sendall(b"\nLast login: Mon Jan 15 10:23:11 2026 from 192.168.1.50\n")
        
        while True:
            conn.sendall(b"root@server-01:~# ")
            command = conn.recv(1024).decode().strip()
            
            if not command: break 
            
            logging.info(f"COMMAND: {addr} executed '{command}'")

            if command == "ls":
                response = FAKE_FILES
            elif command == "pwd":
                response = "/root\n"
            elif command == "whoami":
                response = "root\n"
            elif command == "exit":
                break
            else:
                response = f"bash: {command}: command not found\n"
            
            conn.sendall(response.encode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] GhostShell Active. Listening on port {PORT}...")

    while True:
        conn, addr = server.accept()
        t = threading.Thread(target=handle_intruder, args=(conn, addr))
        t.start()

if __name__ == "__main__":
    start_server()