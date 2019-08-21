#!/usr/bin/env python3
import unittest
from unittest import mock

from dnstls import conf


class ConfTest(unittest.TestCase):
    def test_get_conf(self):
        with mock.patch('os.getenv') as mock_env:
            mock_env.return_value = '123'
            self.assertEqual(conf.get_conf('foo'), '123')
