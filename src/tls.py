#!/usr/bin/env python3
import logging
import socket
import ssl


def query_dns(query, host, port):
    """Queries the external DNS over TLS.
    """

    proto = socket.SOCK_STREAM | socket.SOCK_NONBLOCK
    s = socket.socket(socket.AF_INET, proto)
    s.setblocking(False)

    data = None
    context = ssl.create_default_context()
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            try:
                ssock.connect((host, port))
                logging.debug(f'Connected to {host}:{port}')
            except ValueError:
                logging.warn(f'Already connected to {host}:{port}')
            logging.debug(f'Query: {query}')
            ssock.sendall(query)
            data = ssock.recv(1024)

    logging.debug(f'Got response from {host}: {data}')
    return data
