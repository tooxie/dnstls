#!/usr/bin/env python3
"""This module holds all the logic to connect to the external DNS server
securely over TLS.
"""

import logging
import socket
import ssl


def query_dns(query, host, port):
    """Queries the external DNS over TLS.
    """

    data = None
    context = ssl.create_default_context()
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            try:
                ssock.connect((host, port))
                logging.debug("Connected to %s:%s", host, port)
            except ValueError:
                logging.warning("Already connected to %s:%s", host, port)
            logging.debug("Query: %s", query)
            ssock.sendall(query)
            data = ssock.recv(1024)

    logging.debug("Got response from %s: %s", host, data)
    return data
