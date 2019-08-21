#!/usr/bin/env python3
import unittest
from unittest import mock

from dnstls import udp


class UdpTest(unittest.TestCase):
    def test_get_socket(self):
        args = ('127.0.0.1', 5354)
        sock = udp.get_socket(*args)
        self.assertEqual(sock.getsockname(), args)
        sock.close()

    def test_to_tcp(self):
        data = b'1234'
        tcp_data = udp.to_tcp(data)
        self.assertEqual(tcp_data, b'\x00\x041234')

    def test_to_udp(self):
        data = '1234'
        udp_data = udp.to_udp(data)
        self.assertEqual(udp_data, '34')

    def test_read_handler(self):
        query_dns_mock = unittest.mock.Mock()
        mock_socket = unittest.mock.Mock()
        mock_socket.recv.return_value = (b'1234', '127.0.0.1')

        handler = udp.get_handler(query_dns_mock)
        handler(mock_socket)
