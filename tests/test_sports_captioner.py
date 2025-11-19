import unittest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from PIL import Image
import numpy as np

# Import the actual module
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from sports_captioner import SportsCaptioner


class TestSportsCaptioner(unittest.TestCase):
    """Test cases for the SportsCaptioner class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.captioner = SportsCaptioner()
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up after each test method."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def create_test_image(self, filename="test.jpg", size=(224, 224)):
        """Create a test image file."""
        image_path = os.path.join(self.test_dir, filename)
        # Create a simple test image
        image = Image.new('RGB', size, color='red')
        image.save(image_path)
        return image_path
    
    def test_initialization(self):
        """Test that SportsCaptioner initializes correctly."""
        self.assertIsNotNone(self.captioner.model)
        self.assertIsNotNone(self.captioner.transform)
        self.assertIsNotNone(self.captioner.sports_categories)
        self.assertIsNotNone(self.captioner.action_verbs)
        self.assertIsNotNone(self.captioner.emotion_phrases)
        self.assertEqual(len(self.captioner.sports_categories), 10)
        self.assertEqual(len(self.captioner.action_verbs), 10)
        self.assertEqual(len(self.captioner.emotion_phrases), 8)
    
    def test_preprocess_image_valid_file(self):
        """Test image preprocessing with a valid file."""
        image_path = self.create_test_image()
        image_tensor, success = self.captioner.preprocess_image(image_path)
        
        self.assertTrue(success)
        self.assertIsNotNone(image_tensor)
        # Check tensor shape: should be (1, 3, 224, 224)
        self.assertEqual(image_tensor.shape, (1, 3, 224, 224))
    
    def test_preprocess_image_invalid_file(self):
        """Test image preprocessing with an invalid file."""
        invalid_path = os.path.join(self.test_dir, "nonexistent.jpg")
        image_tensor, success = self.captioner.preprocess_image(invalid_path)
        
        self.assertFalse(success)
        self.assertIsNone(image_tensor)
    
    def test_generate_caption_valid_image(self):
        """Test caption generation with a valid image."""
        image_path = self.create_test_image()
        caption = self.captioner.generate_caption(image_path)
        
        self.assertIsInstance(caption, str)
        self.assertTrue(len(caption) > 0)
        self.assertIn("Caption:", caption)
    
    def test_generate_caption_invalid_image(self):
        """Test caption generation with an invalid image."""
        invalid_path = os.path.join(self.test_dir, "nonexistent.jpg")
        caption = self.captioner.generate_caption(invalid_path)
        
        self.assertIsInstance(caption, str)
        self.assertIn("could not be processed", caption.lower())
    
    def test_sports_categories_coverage(self):
        """Test that all major sports are covered."""
        expected_sports = ['cricket', 'football', 'basketball', 'tennis', 'baseball',
                          'golf', 'hockey', 'rugby', 'volleyball', 'swimming']
        
        for sport in expected_sports:
            self.assertIn(sport, self.captioner.sports_categories)
    
    def test_action_verbs_variety(self):
        """Test that action verbs are diverse and appropriate."""
        expected_verbs = ['playing', 'scoring', 'running', 'jumping', 'throwing',
                          'catching', 'hitting', 'kicking', 'diving', 'swimming']
        
        for verb in expected_verbs:
            self.assertIn(verb, self.captioner.action_verbs)
    
    def test_emotion_phrases_engagement(self):
        """Test that emotion phrases add engagement."""
        for phrase in self.captioner.emotion_phrases:
            self.assertIsInstance(phrase, str)
            self.assertTrue(len(phrase) > 0)
            # Check that phrases contain emotional words
            emotional_words = ['spectacular', 'intense', 'erupts', 'brilliant', 'crucial', 'stunning', 'tension', 'game-changing']
            self.assertTrue(any(word in phrase.lower() for word in emotional_words))
    
    def test_sports_terms_structure(self):
        """Test that sports terms dictionary is properly structured."""
        self.assertIsInstance(self.captioner.sports_terms, dict)
        
        for sport, terms in self.captioner.sports_terms.items():
            self.assertIsInstance(sport, str)
            self.assertIsInstance(terms, list)
            self.assertTrue(len(terms) > 0)
            for term in terms:
                self.assertIsInstance(term, str)
    
    def test_enhance_caption_functionality(self):
        """Test the caption enhancement functionality."""
        test_caption = "a player hits the ball"
        enhanced = self.captioner._enhance_caption(test_caption)
        
        self.assertIsInstance(enhanced, str)
        self.assertTrue(len(enhanced) >= len(test_caption))
        # Should start with capital letter
        self.assertEqual(enhanced[0], enhanced[0].upper())
    
    @patch('random.choice')
    def test_caption_generation_deterministic(self, mock_choice):
        """Test caption generation with mocked randomness."""
        # Mock random.choice to return predictable values
        mock_choice.side_effect = ['cricket', 'playing', 'A spectacular moment as']
        
        image_path = self.create_test_image()
        caption = self.captioner.generate_caption(image_path)
        
        self.assertIn('cricket', caption.lower())
        self.assertIn('playing', caption.lower())
        self.assertIn('spectacular', caption.lower())
    
    def test_device_configuration(self):
        """Test that the model is properly configured for the device."""
        self.assertIsNotNone(self.captioner.device)
        # Device should be either 'cuda' or 'cpu'
        self.assertIn(self.captioner.device.type, ['cuda', 'cpu'])
    
    def test_model_evaluation_mode(self):
        """Test that the model is in evaluation mode."""
        # PyTorch models in eval mode should have training=False
        self.assertFalse(self.captioner.model.training)
    
    def test_generation_parameters(self):
        """Test that generation parameters are properly set."""
        expected_params = ['max_length', 'num_beams', 'no_repeat_ngram_size', 'early_stopping']
        
        for param in expected_params:
            self.assertIn(param, self.captioner.gen_kwargs)
        
        # Check reasonable parameter values
        self.assertGreater(self.captioner.gen_kwargs['max_length'], 0)
        self.assertGreater(self.captioner.gen_kwargs['num_beams'], 0)


class TestSportsCaptionerIntegration(unittest.TestCase):
    """Integration tests for the SportsCaptioner."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.captioner = SportsCaptioner()
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up after integration tests."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_full_workflow(self):
        """Test the complete workflow from image to caption."""
        # Create test image
        image_path = os.path.join(self.test_dir, "workflow_test.jpg")
        image = Image.new('RGB', (256, 256), color='blue')
        image.save(image_path)
        
        # Process image
        image_tensor, success = self.captioner.preprocess_image(image_path)
        self.assertTrue(success)
        
        # Generate caption
        caption = self.captioner.generate_caption(image_path)
        self.assertIsInstance(caption, str)
        self.assertTrue(len(caption) > 0)
        
        # Verify caption structure
        self.assertIn("Caption:", caption)
        caption_text = caption.replace("Caption:", "").strip()
        self.assertTrue(len(caption_text) > 0)
    
    def test_multiple_image_processing(self):
        """Test processing multiple different images."""
        images = []
        captions = []
        
        for i, color in enumerate(['red', 'green', 'blue']):
            image_path = os.path.join(self.test_dir, f"test_{i}.jpg")
            image = Image.new('RGB', (224, 224), color=color)
            image.save(image_path)
            images.append(image_path)
            
            caption = self.captioner.generate_caption(image_path)
            captions.append(caption)
        
        # Verify all captions are generated
        self.assertEqual(len(images), len(captions))
        for caption in captions:
            self.assertIsInstance(caption, str)
            self.assertIn("Caption:", caption)


if __name__ == '__main__':
    unittest.main()
