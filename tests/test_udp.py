#!/usr/bin/env python3
import unittest
from unittest import mock
import socket as sock

from dnstls import udp


class UdpTest(unittest.TestCase):
    def test_get_socket(self):
        args = ('127.0.0.1', 5354)

        with mock.patch('socket.socket') as mock_socket:
            s = udp.get_socket(*args)
            mock_socket.assert_called_with(sock.AF_INET, sock.SOCK_DGRAM)
            s.bind.assert_called_with(args)
            s.setsockopt.assert_called_with(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)

    def test_to_tcp(self):
        data = b'1234'
        tcp_data = udp.to_tcp(data)
        self.assertEqual(tcp_data, b'\x00\x041234')

    def test_to_udp(self):
        data = '1234'
        udp_data = udp.to_udp(data)
        self.assertEqual(udp_data, '34')

    def test_read_handler(self):
        data = b'1234'
        bdata = b'\x00\x041234'
        query_dns_mock = mock.Mock()
        query_dns_mock.return_value = data

        recvfrom = mock.Mock()
        recvfrom.return_value = (data, '127.0.0.1')
        mock_socket = mock.Mock()
        mock_socket.recvfrom = recvfrom

        handler = udp.get_handler(query_dns_mock)
        handler(mock_socket)

        query_dns_mock.assert_called_with(bdata)
