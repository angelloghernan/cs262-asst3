import unittest
import time
import calendar
from GUI_chat_server_test_ver2 import get_timestamp

class TestGetTimestamp(unittest.TestCase):
    def test_get_timestamp(self):
        timestamp = get_timestamp()
        gmt = time.gmtime()
        expected_timestamp = calendar.timegm(gmt)
        self.assertEqual(timestamp, expected_timestamp)

if __name__ == '__main__':
    unittest.main()
