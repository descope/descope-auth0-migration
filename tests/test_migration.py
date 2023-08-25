import unittest
from unittest.mock import mock_open, patch, Mock
from src.migration_utils import read_auth0_export, fetch_auth0_users


class TestMigration(unittest.TestCase):
    def test_read_auth0_export(self):
        mock_data = """{"_id": {"$oid": "1234"}, "email": "test1@email.com"}
{"_id": {"$oid": "5678"}, "email": "test2@email.com"}"""

        # Use mock_open to mock file reading
        with patch("builtins.open", mock_open(read_data=mock_data)):
            users = read_auth0_export("mock_path")

        self.assertEqual(len(users), 2)
        self.assertEqual(users[0]["_id"]["$oid"], "1234")
        self.assertEqual(users[1]["email"], "test2@email.com")

    @patch("requests.get")
    def test_fetch_auth0_users_success(self, mock_get):
        # Mock successful response
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json = Mock(
            return_value=[{"user_id": "auth0|1234", "email": "test1@email.com"}]
        )
        mock_get.return_value = mock_resp

        users = fetch_auth0_users()

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]["email"], "test1@email.com")

    @patch("requests.get")
    def test_fetch_auth0_users_failure(self, mock_get):
        # Mock failed response
        mock_resp = Mock()
        mock_resp.status_code = 400
        mock_get.return_value = mock_resp

        users = fetch_auth0_users()

        self.assertEqual(len(users), 0)


if __name__ == "__main__":
    unittest.main()
