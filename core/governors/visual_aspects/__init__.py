"""
Visual Aspects System for Enochian Governors

This package defines the standardized visual manifestation system for the 91 Enochian Governors.
It provides catalogs, rules, and validation for consistent visual representation while maintaining
sacred authenticity.
"""

from pathlib import Path
from typing import Dict, Any

# Package metadata
PACKAGE_ROOT = Path(__file__).parent
CATALOGS_DIR = PACKAGE_ROOT / "catalogs"
SCHEMAS_DIR = PACKAGE_ROOT / "schemas"
PATTERNS_DIR = PACKAGE_ROOT / "patterns"

# Ensure required directories exist
CATALOGS_DIR.mkdir(exist_ok=True)
SCHEMAS_DIR.mkdir(exist_ok=True)
PATTERNS_DIR.mkdir(exist_ok=True)

# Version info
__version__ = "1.0.0"
__author__ = "Enochian Governors Project" 