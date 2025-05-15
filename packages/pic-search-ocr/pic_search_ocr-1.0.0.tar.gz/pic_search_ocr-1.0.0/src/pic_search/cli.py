import argparse
import os
import shutil
import logging

def _resolve_provided_tesseract_path(provided_path: str | None) -> str | None:
    """
    Attempts to resolve a user-provided path to a Tesseract executable.
    1. Checks if provided_path is a direct executable.
    2. On Windows, if not a dir and no .exe, tries appending .exe.
    3. Checks if provided_path is a directory containing 'tesseract' or 'tesseract.exe'.
    Returns the path to the executable or None if the provided_path cannot be resolved.
    """
    if not provided_path:
        return None

    # 1. Check if provided_path is a direct executable as given
    if os.path.isfile(provided_path) and os.access(provided_path, os.X_OK):
        return provided_path

    # 2. On Windows, if not a directory and doesn't have a common executable extension, try adding .exe
    if os.name == "nt" and not os.path.isdir(provided_path):
        name_lower = provided_path.lower()
        if not any(name_lower.endswith(ext) for ext in (".exe", ".cmd", ".bat")):
            path_with_exe = provided_path + ".exe"
            if os.path.isfile(path_with_exe) and os.access(path_with_exe, os.X_OK):
                return path_with_exe

    # 3. Check if provided_path is a directory containing tesseract[.exe]
    if os.path.isdir(provided_path):
        exe_name = "tesseract.exe" if os.name == "nt" else "tesseract"
        potential_path = os.path.join(provided_path, exe_name)
        if os.path.isfile(potential_path) and os.access(potential_path, os.X_OK):
            return potential_path
    
    return None # Provided path could not be resolved

def parse_args():
    parser = argparse.ArgumentParser(description="Search for text in images.")
    parser.add_argument("search_string", metavar="string", help="The string to search for.")
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Search for the string in all subdirectories.",
    )
    parser.add_argument(
        "-d", "--dir",
        default=".",
        help="The directory to search in. Defaults to the current directory.",
    )
    parser.add_argument(
        "-t", "--tesseract",
        default=os.getenv("TESSERACT_EXE"),
        help="Path to the Tesseract OCR executable or its installation directory. Uses TESSERACT_EXE env var if not set. If all fail, searches system PATH.",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging.",
    )

    args = parser.parse_args()

    # Configure logging based on verbose flag
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(message)s'  # Simple format without timestamp/level for cleaner output
    )

    tesseract_executable_path = _resolve_provided_tesseract_path(args.tesseract)

    if tesseract_executable_path is None:
        # If no path was provided by user/env, OR if the provided one was bad/unresolvable,
        # try finding 'tesseract' in the system PATH as a last resort.
        tesseract_executable_path = shutil.which("tesseract")

    if tesseract_executable_path is None:
        # Second time, if still not found, raise an error
        raise ValueError(
            "Tesseract OCR executable not found. Please ensure Tesseract is installed and try one of the following:\n"
            "1. Provide the full path to the 'tesseract' executable via the -t/--tesseract argument.\n"
            "2. Provide the path to the Tesseract installation directory (containing 'tesseract(.exe)') via the -t/--tesseract argument.\n"
            "3. Set the TESSERACT_EXE environment variable to the Tesseract executable path or installation directory.\n"
            "4. Ensure the directory containing the 'tesseract' executable is in your system's PATH."
        )
    
    args.tesseract = tesseract_executable_path # Store the resolved path to the executable

    return args
