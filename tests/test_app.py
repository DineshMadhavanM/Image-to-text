import unittest
import os
import tempfile
import json
from unittest.mock import patch, MagicMock
import io
from PIL import Image

# Import the Flask app
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app


class TestFlaskApp(unittest.TestCase):
    """Test cases for the Flask web application."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up after each test method."""
        if os.path.exists(self.test_dir):
            import shutil
            shutil.rmtree(self.test_dir)
    
    def create_test_image_file(self, filename="test.jpg", size=(224, 224), color='red'):
        """Create a test image file for upload testing."""
        image_path = os.path.join(self.test_dir, filename)
        image = Image.new('RGB', size, color=color)
        image.save(image_path)
        return image_path
    
    def get_image_data(self, image_path):
        """Get image data as bytes for file upload."""
        with open(image_path, 'rb') as f:
            return io.BytesIO(f.read())
    
    def test_index_page_loads(self):
        """Test that the index page loads successfully."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'html', response.data.lower())
    
    def test_allowed_file_function(self):
        """Test the allowed file validation function."""
        from app import allowed_file
        
        # Test allowed extensions
        self.assertTrue(allowed_file('test.jpg'))
        self.assertTrue(allowed_file('test.jpeg'))
        self.assertTrue(allowed_file('test.png'))
        self.assertTrue(allowed_file('test.gif'))
        
        # Test uppercase extensions
        self.assertTrue(allowed_file('test.JPG'))
        self.assertTrue(allowed_file('test.PNG'))
        
        # Test disallowed extensions
        self.assertFalse(allowed_file('test.txt'))
        self.assertFalse(allowed_file('test.pdf'))
        self.assertFalse(allowed_file('test.mp4'))
        
        # Test files without extensions
        self.assertFalse(allowed_file('test'))
        self.assertFalse(allowed_file('test.'))
    
    @patch('app.captioner.generate_caption')
    def test_generate_caption_success(self, mock_generate):
        """Test successful caption generation."""
        # Mock the caption generation
        mock_generate.return_value = "A spectacular moment as the player scores!"
        
        # Create test image
        image_path = self.create_test_image_file()
        image_data = self.get_image_data(image_path)
        
        # Make POST request
        response = self.client.post('/generate_caption', 
                                  data={'image': (image_data, 'test.jpg')},
                                  content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('caption', response_data)
        self.assertEqual(response_data['caption'], "A spectacular moment as the player scores!")
    
    def test_generate_caption_no_file(self):
        """Test caption generation when no file is provided."""
        response = self.client.post('/generate_caption', 
                                  data={},
                                  content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'No file part')
    
    def test_generate_caption_empty_filename(self):
        """Test caption generation with empty filename."""
        image_data = io.BytesIO(b'fake image data')
        
        response = self.client.post('/generate_caption', 
                                  data={'image': (image_data, '')},
                                  content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'No selected file')
    
    def test_generate_caption_invalid_file_type(self):
        """Test caption generation with invalid file type."""
        # Create a text file instead of image
        text_data = io.BytesIO(b'This is not an image file')
        
        response = self.client.post('/generate_caption', 
                                  data={'image': (text_data, 'test.txt')},
                                  content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'File type not allowed')
    
    @patch('app.captioner.generate_caption')
    def test_generate_caption_captioner_error(self, mock_generate):
        """Test caption generation when captioner raises an exception."""
        # Mock the caption generation to raise an exception
        mock_generate.side_effect = Exception("Model loading failed")
        
        # Create test image
        image_path = self.create_test_image_file()
        image_data = self.get_image_data(image_path)
        
        # Make POST request
        response = self.client.post('/generate_caption', 
                                  data={'image': (image_data, 'test.jpg')},
                                  content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 500)
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)
        self.assertIn('Model loading failed', response_data['error'])
    
    def test_upload_folder_creation(self):
        """Test that upload folder is created."""
        self.assertTrue(os.path.exists(app.config['UPLOAD_FOLDER']))
    
    @patch('app.captioner.generate_caption')
    def test_file_cleanup_after_success(self, mock_generate):
        """Test that temporary files are cleaned up after successful processing."""
        mock_generate.return_value = "Test caption"
        
        # Create test image
        image_path = self.create_test_image_file()
        image_data = self.get_image_data(image_path)
        
        # Make POST request
        response = self.client.post('/generate_caption', 
                                  data={'image': (image_data, 'test_cleanup.jpg')},
                                  content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 200)
        
        # Check that the temporary file was cleaned up
        temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'test_cleanup.jpg')
        self.assertFalse(os.path.exists(temp_file_path))
    
    @patch('app.captioner.generate_caption')
    def test_file_cleanup_after_error(self, mock_generate):
        """Test that temporary files are cleaned up even when processing fails."""
        mock_generate.side_effect = Exception("Processing failed")
        
        # Create test image
        image_path = self.create_test_image_file()
        image_data = self.get_image_data(image_path)
        
        # Make POST request
        response = self.client.post('/generate_caption', 
                                  data={'image': (image_data, 'test_error_cleanup.jpg')},
                                  content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 500)
        
        # Check that the temporary file was cleaned up even after error
        temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'test_error_cleanup.jpg')
        self.assertFalse(os.path.exists(temp_file_path))
    
    def test_max_file_size_config(self):
        """Test that max file size is properly configured."""
        self.assertEqual(app.config['MAX_CONTENT_LENGTH'], 16 * 1024 * 1024)  # 16MB
    
    def test_different_image_formats(self):
        """Test that different image formats are accepted."""
        formats = [
            ('test.jpg', 'JPEG'),
            ('test.jpeg', 'JPEG'),
            ('test.png', 'PNG'),
            ('test.gif', 'GIF')
        ]
        
        for filename, format_name in formats:
            with self.subTest(format=format_name):
                # Create test image
                image_path = self.create_test_image_file(filename=filename, color='blue')
                image_data = self.get_image_data(image_path)
                
                # Mock caption generation
                with patch('app.captioner.generate_caption') as mock_generate:
                    mock_generate.return_value = f"Caption for {format_name}"
                    
                    response = self.client.post('/generate_caption', 
                                              data={'image': (image_data, filename)},
                                              content_type='multipart/form-data')
                    
                    self.assertEqual(response.status_code, 200)
                    response_data = json.loads(response.data)
                    self.assertIn('caption', response_data)
    
    def test_secure_filename_handling(self):
        """Test that filenames are properly secured."""
        # Test with potentially dangerous filename
        dangerous_names = [
            '../../../etc/passwd.jpg',
            'test file with spaces.jpg',
            'test@file.jpg',
            'test#file.jpg'
        ]
        
        for dangerous_name in dangerous_names:
            with self.subTest(filename=dangerous_name):
                image_path = self.create_test_image_file(filename='safe.jpg')
                image_data = self.get_image_data(image_path)
                
                with patch('app.captioner.generate_caption') as mock_generate:
                    mock_generate.return_value = "Test caption"
                    
                    response = self.client.post('/generate_caption', 
                                              data={'image': (image_data, dangerous_name)},
                                              content_type='multipart/form-data')
                    
                    # Should still work (filename is secured in the backend)
                    self.assertEqual(response.status_code, 200)


class TestFlaskAppIntegration(unittest.TestCase):
    """Integration tests for the Flask application."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up after integration tests."""
        if os.path.exists(self.test_dir):
            import shutil
            shutil.rmtree(self.test_dir)
    
    def test_full_workflow_integration(self):
        """Test the complete workflow from file upload to caption generation."""
        # Create a realistic test image
        image_path = os.path.join(self.test_dir, "integration_test.jpg")
        image = Image.new('RGB', (256, 256), color='green')
        image.save(image_path)
        
        # Upload image and get caption
        with open(image_path, 'rb') as f:
            image_data = io.BytesIO(f.read())
        
        response = self.client.post('/generate_caption', 
                                  data={'image': (image_data, 'integration_test.jpg')},
                                  content_type='multipart/form-data')
        
        # Should get a successful response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('caption', response_data)
        self.assertIsInstance(response_data['caption'], str)
        self.assertTrue(len(response_data['caption']) > 0)
    
    def test_concurrent_requests(self):
        """Test handling of multiple concurrent requests."""
        import threading
        import time
        
        results = []
        
        def make_request():
            image_path = os.path.join(self.test_dir, f"concurrent_{threading.get_ident()}.jpg")
            image = Image.new('RGB', (100, 100), color='red')
            image.save(image_path)
            
            with open(image_path, 'rb') as f:
                image_data = io.BytesIO(f.read())
            
            response = self.client.post('/generate_caption', 
                                      data={'image': (image_data, f'concurrent_{threading.get_ident()}.jpg')},
                                      content_type='multipart/form-data')
            results.append(response.status_code)
        
        # Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        self.assertEqual(len(results), 5)
        for status_code in results:
            self.assertEqual(status_code, 200)


if __name__ == '__main__':
    unittest.main()
