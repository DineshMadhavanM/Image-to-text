"""
Configuration settings for the Sports Captioner application.

This file contains all the configurable parameters for the application.
"""
from pathlib import Path
from typing import Dict, List, Union

# Base directory
BASE_DIR = Path(__file__).parent.absolute()

# Application settings
APP_NAME = "Sports Captioner"
VERSION = "1.0.0"
DEBUG = True

# File paths
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"
LOG_DIR = BASE_DIR / "logs"
UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"

# Create necessary directories
for directory in [DATA_DIR, MODEL_DIR, LOG_DIR, UPLOAD_FOLDER]:
    directory.mkdir(exist_ok=True, parents=True)

# Model settings
MODEL_CONFIG = {
    "default_model": "sports-captioner-v1",
    "max_length": 128,
    "num_beams": 5,
    "temperature": 0.9,
}

# API settings (if applicable)
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": True,
}

# Supported image formats
SUPPORTED_IMAGE_FORMATS = {
    ".jpg", ".jpeg", ".png", ".webp", ".bmp"
}

# Logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": LOG_DIR / "sports_captioner.log",
            "formatter": "standard",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

def get_config() -> Dict[str, Union[str, int, bool, Dict]]:
    """Return the current configuration as a dictionary."""
    return {
        "app_name": APP_NAME,
        "version": VERSION,
        "debug": DEBUG,
        "model_config": MODEL_CONFIG,
        "api_config": API_CONFIG,
    }
