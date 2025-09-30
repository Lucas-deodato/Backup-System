import socket
import sys
from pathlib import Path

HOST = "127.0.0.1"
PORT = 3333

def send_file(file_path):
    file = Path(file_path)
    
    if not file.exists():
        print("File not found.")
        return
    
    file_size = file.stat().st_size

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        s.sendall(str(file_size).encode().ljust(1024)) 

        s.sendall(file.name.encode().ljust(1024))

        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                s.sendall(chunk)
            
        # Fecha o envio, 
        s.shutdown(socket.SHUT_WR)

        response = s.recv(1024).decode()
        print("[Servidor]:", response)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 client.py <file path>.")
    else:
        send_file(sys.argv[1])