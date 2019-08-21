#!/usr/bin/env python3
"""Main module. Gathers all the configuration from the environment, and sets up
both TCP and UDP sockets.
"""

import logging
import selectors

import udp
import tcp
from conf import get_conf

HOST = get_conf("HOST")
PORT = get_conf("PORT", t=int)
DNS_HOST = get_conf("DNS_HOST")
DNS_PORT = get_conf("DNS_PORT", t=int)


def main():
    """Create the sockets and start listening.
    """

    selector = selectors.DefaultSelector()
    log_level = get_conf("LOG_LEVEL", logging.WARNING, t=int)
    logging.basicConfig(level=log_level)

    tcp_socket = tcp.get_socket(HOST, PORT)
    selector.register(
        tcp_socket,
        selectors.EVENT_READ,
        tcp.get_handler(selector, selectors.EVENT_READ, DNS_HOST, DNS_PORT))
    logging.debug("Listening on %s:%s/tcp", HOST, PORT)

    udp_socket = udp.get_socket(HOST, PORT)
    selector.register(
        udp_socket,
        selectors.EVENT_READ,
        udp.get_handler(DNS_HOST, DNS_PORT))
    logging.debug("Listening on %s:%s/udp", HOST, PORT)

    try:
        while True:
            events = selector.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
    except KeyboardInterrupt:
        print('Closing sockets... (press ctrl+c again to force)')
        tcp_socket.close()
        udp_socket.close()


if __name__ == "__main__":
    main()
