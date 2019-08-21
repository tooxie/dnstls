#!/usr/bin/env python3
import logging
import socket

from tls import query_dns


def get_socket(host, port, backlog=10):
    """Creates a TCP socket and sets it as non-blocking.
    """

    logging.debug(f"Creating a TCP socket")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(backlog)
    s.setblocking(False)

    return s


def get_handler(selector, event, dns_host, dns_port):
    """Returns a handler that accepts TCP connections
    """

    def accept_tcp(sock, mask):
        """Handler of incoming TCP connections. Will accept the connection and
        register the callback to start reading the incoming data.
        """

        conn, addr = sock.accept()
        logging.info(f"Accepted connection from {addr}")
        selector.register(conn, event, read(selector, dns_host, dns_port))

    return accept_tcp

def read(selector, dns_host, dns_port):
    def readtcp(conn, mask):
        """Reads the incoming data and sends the query out to the external DNS.
        It then sends the response back to the original requester.
        """

        try:
            data = conn.recv(1000)
        except Exception as err:
            logging.error(err)
            return

        logging.info(f"Got '{repr(data)}' from {conn.getpeername()}")
        if data:
            try:
                conn.send(query_dns(data, dns_host, dns_port))
            except Exception as err:
                logging.error(err)
        else:
            logging.debug(f"Closing: {conn.getpeername()}")
            selector.unregister(conn)
            conn.close()

    return readtcp
