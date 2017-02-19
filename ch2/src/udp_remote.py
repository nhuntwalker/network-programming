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
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = sys.argv[2]
    sock.connect((hostname, port))
    print('Client socket name is {}'.format(sock.getsockname()))

    delay = 0.1  # seconds
    text = 'This is another message'
    data = text.encode('ascii')
    while True:
        sock.send(data)
        print('Waiting up to {} seconds for a reply'.format(delay))
        sock.settimeout(delay)
        try:
            data = sock.recv(MAX_BYTES)
        except socket.timeout:
            delay *= 2  # wait even longer for the next request
            if delay > 2.0:
                raise RuntimeError("I think the server is down")
        else:
            break  # we are done, and can stop looping

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
