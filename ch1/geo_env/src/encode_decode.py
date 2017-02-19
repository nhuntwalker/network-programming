#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
"""."""

if __name__ == "__main__":
    # Translate from the outside world of bytes to Unicode characters.
    input_bytes = b'\xff\xfe4\x001\x003\x00 \x00i\x00s\x00 \x00i\x00n\x00.\x00'
    input_chars = input_bytes.decode('utf-16')
    print(repr(input_chars))

    output_chars = "We copy you down, Gold Leader.\n"
    output_bytes = output_chars.encode('utf-8')
    with open('eagle.txt', 'wb') as f:
        f.write(output_bytes)
