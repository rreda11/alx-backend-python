#!/usr/bin/env python3
"""Test suite for GithubOrgClient class."""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOrgClient class."""
    @parameterized.expand([("google",), ("abc",)])
    @patch("client.get_json")
    def test_org(self, org, request_mock):
        """Test that org method returns the correct org."""
        request_mock.return_value = {"login": org}
        obj = GithubOrgClient(org)
        self.assertEqual(obj.org, {"login": org})
        request_mock.assert_called_once_with(
            obj.ORG_URL.format(org=org))


unittest.main()
