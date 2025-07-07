"""
Tests for common utility functions
"""

import pytest
from pathlib import Path
from core.utils.common.text import (
    normalize_text,
    extract_keywords,
    format_list,
    truncate_text,
    slugify
)
from core.utils.common.errors import (
    safe_execute,
    retry_on_error,
    format_error,
    handle_errors
)
from core.utils.common.progress import (
    ProgressStats,
    ProgressTracker,
    track_progress
)

# Text utility tests
@pytest.mark.utils
class TestTextUtils:
    def test_normalize_text(self):
        """Test text normalization"""
        assert normalize_text("  Hello   World  ") == "hello world"
        assert normalize_text("Multiple    Spaces") == "multiple spaces"
        assert normalize_text("UPPERCASE") == "uppercase"
        
    def test_extract_keywords(self):
        """Test keyword extraction"""
        text = "The quick brown fox jumps over the lazy dog"
        keywords = extract_keywords(text, min_length=4)
        assert "quick" in keywords
        assert "brown" in keywords
        assert "jumps" in keywords
        assert "lazy" in keywords
        assert "the" not in keywords  # too short
        
    def test_format_list(self):
        """Test list formatting"""
        assert format_list(["one"]) == "one"
        assert format_list(["one", "two"]) == "one and two"
        assert format_list(["one", "two", "three"]) == "one, two and three"
        assert format_list([]) == ""
        
    def test_truncate_text(self):
        """Test text truncation"""
        text = "This is a long text that needs truncation"
        assert truncate_text(text, 10) == "This is..."
        assert truncate_text(text, 100) == text
        assert truncate_text("", 10) == ""
        
    def test_slugify(self):
        """Test URL slug generation"""
        assert slugify("Hello World") == "hello-world"
        assert slugify("Special@#$Characters") == "specialcharacters"
        assert slugify("  Multiple  Spaces  ") == "multiple-spaces"

# Error handling tests
@pytest.mark.utils
class TestErrorUtils:
    def test_safe_execute(self):
        """Test safe function execution"""
        def good_func():
            return 42
            
        def bad_func():
            raise ValueError("test error")
            
        assert safe_execute(good_func) == 42
        assert safe_execute(bad_func) is None
        
    def test_retry_on_error(self):
        """Test retry decorator"""
        attempts = 0
        
        @retry_on_error(max_retries=3)
        def flaky_function():
            nonlocal attempts
            attempts += 1
            if attempts < 3:
                raise ValueError("temporary error")
            return "success"
            
        result = flaky_function()
        assert result == "success"
        assert attempts == 3
        
    def test_format_error(self):
        """Test error formatting"""
        try:
            raise ValueError("test error")
        except ValueError as e:
            error_info = format_error(e)
            assert error_info["type"] == "ValueError"
            assert error_info["message"] == "test error"
            assert "traceback" in error_info
            
    def test_handle_errors(self):
        """Test error handling decorator"""
        @handle_errors(default_value=None)
        def risky_function():
            raise ValueError("test error")
            
        assert risky_function() is None

# Progress tracking tests
@pytest.mark.utils
class TestProgressUtils:
    def test_progress_stats(self):
        """Test progress statistics"""
        stats = ProgressStats(
            total=100,
            completed=75,
            failed=5,
            start_time=None
        )
        assert stats.success_rate == 0.75
        assert stats.completed == 75
        assert stats.failed == 5
        
    def test_progress_tracker(self):
        """Test progress tracking"""
        tracker = ProgressTracker(total=10)
        
        # Track some progress
        for _ in range(7):
            tracker.update(success=True)
        for _ in range(2):
            tracker.update(success=False)
            
        stats = tracker.get_stats()
        assert stats.completed == 7
        assert stats.failed == 2
        assert stats.total == 10
        
    def test_track_progress(self):
        """Test progress tracking generator"""
        items = range(5)
        processed = []
        
        def process_item(x):
            processed.append(x)
            return x * 2
            
        results = list(track_progress(items, process_item))
        assert len(results) == 5
        assert results == [0, 2, 4, 6, 8]
        assert processed == list(range(5)) 