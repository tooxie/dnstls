#!/usr/bin/env python3
import logging
import selectors
import socket

from conf import get_conf
from tls import query_dns

HOST = get_conf('HOST')
PORT = get_conf('PORT', t=int)
DNS_HOST = get_conf('DNS_HOST')
DNS_PORT = get_conf('DNS_PORT', t=int)

selector = selectors.DefaultSelector()


def get_socket(proto, backlog=10):
    _proto = 'TCP' if (proto == socket.SOCK_STREAM) else 'UDP'
    logging.debug(f"Creating a {_proto} socket")
    s = socket.socket(socket.AF_INET, proto)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    if proto == socket.SOCK_STREAM:
        s.listen(backlog)
        s.setblocking(False)
    return s


# --- TCP
def accept_tcp(sock, mask):
    conn, addr = sock.accept()
    logging.info(f'Accepted connection from {addr}')
    conn.setblocking(False)
    selector.register(conn, selectors.EVENT_READ, readtcp)

def readtcp(conn, mask):
    try:
        data = conn.recv(1000)
    except Exception as err:
        logging.error(err)
        return

    if data:
        logging.debug(f'Sending {repr(data)} to {conn.getpeername()}')
        try:
            conn.send(query_dns(data, DNS_HOST, DNS_PORT))
        except Exception as err:
            logging.error(err)
    else:
        logging.debug(f'Closing: {conn.getpeername()}')
        selector.unregister(conn)
        conn.close()


# --- UDP
def totcp(data):
    return bytes('\x00' + chr(len(data)) + data.decode('cp1252'), 'utf-8')

def accept_udp(conn, mask):
    try:
        data, addr = conn.recvfrom(65565)
    except Exception as err:
        logging.error(err)
        return

    logging.info('got', repr(data), 'from', addr)
    try:
        response = query_dns(totcp(data), DNS_HOST, DNS_PORT)
        logging.debug('sending', repr(response), 'to', addr)
        conn.sendto(response, addr)
    except Exception as err:
        logging.error(err)

def main():
    log_level = get_conf('LOG_LEVEL', logging.WARNING, t=int)
    logging.basicConfig(level=log_level)

    tcp_socket = get_socket(socket.SOCK_STREAM)
    selector.register(tcp_socket, selectors.EVENT_READ, accept_tcp)
    logging.debug(f'Listening on {HOST}:{PORT}/tcp')

    udp_socket = get_socket(socket.SOCK_DGRAM)
    selector.register(udp_socket, selectors.EVENT_READ, accept_udp)
    logging.debug(f'Listening on {HOST}:{PORT}/udp')

    while True:
        events = selector.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)


if __name__ == '__main__':
    main()
