"""
Tests for logging utilities
"""

import logging
import os
from io import StringIO
from pathlib import Path
import pytest
from datetime import datetime
from core.utils.custom_logging import (
    setup_logger,
    get_batch_logger,
    get_mystical_logger,
    get_governor_logger
)

@pytest.fixture(autouse=True)
def cleanup_loggers():
    """Clean up loggers before and after each test"""
    # Clean up before test
    root = logging.getLogger()
    root.setLevel(logging.WARNING)  # Reset root logger level
    
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        logger.setLevel(logging.NOTSET)  # Reset level
        logger.propagate = True  # Reset propagate
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
    
    yield
    
    # Clean up after test
    root = logging.getLogger()
    root.setLevel(logging.WARNING)  # Reset root logger level
    
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        logger.setLevel(logging.NOTSET)  # Reset level
        logger.propagate = True  # Reset propagate
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

@pytest.fixture
def temp_log_dir(tmp_path):
    """Create a temporary log directory"""
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    
    # Create subdirectories for specialized loggers
    (log_dir / "batch").mkdir()
    (log_dir / "mystical").mkdir()
    (log_dir / "governor").mkdir()
    (log_dir / "batch_path").mkdir()
    (log_dir / "mystical_path").mkdir()
    (log_dir / "governor_path").mkdir()
    
    return log_dir

def test_setup_logger(temp_log_dir):
    """Test basic logger setup"""
    # Test console-only logger
    logger = setup_logger("test_console")
    assert logger.name == "test_console"
    assert logger.level == logging.INFO
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.StreamHandler)
    
    # Test logger with file output
    log_file = temp_log_dir / "test.log"
    logger = setup_logger(
        "test_file",
        log_file=log_file,
        level=logging.DEBUG
    )
    assert logger.name == "test_file"
    assert logger.level == logging.DEBUG
    assert len(logger.handlers) == 2  # Console and file
    assert isinstance(logger.handlers[0], logging.StreamHandler)
    assert isinstance(logger.handlers[1], logging.FileHandler)
    
    # Test logging output
    logger.info("Test message")
    assert log_file.exists()
    content = log_file.read_text()
    assert "Test message" in content
    
    # Test file_mode parameter
    write_file = temp_log_dir / "write_test.log"
    logger = setup_logger(
        "test_write",
        log_file=write_file,
        file_mode='w'
    )
    logger.info("First message")
    logger.info("Second message")
    content = write_file.read_text()
    assert content.count("First message") == 1
    assert content.count("Second message") == 1
    
    # Test string path handling
    str_path = str(temp_log_dir / "str_path.log")
    logger = setup_logger("test_str_path", log_file=str_path)
    logger.info("String path test")
    assert Path(str_path).exists()
    
    # Test invalid log file path
    invalid_path = temp_log_dir / "nonexistent_dir" / "test.log"
    with pytest.raises(ValueError) as exc:
        setup_logger("test_invalid", log_file=invalid_path)
    assert "Log directory does not exist" in str(exc.value)
    
    # Test existing logger
    existing_logger = setup_logger("test_existing")
    same_logger = setup_logger("test_existing")
    assert existing_logger is same_logger
    assert len(same_logger.handlers) == 1  # Should not add duplicate handlers

def test_get_batch_logger(temp_log_dir):
    """Test batch logger setup"""
    # Test console-only logger
    logger = get_batch_logger("test_batch", log_file=None)
    assert logger.name == "batch_test_batch"
    assert logger.level == logging.INFO
    assert len(logger.handlers) == 1
    
    # Test with file output and base_dir as string
    base_dir_str = str(temp_log_dir / "batch")
    logger = get_batch_logger(
        "test_batch_2",  # Use different name to avoid handler accumulation
        base_dir=base_dir_str
    )
    assert len(logger.handlers) == 2
    
    # Test with file output and base_dir as Path
    base_dir_path = temp_log_dir / "batch_path"
    logger = get_batch_logger(
        "test_batch_3",  # Use different name to avoid handler accumulation
        base_dir=base_dir_path
    )
    assert len(logger.handlers) == 2
    
    # Test timestamp-based file creation
    current_time = datetime.now().strftime("%Y%m%d")
    logger = get_batch_logger("timestamp_test", base_dir=temp_log_dir / "batch")
    log_files = list((temp_log_dir / "batch").glob(f"batch_timestamp_test_{current_time}*.log"))
    assert len(log_files) == 1
    
    # Test logging output
    logger.info("Test batch message")
    content = log_files[0].read_text()
    assert "Test batch message" in content
    
    # Test with explicit log file
    explicit_log = temp_log_dir / "batch" / "explicit_batch.log"
    logger = get_batch_logger("explicit", log_file=explicit_log)
    logger.info("Explicit file test")
    assert explicit_log.exists()
    content = explicit_log.read_text()
    assert "Explicit file test" in content

