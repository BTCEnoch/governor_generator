"""
Universal JSON Cleaner
Handles JSON cleaning, validation, and normalization
"""

import json
import re
import logging
from pathlib import Path
from typing import Any, Dict, List, Union, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class JSONCleaner:
    """
    Universal JSON cleaner for handling various JSON-related tasks
    """
    
    def __init__(self, log_dir: Optional[str] = None):
        """
        Initialize the cleaner
        
        Args:
            log_dir: Optional directory for cleaning logs
        """
        self.log_dir = Path(log_dir) if log_dir else Path("logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.cleaning_log = self.log_dir / "cleaning_log.txt"
        
    def clean_json(self, data: Union[Dict, List]) -> Union[Dict, List]:
        """
        Clean JSON data by handling common issues
        
        Args:
            data: JSON data to clean
            
        Returns:
            Cleaned JSON data
        """
        if isinstance(data, dict):
            return self._clean_dict(data)
        elif isinstance(data, list):
            return self._clean_list(data)
        else:
            return data
            
    def _clean_dict(self, data: Dict) -> Dict:
        """Clean a dictionary"""
        cleaned = {}
        for key, value in data.items():
            # Clean key
            clean_key = self._clean_string(str(key))
            
            # Clean value
            if isinstance(value, dict):
                cleaned[clean_key] = self._clean_dict(value)
            elif isinstance(value, list):
                cleaned[clean_key] = self._clean_list(value)
            elif isinstance(value, str):
                cleaned[clean_key] = self._clean_string(value)
            else:
                cleaned[clean_key] = value
                
        return cleaned
        
    def _clean_list(self, data: List) -> List:
        """Clean a list"""
        cleaned = []
        for item in data:
            if isinstance(item, dict):
                cleaned.append(self._clean_dict(item))
            elif isinstance(item, list):
                cleaned.append(self._clean_list(item))
            elif isinstance(item, str):
                cleaned.append(self._clean_string(item))
            else:
                cleaned.append(item)
                
        return cleaned
        
    def _clean_string(self, text: str) -> str:
        """
        Clean a string by:
        - Removing control characters
        - Normalizing whitespace
        - Handling special characters
        - Converting smart quotes
        """
        # Remove control characters
        text = "".join(char for char in text if ord(char) >= 32 or char in "\n\r\t")
        
        # Normalize whitespace
        text = " ".join(text.split())
        
        # Convert smart quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        # Handle other special characters
        text = text.replace('—', '-').replace('–', '-')
        text = text.replace('…', '...')
        
        return text
        
    def clean_file(self, input_file: Union[str, Path], output_file: Optional[Union[str, Path]] = None) -> Path:
        """
        Clean a JSON file
        
        Args:
            input_file: Path to input JSON file
            output_file: Optional path for output file (defaults to input_file)
            
        Returns:
            Path to the cleaned file
        """
        input_path = Path(input_file)
        output_path = Path(output_file) if output_file else input_path
        
        logger.info(f"Cleaning JSON file: {input_path}")
        
        try:
            # Read input file
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Clean data
            cleaned_data = self.clean_json(data)
            
            # Write output file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
                
            # Log success
            self._log_cleaning(input_path, output_path, success=True)
            
            logger.info(f"Successfully cleaned file: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error cleaning file {input_path}: {e}")
            self._log_cleaning(input_path, output_path, success=False, error=str(e))
            raise
            
    def validate_json(self, data: Union[Dict, List], schema: Optional[Dict] = None) -> bool:
        """
        Validate JSON data
        
        Args:
            data: JSON data to validate
            schema: Optional JSON schema for validation
            
        Returns:
            bool indicating if data is valid
        """
        try:
            # Basic JSON validation
            json.dumps(data)
            
            # Schema validation if provided
            if schema:
                from jsonschema import validate
                validate(instance=data, schema=schema)
                
            return True
            
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return False
            
    def normalize_json(self, data: Union[Dict, List]) -> Union[Dict, List]:
        """
        Normalize JSON data by:
        - Sorting dictionary keys
        - Ensuring consistent value types
        - Normalizing string values
        
        Args:
            data: JSON data to normalize
            
        Returns:
            Normalized JSON data
        """
        if isinstance(data, dict):
            return {
                key: self.normalize_json(value)
                for key, value in sorted(data.items())
            }
        elif isinstance(data, list):
            return [self.normalize_json(item) for item in data]
        elif isinstance(data, str):
            return self._clean_string(data)
        else:
            return data
            
    def _log_cleaning(
        self,
        input_file: Path,
        output_file: Path,
        success: bool,
        error: Optional[str] = None
    ):
        """Log cleaning operation"""
        timestamp = datetime.now().isoformat()
        status = "SUCCESS" if success else "ERROR"
        error_msg = f" - {error}" if error else ""
        
        log_entry = f"[{timestamp}] {status}: {input_file} -> {output_file}{error_msg}\n"
        
        with open(self.cleaning_log, 'a', encoding='utf-8') as f:
            f.write(log_entry)
            
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Example usage
    cleaner = JSONCleaner()
    
    # Clean a file
    try:
        cleaner.clean_file("input.json", "output.json")
    except Exception as e:
        logger.error(f"Failed to clean file: {e}") 