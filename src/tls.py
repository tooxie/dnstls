#!/usr/bin/env python3
import logging
import socket
import ssl


def query_dns(query, host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM | socket.SOCK_NONBLOCK)
    s.setblocking(False)

    logging.debug(f'Connecting to {host}:{port}')
    logging.debug(f'Query: {query}')
    data = None
    context = ssl.create_default_context()
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            try:
                ssock.connect((host, port))
            except ValueError:
                logging.warn(f'Already connected to {host}:{port}')
            ssock.sendall(query)
            data = ssock.recv(1024)

    logging.debug(f'Got response from {host}: {data}')
    return data
