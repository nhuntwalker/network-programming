#!/usr/bin/env python3
# Fundamentals of Python Network Programming, Third Edition
"""."""

import argparse
import random
import socket
import sys

MAX_BYTES = 65535


def server(interface, port):
    """UDP server."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print('Listening at', sock.getsockname())
    while True:
        data, addr_info = sock.recvfrom(MAX_BYTES)
        if random.random() < 0.5:
            print('Pretending to drop packet from {}'.format(addr_info))
            continue
        text = data.decode('ascii')
        print('The client at {} says {!r}'.format(addr_info, text))
        message = 'Your data was {} bytes long'.format(len(data))
        sock.sendto(message.encode('ascii'), addr_info)


def client(hostname, port):
    """UDP client."""
    pass

if __name__ == "__main__":
    choices = {"client": client, "server": server}
    desc = "Send and receive UDP, pretending that packets are often dropped."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('role', choices=choices, help="which role to take.")
    host_desc = 'interface the server listens at; host the client sends to'
    parser.add_argument('host', help=host_desc)
    parser.add_argument('-p', metavar="PORT", type=int,
                        default=1060, help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
