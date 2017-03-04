#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
"""Small application that uses several different message queues."""

import random
import threading
import time
import zmq

B = 32  # number of bits of precision in each random integer


def ones_and_zeros(digits):
    """Express `n` in at least `d` binary digits, with no special prefix."""
    return bin(random.getrandbits(digits)).lstrip('0b').zfill(digits)


def bitsource(zcontext, url):
    """Produce random points in the unit square."""
    zsock = zcontext.socket(zmq.PUB)
    zsock.bind(url)
    while True:
        zsock.send_string(ones_and_zeros(B * 2))
        time.sleep(0.01)


def always_yes(zcontext, in_url, out_url):
    """Coordinate in the lower-left quadrant is inside the unit circle."""
    in_sock = zcontext.socket(zmq.SUB)
    in_sock.connect(in_url)
    in_sock.setsockopt(zmq.SUBSCRIBE, b'00')
    out_sock = zcontext.socket(zmq.PUSH)
    out_sock.connect(out_url)
    while True:
        in_sock.recv_string()
        out_sock.send_string('Y')


def judge(zcontext, in_url, pythagoras_url, out_url):
    """Determine whether each input coordinate is inside the unit circle."""
    in_sock = zcontext.socket(zmq.SUB)
    in_sock.connect(in_url)
    for prefix in b'01', b'10', b'11':
        in_sock.setsockopt(zmq.SUBSCRIBE, prefix)
    pythag_sock = zcontext.socket(zmq.REQ)
    pythag_sock.connect(pythagoras_url)
    out_sock = zcontext.socket(zmq.PUSH)
    out_sock.connect(out_url)
    unit = 2 ** (B * 2)
    while True:
        bits = in_sock.recv_string()
        n, m = int(bits[::2], 2), int(bits[1::2], 2)
        pythag_sock.send_json((n, m))
        sumsquares = pythag_sock.recv_json()
        out_sock.send_string('Y' if sumsquares < unit else 'N')


def pythagoras(zcontext, url):
    """Return the sum-of-squares of number sequences."""
    zsock = zcontext.socket(zmq.REP)
    zsock.bind(url)
    while True:
        numbers = zsock.recv_json()
        zsock.send_json(sum(n * n for n in numbers))


def tally(zcontext, url):
    """Tally how many points fall within the unit circle, and print pi."""
    zsock = zcontext.socket(zmq.PULL)
    zsock.bind(url)
    p = q = 0
    while True:
        decision = zsock.recv_string()
        q += 1
        if decision == 'Y':
            p += 4
        print(decision, p / q)


def start_thread(function, *args):
    """Start a thread."""
    thread = threading.Thread(target=function, args=args)
    thread.daemon = True  # so you can easily Ctrl-C the whole program
    thread.start()


def main(zcontext):
    """The main function of the program."""
    pubsub = 'tcp://127.0.0.1:6700'
    reqrep = 'tcp://127.0.0.1:6701'
    pushpull = 'tcp://127.0.0.1:6702'
    start_thread(bitsource, zcontext, pubsub)
    start_thread(always_yes, zcontext, pubsub, pushpull)
    start_thread(judge, zcontext, pubsub, reqrep, pushpull)
    start_thread(pythagoras, zcontext, reqrep)
    start_thread(tally, zcontext, pushpull)
    time.sleep(30)

if __name__ == "__main__":
    main(zmq.Context())
