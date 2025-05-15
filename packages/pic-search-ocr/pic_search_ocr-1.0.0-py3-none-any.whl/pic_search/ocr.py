import os
import logging
import pytesseract
from PIL import Image

# 1. Define supported image extensions
SUPPORTED_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".gif")

# Configure a logger for this module
logger = logging.getLogger(__name__)

def image_contains_text(image_path: str, search_text: str, tesseract_cmd: str | None = None) -> bool:
    """ 
    Checks if the given image contains the search_text using Tesseract OCR.

    Args:
        image_path: Path to the image file.
        search_text: The text string to search for (case-insensitive).
        tesseract_cmd: Optional path to the Tesseract executable.

    Returns:
        True if the text is found, False otherwise.
    """
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    try:
        logger.debug(f"Processing image: {image_path}")
        # Open image using Pillow to ensure it's a valid image file first
        # and to potentially handle more formats smoothly with pytesseract
        with Image.open(image_path) as img:
            extracted_text = pytesseract.image_to_string(img)
        
        logger.debug(f"Extracted text from {image_path}:\n---\n{extracted_text[:200]}...\n---") # Log a snippet
        return search_text.lower() in extracted_text.lower()
    except pytesseract.TesseractNotFoundError:
        logger.error(
            f"Tesseract not found. Ensure it is installed and configured correctly. "
            f"Tried command: {pytesseract.pytesseract.tesseract_cmd if tesseract_cmd else 'tesseract (from PATH)'}"
        )
        # Re-raise as a more specific error or handle as per application needs.
        # For now, if Tesseract is not found globally, we should have caught it earlier.
        # This might indicate an issue if a specific tesseract_cmd was faulty.
        raise # Re-raise to be caught by the main error handler in __init__.py
    except Exception as e:
        logger.error(f"Error processing image {image_path}: {e}")
        return False

def search_directory(directory_path: str, search_text: str, tesseract_cmd: str | None = None) -> list[str]:
    """
    Searches for images containing search_text in the specified directory (non-recursive).

    Args:
        directory_path: The path to the directory to search.
        search_text: The text string to search for.
        tesseract_cmd: Optional path to the Tesseract executable.

    Returns:
        A list of paths to images containing the search_text.
    """
    found_images = []
    logger.debug(f"Searching directory: {directory_path}")
    for item_name in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item_name)
        if os.path.isfile(item_path) and item_name.lower().endswith(SUPPORTED_IMAGE_EXTENSIONS):
            if image_contains_text(item_path, search_text, tesseract_cmd):
                logger.debug(f"Found '{search_text}' in {item_path}")
                found_images.append(item_path)
        elif os.path.isfile(item_path):
            logger.debug(f"Skipping non-image file: {item_path}")
    return found_images

def search_directory_recursive(directory_path: str, search_text: str, tesseract_cmd: str | None = None) -> list[str]:
    """
    Recursively searches for images containing search_text in the specified directory and its subdirectories.

    Args:
        directory_path: The path to the root directory to start searching from.
        search_text: The text string to search for.
        tesseract_cmd: Optional path to the Tesseract executable.

    Returns:
        A list of paths to images containing the search_text.
    """
    found_images = []
    logger.debug(f"Recursively searching directory: {directory_path}")
    for root, _, files in os.walk(directory_path):
        logger.debug(f"Scanning subdirectory: {root}")
        for filename in files:
            if filename.lower().endswith(SUPPORTED_IMAGE_EXTENSIONS):
                file_path = os.path.join(root, filename)
                if image_contains_text(file_path, search_text, tesseract_cmd):
                    logger.debug(f"Found '{search_text}' in {file_path}")
                    found_images.append(file_path)
            elif os.path.isfile(os.path.join(root, filename)):
                 logger.debug(f"Skipping non-image file in recursive scan: {os.path.join(root, filename)}")

    return found_images
