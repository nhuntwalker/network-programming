#!/usr/bin/env python3
"""."""
import socket
import sys


def server(buffer_length=8):
    """."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 2000))
    sock.listen(1)
    print("Server running at", sock.getsockname())
    try:
        while True:
            msg = ""
            conn, addr_info = sock.accept()
            while True:
                part = conn.recv(buffer_length)
                if not part:
                    break
                msg += part.decode('utf8')
            print(msg)
            conn.close()

    except KeyboardInterrupt:
        sock.close()
        sys.exit(1)


if __name__ == "__main__":
    server()
