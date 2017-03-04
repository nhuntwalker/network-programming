#!/usr/bin/env python3
# Fundamentals of Python Network Programming, Third Edition
"""Simple TCP client and server that send and receive 16 octets."""

import argparse
import socket
import sys


def server(interface, port, bytecount):
    """Socket server."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print("Server listening at", sock.getsockname())
    try:
        while True:
            conn, addr_info = sock.accept()
            print("Processing up to 1024 bytes at at time from", addr_info)
            n = 0
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                output = data.decode('ascii').upper().encode('ascii')
                conn.sendall(output)  # send back as uppercase
                n += len(data)
                print('\r  {} bytes processed so far'.format(n), end=' ')
                sys.stdout.flush()
            print()
            conn.close()
            print("    Reply sent, socket closed.")
    except KeyboardInterrupt:
        print("Shutting down server.")
        sock.close()
        sys.exit(0)


def client(host, port, bytecount):
    """Socket client."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bytecount = (bytecount + 15) // 16 * 16
    message = b'capitalize this!'  # 16-byte message to repeat over and over
    print('Sending', bytecount, 'bytes of data, in chunks of 16 bytes')
    sock.connect((host, port))
    sent = 0
    while sent < bytecount:
        sock.sendall(message)
        sent += len(message)
        print('\r {} bytes sent'.format(sent), end=' ')
        sys.stdout.flush()

    print()
    sock.shutdown(socket.SHUT_WR)

    print("Receiving all the data the server sends back")

    received = 0
    while True:
        data = sock.recv(42)
        if not received:
            print('    The first data received says', repr(data))
        if not data:
            break
        received += len(data)
        print('\r    {} bytes received'.format(received), end=' ')
    print()
    sock.close()

if __name__ == "__main__":
    choices = {"client": client, "server": server}
    parser = argparse.ArgumentParser(description="Send and receive over TCP")
    parser.add_argument("role", choices=choices, help="which role to play")
    parser.add_argument("host", help="interface the server listens at; host the client send to")
    parser.add_argument("bytecount", type=int, nargs="?", default=16, help="number of bytes for client to send (default 16)")
    parser.add_argument("-p", metavar="PORT", type=int, default=1060, help="TCP port (default 1060)")
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p, args.bytecount)
