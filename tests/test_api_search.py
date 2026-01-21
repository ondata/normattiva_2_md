import unittest
from unittest import mock

from normattiva2md.api import search_law
from normattiva2md.exceptions import APIKeyError


class FakeResponse:
    def __init__(self, status_code=200, payload=None, text=""):
        self.status_code = status_code
        self._payload = payload or {}
        self.text = text

    def json(self):
        return self._payload


class TestApiSearch(unittest.TestCase):
    def test_search_law_missing_api_key(self):
        with mock.patch("normattiva2md.api.load_env_file"), mock.patch(
            "os.getenv", return_value=None
        ):
            with self.assertRaises(APIKeyError):
                search_law("legge stanca", quiet=True)

    def test_search_law_non_200(self):
        response = FakeResponse(status_code=500, text="error")
        with mock.patch("normattiva2md.api.load_env_file"), mock.patch(
            "os.getenv", return_value="key"
        ), mock.patch(
            "requests.post", return_value=response
        ):
            results = search_law("test", quiet=True)
        self.assertEqual(results, [])

    def test_search_law_empty_results(self):
        response = FakeResponse(status_code=200, payload={"results": []})
        with mock.patch("normattiva2md.api.load_env_file"), mock.patch(
            "os.getenv", return_value="key"
        ), mock.patch(
            "requests.post", return_value=response
        ):
            results = search_law("test", quiet=True)
        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
