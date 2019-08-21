#!/usr/bin/env python3
import unittest
from unittest import mock
import socket

from dnstls import tls


class TlsTest(unittest.TestCase):
    def test_query_dns(self):
        with unittest.mock.patch('socket.socket') as mock_socket:
            getsockopt = mock.Mock()
            getsockopt.return_value = socket.SOCK_STREAM
            mock_socket.return_value = getsockopt

            with unittest.mock.patch('socket.create_connection') as mock_conn:
                mock_conn.return_value = Mock(spec=)
                tls.query_dns('foo', '127.0.0.1', 1234)
