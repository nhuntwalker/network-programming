#!/usr/bin/env python3
# Fundamentals of Python Network Programming
"""Client that sends data then closes the socket, not expecting a reply."""

import socket
from argparse import ArgumentParser


def server(address):
    """A TCP server."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(1)
    print("Run this script in another window with '-c' to connect")
    print("Listening at ", sock.getsockname())
    conn, addr_info = sock.accept()
    print("Accepted connection from", addr_info)
    conn.shutdown(socket.SHUT_WR)
    msg = b''
    while True:
        part = conn.recv(8192)  # arbitrary value of 8k
        if not part:  # socket has closed when recv() returns ''
            print('Received zero bytes - end of file')
            break
        print('Received {} bytes'.format(len(part)))
        msg += part
    print('Message:\n')
    print(msg.decode('ascii'))
    conn.close()
    sock.close()


def client(address):
    """A client."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    sock.shutdown(socket.SHUT_RD)
    sock.sendall(b'Beautiful is better than ugly.\n')
    sock.sendall(b'Explicit is better than implicit.\n')
    sock.sendall(b'Simple is better than complex.\n')
    sock.close()

if __name__ == "__main__":
    parser = ArgumentParser(description="Transmit & receive a data stream.")
    parser.add_argument('hostname', nargs='?', default='127.0.0.1',
                        help='IP address or hostname (default: %(default)s)')
    parser.add_argument('-c', action='store_true', help='run as the client')
    parser.add_argument('-p', type=int, metavar='port', default=1060,
                        help='TCP port number (default: %(default)s)')
    args = parser.parse_args()
    function = client if args.c else server
    function((args.hostname, args.p))
