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
from typing import Dict, List, Tuple, Any
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('json_cleaner/cleaning_log.txt'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MasterUnicodeCleaner:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.stats: Dict[str, Any] = {
            'files_processed': 0,
            'files_cleaned': 0,
            'files_errors': 0,
            'unicode_chars_replaced': 0,
            'backup_files_created': 0
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
        }
        
        logger.info("Master Unicode Cleaner initialized")
        logger.info(f"Project root: {self.project_root.absolute()}")
        logger.info(f"Unicode replacements loaded: {len(self.unicode_replacements)} mappings")
    
    def find_json_files(self) -> List[Path]:
        """Find all JSON files in the project, excluding backups and temp files"""
        json_files = []
        
        # Directories to exclude
        exclude_dirs = {
            '.git', '__pycache__', '.cursor', 'node_modules', 
            'profile_backups', 'json_cleaner', 'logs', 'temp'
        }
        
        # File patterns to exclude
        exclude_patterns = {
            '*_backup.json', '*_backup_*.json', '*.backup.json',
            '*_temp.json', '*_temporary.json', '*.temp.json'
        }
        
        logger.info("Scanning for JSON files...")
        
        for json_file in self.project_root.rglob('*.json'):
            # Skip if in excluded directory
            if any(excluded in json_file.parts for excluded in exclude_dirs):
                continue
                
            # Skip if matches excluded pattern
            if any(json_file.match(pattern) for pattern in exclude_patterns):
                continue
                
            # Skip if it's a backup file we might have created
            if '_unicode_backup' in json_file.name:
                continue
                
            json_files.append(json_file)
        
        logger.info(f"Found {len(json_files)} JSON files to process")
        return sorted(json_files)
    
    def clean_json_file(self, file_path: Path, create_backup: bool = True) -> bool:
        """Clean Unicode characters from a single JSON file"""
        try:
            logger.info(f"Processing: {file_path.relative_to(self.project_root)}")
            
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
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
                backup_path = file_path.with_suffix('.json_unicode_backup')
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
            
            # Validate JSON structure
            try:
                json.loads(cleaned_content)
                logger.info(f"  [OK] JSON structure validated")
            except json.JSONDecodeError as e:
                logger.error(f"  [ERROR] JSON validation failed: {e}")
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
    
    def clean_all_json_files(self, create_backups: bool = True) -> Dict[str, Any]:
        """Clean all JSON files in the project"""
        start_time = datetime.now()
        logger.info("=" * 60)
        logger.info("MASTER UNICODE CLEANER - STARTING BATCH PROCESSING")
        logger.info("=" * 60)
        
        # Find all JSON files
        json_files = self.find_json_files()
        
        if not json_files:
            logger.warning("No JSON files found to process")
            return self.stats
        
        # Process each file
        for file_path in json_files:
            self.stats['files_processed'] += 1
            
            if self.clean_json_file(file_path, create_backups):
                self.stats['files_cleaned'] += 1
        
        # Calculate processing time
        end_time = datetime.now()
        processing_time = end_time - start_time
        
        # Generate final report
        logger.info("=" * 60)
        logger.info("MASTER UNICODE CLEANER - PROCESSING COMPLETE")
        logger.info("=" * 60)
        logger.info(f"[STATS] FINAL STATISTICS:")
        logger.info(f"  • Files processed: {self.stats['files_processed']}")
        logger.info(f"  • Files cleaned: {self.stats['files_cleaned']}")
        logger.info(f"  • Files with errors: {self.stats['files_errors']}")
        logger.info(f"  • Unicode characters replaced: {self.stats['unicode_chars_replaced']:,}")
        logger.info(f"  • Backup files created: {self.stats['backup_files_created']}")
        logger.info(f"  • Processing time: {processing_time}")
        logger.info("=" * 60)
        
        # Add processing time to stats
        self.stats['processing_time'] = str(processing_time)
        self.stats['start_time'] = start_time.isoformat()
        self.stats['end_time'] = end_time.isoformat()
        
        return self.stats
    
    def cleanup_backup_files(self) -> int:
        """Clean up backup files created during processing"""
        logger.info("Cleaning up backup files...")
        
        backup_files = list(self.project_root.rglob('*.json_unicode_backup'))
        
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
    
    parser = argparse.ArgumentParser(description='Master Unicode Cleaner for JSON files')
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
    stats = cleaner.clean_all_json_files(create_backups=not args.no_backups)
    
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