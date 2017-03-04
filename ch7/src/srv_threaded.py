#!/usr/bin/env python3
# Foundations of Python Network Programming
"""Using multiple threads to serve several clients in parallel."""

import zen_utils
from threading import Thread


def start_threads(listener, workers=4):
    """Given a listener create a number of threads for incoming connections."""
    thread_base = (listener,)
    for i in range(workers):
        Thread(
            target=zen_utils.accept_connections_forever,
            args=thread_base
        ).start()

if __name__ == "__main__":
    address = zen_utils.parse_command_line('simple single-threaded server')
    listener = zen_utils.create_srv_socket(address)
    start_threads(listener)
