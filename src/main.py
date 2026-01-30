#!/usr/bin/env python3
"""
Image Format Converter CLI Application

A comprehensive tool for converting between various image formats including:
- Raster formats: .jpg, .png, .gif, .bmp, .ico, .webp, .tiff
- Vector formats: .svg (with additional dependencies)
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

try:
    from .converter import FileConverter
    from .utils import setup_logging
except ImportError:
    # When running as a script
    from converter import FileConverter
    from utils import setup_logging


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog='image-converter',
        description='Convert images between various formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -i image.png -o output.jpg
  %(prog)s -i image.svg -f png -o output/
  %(prog)s -i *.png -f jpg -o output/
  %(prog)s --batch images.txt -f ico -o output/
        """
    )
    
    # Input arguments
    input_group = parser.add_argument_group('input')
    input_group.add_argument(
        '-i', '--input',
        nargs='+',
        dest='input_paths',
        help='Input file(s) or glob pattern to convert'
    )
    input_group.add_argument(
        '--batch',
        type=Path,
        help='File containing list of input files to process'
    )
    
    # Output arguments
    output_group = parser.add_argument_group('output')
    output_group.add_argument(
        '-f', '--format',
        dest='output_format',
        help='Desired output format (e.g., png, jpg, gif, ico, webp)'
    )
    output_group.add_argument(
        '-o', '--output',
        type=Path,
        help='Output file or directory path'
    )
    
    # Additional options
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    return parser


def validate_args(args: argparse.Namespace) -> bool:
    """Validate command line arguments."""
    errors = []
    
    # Check if input is provided
    if not args.input_paths and not args.batch:
        errors.append("Either --input or --batch must be specified")
    
    # Check if output format is provided when input is a list
    if args.input_paths and len(args.input_paths) > 1 and not args.output_format:
        errors.append("Output format must be specified when converting multiple files")
    
    # Check if output format is provided when input is a glob pattern
    if args.input_paths and '*' in ' '.join(args.input_paths) and not args.output_format:
        errors.append("Output format must be specified when using glob patterns")
    
    # Validate input files exist
    if args.input_paths:
        for path_str in args.input_paths:
            path = Path(path_str)
            if not path.exists():
                errors.append(f"Input file does not exist: {path}")
    
    # Validate batch file exists
    if args.batch and not args.batch.exists():
        errors.append(f"Batch file does not exist: {args.batch}")
    
    # Show errors and exit if any
    if errors:
        for error in errors:
            print(f"Error: {error}", file=sys.stderr)
        return False
    
    return True


def get_input_files(args: argparse.Namespace) -> List[Path]:
    """Get list of input files to process."""
    input_files = []
    
    if args.batch:
        # Read files from batch file
        with open(args.batch, 'r') as f:
            for line in f:
                path = Path(line.strip())
                if path.exists():
                    input_files.append(path)
    elif args.input_paths:
        # Process input paths (could be glob patterns)
        for path_str in args.input_paths:
            path = Path(path_str)
            if path.is_file():
                input_files.append(path)
            elif '*' in path_str:
                # Handle glob patterns
                parent_dir = path.parent if path.parent != Path('.') else Path('.')
                pattern = path.name
                input_files.extend(parent_dir.glob(pattern))
            else:
                # Handle directory
                if path.is_dir():
                    input_files.extend([f for f in path.iterdir() if f.is_file()])
    
    return input_files


def main() -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging(args.verbose)
    
    # Validate arguments
    if not validate_args(args):
        return 1
    
    try:
        # Get input files
        input_files = get_input_files(args)
        
        if not input_files:
            print("No input files found to process", file=sys.stderr)
            return 1
        
        # Determine output format
        output_format = args.output_format
        if not output_format:
            # If only one file and output is specified, infer format from output extension
            if len(input_files) == 1 and args.output:
                output_format = args.output.suffix.lstrip('.').lower()
            else:
                print("Output format must be specified", file=sys.stderr)
                return 1
        
        # Initialize converter
        converter = FileConverter(logger)
        
        # Perform conversion
        success_count = 0
        for input_file in input_files:
            try:
                output_path = converter.convert(
                    input_path=input_file,
                    output_format=output_format,
                    output_dir=args.output
                )
                logger.info(f"Successfully converted {input_file} -> {output_path}")
                success_count += 1
            except Exception as e:
                logger.error(f"Failed to convert {input_file}: {str(e)}")
        
        logger.info(f"Conversion completed: {success_count}/{len(input_files)} files processed successfully")
        return 0 if success_count > 0 else 1
        
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())