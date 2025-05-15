from .cli import parse_args
from .ocr import search_directory, search_directory_recursive
import sys
import logging
import pytesseract

logger = logging.getLogger(__name__) # Use a logger for this module as well

def main() -> None:
    try:
        args = parse_args()
        logger.debug(f"Parsed arguments: {args}")

        if args.tesseract:
            logger.debug(f"Using Tesseract executable at: {args.tesseract}")
        else:
            logger.debug("Tesseract command not explicitly set, relying on pytesseract's PATH search.")

        found_files: list[str] = []
        if args.recursive:
            logger.debug(f"Starting recursive search for '{args.search_string}' in directory '{args.dir}'")
            found_files = search_directory_recursive(
                directory_path=args.dir,
                search_text=args.search_string,
                tesseract_cmd=args.tesseract
            )
        else:
            logger.debug(f"Starting non-recursive search for '{args.search_string}' in directory '{args.dir}'")
            found_files = search_directory(
                directory_path=args.dir,
                search_text=args.search_string,
                tesseract_cmd=args.tesseract
            )

        if found_files:
            logger.debug(f"Search complete. Found '{args.search_string}' in the following images:")
            for file_path in found_files:
                print(file_path) 
        else:
            print(f"Search complete. No images found containing '{args.search_string}' in '{args.dir}'{(' recursively' if args.recursive else '')}.")

    except ValueError as e:
        # ValueErrors from parse_args (e.g., Tesseract not found by cli.py)
        logging.error(str(e)) 
        sys.exit(1)
    except pytesseract.TesseractNotFoundError as e: # Catch TesseractNotFoundError from ocr.py
        logging.error(f"OCR Error: {e} - Please ensure Tesseract is installed and accessible.")
        sys.exit(1)
    except Exception as e:
        # Catch any other unexpected errors during OCR or file processing
        logger.error(f"An unexpected error occurred: {e}", exc_info=True) # Log traceback for unexpected errors
        sys.exit(1)
