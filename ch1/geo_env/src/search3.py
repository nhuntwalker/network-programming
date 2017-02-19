#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
"""."""

import http.client
import json
from urllib.parse import quote_plus

base = "/maps/api/geocode/json"


def geocode(address):
    """An implementation of the Google geocoder."""
    path = '{}?address={}&sensor=false'.format(base, quote_plus(address))
    connection = http.client.HTTPConnection('maps.google.com')
    connection.request('GET', path)
    raw_reply = connection.getresponse().read()
    reply = json.loads(raw_reply.decode('utf-8'))
    print(reply['results'][0]['geometry']['location'])

if __name__ == "__main__":
    geocode("1903 NE 85th St., Seattle, WA")
