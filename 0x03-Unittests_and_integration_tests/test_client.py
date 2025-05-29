#!/usr/bin/env python3
"""Test suite for GithubOrgClient class."""

import unittest
from unittest.mock import patch, PropertyMock
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
        
    def test_public_repos_url(self):
        """Test _public_repos_url returns expected URL from org."""
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) 
        as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/test_org/repos"
            }

            client = GithubOrgClient("test_org")
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/test_org/repos"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos method returns expected list of repos."""
        # Sample payload returned by get_json
        sample_repos = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": {"key": "mit"}},
        ]
        mock_get_json.return_value = sample_repos

        # Patch the _public_repos_url property
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) 
        as mock_repos_url:
            mock_repos_url.return_value = "https://api.github.com/orgs/test_org/repos"

            client = GithubOrgClient("test_org")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/test_org/repos")
            mock_repos_url.assert_called_once()


unittest.main()