def test_get_mystical_logger(temp_log_dir):
    """Test mystical logger setup"""
    # Test console-only logger
    logger = get_mystical_logger("test_mystical", log_file=None)
    assert logger.name == "mystical_test_mystical"
    assert logger.level == logging.INFO
    assert len(logger.handlers) == 1
    
    # Test with base_dir as string
    base_dir_str = str(temp_log_dir / "mystical")
    logger = get_mystical_logger(
        "test_mystical_2",  # Use different name to avoid handler accumulation
        base_dir=base_dir_str
    )
    assert len(logger.handlers) == 2
    
    # Test with base_dir as Path
    base_dir_path = temp_log_dir / "mystical_path"
    logger = get_mystical_logger(
        "test_mystical_3",  # Use different name to avoid handler accumulation
        base_dir=base_dir_path
    )
    assert len(logger.handlers) == 2
    
    # Test log file creation
    logger = get_mystical_logger("file_test", base_dir=temp_log_dir / "mystical")
    log_file = temp_log_dir / "mystical" / "file_test.log"
    assert log_file.exists()
    
    # Test logging output
    logger.info("Test mystical message")
    content = log_file.read_text()
    assert "Test mystical message" in content
    
    # Test with explicit log file
    explicit_log = temp_log_dir / "mystical" / "explicit_mystical.log"
    logger = get_mystical_logger("explicit", log_file=explicit_log)
    logger.info("Explicit file test")
    assert explicit_log.exists()
    content = explicit_log.read_text()
    assert "Explicit file test" in content

def test_get_governor_logger(temp_log_dir):
    """Test governor logger setup"""
    # Test console-only logger
    logger = get_governor_logger("test_governor", log_file=None)
    assert logger.name == "governor_test_governor"
    assert logger.level == logging.INFO
    assert len(logger.handlers) == 1
    
    # Test with base_dir as string
    base_dir_str = str(temp_log_dir / "governor")
    logger = get_governor_logger(
        "test_governor_2",  # Use different name to avoid handler accumulation
        base_dir=base_dir_str
    )
    assert len(logger.handlers) == 2
    
    # Test with base_dir as Path
    base_dir_path = temp_log_dir / "governor_path"
    logger = get_governor_logger(
        "test_governor_3",  # Use different name to avoid handler accumulation
        base_dir=base_dir_path
    )
    assert len(logger.handlers) == 2
    
    # Test log file creation
    logger = get_governor_logger("file_test", base_dir=temp_log_dir / "governor")
    log_file = temp_log_dir / "governor" / "governor_file_test.log"
    assert log_file.exists()
    
    # Test logging output
    logger.info("Test governor message")
    content = log_file.read_text()
    assert "Test governor message" in content
    
    # Test with explicit log file
    explicit_log = temp_log_dir / "governor" / "explicit_governor.log"
    logger = get_governor_logger("explicit", log_file=explicit_log)
    logger.info("Explicit file test")
    assert explicit_log.exists()
    content = explicit_log.read_text()
    assert "Explicit file test" in content

def test_logger_format():
    """Test logger format customization"""
    # Test custom format
    logger = setup_logger(
        "test_format",
        format_string="%(levelname)s - %(message)s"
    )
    
    # Test log output format
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logger.handlers[0].formatter)
    logger.addHandler(handler)
    
    logger.info("Test message")
    output = stream.getvalue()
    assert "INFO - Test message" in output
    
    # Test with different format
    logger = setup_logger(
        "test_format_2",
        format_string="[%(name)s] %(message)s"
    )
    
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logger.handlers[0].formatter)
    logger.addHandler(handler)
    
    logger.info("Test message")
    output = stream.getvalue()
    assert "[test_format_2] Test message" in output 