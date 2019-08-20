#!/usr/bin/env python3
import ssl
import socket


def query_dns(query, host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM | socket.SOCK_NONBLOCK)
    s.setblocking(False)
    # s.settimeout(3)

    print('Querying DNS', host, port, query)
    data = None
    context = ssl.create_default_context()
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            try:
                ssock.connect((host, port))
            except ValueError:
                pass  # Already connected
            ssock.sendall(query)
            data = ssock.recv(1024)

    print(host, 'response:', data)
    return data
