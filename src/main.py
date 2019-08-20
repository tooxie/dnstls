#!/usr/bin/env python3
import selectors
import socket

from tls import query_dns
from conf import get_conf

HOST = get_conf('host')
PORT = get_conf('port', t=int)
DNS_HOST = get_conf('dns_host')
DNS_PORT = get_conf('dns_port', t=int)

selector = selectors.DefaultSelector()

def get_socket(proto, backlog=10):
    s = socket.socket(socket.AF_INET, proto)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    if proto == socket.SOCK_STREAM:
        s.listen(backlog)
        s.setblocking(False)
    return s


# --- TCP
def mktcp(data):
    return bytes('\x00' + chr(len(data)) + data.decode('cp1252'), 'utf-8')

def accept_tcp(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    selector.register(conn, selectors.EVENT_READ, readtcp)

def readtcp(conn, mask):
    try:
        data = conn.recv(1000)  # Should be ready
    except Exception as err:
        print(err)
        return

    if data:
        print('echoing', repr(data), 'to', conn)
        try:
            conn.send(query_dns(data, DNS_HOST, DNS_PORT))
        except Exception as err:
            print(err)
    else:
        print('closing', conn)
        selector.unregister(conn)
        conn.close()


# --- UDP
def accept_udp(conn, mask):
    try:
        data, addr = conn.recvfrom(65565)
    except Exception as err:
        print(err)
        return

    print('got', repr(data), 'from', addr)
    try:
        response = query_dns(mktcp(data), DNS_HOST, DNS_PORT)
        print('sending', repr(response), 'to', addr)
        conn.sendto(response, addr)
    except Exception as err:
        print(err)


if __name__ == '__main__':
    tcp_socket = get_socket(socket.SOCK_STREAM)
    selector.register(tcp_socket, selectors.EVENT_READ, accept_tcp)

    udp_socket = get_socket(socket.SOCK_DGRAM)
    selector.register(udp_socket, selectors.EVENT_READ, accept_udp)

    while True:
        events = selector.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)
