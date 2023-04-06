python GUI_chat_client.py
python GUI_chat_server_test_ver2.py 

test_load_database unittest: This test case checks whether the loadDatabase function correctly reads a pickled file and calls the unpackage_data function with the correct arguments.

The unittest alsot checks if the loadDatabase function raises an exception when the pickled data is invalid (e.g., corrupted or not a pickled file), and checks if the loadDatabase function correctly reads a pickled file with a custom server name, and whether the pickle.load function is called.

We also have test case to check if the get_timestamp function returns the correct Unix timestamp (seconds since the epoch) value based on the current time in the UTC timezone. Moreover, we check if the send_pickled_data function sends the serialized data correctly over a socket connection. They use MagicMock instances for sockets and mock the package_data function to return either an empty dictionary or a custom dictionary as needed. Finally, we check if the updateDatabase function properly updates the database by serializing data and writing it to a temporary file, followed by replacing the original file. The test case uses MagicMock instances for NamedTemporaryFile, the os.replace function, and the package_data function. It also uses mock_open to mock the file writing process.