import os
import unittest
from flask import Flask
from app import app, UploadAgent, ClassifierAgent, MoveFileAgent
from werkzeug.datastructures import FileStorage

# We use unittest.TestCase as the base class for our test case as it provides a rich set of methods for assertions and setup/teardown routines.
class AppTestCase(unittest.TestCase):

    def setUp(self):
        # We use Flask's built-in test client for our tests. This allows us to simulate HTTP requests to our application without needing to run an actual server.
        self.app = app
        self.client = self.app.test_client()

    def test_upload_file(self):
        # We test the home page as a simple smoke test to ensure the app is running correctly.
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_upload_files(self):
        # We create the uploads directory if it doesn't exist. This is to ensure that the file upload functionality can be tested even if the directory was deleted.
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        # We create a test file to simulate a user uploading a file.
        with open('uploads/test_file.txt', 'w') as f:
            f.write('This is a test file.')
        # We use Werkzeug's FileStorage class to simulate a file being uploaded.
        with open('uploads/test_file.txt', 'rb') as f:
            file = FileStorage(stream=f, filename='test_file.txt')
            data = {
                'file': file
            }
            # We send a POST request to the upload endpoint with the test file to test the file upload functionality.
            response = self.client.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 302)

    def test_UploadAgent(self):
        # We test the UploadAgent function by creating a test file and checking that it is correctly moved to the safe or suspicious directory.
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        with open('uploads/test_file.txt', 'w') as f:
            f.write('This is a test file.')
        with open('uploads/test_file.txt', 'r') as f:
            file = FileStorage(stream=f, filename='test_file.txt')
            UploadAgent(file)
        self.assertTrue(os.path.exists('safe/test_file.txt') or os.path.exists('suspicious/test_file.txt'))

    def test_ClassifierAgent(self):
        # We test the ClassifierAgent function by creating a test file and checking that it is correctly classified and moved to the safe or suspicious directory.
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        with open('uploads/test_file.txt', 'w') as f:
            f.write('This is a test file.')
        ClassifierAgent('test_file.txt')
        self.assertTrue(os.path.exists('safe/test_file.txt') or os.path.exists('suspicious/test_file.txt'))

    def test_MoveFileAgent(self):
        # We test the MoveFileAgent function by creating a test file and checking that it is correctly moved to the specified directory.
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        with open('uploads/test_file.txt', 'w') as f:
            f.write('This is a test file.')
        MoveFileAgent('test_file.txt', 'safe')
        self.assertTrue(os.path.exists('safe/test_file.txt'))

    def test_view_files(self):
        # We test the view files endpoint to ensure it is working correctly.
        response = self.client.get('/view')
        self.assertEqual(response.status_code, 200)
    
    def tearDown(self):
        # We clean up the test files after each test to ensure that the file system is in a clean state for the next test.
        if os.path.exists('uploads/test_file.txt'):
            os.remove('uploads/test_file.txt')
        if os.path.exists('safe/test_file.txt'):
            os.remove('safe/test_file.txt')
        if os.path.exists('suspicious/test_file.txt'):
            os.remove('suspicious/test_file.txt')

# We use the standard Python idiom for the main entry point of the script. This allows the script to be used both as a standalone program and as a module in other scripts.
if __name__ == "__main__":
    unittest.main()
