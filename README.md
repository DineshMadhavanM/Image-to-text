<div align="center">
  <h1>🏆 Sports Image Captioning AI Agent</h1>
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
  [![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/DineshMadhavanM/Image-to-text/issues)

  An AI-powered tool that generates natural language descriptions for sports-related images.
</div>

## 🚀 Features

- 🏏 Automatically detects sports actions and players in images
- ⚽ Generates engaging, human-like captions
- 🏀 Supports multiple sports including cricket, football, and basketball
- 🎾 Adds emotional context to make captions more engaging
- ⚡ Works on both CPU and GPU (if available)

## 📦 Installation

1. Clone this repository
   ```bash
   git clone https://github.com/DineshMadhavanM/Image-to-text.git
   cd Image-to-text
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Usage

Run the script with:
```bash
python sports_captioner.py
```

When prompted, enter the path to a sports image file. The AI will analyze the image and generate a caption.

### Example Usage

```bash
Enter the path to a sports image (or 'q' to quit):
> path/to/your/image.jpg

================================================================================
Caption: A spectacular moment as the batsman drives the ball through the covers for four runs.
================================================================================
```

## 🏆 Supported Sports

- Cricket 🏏
- Football (Soccer) ⚽
- Basketball 🏀
- Tennis 🎾
- And more! (The AI can often generalize to other sports as well)

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) to get started.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔒 Security

For security-related issues, please review our [Security Policy](SECURITY.md).

## 📬 Contact

For questions or feedback, please open an issue on GitHub.

---

<div align="center">
  Made with ❤️ by Dinesh Madhavan
</div>

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
