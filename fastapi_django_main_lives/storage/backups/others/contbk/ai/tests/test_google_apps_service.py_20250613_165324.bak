import unittest
from unittest.mock import patch
from google_apps_service import GoogleAppsService

class TestGoogleAppsService(unittest.TestCase):
    def setUp(self):
        self.script_id = "test_script_id"
        self.service = GoogleAppsService(self.script_id)

    @patch("google_apps_script.GoogleAppsScript")
    def test_execute_script(self, mock_script):
        mock_script.return_value.execute_script.return_value = "success"
        result = self.service.execute_script("test_function", ["param1", "param2"])
        self.assertEqual(result, "success")

if __name__ == "__main__":
    unittest.main()