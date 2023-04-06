import unittest
from unittest.mock import patch, mock_open
import pickle
from GUI_chat_server_test_ver2 import updateDatabase, package_data

class TestUpdateDatabase(unittest.TestCase):
    @patch("GUI_chat_server_test_ver2.package_data")
    @patch("tempfile.NamedTemporaryFile")
    @patch("os.replace")
    def test_update_database(self, mock_replace, mock_named_temp_file, mock_package_data):
        mock_package_data.return_value = "test_data"
        m = mock_open()
        mock_named_temp_file.return_value.__enter__.return_value = m.return_value

        updateDatabase()

        m.return_value.write.assert_called_once_with(pickle.dumps("test_data"))
        m.return_value.flush.assert_called_once()
        mock_replace.assert_called_once()

if __name__ == '__main__':
    unittest.main()
