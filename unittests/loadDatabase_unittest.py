import unittest
from unittest.mock import patch, mock_open
import pickle
from GUI_chat_server_test_ver2 import loadDatabase, unpackage_data

class TestLoadDatabase(unittest.TestCase):
    @patch("GUI_chat_server_test_ver2.unpackage_data")
    @patch("builtins.open", new_callable=mock_open, read_data=pickle.dumps("test_data"))
    def test_load_database(self, mock_file, mock_unpackage_data):
        loadDatabase()
        mock_file.assert_called_once_with("files/serverdb.pickle", "rb")
        mock_unpackage_data.assert_called_once_with("test_data", update_servers=True)

if __name__ == '__main__':
    unittest.main()
