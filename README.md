# Sports Image Captioning AI Agent

An AI-powered tool that generates natural language descriptions for sports-related images, including cricket, football, basketball, tennis, and more.

## Features

- Automatically detects sports actions and players in images
- Generates engaging, human-like captions
- Supports multiple sports including cricket, football, basketball, and tennis
- Adds emotional context to make captions more engaging
- Works on both CPU and GPU (if available)

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the script with:
```
python sports_captioner.py
```

When prompted, enter the path to a sports image file. The AI will analyze the image and generate a caption.

## Example Usage

```
Enter the path to a sports image (or 'q' to quit):
> path/to/your/image.jpg

================================================================================
Caption: A spectacular moment as the batsman drives the ball through the covers for four runs.
================================================================================
```

## Supported Sports

- Cricket
- Football (Soccer)
- Basketball
- Tennis
- And more! (The AI can often generalize to other sports as well)

## Requirements

- Python 3.7+
- PyTorch
- Transformers
- Pillow
- NumPy
- SentencePiece

## Note

- The first run will download the pre-trained model (about 1.5GB)
- For best results, use clear images with visible sports action
- The AI works best with images that clearly show the sport being played
