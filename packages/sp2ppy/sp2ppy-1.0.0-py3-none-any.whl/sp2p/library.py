import socket
import threading
import uuid

class Server:
    def __init__(self, host='0.0.0.0', port=1414):
        self.host = host
        self.port = port
        self.clients = {}
        self.lock = threading.Lock()

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen()
        print(f"SP2P Server running on {self.host}:{self.port}")

        while True:
            conn, _ = server.accept()
            threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()

    def handle_client(self, conn):
        addr = uuid.uuid4().hex[:8]
        self.send(conn, f"YOURADDR {addr}")

        with self.lock:
            self.clients[addr] = conn

        try:
            data = conn.recv(1024).decode().strip()
            if not data.startswith("CONN "):
                self.send(conn, "ERR Invalid handshake")
                return conn.close()

            target = data[5:]

            with self.lock:
                if target not in self.clients:
                    self.send(conn, "ERR No such address")
                    self.clients.pop(addr, None)
                    return conn.close()

                peer = self.clients[target]
                self.send(conn, "OK")
                self.send(peer, f"CONNED {addr}")

                threading.Thread(target=self.relay, args=(conn, peer, addr), daemon=True).start()
                threading.Thread(target=self.relay, args=(peer, conn, target), daemon=True).start()
        except:
            conn.close()
            with self.lock:
                self.clients.pop(addr, None)

    def relay(self, sender, receiver, sender_addr):
        try:
            while True:
                data = sender.recv(1024)
                if not data:
                    break
                message = data.decode().strip()
                if ':' in message:
                    parts = message.split(':', 1)
                    possible_addr = parts[0].strip()
                    payload = parts[1].strip()

                    with self.lock:
                        target_conn = self.clients.get(possible_addr)

                    if target_conn:
                        packet = f"{sender_addr}: {payload}"
                        self.send(target_conn, packet)
                        continue
                packet = f"{sender_addr}: {message}"
                receiver.sendall(packet.encode())
        except:
            pass
        finally:
            self.send(receiver, "DISCONN")
            sender.close()
            receiver.close()

    def send(self, conn, msg):
        try:
            conn.sendall((msg + '\n').encode())
        except:
            pass


class Client:
    def __init__(self, server_host='127.0.0.1', server_port=1414):
        self.server_host = server_host
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = None
        self.peer_address = None

    def connect(self):
        self.sock.connect((self.server_host, self.server_port))
        threading.Thread(target=self.listen, daemon=False).start()

    def send(self, message):
        self.sock.sendall((message + '\n').encode())

    def listen(self):
        while True:
            data = self.sock.recv(1024)
            if not data:
                self.on_disconnected()
                break
            for line in data.decode().splitlines():
                self.handle_packet(line.strip())

    def handle_packet(self, packet):
        if packet.startswith("YOURADDR "):
            self.address = packet.split()[1]
            self.on_ready(self.address)
        elif packet == "OK":
            self.on_connected()
        elif packet.startswith("CONNED "):
            self.peer_address = packet.split()[1]
            self.on_peer_connected(self.peer_address)
        elif packet == "DISCONN":
            self.on_disconnected()
        elif ":" in packet:
            sender, msg = packet.split(":", 1)
            self.on_message(sender.strip(), msg.strip())

    def on_ready(self, address):
        print(f"Connected. Your address: {address}")

    def on_connected(self):
        print("Successfully connected to peer.")

    def on_peer_connected(self, peer_address):
        print(f"Peer {peer_address} connected to you.")

    def on_disconnected(self):
        print("Peer disconnected.")

    def on_message(self, sender_address, message):
        print(f"{sender_address}: {message}")
