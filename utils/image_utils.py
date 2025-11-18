""
Utility functions for image processing and validation.
"""
import os
from typing import Tuple, Optional
from PIL import Image, UnidentifiedImageError

def validate_image(file_path: str) -> Tuple[bool, Optional[str]]:
    """
    Validate if the file is a valid image.
    
    Args:
        file_path: Path to the image file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not os.path.exists(file_path):
        return False, "File does not exist"
        
    if not os.path.isfile(file_path):
        return False, "Path is not a file"
        
    valid_extensions = ('.jpg', '.jpeg', '.png')
    if not file_path.lower().endswith(valid_extensions):
        return False, f"Unsupported file format. Supported formats: {', '.join(valid_extensions)}"
    
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True, None
    except (UnidentifiedImageError, Exception) as e:
        return False, f"Invalid image file: {str(e)}"

def get_image_metadata(file_path: str) -> dict:
    """
    Get metadata for an image file.
    
    Args:
        file_path: Path to the image file
        
    Returns:
        Dictionary containing image metadata
    """
    try:
        with Image.open(file_path) as img:
            return {
                'format': img.format,
                'mode': img.mode,
                'size': img.size,
                'width': img.width,
                'height': img.height,
                'file_size': os.path.getsize(file_path)
            }
    except Exception as e:
        return {'error': str(e)}

def resize_image(
    file_path: str, 
    output_path: str, 
    max_size: Tuple[int, int] = (800, 800)
) -> bool:
    """
    Resize an image while maintaining aspect ratio.
    
    Args:
        file_path: Path to the source image
        output_path: Path to save the resized image
        max_size: Maximum (width, height) of the output image
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with Image.open(file_path) as img:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            img.save(output_path)
            return True
    except Exception as e:
        return False
