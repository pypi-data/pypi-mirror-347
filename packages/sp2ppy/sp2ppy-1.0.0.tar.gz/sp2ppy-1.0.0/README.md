# SP2PPY



- [API](#api)
    - [Server](#server)
    - [Client](#client)


## API

- [Server](#server)
- [Client](#client)


### Server

SP2P (Super Peer-to-Peer) Relay Server


Responsibilities:
- Accepts TCP connections from clients.
- Assigns unique 8-character hex addresses to clients.
- Allows clients to connect to each other via the `CONN <ADDRESS>` command.
- Relays data between paired clients.

SP2P Protocol:
- On connect: `YOURADDR <ADDRESS>` is sent to the client.
- To connect to a peer: send `CONN <TARGET_ADDRESS>`.
- On success: connecting client receives `OK`, the target peer receives `CONNED <ADDRESS>`.
- All relayed messages: `<SENDER_ADDRESS>: <DATA>`.
- On disconnect initiated by a peer: the other side receives `DISCONN`.


### Client

SP2P (Super Peer-to-Peer) TCP Client


Responsibilities:
- Connects to an SP2P `Server` and receives its unique address.
- Sends `CONN <ADDRESS>` to initiate a connection to another peer.
- Handles incoming commands and packets:
    * `YOURADDR <ADDR>`: own assigned address
    * `OK`: connection to peer successful
    * `CONNED <ADDR>`: peer has connected to you
    * `DISCONN`: peer has disconnected
    * `<ADDR>: <DATA>`: message relayed from peer

Hooks (override in subclass or override instance methods):
- on_ready(address): Called with own address after connecting to server.
- on_connected(): Called after successful connection to peer.
- on_peer_connected(peer_address): Called when a peer connects to you.
- on_disconnected(): Called when the peer disconnects.
- on_message(sender_address, message): Called on incoming message.
