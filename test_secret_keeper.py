import unittest
from app import home
from pywebio import start_server
import requests
import threading

class TestSecretKeeper(unittest.TestCase):
    def setUp(self):
        # Start the PyWebIO server in a separate thread for testing
        self.server_thread = threading.Thread(target=self.start_pywebio_server)
        self.server_thread.daemon = True  # Set the thread as a daemon so it will exit when the main program exits
        self.server_thread.start()
        # Give the server some time to start
        import time
        time.sleep(1)

    def start_pywebio_server(self):
        start_server(home, port=8085)

    def test_application_up(self):
        # Test if the application is up by sending a GET request
        response = requests.get('http://localhost:8085/')
        self.assertEqual(response.status_code, 200)  # Should return a 200 status code

if __name__ == '__main__':
    unittest.main()
