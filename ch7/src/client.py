#!/usr/bin/env python3
# Foundations of Python Network Programming
"""Simple Zen-of-Python client that asks three questions then disconnects."""

import argparse
import random
import socket
import zen_utils


def client(address, cause_error=False):
    """A client for asking about the Zen of Python."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    aphorisms = list(zen_utils.APHORISMS)
    if cause_error:
        sock.sendall(aphorisms[0][:-1])
        return

    for aphorism in random.sample(aphorisms, 3):
        sock.sendall(aphorism)
        print(aphorism, zen_utils.recv_until(sock, b'.'))
    sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Example Client")
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-e', action='store_true', help='cause an error')
    parser.add_argument('-p', metavar='port', type=int, default=1060,
                        help='TCP Port (default 1060)')
    args = parser.parse_args()
    address = (args.host, args.p)
    client(address, args.e)
