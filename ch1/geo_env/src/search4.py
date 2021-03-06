#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
"""."""
import socket
from urllib.parse import quote_plus

request_text = """\
GET /maps/api/geocode/json?address={}&sensor=false HTTP/1.1\r\n\
Host: maps.google.com:80\r\n\
User-Agent: search4.py (Foundations of Python Network Programming)\r\n\
Connection: close\r\n\r\n\
"""


def geocode(address):
    """An implementation of the Google geocoder."""
    sock = socket.socket()
    sock.connect(('maps.google.com', 80))
    request = request_text.format(quote_plus(address))
    sock.sendall(request.encode('ascii'))
    raw_reply = b''
    while True:
        more = sock.recv(4096)
        if not more:
            break
        raw_reply += more
    sock.close()
    print(raw_reply.decode('utf-8'))


if __name__ == "__main__":
    geocode("1903 NE 85th St., Seattle, WA")
