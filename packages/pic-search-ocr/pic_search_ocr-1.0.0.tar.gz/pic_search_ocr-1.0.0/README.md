# pic-search

Search the text of images in your folder.

## Usage

```
pic-search "string" [--recursive] [--dir $DIR] [--tesseract $DIR]
```

Where:
- `string` is the string to search for.
- `--recursive` (optional) will search for the string in all subdirectories.
- `--dir $DIR` (optional) is the directory to search in. Defaults to the current directory.
- `--tesseract $EXE` (optional) is the path to the tesseract executable, only needed if it's not in the path or TESSERACT_EXE environment variable.



## Installation

Install Tesseract: https://tesseract-ocr.github.io/tessdoc/Installation.html

Tesseract MUST be installed separately.

Then, tesseract directory must either be:
- In the path
- In the folder of `TESSERACT_EXE` environment variable
- Given as `--tesseract $EXE` CLI Option

This tool itself can be installed with pip:

```
pip install pic-search
```

Or any similar package manager, like `uv`:

```
uv pip install pic-search
```

