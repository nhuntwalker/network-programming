#!/usr/bin/env python3
# Fundamentals of Python Network Programming, Third Edition
"""Simple TCP client and server that send and receive 16 octets."""

import argparse
import socket
import sys


def recvall(sock, length):
    """Receive all of a data stream."""
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError("was expecting {} bytes but only received {} bytes before the socket closed.".format(
                length, len(data)))

        data += more
    return data


def server(interface, port):
    """Socket server."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print("Server listening at", sock.getsockname())
    try:
        while True:
            conn, addr_info = sock.accept()
            print("We have accepted a connection from", addr_info)
            print("    Socket name:", conn.getsockname())
            print("    Socket peer:", conn.getpeername())
            message = recvall(conn, 16)
            print("    Incoming sixteen-octet mesage:", repr(message))
            conn.sendall(b'Farewell, client')
            conn.close()
            print("    Reply sent, socket closed.")
    except KeyboardInterrupt:
        print("Shutting down server.")
        sock.close()
        sys.exit(0)


def client(host, port):
    """Socket client."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print("Client has been assigned socket name", sock.getsockname())
    sock.sendall(b"Hi there, server")
    reply = recvall(sock, 16)
    print("The server said", repr(reply))
    sock.close()

if __name__ == "__main__":
    choices = {"client": client, "server": server}
    parser = argparse.ArgumentParser(description="Send and receive over TCP")
    parser.add_argument("role", choices=choices, help="which role to play")
    parser.add_argument("host", help="interface the server listens at; host the client send to")
    parser.add_argument("-p", metavar="PORT", type=int, default=1060, help="TCP port (default 1060)")
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
