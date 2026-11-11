import socket
import threading
import sys

active_connections = 0
lock = threading.Lock()

def handle_client(client_socket, address):
    global active_connections
    with lock:
        active_connections += 1
    try:
        data = client_socket.recv(1024)
        if data:
            response = b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK"
            client_socket.sendall(response)
    finally:
        with lock:
            active_connections -= 1
        client_socket.close()

def run_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"[*] TCP Server successfully started and listening on port {port}...")

    while True:
        client_sock, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_sock, addr)).start()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8001
    run_server(port)
