#!/usr/bin/env python3
"""Module to hold all the UDP-related methods.
"""

import logging
import socket


def get_socket(host, port):
    """Creates a UDP socket.
    """

    logging.debug("Creating a UDP socket")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))

    return s

def to_tcp(data):
    """Given a UDP datagram, prepend TCP-specific information.
    """

    return bytes("\x00" + chr(len(data)), "utf-8") + data

def to_udp(data):
    """Remove the TCP-headers.
    """

    return data[2:]

def get_handler(query_dns_fn):
    """Returns a handler that reads UDP data.
    """

    def read(conn):
        """Receive the query and hand it over to the injected `query_dns_fn`.
        """

        try:
            data, addr = conn.recvfrom(65565)
        except Exception:
            logging.exception("Error reading UDP data")
            raise

        logging.info("Got %s from %s over UDP", str(data), addr)
        try:
            response = query_dns_fn(to_tcp(data))
            logging.debug("Sending %s to %s", repr(response), addr)
            conn.sendto(to_udp(response), addr)
        except Exception as err:
            logging.error(err)

    return read
