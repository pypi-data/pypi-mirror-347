from .library import Client

class MyClient(Client):
    def on_ready(self, address):
        print(f"[SP2P] Your address is: {address}")
        # Пример: попытка подключиться к другому адресу
        target = input("Enter target address to connect: ").strip()
        self.send(f"CONN {target}")

    def on_connected(self):
        print("[SP2P] Connected to peer. Type messages to send.")

        def send_loop():
            while True:
                msg = input()
                if msg:
                    self.send(msg)

        import threading
        threading.Thread(target=send_loop, daemon=True).start()

    def on_peer_connected(self, peer_address):
        print(f"[SP2P] Peer {peer_address} connected to you.")

    def on_disconnected(self):
        print("[SP2P] Peer disconnected. Exiting.")
        exit()

    def on_message(self, sender_address, message):
        print(f"[{sender_address}] {message}")

if __name__ == "__main__":
    client = MyClient(server_host='127.0.0.1', server_port=1414)
    client.connect()

