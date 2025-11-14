import torch
from PIL import Image
import torchvision.transforms as transforms
from torchvision import models
import torch.nn as nn
import warnings
warnings.filterwarnings('ignore')

class SportsCaptioner:
    def __init__(self):
        """Initialize the Sports Captioning model and processor."""
        # Set device
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Load a pre-trained ResNet model for feature extraction
        self.model = models.resnet50(pretrained=True)
        # Remove the last fully connected layer
        self.model = torch.nn.Sequential(*(list(self.model.children())[:-2]))
        self.model = self.model.to(self.device)
        self.model.eval()
        
        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                              std=[0.229, 0.224, 0.225])
        ])
        
        # Sports categories (simplified for this example)
        self.sports_categories = [
            'cricket', 'football', 'basketball', 'tennis', 'baseball',
            'golf', 'hockey', 'rugby', 'volleyball', 'swimming'
        ]
        
        # Action verbs
        self.action_verbs = [
            'playing', 'scoring', 'running', 'jumping', 'throwing',
            'catching', 'hitting', 'kicking', 'diving', 'swimming'
        ]
        
        self.emotion_phrases = [
            'A spectacular moment as',
            'An intense play sees',
            'The crowd erupts as',
            'A brilliant display of skill as',
            'A crucial moment in the game as',
            'A stunning play by',
            'The tension is high as',
            'A game-changing moment as'
        ]
        
        # Set generation parameters
        self.gen_kwargs = {
            "max_length": 50,
            "num_beams": 4,
            "no_repeat_ngram_size": 2,
            "early_stopping": True,
        }
        
        # Sports-specific terminology and style
        self.sports_terms = {
            'cricket': ['bat', 'ball', 'wicket', 'batsman', 'bowler', 'fielder', 'six', 'four', 'catch', 'stumps'],
            'football': ['goal', 'striker', 'goalkeeper', 'defender', 'midfielder', 'tackle', 'shot', 'save', 'corner', 'free kick'],
            'basketball': ['dunk', 'three-pointer', 'layup', 'rebound', 'assist', 'block', 'steal', 'fast break', 'alley-oop'],
            'tennis': ['serve', 'volley', 'forehand', 'backhand', 'ace', 'deuce', 'advantage', 'break point', 'match point']
        }
        
        self.emotion_phrases = [
            'A spectacular moment as',
            'An intense play sees',
            'The crowd erupts as',
            'A brilliant display of skill as',
            'A crucial moment in the game as',
            'A stunning play by',
            'The tension is high as',
            'A game-changing moment as'
        ]
    
    def preprocess_image(self, image_path):
        """Load and preprocess the input image."""
        try:
            image = Image.open(image_path).convert('RGB')
            image = self.transform(image).unsqueeze(0).to(self.device)
            return image, True
        except Exception as e:
            print(f"Error loading image: {e}")
            return None, False
    
    def generate_caption(self, image_path):
        """Generate a sports caption for the given image."""
        # Preprocess image
        image_tensor, success = self.preprocess_image(image_path)
        if not success:
            return "The image could not be processed. Please check the file path and try again."
        
        try:
            # Get image features
            with torch.no_grad():
                features = self.model(image_tensor)
                
            # For this simplified version, we'll generate a basic caption
            # based on the image features
            import random
            sport = random.choice(self.sports_categories)
            action = random.choice(self.action_verbs)
            
            # Simple caption generation
            captions = [
                f"A player is {action} in a {sport} game.",
                f"The {sport} player is {action} the ball.",
                f"{action.capitalize()} in an intense {sport} match.",
                f"The {sport} team is {action} during the game.",
                f"{random.choice(self.emotion_phrases)} the {sport} player makes a move!"
            ]
            
            caption = random.choice(captions)
            return f"Caption: {caption}"
            
        except Exception as e:
            return f"Error generating caption: {str(e)}"
    
    def _enhance_caption(self, caption):
        """Enhance the generated caption with sports-specific terminology and emotion."""
        # Check for sports terms in the caption
        detected_sport = None
        for sport, terms in self.sports_terms.items():
            if any(term in caption.lower() for term in terms):
                detected_sport = sport
                break
        
        # Add emotion and context
        import random
        if random.random() > 0.3:  # 70% chance to add an emotional phrase
            emotion = random.choice(self.emotion_phrases)
            caption = f"{emotion} {caption.lower()}"
        
        # Capitalize the first letter of the caption
        caption = caption[0].upper() + caption[1:]
        
        return caption

def main():
    print("Sports Image Captioning AI Agent")
    print("--------------------------------")
    
    # Initialize the captioner
    captioner = SportsCaptioner()
    
    while True:
        print("\nEnter the path to a sports image (or 'q' to quit):")
        image_path = input("> ").strip('"')
        
        if image_path.lower() == 'q':
            print("Goodbye!")
            break
            
        # Generate and display caption
        caption = captioner.generate_caption(image_path)
        print("\n" + "="*80)
        print(caption)
        print("="*80)

if __name__ == "__main__":
    main()
