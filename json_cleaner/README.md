# Universal JSON Cleaner

A powerful and efficient Unicode text cleaning system designed for the Enochian Governor Generation Project. This tool helps maintain consistent text encoding and handles special characters across JSON and text files.

## Features

- 🚀 Asynchronous processing for improved performance
- 🔄 Comprehensive Unicode character handling
- 📝 JSON structure preservation and validation
- 💾 Automatic file backups
- 📊 Detailed processing statistics
- 🎯 Configurable cleaning rules
- 🔍 Smart encoding detection
- 🛡️ Robust error handling

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python -m json_cleaner.main --root /path/to/directory
```

### Advanced Options

```bash
# Custom configuration
python -m json_cleaner.main --root /path/to/directory --config custom_config.json

# Disable backups
python -m json_cleaner.main --root /path/to/directory --no-backup

# Set maximum file size (in MB)
python -m json_cleaner.main --root /path/to/directory --max-size 50

# Set concurrent processing limit
python -m json_cleaner.main --root /path/to/directory --concurrent 5

# Enable strict mode
python -m json_cleaner.main --root /path/to/directory --strict
```

## Configuration

The cleaner can be configured through a JSON file or command-line arguments. Default settings can be found in `config.py`.

### Example Configuration File

```json
{
    "backup_enabled": true,
    "max_file_size_mb": 100,
    "max_concurrent_files": 10,
    "validation_enabled": true,
    "strict_mode": false,
    "log_level": "INFO"
}
```

## Project Structure

```
json_cleaner/
├── main.py              # Entry point and CLI interface
├── cleaner.py           # Core cleaning implementation
├── config.py            # Configuration and constants
├── utils.py             # Utility functions
├── logs/                # Log files directory
└── backups/             # Backup files directory
```

## Features in Detail

### Asynchronous Processing

The cleaner uses Python's asyncio to process multiple files concurrently, significantly improving performance on large directories.

### Unicode Handling

Comprehensive handling of:
- Emoji and special symbols
- Smart quotes and punctuation
- Various types of spaces and line endings
- Mathematical and special characters

### Backup System

- Automatic backup creation before processing
- Timestamped backup files
- Configurable backup behavior

### Validation

- JSON structure preservation
- Encoding validation
- File integrity checks
- Configurable validation rules

### Error Handling

- Graceful error recovery
- Detailed error logging
- Optional strict mode
- Comprehensive error statistics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is part of the Enochian Governor Generation Project and is subject to its licensing terms.

## Acknowledgments

This tool is designed to work seamlessly with the Enochian Governor Generation Project's requirements for maintaining sacred text integrity while ensuring technical compatibility. 