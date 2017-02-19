#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
"""."""

import requests


def geocode(address):
    """An implementation of the Google geocoder."""
    parameters = {"address": address, "sensor": "false"}
    base = "http://maps.googleapis.com/maps/api/geocode/json"
    response = requests.get(base, params=parameters)
    answer = response.json()
    print(answer["results"][0]["geometry"]["location"])

if __name__ == "__main__":
    geocode("1903 NE 85th St., Seattle, WA")
