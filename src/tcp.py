#!/usr/bin/env python3
"""Module to hold all the TCP-related methods.
"""

import logging
import socket


def get_socket(host, port, backlog=10):
    """Creates a TCP socket and sets it as non-blocking.
    """

    logging.debug("Creating a TCP socket")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(backlog)
    s.setblocking(False)

    return s


def get_handler(query_dns_fn, selector, event):
    """Returns a handler that accepts TCP connections.
    """

    def accept_tcp(sock):
        """Handler of incoming TCP connections. Will accept the connection and
        register the callback to start reading the incoming data.
        """

        conn, addr = sock.accept()
        logging.info("Accepted connection from %s", addr)
        selector.register(
            conn,
            event,
            get_read_handler(query_dns_fn, selector))

    return accept_tcp

def get_read_handler(query_dns_fn, selector):
    """Returns a handler that reads from a TCP socket.
    """

    def read(conn):
        """Reads the incoming data and sends the query out to the external DNS.
        It then sends the response back to the original requester.
        """

        try:
            data = conn.recv(1024)
        except Exception:
            logging.exception("Error reading from TCP socket")
            raise

        if data:
            logging.info("Got '%s' from %s over TCP", repr(data), conn.getpeername())
            response = None
            try:
                response = query_dns_fn(data)
            except Exception:
                logging.exception("Error querying the external DNS")
                raise

            try:
                conn.send(response)
            except Exception:
                logging.exception("Error sending the response back to the client")
                raise
        else:
            logging.debug("Closing: %s", conn.getpeername())
            selector.unregister(conn)
            conn.close()

    return read
