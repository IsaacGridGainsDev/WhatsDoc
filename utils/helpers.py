import os
import datetime
import shutil
import zipfile
from pathlib import Path

def ensure_dir(directory):
    """
    Ensure a directory exists, creating it if necessary
    
    Args:
        directory (str): Directory path
        
    Returns:
        str: Directory path
    """
    os.makedirs(directory, exist_ok=True)
    return directory

def get_timestamp():
    """
    Get current timestamp in a formatted string
    
    Returns:
        str: Formatted timestamp (YYYY-MM-DD_HH-MM-SS)
    """
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def generate_filename(prefix, extension, directory=None):
    """
    Generate a filename with timestamp
    
    Args:
        prefix (str): Filename prefix
        extension (str): File extension (without dot)
        directory (str, optional): Directory path
        
    Returns:
        str: Generated filepath
    """
    filename = f"{prefix}_{get_timestamp()}.{extension}"
    
    if directory:
        ensure_dir(directory)
        return os.path.join(directory, filename)
    
    return filename

def create_zip_archive(files, output_path):
    """
    Create a ZIP archive of files
    
    Args:
        files (list): List of file paths to include
        output_path (str): Path to save the ZIP file
        
    Returns:
        str: Path to the created ZIP file
    """
    try:
        with zipfile.ZipFile(output_path, 'w') as zipf:
            for file in files:
                if os.path.exists(file):
                    zipf.write(file, os.path.basename(file))
        return output_path
    except Exception as e:
        print(f"Error creating ZIP archive: {str(e)}")
        return None

def sanitize_filename(filename):
    """
    Sanitize a filename by removing invalid characters
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Sanitized filename
    """
    # Replace invalid characters with underscore
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def get_file_extension(file_path):
    """
    Get the extension of a file
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: File extension (without dot)
    """
    return os.path.splitext(file_path)[1][1:].lower()

def is_audio_file(file_path):
    """
    Check if a file is an audio file based on extension
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        bool: True if file is an audio file, False otherwise
    """
    audio_extensions = ['mp3', 'm4a', 'wav', 'ogg', 'flac', 'aac']
    return get_file_extension(file_path) in audio_extensions

def is_image_file(file_path):
    """
    Check if a file is an image file based on extension
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        bool: True if file is an image file, False otherwise
    """
    image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff']
    return get_file_extension(file_path) in image_extensions

def format_file_size(size_bytes):
    """
    Format file size in human-readable format
    
    Args:
        size_bytes (int): File size in bytes
        
    Returns:
        str: Formatted file size
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"