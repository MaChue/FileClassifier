import os
import unittest
from flask import Flask
from app import app, UploadAgent, ClassifierAgent, MoveFileAgent
from werkzeug.datastructures import FileStorage

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def test_upload_file(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_upload_files(self):
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        with open('uploads/test_file.txt', 'w') as f:
            f.write('This is a test file.')
        with open('uploads/test_file.txt', 'rb') as f:
            file = FileStorage(stream=f, filename='test_file.txt')
            data = {
                'file': file
            }
            response = self.client.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 302)

    def test_UploadAgent(self):
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        with open('uploads/test_file.txt', 'w') as f:
            f.write('This is a test file.')
        with open('uploads/test_file.txt', 'r') as f:
            file = FileStorage(stream=f, filename='test_file.txt')
            UploadAgent(file)
        self.assertTrue(os.path.exists('safe/test_file.txt') or os.path.exists('suspicious/test_file.txt'))

    def test_ClassifierAgent(self):
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        with open('uploads/test_file.txt', 'w') as f:
            f.write('This is a test file.')
        ClassifierAgent('test_file.txt')
        self.assertTrue(os.path.exists('safe/test_file.txt') or os.path.exists('suspicious/test_file.txt'))

    def test_MoveFileAgent(self):
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        with open('uploads/test_file.txt', 'w') as f:
            f.write('This is a test file.')
        MoveFileAgent('test_file.txt', 'safe')
        self.assertTrue(os.path.exists('safe/test_file.txt'))

    
    def test_view_files(self):
        response = self.client.get('/view')
        self.assertEqual(response.status_code, 200)
    
    def tearDown(self):
        if os.path.exists('uploads/test_file.txt'):
            os.remove('uploads/test_file.txt')
        if os.path.exists('safe/test_file.txt'):
            os.remove('safe/test_file.txt')
        if os.path.exists('suspicious/test_file.txt'):
            os.remove('suspicious/test_file.txt')

if __name__ == "__main__":
    unittest.main()
