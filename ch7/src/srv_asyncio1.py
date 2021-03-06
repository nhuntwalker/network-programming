#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
"""Asynchronous I/O inside "asyncio" callback methods."""

import asyncio
import zen_utils


class ZenServer(asyncio.Protocol):
    """An asyncio server."""

    def connection_made(self, transport):
        """Accept a connection."""
        self.transport = transport
        self.address = transport.get_extra_info("peername")
        self.data = b''
        print('Accepted connection from {}'.format(self.address))

    def data_received(self, data):
        """Receive and store the data on the object."""
        self.data += data
        if self.data.endswith(b'?'):
            answer = zen_utils.get_answer(self.data)
            self.transport.write(answer)
            self.data = b''

    def connection_lost(self, exc):
        """Handle situations where the connections close."""
        if exc:
            print('Client {} error: {}'.format(self.address, exc))
        elif self.data:
            print('Client {} sent {} but then closed.'.format(self.address, self.data))
        else:
            print('Client {} closed socket'.format(self.address))


if __name__ == "__main__":
    address = zen_utils.parse_command_line('asyncio server using callbacks')
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ZenServer, *address)
    server = loop.run_until_complete(coro)
    print('Listening at {}'.format(address))
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.close()
