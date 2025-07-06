"""
Test runner script for core utilities
"""

import os
import sys
import pytest
from pathlib import Path

def run_tests():
    """Run all tests with coverage reporting"""
    # Get the test directory
    test_dir = Path(__file__).parent
    
    # Add the project root to Python path
    project_root = test_dir.parent.parent.parent
    sys.path.insert(0, str(project_root))
    
    # Configure test arguments
    args = [
        str(test_dir),  # Test directory
        "-v",           # Verbose output
        "--cov=core.utils",  # Coverage for core.utils
        "--cov-report=term-missing",  # Show lines missing coverage
        "--cov-report=html:coverage_report"  # Generate HTML report
    ]
    
    # Run tests
    return pytest.main(args)

if __name__ == "__main__":
    sys.exit(run_tests()) 