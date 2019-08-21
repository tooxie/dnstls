#!/usr/bin/env python3
import logging
import selectors

import udp
import tcp
from conf import get_conf

HOST = get_conf("HOST")
PORT = get_conf("PORT", t=int)
DNS_HOST = get_conf("DNS_HOST")
DNS_PORT = get_conf("DNS_PORT", t=int)

selector = selectors.DefaultSelector()


def main():
    log_level = get_conf("LOG_LEVEL", logging.WARNING, t=int)
    logging.basicConfig(level=log_level)

    tcp_socket = tcp.get_socket(HOST, PORT)
    selector.register(
        tcp_socket,
        selectors.EVENT_READ,
        tcp.get_handler(selector, selectors.EVENT_READ, DNS_HOST, DNS_PORT))
    logging.debug(f"Listening on {HOST}:{PORT}/tcp")

    udp_socket = udp.get_socket(HOST, PORT)
    selector.register(
        udp_socket,
        selectors.EVENT_READ,
        udp.get_handler(DNS_HOST, DNS_PORT))
    logging.debug(f"Listening on {HOST}:{PORT}/udp")

    while True:
        events = selector.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)


if __name__ == "__main__":
    main()
