""
Utility functions for file operations in the Sports Captioner application.
"""
import os
import shutil
import logging
from pathlib import Path
from typing import List, Optional, Union, Tuple
from datetime import datetime

# Set up logging
logger = logging.getLogger(__name__)


def ensure_directory_exists(directory: Union[str, Path]) -> Path:
    """Ensure a directory exists, create it if it doesn't.
    
    Args:
        directory: Path to the directory
        
    Returns:
        Path: Path object of the directory
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_file_extension(filename: str) -> str:
    """Get the lowercase extension of a file.
    
    Args:
        filename: Name of the file
        
    Returns:
        str: File extension in lowercase (e.g., '.jpg', '.png')
    """
    return Path(filename).suffix.lower()


def is_valid_image_file(filename: str, allowed_extensions: set) -> bool:
    """Check if a file has a valid image extension.
    
    Args:
        filename: Name of the file to check
        allowed_extensions: Set of allowed file extensions (e.g., {'.jpg', '.png'})
        
    Returns:
        bool: True if the file has a valid extension, False otherwise
    """
    return get_file_extension(filename) in allowed_extensions


def save_uploaded_file(file, upload_folder: Union[str, Path], allowed_extensions: set) -> Tuple[bool, str]:
    """Save an uploaded file to the specified folder.
    
    Args:
        file: File object from request.files
        upload_folder: Directory to save the uploaded file
        allowed_extensions: Set of allowed file extensions
        
    Returns:
        Tuple[bool, str]: (success status, message or filepath)
    """
    if not file or file.filename == '':
        return False, 'No file selected'
    
    if not is_valid_image_file(file.filename, allowed_extensions):
        return False, f'Invalid file type. Allowed types: {", ".join(allowed_extensions)}'
    
    try:
        # Create upload directory if it doesn't exist
        upload_path = ensure_directory_exists(upload_folder)
        
        # Generate a unique filename to prevent overwriting
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = get_file_extension(file.filename)
        filename = f"upload_{timestamp}{file_extension}"
        filepath = upload_path / filename
        
        # Save the file
        file.save(str(filepath))
        logger.info(f"File saved successfully: {filepath}")
        return True, str(filepath)
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        return False, f'Error saving file: {str(e)}'


def delete_file(filepath: Union[str, Path]) -> bool:
    """Delete a file if it exists.
    
    Args:
        filepath: Path to the file to delete
        
    Returns:
        bool: True if file was deleted or didn't exist, False otherwise
    """
    try:
        path = Path(filepath)
        if path.exists() and path.is_file():
            path.unlink()
            logger.info(f"Deleted file: {filepath}")
        return True
    except Exception as e:
        logger.error(f"Error deleting file {filepath}: {e}")
        return False


def clean_directory(directory: Union[str, Path], 
                  extensions: Optional[set] = None,
                  older_than_days: Optional[int] = None) -> bool:
    """Clean files in a directory based on criteria.
    
    Args:
        directory: Directory to clean
        extensions: Optional set of file extensions to include (None for all)
        older_than_days: Optional number of days (delete files older than this)
        
    Returns:
        bool: True if operation completed successfully
    """
    try:
        path = Path(directory)
        if not path.exists() or not path.is_dir():
            return False
            
        current_time = datetime.now()
        
        for item in path.iterdir():
            if item.is_file():
                # Check file extension if filter is provided
                if extensions and item.suffix.lower() not in extensions:
                    continue
                    
                # Check file age if filter is provided
                if older_than_days is not None:
                    file_mtime = datetime.fromtimestamp(item.stat().st_mtime)
                    if (current_time - file_mtime).days < older_than_days:
                        continue
                        
                # Delete the file
                item.unlink()
                logger.info(f"Cleaned up file: {item}")
                
        return True
    except Exception as e:
        logger.error(f"Error cleaning directory {directory}: {e}")
        return False


def get_directory_size(directory: Union[str, Path]) -> int:
    """Calculate the total size of a directory in bytes.
    
    Args:
        directory: Path to the directory
        
    Returns:
        int: Total size in bytes
    """
    try:
        path = Path(directory)
        return sum(f.stat().st_size for f in path.glob('**/*') if f.is_file())
    except Exception as e:
        logger.error(f"Error calculating directory size {directory}: {e}")
        return 0


if __name__ == "__main__":
    # Example usage
    upload_dir = Path("uploads")
    ensure_directory_exists(upload_dir)
    print(f"Directory exists: {upload_dir.exists()}")
    
    # Example of getting directory size
    size_bytes = get_directory_size(upload_dir)
    print(f"Directory size: {size_bytes / (1024 * 1024):.2f} MB")
