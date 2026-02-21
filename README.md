# img2pdf

A command-line tool to convert multiple images into a single PDF file.

## Supported Formats

- jpg
- jpeg
- png
- heic
- heif
- bmp
- tiff
- tif
- webp

## Installation

```bash
pip install -r requirements.txt
```

Requires Python 3.10+.

## Usage

```bash
# Basic — output filename is auto-generated (YYYYMMDD-HHMMSS.pdf)
python img2pdf.py image1.jpg image2.png photo.heic

# Custom output path
python img2pdf.py image1.jpg image2.png -o output.pdf
```
