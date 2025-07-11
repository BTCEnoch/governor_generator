"""
Pytest configuration file
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Configure logging for tests
from core.utils.custom_logging.custom_logger import setup_logger
logger = setup_logger("test_logger") 