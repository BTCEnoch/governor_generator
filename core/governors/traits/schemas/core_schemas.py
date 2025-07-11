"""
Core trait schema definitions and validation logic.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
import json
from pathlib import Path

@dataclass
class TraitMetadata:
    """Metadata for a trait definition"""
    source: str
    notes: Optional[str] = None

@dataclass 
class TraitEntry:
    """Single trait definition entry"""
    id: str
    name: str
    definition: str
    category: str
    metadata: TraitMetadata
    subcategory: Optional[str] = None
    correspondences: Optional[List[str]] = None

    def validate(self) -> List[str]:
        """Validate trait entry data
        
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        if not self.id or not self.id.isalnum():
            errors.append(f"Invalid id: {self.id}")
        if not self.name:
            errors.append(f"Missing name for {self.id}")
        if not self.definition:
            errors.append(f"Missing definition for {self.id}")
        if not self.category:
            errors.append(f"Missing category for {self.id}")
        return errors

@dataclass
class TraitIndex:
    """Collection of trait definitions"""
    schema_version: str
    last_updated: datetime
    entries: List[TraitEntry]

    def validate(self) -> List[str]:
        """Validate entire trait index
        
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        # Version format
        if not self.schema_version or not self.schema_version.count('.') == 2:
            errors.append(f"Invalid schema version: {self.schema_version}")
            
        # Last updated
        if not self.last_updated:
            errors.append("Missing last_updated timestamp")
            
        # Entries
        if not self.entries:
            errors.append("No entries defined")
        
        # Validate each entry
        for entry in self.entries:
            errors.extend(entry.validate())
            
        # Check for duplicate IDs
        ids = [e.id for e in self.entries]
        if len(ids) != len(set(ids)):
            errors.append("Duplicate entry IDs found")
            
        return errors

    @classmethod
    def load_from_file(cls, file_path: str) -> 'TraitIndex':
        """Load trait index from JSON file
        
        Args:
            file_path: Path to JSON trait index file
            
        Returns:
            Loaded TraitIndex instance
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Trait index file not found: {file_path}")
            
        with open(path) as f:
            data = json.load(f)
            
        return cls(
            schema_version=data['schema_version'],
            last_updated=datetime.fromisoformat(data['last_updated']),
            entries=[
                TraitEntry(
                    id=e['id'],
                    name=e['name'], 
                    definition=e['definition'],
                    category=e['category'],
                    metadata=TraitMetadata(**e['metadata']),
                    subcategory=e.get('subcategory'),
                    correspondences=e.get('correspondences', [])
                )
                for e in data['entries']
            ]
        ) 