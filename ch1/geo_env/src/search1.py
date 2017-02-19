#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
"""."""

from pygeocoder import Geocoder

if __name__ == "__main__":
    address = "1903 NE 85th St., Seattle, WA"
    print(Geocoder.geocode(address)[0].coordinates)
