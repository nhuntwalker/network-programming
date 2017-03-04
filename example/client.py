#!/usr/bin/env python3
"""."""
import socket
import sys


def client(msg):
    """."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 2000))
    sock.sendall(msg.encode('utf8'))
    sock.shutdown(socket.SHUT_WR)
    sock.close()


if __name__ == "__main__":
    msg = sys.argv[1]
    client(msg)
