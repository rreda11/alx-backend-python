#!/usr/bin/env python3
"""Module For Testing Utils"""


import unittest
from unittest.mock import patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Class to Test Access Nested Map"""
    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(self, mapping, seq, expected):
        """Test access_nested_map function"""
        self.assertEqual(access_nested_map(mapping, seq), expected)

    @parameterized.expand([({}, ("a",)), ({"a": 1}, ("a", "b"))])
    def test_access_nested_map_exception(self, mapping, seq):
        """Test access_nested_map raises KeyError"""
        self.assertRaises(KeyError, access_nested_map, mapping, seq)


class TestGetJson(unittest.TestCase):
    """Class to Test Get JSON"""
    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    @patch("utils.requests.get")
    def test_get_json(self, url, data, mock_request_get):
        """Test get_json function"""
        mock_request_get.return_value.json.return_value = data

        self.assertEqual(get_json(url), data)
        mock_request_get.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
    """Class to Test Memoization"""

    def test_memoize(self):
        """Test memoization decorator"""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock:
            obj = TestClass()
            call1 = obj.a_property
            call2 = obj.a_property
            self.assertEqual(call1, 42)
            self.assertEqual(call2, 42)
            mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()

    """def test_access_nested_map_exception(self, mapping, seq):
         Test access_nested_map raises KeyError
        self.assertRaises(KeyError, access_nested_map, mapping, seq)"""
    
