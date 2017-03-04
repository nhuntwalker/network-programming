#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
"""Constants and routines for supporting a certain network conversation."""

import argparse
import socket
import time

APHORISMS = {
    b'Beautiful is better than?': b'Ugly.',
    b'Explicit is better than?': b'Implicit.',
    b'Simple is better than?': b'Complex.'
}


def get_answer(aphorism):
    """Return the string response to a particular Zen-of-Python aphorism."""
    time.sleep(0.0)  # increase to simulate an expensive operation
    return APHORISMS.get(aphorism, b'Error: unknown aphorism.')


def parse_command_line(description):
    """Parse command line and return a socket address."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-p', metavar='port', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    address = (args.host, args.p)
    return address


def create_srv_socket(address):
    """Build and return a listening server socket."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(64)
    print('Listening at {}'.format(address))
    return sock


def accept_connections_forever(listener):
    """Forever answer incoming connections on a listening socket."""
    while True:
        sock, address = listener.accept()
        print('Accepted connection from {}'.format(address))
        handle_conversation(sock, address)


def handle_conversation(sock, address):
    """Converse with a client over 'sock' until they are done talking."""
    try:
        while True:
            handle_request(sock)
    except EOFError:
        print('Client socket to {} has closed'.format(address))
    except Exception as e:
        print('Client {} error: {}'.format(address, e))
    finally:
        sock.close()


def handle_request(sock):
    """Receive a single client request on 'sock' and send the answer."""
    aphorism = recv_until(sock, b'?')
    answer = get_answer(aphorism)
    sock.sendall(answer)


def recv_until(sock, suffix):
    """Receive bytes over socket 'sock' until we receive the 'suffix'."""
    msg = sock.recv(4096)
    if not msg:
        raise EOFError('socket closed')
    while not msg.endswith(suffix):
        data = sock.recv(4096)
        if not data:
            raise IOError('received {!r} then socket closed'.format(msg))
        msg += data
    return msg
