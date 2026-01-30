"""
Utility functions for the file converter application
"""

import logging
from pathlib import Path
from typing import List


def setup_logging(verbose: bool = False) -> logging.Logger:
    """
    Setup logging configuration.
    
    Args:
        verbose: Enable verbose logging if True
        
    Returns:
        Configured logger instance
    """
    level = logging.DEBUG if verbose else logging.INFO
    
    # Create logger
    logger = logging.getLogger('file_converter')
    logger.setLevel(level)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Create console handler
    handler = logging.StreamHandler()
    handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger


def validate_file_exists(file_path: Path) -> bool:
    """
    Validate that a file exists.
    
    Args:
        file_path: Path to check
        
    Returns:
        True if file exists, False otherwise
    """
    return file_path.exists() and file_path.is_file()


def validate_output_format(output_format: str, supported_formats: List[str]) -> bool:
    """
    Validate that the output format is supported.
    
    Args:
        output_format: Format to validate
        supported_formats: List of supported formats
        
    Returns:
        True if format is supported, False otherwise
    """
    return output_format.lower() in [fmt.lower() for fmt in supported_formats]


def get_supported_formats() -> List[str]:
    """
    Get list of supported file formats.
    
    Returns:
        List of supported formats
    """
    return [
        'txt', 'csv', 'json', 'xml', 'yaml', 'yml',
        'pdf', 'docx', 'md',
        'jpg', 'jpeg', 'png', 'gif', 'bmp',
        'xlsx'
    ]