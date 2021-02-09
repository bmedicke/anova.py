"""Util module for anova"""

import socket
from typing import Tuple


def _decode(line: bytes) -> Tuple[int, str]:
    """Decode Anova messages"""
    rot = 1
    output = ""
    length = line[1]
    recived_checksum = line[-1]
    calculated_checksum = 0
    for p in line[2:-1]:
        output += chr(p >> (rot) | ((p & (2 ** rot) - 1) << 8 - rot))
        rot += 1
        rot %= 7
        calculated_checksum += p

    if recived_checksum == (calculated_checksum & 255):
        return (length, output.rstrip())

    return (0, "")


def get_secret_cookerid(ip: str) -> Tuple[str, str]:
    """Get secret and cooker_id from anova."""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as anova_socket:
        anova_socket.connect((ip, 9988))
        count = 0
        cooker_id = None
        secret = None
        while (cooker_id is None) and (secret is None):
            line = bytearray()
            if count % 128:
                anova_socket.send(b"h")

            data = anova_socket.recv(1024)
            for d in range(0, len(data) - 1):
                if (data[d], data[d + 1]) == (22, 104):
                    length, decoded = _decode(line)
                    if length == 22:
                        cooker_id = decoded
                    if length == 11:
                        secret = decoded

                    line = bytearray()
                else:
                    line.append(data[d])

            length, decoded = _decode(line)
            if length == 22:
                cooker_id = decoded
            if length == 11:
                secret = decoded
            count += 1

    return (cooker_id, secret)
