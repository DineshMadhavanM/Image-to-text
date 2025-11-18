""
Tests for image_utils.py
"""
import os
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the module to test
from utils.image_utils import validate_image, get_image_metadata, resize_image

class TestImageUtils(unittest.TestCase):
    """Test cases for image utilities."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_image = os.path.join(self.test_dir, '..', 'static', 'test_image.jpg')
        self.temp_dir = tempfile.mkdtemp()
        
    def test_validate_image_nonexistent(self):
        """Test validation of non-existent image."""
        result, message = validate_image("nonexistent.jpg")
        self.assertFalse(result)
        self.assertIn("does not exist", message.lower())
        
    @patch('PIL.Image.open')
    def test_validate_image_invalid(self, mock_open):
        """Test validation of invalid image."""
        mock_open.side_effect = Exception("Invalid image")
        result, message = validate_image("dummy.jpg")
        self.assertFalse(result)
        self.assertIn("invalid", message.lower())
        
    @patch('PIL.Image.open')
    def test_get_image_metadata(self, mock_open):
        """Test getting image metadata."""
        # Create a mock image
        mock_img = MagicMock()
        mock_img.format = 'JPEG'
        mock_img.mode = 'RGB'
        mock_img.size = (800, 600)
        mock_img.width = 800
        mock_img.height = 600
        mock_open.return_value.__enter__.return_value = mock_img
        
        # Mock file size
        with patch('os.path.getsize', return_value=1024):
            metadata = get_image_metadata("dummy.jpg")
            
        self.assertEqual(metadata['format'], 'JPEG')
        self.assertEqual(metadata['mode'], 'RGB')
        self.assertEqual(metadata['size'], (800, 600))
        self.assertEqual(metadata['file_size'], 1024)
        
    @patch('PIL.Image.Image.thumbnail')
    @patch('PIL.Image.open')
    def test_resize_image(self, mock_open, mock_thumbnail):
        """Test image resizing."""
        # Setup mock
        mock_img = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_img
        
        # Call the function
        result = resize_image("input.jpg", "output.jpg")
        
        # Assertions
        self.assertTrue(result)
        mock_thumbnail.assert_called_once()
        mock_img.save.assert_called_once_with("output.jpg")

if __name__ == '__main__':
    unittest.main()
