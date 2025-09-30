import socket
import threading
from datetime import datetime
from pathlib import Path
from utils import process_file

HOST = "127.0.0.1"
PORT = 3333
lock = threading.Lock()
BACKUP_DIR = Path("backups")
BACKUP_DIR.mkdir(exist_ok=True)

def handle_client(conn, addr):
    print(f"[+] Conexão com {addr}")
    file_path = None
    try:
        size_data = conn.recv(1024).decode()
        file_size = int(size_data.strip())
        
        filename = conn.recv(1024).decode().strip()
        if not filename:
            return
        
        file_path = BACKUP_DIR / filename

        bytes_received = 0
        with open(file_path, "wb") as file:
            while bytes_received < file_size:
                data = conn.recv(min(file_size - bytes_received, 4096))
                if not data:
                    break
                file.write(data)
                bytes_received += len(data)
        
        compressed = process_file(file_path)

        with lock:
            with open("backup.log", "a") as log:
                log.write(f"{datetime.now()} - {addr} - {filename} -> {compressed}\n")
        
        conn.sendall(f"Arquivo {filename} armazenado e comprimido.".encode())
    
    except Exception as e:
        print(f"[ERRO] {addr}: {e}")
    finally:
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Servidor de backup rodando em {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[INFO] Clients ativos: {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()