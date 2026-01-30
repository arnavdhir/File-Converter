"""
Image format conversion logic module
Handles the actual conversion between different image formats
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Union
import logging
from PIL import Image


class ConversionError(Exception):
    """Custom exception for conversion errors."""
    pass


class FileConverter:
    """Main image converter class that handles different image format conversions."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        # Define supported formats
        self.supported_formats = {
            'jpg', 'jpeg', 'png', 'gif', 'bmp', 'ico', 'webp', 'tiff'
            # Note: SVG is excluded because it requires external dependencies that may not be available
        }

    def convert(self, input_path: Path, output_format: str, output_dir: Path = None) -> Path:
        """
        Convert an image file from input_path to the specified output_format.

        Args:
            input_path: Path to the input file
            output_format: Desired output format
            output_dir: Directory to place output file (optional)

        Returns:
            Path to the output file
        """
        if output_format.lower() not in self.supported_formats:
            raise ConversionError(f"Unsupported output format: {output_format}")

        input_ext = input_path.suffix.lower().lstrip('.')

        if input_ext == output_format.lower():
            raise ConversionError(f"Input and output formats are the same: {input_ext}")

        # Determine output path
        if output_dir:
            if output_dir.is_file():
                output_path = output_dir
            else:
                output_path = output_dir / f"{input_path.stem}.{output_format}"
        else:
            output_path = input_path.with_suffix(f'.{output_format}')

        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Perform conversion based on input and output formats
        conversion_method = self._get_conversion_method(input_ext, output_format.lower())
        if not conversion_method:
            raise ConversionError(f"Conversion from {input_ext} to {output_format} is not supported")

        self.logger.info(f"Converting {input_path} ({input_ext}) to {output_path} ({output_format})")
        conversion_method(input_path, output_path)

        return output_path

    def _get_conversion_method(self, input_format: str, output_format: str):
        """Get the appropriate conversion method based on input and output formats."""
        methods = {
            ('jpg', 'png'): self._image_to_image,
            ('jpeg', 'png'): self._image_to_image,
            ('gif', 'png'): self._image_to_image,
            ('bmp', 'png'): self._image_to_image,
            ('ico', 'png'): self._image_to_image,
            ('webp', 'png'): self._image_to_image,
            ('tiff', 'png'): self._image_to_image,

            ('png', 'jpg'): self._image_to_image,
            ('png', 'jpeg'): self._image_to_image,
            ('png', 'gif'): self._image_to_image,
            ('png', 'bmp'): self._image_to_image,
            ('png', 'ico'): self._image_to_image,
            ('png', 'webp'): self._image_to_image,
            ('png', 'tiff'): self._image_to_image,

            ('jpg', 'gif'): self._image_to_image,
            ('jpeg', 'gif'): self._image_to_image,
            ('gif', 'jpg'): self._image_to_image,
            ('gif', 'jpeg'): self._image_to_image,
            ('gif', 'bmp'): self._image_to_image,
            ('gif', 'ico'): self._image_to_image,
            ('gif', 'webp'): self._image_to_image,
            ('gif', 'tiff'): self._image_to_image,

            ('bmp', 'jpg'): self._image_to_image,
            ('bmp', 'jpeg'): self._image_to_image,
            ('bmp', 'gif'): self._image_to_image,
            ('bmp', 'ico'): self._image_to_image,
            ('bmp', 'webp'): self._image_to_image,
            ('bmp', 'tiff'): self._image_to_image,

            ('ico', 'jpg'): self._image_to_image,
            ('ico', 'jpeg'): self._image_to_image,
            ('ico', 'gif'): self._image_to_image,
            ('ico', 'bmp'): self._image_to_image,
            ('ico', 'webp'): self._image_to_image,
            ('ico', 'tiff'): self._image_to_image,

            ('webp', 'jpg'): self._image_to_image,
            ('webp', 'jpeg'): self._image_to_image,
            ('webp', 'gif'): self._image_to_image,
            ('webp', 'bmp'): self._image_to_image,
            ('webp', 'ico'): self._image_to_image,
            ('webp', 'tiff'): self._image_to_image,

            ('tiff', 'jpg'): self._image_to_image,
            ('tiff', 'jpeg'): self._image_to_image,
            ('tiff', 'gif'): self._image_to_image,
            ('tiff', 'bmp'): self._image_to_image,
            ('tiff', 'ico'): self._image_to_image,
            ('tiff', 'webp'): self._image_to_image,
        }

        return methods.get((input_format, output_format))

    def _image_to_image(self, input_path: Path, output_path: Path):
        """Convert between raster image formats."""
        try:
            with Image.open(input_path) as img:
                # Convert RGBA to RGB if saving to JPEG
                if output_path.suffix.lower() in ['.jpg', '.jpeg'] and img.mode in ('RGBA', 'LA'):
                    # Create white background
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'RGBA':
                        background.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
                    else:  # LA mode
                        background.paste(img, mask=img.split()[-1])
                    img = background
                elif output_path.suffix.lower() == '.ico':
                    # Resize for ICO format if needed
                    img = img.resize((256, 256), Image.Resampling.LANCZOS)

                img.save(output_path, optimize=True, quality=95)
        except Exception as e:
            raise ConversionError(f"Failed to convert image: {str(e)}")