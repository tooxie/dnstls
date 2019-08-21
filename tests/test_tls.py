#!/usr/bin/env python3
import unittest
import socket

from dnstls import tls

# mock_socket = mock.Mock()
# mock_socket.recv.return_value = data


class TlsTest(unittest.TestCase):
    def setUp(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.

    def tearDown(self):
        self.sock.close()
