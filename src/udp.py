#!/usr/bin/env python3
import logging
import socket

from tls import query_dns


def get_socket(host, port, backlog=10):
    """Creates a UDP socket.
    """

    logging.debug(f"Creating a UDP socket")
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

def get_handler(dns_host, dns_port):
    """Returns a handler that reads UDP data
    """

    def read(conn, mask):
        """Receive the query and hand it over to `tls.query_dns`.
        """

        try:
            data, addr = conn.recvfrom(65565)
        except Exception as err:
            logging.error(err)
            return

        logging.info(f"Got {str(data)} from {addr}")
        try:
            response = query_dns(to_tcp(data), dns_host, dns_port)
            logging.debug(f"Sending {repr(response)} to {addr}")
            conn.sendto(to_udp(response), addr)
        except Exception as err:
            logging.error(err)

    return read