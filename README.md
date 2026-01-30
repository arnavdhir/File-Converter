# Image Format Converter CLI Application

A comprehensive command-line tool for converting between various image formats including SVG, JPG, PNG, ICO, and more.

## Features

- Convert between multiple image formats:
  - **Raster formats**: `.jpg`, `.png`, `.gif`, `.bmp`, `.ico`, `.webp`, `.tiff`
  - **Vector formats**: `.svg` (requires additional dependencies)
  - **Other formats**: `.psd`, `.raw`
- Batch conversion of multiple files
- Clean CLI interface with intuitive options
- Proper error handling and validation
- Progress indication and logging
- Cross-platform compatibility

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Cloning the Repository

```bash
git clone https://github.com/arnavdhir/File-Converter.git
cd File-Converter
```

### Installing Dependencies

```bash
pip install -r requirements.txt
```

Or install directly from the setup.py:

```bash
pip install .
```

## Usage

### Basic Conversion

Convert a single image to a different format:

```bash
python -m src.main -i input.png -o output.jpg
```

Specify output format separately:

```bash
python -m src.main -i input.svg -f png -o output.png
```

### Batch Conversion

Convert multiple images to the same format:

```bash
python -m src.main -i file1.png file2.jpg -f ico -o output/
```

Use glob patterns:

```bash
python -m src.main -i "*.png" -f jpg -o output/
```

### Using Batch File

Create a text file with a list of input files (one per line):

```bash
python -m src.main --batch input_files.txt -f png -o output/
```

### Options

- `-i, --input`: Input file(s) or glob pattern to convert
- `--batch`: File containing list of input files to process
- `-f, --format`: Desired output format (e.g., pdf, docx, json, csv)
- `-o, --output`: Output file or directory path
- `-v, --verbose`: Enable verbose logging
- `--version`: Show program version

## Supported Conversions

The application supports the following conversion combinations:

| From \ To | jpg | png | gif | bmp | ico | webp | tiff |
|-----------|-----|-----|-----|-----|-----|------|------|
| jpg       |  ✗  | ✓   | ✓   | ✓   | ✓   |  ✓   |  ✓   |
| png       | ✓   |  ✗  | ✓   | ✓   | ✓   |  ✓   |  ✓   |
| gif       | ✓   | ✓   |  ✗  | ✓   | ✓   |  ✓   |  ✓   |
| bmp       | ✓   | ✓   | ✓   |  ✗  | ✓   |  ✓   |  ✓   |
| ico       | ✓   | ✓   | ✓   | ✓   |  ✗  |  ✓   |  ✓   |
| webp      | ✓   | ✓   | ✓   | ✓   | ✓   |  ✗   |  ✓   |
| tiff      | ✓   | ✓   | ✓   | ✓   | ✓   |  ✓   |  ✗   |

Note: SVG format is temporarily not supported due to external dependencies. To enable SVG conversions, install additional dependencies: `pip install cairosvg`.

Legend: ✓ = Supported, ✗ = Not supported (same format)

## Examples

### Convert PNG to JPG

```bash
python -m src.main -i image.png -f jpg -o converted/
```

### Convert multiple PNG files to ICO

```bash
python -m src.main -i "*.png" -f ico -o favicon_output/
```

### Convert SVG to multiple formats

```bash
python -m src.main -i logo.svg -f png -o png_output/
python -m src.main -i logo.svg -f jpg -o jpg_output/
```

### Verbose conversion with detailed logging

```bash
python -m src.main -i input.png -f jpg -o output.jpg -v
```

### Practical Examples

#### Example 1: Converting an SVG to PNG
```bash
# Convert an SVG file to PNG
python -m src.main -i logo.svg -f png -o logo.png
```

#### Example 2: Converting multiple image files
```bash
# Convert all PNG files in current directory to JPG
python -m src.main -i "*.png" -f jpg -o converted_images/
```

#### Example 3: Batch conversion using a file list
```bash
# Create a file with list of image files to convert
echo "image1.png" > image_batch.txt
echo "image2.jpg" >> image_batch.txt
echo "image3.gif" >> image_batch.txt

# Process all files in the list
python -m src.main --batch image_batch.txt -f ico -o icon_outputs/
```

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Troubleshooting

### Common Issues

#### Missing Dependencies
If you get a "ModuleNotFoundError", make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

#### SVG conversion issues
SVG format is temporarily not supported due to external dependencies. To enable SVG conversions, install additional dependencies:
```bash
pip install cairosvg
```

Then update the converter code to include SVG conversion methods.

#### Permission Errors
If you encounter permission errors, try running with elevated privileges or use the user flag:
```bash
pip install --user -r requirements.txt
```

#### Unsupported format error
Make sure the input and output formats are supported by checking the table above.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgments

- Built with Python and various open-source libraries
- Inspired by the need for a versatile file conversion tool
