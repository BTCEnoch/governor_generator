#!/usr/bin/env python3
"""
Master Unicode Cleaner - Comprehensive JSON Unicode cleaning solution
Combines the best features from all previous cleaning scripts
"""

import json
import os
import re
import glob
import shutil
import mimetypes
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path
import logging
from datetime import datetime

# Try to import chardet for encoding detection
try:
    import chardet
    CHARDET_AVAILABLE = True
except ImportError:
    CHARDET_AVAILABLE = False
    logging.warning("chardet not available - will use utf-8 encoding by default")

# Configure logging
def setup_logging():
    """Setup logging with proper path handling"""
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "cleaning_log.txt"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

setup_logging()
logger = logging.getLogger(__name__)

class MasterUnicodeCleaner:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.stats: Dict[str, Any] = {
            'files_processed': 0,
            'files_cleaned': 0,
            'files_errors': 0,
            'files_skipped': 0,
            'unicode_chars_replaced': 0,
            'backup_files_created': 0,
            'file_types_processed': {},
            'encoding_types_used': {},
            'validation_failures': 0,
            'binary_files_skipped': 0
        }
        
        # Comprehensive Unicode replacement dictionary
        self.unicode_replacements = {
            # Emoji replacements
            '🧙‍♂️': '[WIZARD]',
            '🎭': '[THEATER]',
            '🔮': '[CRYSTAL_BALL]',
            '⚡': '[LIGHTNING]',
            '🌟': '[STAR]',
            '✨': '[SPARKLES]',
            '🌙': '[MOON]',
            '☀️': '[SUN]',
            '🌈': '[RAINBOW]',
            '🔥': '[FIRE]',
            '💫': '[DIZZY]',
            '🌸': '[CHERRY_BLOSSOM]',
            '🎵': '[MUSIC_NOTE]',
            '🎶': '[MUSIC_NOTES]',
            '🎯': '[TARGET]',
            '🎨': '[PALETTE]',
            '🎪': '[CIRCUS]',
            '🎲': '[DICE]',
            '🎸': '[GUITAR]',
            '🎺': '[TRUMPET]',
            '🎻': '[VIOLIN]',
            '🎼': '[MUSICAL_SCORE]',
            '🎤': '[MICROPHONE]',
            '🎧': '[HEADPHONES]',
            '🎬': '[MOVIE_CAMERA]',
            '🎥': '[VIDEO_CAMERA]',
            '📚': '[BOOKS]',
            '📖': '[BOOK]',
            '📝': '[MEMO]',
            '📊': '[BAR_CHART]',
            '📈': '[CHART_UP]',
            '📉': '[CHART_DOWN]',
            '📋': '[CLIPBOARD]',
            '📌': '[PUSHPIN]',
            '📍': '[LOCATION_PIN]',
            '📎': '[PAPERCLIP]',
            '📏': '[RULER]',
            '📐': '[TRIANGLE_RULER]',
            '📑': '[BOOKMARK_TABS]',
            '📒': '[LEDGER]',
            '📓': '[NOTEBOOK]',
            '📔': '[NOTEBOOK_DECORATED]',
            '📕': '[CLOSED_BOOK]',
            '📗': '[GREEN_BOOK]',
            '📘': '[BLUE_BOOK]',
            '📙': '[ORANGE_BOOK]',
            '📜': '[SCROLL]',
            '📄': '[PAGE]',
            '📃': '[PAGE_CURL]',
            '📰': '[NEWSPAPER]',
            '📱': '[MOBILE_PHONE]',
            '📲': '[MOBILE_PHONE_ARROW]',
            '📞': '[PHONE_RECEIVER]',
            '📟': '[PAGER]',
            '📠': '[FAX]',
            '📡': '[SATELLITE]',
            '📢': '[LOUDSPEAKER]',
            '📣': '[MEGAPHONE]',
            '📻': '[RADIO]',
            '📺': '[TV]',
            '📹': '[VIDEO_CAMERA]',
            '📷': '[CAMERA]',
            '📸': '[CAMERA_FLASH]',
            '📼': '[VIDEOCASSETTE]',
            '📽️': '[FILM_PROJECTOR]',
            '🎞️': '[FILM_STRIP]',
            '📿': '[PRAYER_BEADS]',
            '🔍': '[MAGNIFYING_GLASS_LEFT]',
            '🔎': '[MAGNIFYING_GLASS_RIGHT]',
            '🔬': '[MICROSCOPE]',
            '🔭': '[TELESCOPE]',
            '🗝️': '[OLD_KEY]',
            '🔑': '[KEY]',
            '🔒': '[LOCKED]',
            '🔓': '[UNLOCKED]',
            '🔐': '[LOCKED_WITH_KEY]',
            '🔏': '[LOCKED_WITH_PEN]',
            '🔔': '[BELL]',
            '🔕': '[BELL_SLASH]',
            '🔖': '[BOOKMARK]',
            '🔗': '[LINK]',
            '🔘': '[RADIO_BUTTON]',
            '🔙': '[BACK_ARROW]',
            '🔚': '[END_ARROW]',
            '🔛': '[ON_ARROW]',
            '🔜': '[SOON_ARROW]',
            '🔝': '[TOP_ARROW]',
            
            # Smart quotes and punctuation
            ''': "'",  # Left single quotation mark
            ''': "'",  # Right single quotation mark
            '"': '"',  # Left double quotation mark
            '"': '"',  # Right double quotation mark
            '„': '"',  # Double low-9 quotation mark
            '‚': "'",  # Single low-9 quotation mark
            '«': '"',  # Left-pointing double angle quotation mark
            '»': '"',  # Right-pointing double angle quotation mark
            '‹': "'",  # Single left-pointing angle quotation mark
            '›': "'",  # Single right-pointing angle quotation mark
            
            # Dashes and hyphens
            '–': '-',   # En dash
            '—': '--',  # Em dash
            '―': '--',  # Horizontal bar
            '‐': '-',   # Hyphen
            '‑': '-',   # Non-breaking hyphen
            '‒': '-',   # Figure dash
            '−': '-',   # Minus sign
            
            # Spaces and special characters
            ' ': ' ',   # Non-breaking space
            ' ': ' ',   # En quad
            ' ': ' ',   # Em quad
            ' ': ' ',   # Three-per-em space
            ' ': ' ',   # Four-per-em space
            ' ': ' ',   # Six-per-em space
            ' ': ' ',   # Figure space
            ' ': ' ',   # Punctuation space
            ' ': ' ',   # Thin space
            ' ': ' ',   # Hair space
            '​': '',    # Zero width space
            '‌': '',    # Zero width non-joiner
            '‍': '',    # Zero width joiner
            
            # Ellipsis and dots
            '…': '...',  # Horizontal ellipsis
            '⋯': '...',  # Midline horizontal ellipsis
            '⋮': '...',  # Vertical ellipsis
            '⋱': '...',  # Down right diagonal ellipsis
            
            # Escape sequences (literal strings, not actual escapes)
            '\\n\\n': ' ',  # Double newline escape sequences -> single space
            '\\n\\n\\n': ' ',  # Triple newline escape sequences -> single space
            '\\n\\n\\n\\n': ' ',  # Quadruple newline escape sequences -> single space
            '\\n': ' ',  # Single newline escape sequences -> single space
            
            # Mathematical and special symbols
            '°': ' degrees',  # Degree symbol
            '±': '+/-',       # Plus-minus sign
            '×': 'x',         # Multiplication sign
            '÷': '/',         # Division sign
            '≈': '~',         # Almost equal to
            '≠': '!=',        # Not equal to
            '≤': '<=',        # Less than or equal to
            '≥': '>=',        # Greater than or equal to
            '∞': 'infinity',  # Infinity
            'π': 'pi',        # Greek small letter pi
            'α': 'alpha',     # Greek small letter alpha
            'β': 'beta',      # Greek small letter beta
            'γ': 'gamma',     # Greek small letter gamma
            'δ': 'delta',     # Greek small letter delta
            'ε': 'epsilon',   # Greek small letter epsilon
            'ζ': 'zeta',      # Greek small letter zeta
            'η': 'eta',       # Greek small letter eta
            'θ': 'theta',     # Greek small letter theta
            'ι': 'iota',      # Greek small letter iota
            'κ': 'kappa',     # Greek small letter kappa
            'λ': 'lambda',    # Greek small letter lambda
            'μ': 'mu',        # Greek small letter mu
            'ν': 'nu',        # Greek small letter nu
            'ξ': 'xi',        # Greek small letter xi
            'ο': 'omicron',   # Greek small letter omicron
            'π': 'pi',        # Greek small letter pi
            'ρ': 'rho',       # Greek small letter rho
            'σ': 'sigma',     # Greek small letter sigma
            'τ': 'tau',       # Greek small letter tau
            'υ': 'upsilon',   # Greek small letter upsilon
            'φ': 'phi',       # Greek small letter phi
            'χ': 'chi',       # Greek small letter chi
            'ψ': 'psi',       # Greek small letter psi
            'ω': 'omega',     # Greek small letter omega
            
            # Arrows
            '→': '->',   # Right arrow
            '←': '<-',   # Left arrow
            '↑': '^',    # Up arrow
            '↓': 'v',    # Down arrow
            '↔': '<->', # Left-right arrow
            '↕': '^v',   # Up-down arrow
            '⇒': '=>',   # Right double arrow
            '⇐': '<=',   # Left double arrow
            '⇔': '<=>',  # Left-right double arrow
            
            # Trademark and copyright
            '™': '(TM)',  # Trademark symbol
            '®': '(R)',   # Registered trademark
            '©': '(C)',   # Copyright symbol
            '℠': '(SM)',  # Service mark
            
            # Bullets and list markers
            '•': '*',     # Bullet
            '‣': '*',     # Triangular bullet
            '⁃': '-',     # Hyphen bullet
            '◦': 'o',     # White bullet
            '‰': '%',     # Per mille sign
            '‱': '%',     # Per ten thousand sign
            
            # Fractions
            '½': '1/2',   # Vulgar fraction one half
            '⅓': '1/3',   # Vulgar fraction one third
            '⅔': '2/3',   # Vulgar fraction two thirds
            '¼': '1/4',   # Vulgar fraction one quarter
            '¾': '3/4',   # Vulgar fraction three quarters
            '⅕': '1/5',   # Vulgar fraction one fifth
            '⅖': '2/5',   # Vulgar fraction two fifths
            '⅗': '3/5',   # Vulgar fraction three fifths
            '⅘': '4/5',   # Vulgar fraction four fifths
            '⅙': '1/6',   # Vulgar fraction one sixth
            '⅚': '5/6',   # Vulgar fraction five sixths
            '⅐': '1/7',   # Vulgar fraction one seventh
            '⅛': '1/8',   # Vulgar fraction one eighth
            '⅜': '3/8',   # Vulgar fraction three eighths
            '⅝': '5/8',   # Vulgar fraction five eighths
            '⅞': '7/8',   # Vulgar fraction seven eighths
            '⅑': '1/9',   # Vulgar fraction one ninth
            '⅒': '1/10',  # Vulgar fraction one tenth
            
            # Accented characters - Latin
            'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'å': 'a', 'æ': 'ae',
            'ç': 'c', 'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e', 'ì': 'i', 'í': 'i', 
            'î': 'i', 'ï': 'i', 'ð': 'd', 'ñ': 'n', 'ò': 'o', 'ó': 'o', 'ô': 'o', 
            'õ': 'o', 'ö': 'o', 'ø': 'o', 'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u', 
            'ý': 'y', 'þ': 'th', 'ÿ': 'y', 'ß': 'ss',
            'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A', 'Å': 'A', 'Æ': 'AE',
            'Ç': 'C', 'È': 'E', 'É': 'E', 'Ê': 'E', 'Ë': 'E', 'Ì': 'I', 'Í': 'I', 
            'Î': 'I', 'Ï': 'I', 'Ð': 'D', 'Ñ': 'N', 'Ò': 'O', 'Ó': 'O', 'Ô': 'O', 
            'Õ': 'O', 'Ö': 'O', 'Ø': 'O', 'Ù': 'U', 'Ú': 'U', 'Û': 'U', 'Ü': 'U', 
            'Ý': 'Y', 'Þ': 'TH', 'Ÿ': 'Y',
            
            # Extended Latin characters
            'ā': 'a', 'ă': 'a', 'ą': 'a', 'ć': 'c', 'ĉ': 'c', 'ċ': 'c', 'č': 'c',
            'ď': 'd', 'đ': 'd', 'ē': 'e', 'ĕ': 'e', 'ė': 'e', 'ę': 'e', 'ě': 'e',
            'ĝ': 'g', 'ğ': 'g', 'ġ': 'g', 'ģ': 'g', 'ĥ': 'h', 'ħ': 'h', 'ĩ': 'i',
            'ī': 'i', 'ĭ': 'i', 'į': 'i', 'İ': 'I', 'ı': 'i', 'ĵ': 'j', 'ķ': 'k',
            'ĸ': 'k', 'ĺ': 'l', 'ļ': 'l', 'ľ': 'l', 'ŀ': 'l', 'ł': 'l', 'ń': 'n',
            'ņ': 'n', 'ň': 'n', 'ŉ': 'n', 'ŋ': 'ng', 'ō': 'o', 'ŏ': 'o', 'ő': 'o',
            'œ': 'oe', 'ŕ': 'r', 'ŗ': 'r', 'ř': 'r', 'ś': 's', 'ŝ': 's', 'ş': 's',
            'š': 's', 'ţ': 't', 'ť': 't', 'ŧ': 't', 'ũ': 'u', 'ū': 'u', 'ŭ': 'u',
            'ů': 'u', 'ű': 'u', 'ų': 'u', 'ŵ': 'w', 'ŷ': 'y', 'ź': 'z', 'ż': 'z',
            'ž': 'z',
            
            # Currency symbols
            '€': 'EUR', '£': 'GBP', '¥': 'JPY', '₹': 'INR', '₽': 'RUB', '₩': 'KRW',
            '₪': 'ILS', '₫': 'VND', '₵': 'GHS', '₡': 'CRC', '₨': 'PKR', '₦': 'NGN',
            '₴': 'UAH', '₱': 'PHP', '₲': 'PYG', '₳': 'ARA', '₭': 'LAK', '₮': 'MNT',
            '₯': 'GRD', '₰': 'PF', '₸': 'KZT', '₹': 'INR', '₺': 'TRY', '₻': 'CE',
            '₼': 'AZN', '₽': 'RUB', '₾': 'GEL', '₿': 'BTC', '¢': 'cents', '¤': 'currency',
            
            # Additional symbols
            '§': 'section', '¶': 'paragraph', '†': 'dagger', '‡': 'double-dagger',
            '‰': 'per-mille', '‱': 'per-ten-thousand', '′': "'", '″': '"', '‴': "'''",
            '‵': '`', '‶': '``', '‷': '```', '‸': '^', '‹': '<', '›': '>', '※': 'note',
            '‼': '!!', '⁇': '??', '⁈': '?!', '⁉': '!?', '⁊': '&', '⁋': 'reversed-paragraph',
            '⁌': 'reference', '⁍': 'x', '⁎': '*', '⁏': ';', '⁐': 'close-up',
            '⁑': '*', '⁒': '%', '⁓': '~', '⁔': '~', '⁕': '*', '⁖': '...', '⁗': '....',
            '⁘': '....', '⁙': '.....', '⁚': '......', '⁛': '......', '⁜': '......',
            '⁝': '......', '⁞': '......'
        }
        
        logger.info("Master Unicode Cleaner initialized")
        logger.info(f"Project root: {self.project_root.absolute()}")
        logger.info(f"Unicode replacements loaded: {len(self.unicode_replacements)} mappings")
        logger.info(f"Chardet available: {CHARDET_AVAILABLE}")
    
    def detect_file_encoding(self, file_path: Path) -> str:
        """Detect the encoding of a file using chardet or fallback to utf-8"""
        if not CHARDET_AVAILABLE:
            return 'utf-8'
        
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # Read first 10KB for detection
            
            if not raw_data:
                return 'utf-8'
            
            detection = chardet.detect(raw_data)
            if detection and detection['encoding']:
                confidence = detection.get('confidence', 0)
                if confidence > 0.7:  # Only use if confidence is high
                    return detection['encoding']
            
            return 'utf-8'  # Fallback to utf-8
            
        except Exception:
            return 'utf-8'
    
    def detect_file_type(self, file_path: Path) -> str:
        """Detect the type of file based on extension and content"""
        extension = file_path.suffix.lower()
        
        # File type mapping
        type_mapping = {
            '.py': 'python',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.md': 'markdown',
            '.txt': 'text',
            '.html': 'html',
            '.css': 'css',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.xml': 'xml',
            '.csv': 'csv',
            '.log': 'log',
            '.conf': 'config',
            '.cfg': 'config',
            '.ini': 'config',
            '.toml': 'config',
            '.rst': 'restructuredtext',
            '.sh': 'shell',
            '.bash': 'shell',
            '.ps1': 'powershell',
            '.bat': 'batch',
            '.sql': 'sql',
            '.r': 'r',
            '.R': 'r'
        }
        
        return type_mapping.get(extension, 'text')
    
    def is_binary_file(self, file_path: Path) -> bool:
        """Check if file is binary (contains null bytes)"""
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                return b'\x00' in chunk
        except Exception:
            return False
    
    def validate_cleaned_file(self, file_path: Path, content: str, file_type: str) -> bool:
        """Validate that cleaned content is still valid for the file type"""
        try:
            if file_type == 'json':
                # Validate JSON structure
                json.loads(content)
                logger.info(f"  [OK] JSON structure validated")
                return True
            
            elif file_type == 'yaml':
                # Validate YAML structure (if PyYAML is available)
                try:
                    import yaml
                    yaml.safe_load(content)
                    logger.info(f"  [OK] YAML structure validated")
                    return True
                except ImportError:
                    logger.warning(f"  [WARNING] PyYAML not available, skipping YAML validation")
                    return True
            
            elif file_type == 'python':
                # Basic Python syntax validation
                try:
                    compile(content, str(file_path), 'exec')
                    logger.info(f"  [OK] Python syntax validated")
                    return True
                except SyntaxError as e:
                    logger.error(f"  [ERROR] Python syntax error: {e}")
                    return False
            
            elif file_type == 'xml':
                # Basic XML validation
                try:
                    import xml.etree.ElementTree as ET
                    ET.fromstring(content)
                    logger.info(f"  [OK] XML structure validated")
                    return True
                except ET.ParseError as e:
                    logger.error(f"  [ERROR] XML parse error: {e}")
                    return False
            
            elif file_type == 'csv':
                # Basic CSV validation
                try:
                    import csv
                    from io import StringIO
                    csv_reader = csv.reader(StringIO(content))
                    list(csv_reader)  # Try to read all rows
                    logger.info(f"  [OK] CSV structure validated")
                    return True
                except csv.Error as e:
                    logger.error(f"  [ERROR] CSV error: {e}")
                    return False
            
            else:
                # For other file types, just check if content is not empty
                if content.strip():
                    logger.info(f"  [OK] Content validated for {file_type}")
                    return True
                else:
                    logger.warning(f"  [WARNING] Content is empty after cleaning")
                    return False
        
        except Exception as e:
            logger.error(f"  [ERROR] Validation failed: {e}")
            return False
    
    def find_text_files(self) -> List[Path]:
        """Find all text files in the project, excluding backups and temp files"""
        text_files = []
        
        # Directories to exclude
        exclude_dirs = {
            '.git', '__pycache__', '.cursor', 'node_modules', 
            'profile_backups', 'json_cleaner', 'logs', 'temp',
            'build', 'dist', '.venv', 'venv', '.env'
        }
        
        # File extensions to include (text files only)
        include_extensions = {
            '.py', '.json', '.md', '.txt', '.yaml', '.yml', 
            '.js', '.ts', '.html', '.css', '.xml', '.csv', 
            '.log', '.conf', '.cfg', '.ini', '.toml', '.rst',
            '.sh', '.bash', '.ps1', '.bat', '.sql', '.r', '.R'
        }
        
        # File patterns to exclude
        exclude_patterns = {
            '*_backup.*', '*_backup_*.*', '*.backup.*',
            '*_temp.*', '*_temporary.*', '*.temp.*',
            '*_unicode_backup*', '*.lock', '*.tmp'
        }
        
        logger.info("Scanning for text files...")
        
        for file_path in self.project_root.rglob('*'):
            # Skip directories
            if file_path.is_dir():
                continue
            
            # Skip if in excluded directory
            if any(excluded in file_path.parts for excluded in exclude_dirs):
                continue
                
            # Skip if not a text file extension
            if file_path.suffix.lower() not in include_extensions:
                continue
                
            # Skip if matches excluded pattern
            if any(file_path.match(pattern) for pattern in exclude_patterns):
                continue
                
            # Skip if it's a backup file we might have created
            if '_unicode_backup' in file_path.name:
                continue
                
            text_files.append(file_path)
        
        logger.info(f"Found {len(text_files)} text files to process")
        return sorted(text_files)
    
    def clean_text_file(self, file_path: Path, create_backup: bool = True) -> bool:
        """Clean Unicode characters from a text file"""
        try:
            logger.info(f"Processing: {file_path.relative_to(self.project_root)}")
            
            # Skip binary files
            if self.is_binary_file(file_path):
                logger.info(f"  [SKIP] Binary file detected")
                self.stats['binary_files_skipped'] += 1
                return False
            
            # Detect file encoding
            encoding = self.detect_file_encoding(file_path)
            file_type = self.detect_file_type(file_path)
            
            # Track file type and encoding statistics
            self.stats['file_types_processed'][file_type] = self.stats['file_types_processed'].get(file_type, 0) + 1
            self.stats['encoding_types_used'][encoding] = self.stats['encoding_types_used'].get(encoding, 0) + 1
            
            logger.info(f"  [INFO] File type: {file_type}, Encoding: {encoding}")
            
            # Read the file with detected encoding
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    original_content = f.read()
            except UnicodeDecodeError:
                # Fallback to utf-8 with error handling
                logger.warning(f"  [WARNING] Failed to read with {encoding}, trying utf-8")
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                        original_content = f.read()
                except UnicodeDecodeError:
                    logger.error(f"  [ERROR] Cannot read file with any encoding")
                    return False
            
            # Check if file needs cleaning
            needs_cleaning = False
            for unicode_char in self.unicode_replacements.keys():
                if unicode_char in original_content:
                    needs_cleaning = True
                    break
            
            if not needs_cleaning:
                logger.info(f"  [CLEAN] No Unicode characters found")
                return False
            
            # Create backup if requested
            if create_backup:
                backup_path = file_path.with_suffix(f'{file_path.suffix}_unicode_backup')
                shutil.copy2(file_path, backup_path)
                self.stats['backup_files_created'] += 1
                logger.info(f"  [BACKUP] Backup created: {backup_path.name}")
            
            # Apply Unicode replacements
            cleaned_content = original_content
            replacements_made = 0
            
            for unicode_char, replacement in self.unicode_replacements.items():
                if unicode_char in cleaned_content:
                    count = cleaned_content.count(unicode_char)
                    cleaned_content = cleaned_content.replace(unicode_char, replacement)
                    replacements_made += count
                    if count > 0:
                        logger.info(f"  • Replaced {count}x '{unicode_char}' with '{replacement}'")
            
            # Validate cleaned content
            if not self.validate_cleaned_file(file_path, cleaned_content, file_type):
                logger.error(f"  [ERROR] File validation failed - restoring from backup")
                self.stats['validation_failures'] += 1
                return False
            
            # Write cleaned content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            self.stats['unicode_chars_replaced'] += replacements_made
            logger.info(f"  [SUCCESS] Cleaned {replacements_made} Unicode characters")
            return True
            
        except Exception as e:
            logger.error(f"  ✗ Error processing file: {e}")
            self.stats['files_errors'] += 1
            return False
    
    def clean_all_text_files(self, create_backups: bool = True) -> Dict[str, Any]:
        """Clean all text files in the project"""
        start_time = datetime.now()
        logger.info("=" * 60)
        logger.info("UNIVERSAL UNICODE CLEANER - STARTING BATCH PROCESSING")
        logger.info("=" * 60)
        
        # Find all text files
        text_files = self.find_text_files()
        
        if not text_files:
            logger.warning("No text files found to process")
            return self.stats
        
        logger.info(f"Found {len(text_files)} text files to process")
        
        # Process each file with progress tracking
        for idx, file_path in enumerate(text_files, 1):
            self.stats['files_processed'] += 1
            
            # Progress indication
            progress = (idx / len(text_files)) * 100
            logger.info(f"[{idx}/{len(text_files)}] ({progress:.1f}%) Processing file...")
            
            try:
                if self.clean_text_file(file_path, create_backups):
                    self.stats['files_cleaned'] += 1
                else:
                    self.stats['files_skipped'] += 1
            except Exception as e:
                logger.error(f"  [ERROR] Unexpected error processing {file_path}: {e}")
                self.stats['files_errors'] += 1
        
        # Calculate processing time
        end_time = datetime.now()
        processing_time = end_time - start_time
        
        # Generate comprehensive final report
        logger.info("=" * 60)
        logger.info("UNIVERSAL UNICODE CLEANER - PROCESSING COMPLETE")
        logger.info("=" * 60)
        logger.info(f"[STATS] COMPREHENSIVE FINAL STATISTICS:")
        logger.info(f"  • Total files processed: {self.stats['files_processed']}")
        logger.info(f"  • Files cleaned: {self.stats['files_cleaned']}")
        logger.info(f"  • Files skipped: {self.stats['files_skipped']}")
        logger.info(f"  • Files with errors: {self.stats['files_errors']}")
        logger.info(f"  • Binary files skipped: {self.stats['binary_files_skipped']}")
        logger.info(f"  • Validation failures: {self.stats['validation_failures']}")
        logger.info(f"  • Unicode characters replaced: {self.stats['unicode_chars_replaced']:,}")
        logger.info(f"  • Backup files created: {self.stats['backup_files_created']}")
        logger.info(f"  • Processing time: {processing_time}")
        
        # File type breakdown
        if self.stats['file_types_processed']:
            logger.info(f"[BREAKDOWN] File types processed:")
            for file_type, count in sorted(self.stats['file_types_processed'].items()):
                logger.info(f"  • {file_type}: {count} files")
        
        # Encoding breakdown
        if self.stats['encoding_types_used']:
            logger.info(f"[BREAKDOWN] Encodings detected:")
            for encoding, count in sorted(self.stats['encoding_types_used'].items()):
                logger.info(f"  • {encoding}: {count} files")
        
        logger.info("=" * 60)
        
        # Add processing time to stats
        self.stats['processing_time'] = str(processing_time)
        self.stats['start_time'] = start_time.isoformat()
        self.stats['end_time'] = end_time.isoformat()
        
        return self.stats
    
    def cleanup_backup_files(self) -> int:
        """Clean up backup files created during processing"""
        logger.info("Cleaning up backup files...")
        
        backup_files = list(self.project_root.rglob('*_unicode_backup'))
        
        for backup_file in backup_files:
            try:
                backup_file.unlink()
                logger.info(f"  [DELETED] Removed: {backup_file.name}")
            except Exception as e:
                logger.error(f"  [ERROR] Failed to remove {backup_file.name}: {e}")
        
        logger.info(f"Removed {len(backup_files)} backup files")
        return len(backup_files)

def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Universal Unicode Cleaner for all text files')
    parser.add_argument('--no-backups', action='store_true', 
                       help='Skip creating backup files')
    parser.add_argument('--cleanup-backups', action='store_true',
                       help='Remove all backup files after cleaning')
    parser.add_argument('--project-root', type=str, default='.',
                       help='Project root directory (default: current directory)')
    
    args = parser.parse_args()
    
    # Initialize cleaner
    cleaner = MasterUnicodeCleaner(args.project_root)
    
    # Run cleaning process
    stats = cleaner.clean_all_text_files(create_backups=not args.no_backups)
    
    # Cleanup backups if requested
    if args.cleanup_backups:
        cleaner.cleanup_backup_files()
    
    # Exit with appropriate code
    if stats['files_errors'] > 0:
        logger.warning(f"Completed with {stats['files_errors']} errors")
        exit(1)
    else:
        logger.info("All files processed successfully!")
        exit(0)

if __name__ == "__main__":
    main() 