import unittest
import socket
import pickle
from unittest.mock import patch, call
from GUI_chat_server_test_ver2 import send_pickled_data, package_data

class TestScript(unittest.TestCase):
    @patch("socket.socket")
    def test_send_pickled_data_empty_data(self, mock_socket):
        with patch("GUI_chat_server_test_ver2.package_data") as mock_package_data:
            # Mock the package_data function to return an empty dictionary
            mock_package_data.return_value = {}
            
            # Create a MagicMock instance for the socket
            mock_conn = mock_socket.return_value

            # Call the send_pickled_data function with the MagicMock instance
            send_pickled_data(mock_conn)

            # Check if the socket.send method was called with the correct arguments
            data = {}
            serialized_data = pickle.dumps(data)

            expected_calls = [
                call(str(len(serialized_data)).encode("utf-8")),
                call("FINISH".encode("utf-8"))
            ]
            mock_conn.send.assert_has_calls(expected_calls)
            mock_conn.sendall.assert_called_once_with(serialized_data)

    @patch("socket.socket")
    def test_send_pickled_data_non_default_data(self, mock_socket):
        with patch("GUI_chat_server_test_ver2.package_data") as mock_package_data:
            # Mock the package_data function to return a custom dictionary
            mock_package_data.return_value = {"key": "value"}
            
            # Create a MagicMock instance for the socket
            mock_conn = mock_socket.return_value

            # Call the send_pickled_data function with the MagicMock instance
            send_pickled_data(mock_conn)

            # Check if the socket.send method was called with the correct arguments
            data = {"key": "value"}
            serialized_data = pickle.dumps(data)

            expected_calls = [
                call(str(len(serialized_data)).encode("utf-8")),
                call("FINISH".encode("utf-8"))
            ]
            mock_conn.send.assert_has_calls(expected_calls)
            mock_conn.sendall.assert_called_once_with(serialized_data)

if __name__ == '__main__':
    unittest.main()
