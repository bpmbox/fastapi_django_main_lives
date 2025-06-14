import unittest
from unittest.mock import patch
from google_apps_script import GoogleAppsScript

class TestGoogleAppsScript(unittest.TestCase):
    def setUp(self):
        self.script_id = "test_script_id"
        self.service = GoogleAppsScript(self.script_id)

    @patch("googleapiclient.discovery.build")
    def test_build_service(self, mock_build):
        self.service._build_service()
        mock_build.assert_called_once()

    @patch("googleapiclient.discovery.build")
    def test_execute_script(self, mock_build):
        mock_response = {"response": {"result": "success"}}
        mock_service = mock_build.return_value
        mock_service.scripts.return_value.run.return_value.execute.return_value = mock_response
        result = self.service.execute_script("test_function", ["param1", "param2"])
        self.assertEqual(result, "success")

if __name__ == "__main__":
    unittest.main()