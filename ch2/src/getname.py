#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
"""."""
import socket

if __name__ == "__main__":
    # resolve the IP for a given domain name
    hostname = "www.python.org"
    addr = socket.gethostbyname(hostname)
    print("The IP address of {} is {}".format(hostname, addr))
