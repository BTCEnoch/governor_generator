"""
Migrates existing trait definitions into the new standardized structure.
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

from core.governors.traits.schemas.core_schemas import TraitIndex, TraitEntry, TraitMetadata

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TraitMigrator:
    """Handles migration of trait definitions to new structure"""
    
    def __init__(self):
        self.workspace_root = Path(__file__).parent.parent
        self.source_paths = {
            'dossiers': self.workspace_root / 'governor_dossier',
            'indexes': self.workspace_root / 'data/governors/indexes',
            'seeds': self.workspace_root / 'data/governors/seeds'
        }
        self.target_path = self.workspace_root / 'core/governors/traits/indexes'
        
    def migrate_all(self):
        """Migrate all trait definitions to new structure"""
        logger.info("Starting trait definition migration...")
        
        # Ensure target directories exist
        for subdir in ['core', 'personality', 'mystical', 'visual', 'relationships']:
            (self.target_path / subdir).mkdir(parents=True, exist_ok=True)
            
        # Migrate core traits
        self._migrate_core_traits()
        
        # Migrate personality traits
        self._migrate_personality_traits()
        
        # Migrate mystical traits
        self._migrate_mystical_traits()
        
        # Migrate visual traits
        self._migrate_visual_traits()
        
        # Migrate relationship definitions
        self._migrate_relationship_traits()
        
        logger.info("Trait definition migration complete!")

    def _migrate_personality_traits(self):
        """Migrate personality trait definitions"""
        logger.info("Migrating personality traits...")
        
        # Migrate virtues
        virtues = self._collect_virtues()
        self._write_trait_index('personality/virtues.json', virtues)
        
        # Migrate flaws
        flaws = self._collect_flaws()
        self._write_trait_index('personality/flaws.json', flaws)
        
        # Migrate approaches
        approaches = self._collect_approaches()
        self._write_trait_index('personality/approaches.json', approaches)
        
        # Migrate tones
        tones = self._collect_tones()
        self._write_trait_index('personality/tones.json', tones)

    def _migrate_mystical_traits(self):
        """Migrate mystical trait definitions"""
        logger.info("Migrating mystical traits...")
        
        # Migrate aethyrs
        aethyrs = self._collect_aethyrs()
        self._write_trait_index('mystical/aethyrs.json', aethyrs)
        
        # Migrate traditions
        traditions = self._collect_traditions()
        self._write_trait_index('mystical/traditions.json', traditions)
        
        # Migrate practices
        practices = self._collect_practices()
        self._write_trait_index('mystical/practices.json', practices)

    def _migrate_visual_traits(self):
        """Migrate visual trait definitions"""
        logger.info("Migrating visual traits...")
        
        # Migrate forms
        forms = self._collect_forms()
        self._write_trait_index('visual/forms.json', forms)
        
        # Migrate colors
        colors = self._collect_colors()
        self._write_trait_index('visual/colors.json', colors)
        
        # Migrate patterns
        patterns = self._collect_patterns()
        self._write_trait_index('visual/patterns.json', patterns)

    def _migrate_relationship_traits(self):
        """Migrate relationship definitions"""
        logger.info("Migrating relationship traits...")
        
        # Migrate governor relationships
        governor_rels = self._collect_governor_relationships()
        self._write_trait_index('relationships/governor.json', governor_rels)
        
        # Migrate tradition relationships
        tradition_rels = self._collect_tradition_relationships()
        self._write_trait_index('relationships/tradition.json', tradition_rels)
        
    def _migrate_core_traits(self):
        """Migrate core trait definitions"""
        logger.info("Migrating core traits...")
        
        # Migrate archetypes
        archetypes = self._collect_archetypes()
        self._write_trait_index('core/archetypes.json', archetypes)
        
        # Migrate elements
        elements = self._collect_elements()
        self._write_trait_index('core/elements.json', elements)
        
        # Migrate alignments
        alignments = self._collect_alignments()
        self._write_trait_index('core/alignments.json', alignments)
        
        # Migrate polarities
        polarities = self._collect_polarities()
        self._write_trait_index('core/polarities.json', polarities)
        
    def _collect_archetypes(self) -> List[TraitEntry]:
        """Collect all role archetype definitions"""
        archetypes = []
        
        # Read from role_archetypes.json
        role_file = self.source_paths['indexes'] / 'role_archetypes.json'
        if role_file.exists():
            with open(role_file) as f:
                data = json.load(f)
                for entry in data['archetypes']:
                    archetypes.append(
                        TraitEntry(
                            id=entry['id'].lower(),
                            name=entry['name'],
                            definition=entry['description'],
                            category='role_archetype',
                            metadata=TraitMetadata(
                                source=str(role_file),
                                notes=entry.get('notes')
                            )
                        )
                    )
                    
        # Collect from governor dossiers
        for dossier in self.source_paths['dossiers'].glob('*.json'):
            if dossier.name.endswith('_visual.json'):
                continue
            with open(dossier) as f:
                data = json.load(f)
                if 'persona' in data and 'polar_traits' in data['persona']:
                    archetype = data['persona']['polar_traits'].get('role_archetype')
                    if archetype:
                        # Only add if not already present
                        if not any(a.name.lower() == archetype.lower() for a in archetypes):
                            archetypes.append(
                                TraitEntry(
                                    id=archetype.lower(),
                                    name=archetype,
                                    definition=f"Role archetype found in governor {data['governor_name']}",
                                    category='role_archetype',
                                    metadata=TraitMetadata(
                                        source=str(dossier),
                                        notes=f"Extracted from {data['governor_name']} dossier"
                                    )
                                )
                            )
        
        return archetypes
        
    def _collect_elements(self) -> List[TraitEntry]:
        """Collect all elemental associations"""
        elements = []
        # Similar collection logic for elements
        return elements
        
    def _collect_alignments(self) -> List[TraitEntry]:
        """Collect all motive alignments"""
        alignments = []
        # Similar collection logic for alignments
        return alignments
        
    def _collect_polarities(self) -> List[TraitEntry]:
        """Collect all polarity definitions"""
        polarities = []
        # Similar collection logic for polarities
        return polarities

    def _collect_virtues(self) -> List[TraitEntry]:
        """Collect all virtue definitions"""
        virtues = {}  # Using dict to deduplicate
        
        # First check virtues_pool.json
        virtues_file = self.source_paths['indexes'] / 'virtues_pool.json'
        if virtues_file.exists():
            with open(virtues_file) as f:
                data = json.load(f)
                for virtue in data['virtues']:
                    virtues[virtue['name'].lower()] = TraitEntry(
                        id=virtue['name'].lower().replace(' ', '_'),
                        name=virtue['name'],
                        definition=virtue['description'],
                        category='virtue',
                        metadata=TraitMetadata(
                            source=str(virtues_file),
                            notes=virtue.get('notes')
                        )
                    )
        
        # Then collect from governor dossiers
        for dossier in self.source_paths['dossiers'].glob('*.json'):
            if dossier.name.endswith('_visual.json'):
                continue
                
            with open(dossier) as f:
                data = json.load(f)
                if 'persona' in data and 'polar_traits' in data['persona']:
                    governor_virtues = data['persona']['polar_traits'].get('virtues', [])
                    for virtue in governor_virtues:
                        virtue_lower = virtue.lower()
                        if virtue_lower not in virtues:
                            virtues[virtue_lower] = TraitEntry(
                                id=virtue_lower.replace(' ', '_'),
                                name=virtue,
                                definition=f"Virtue found in governor {data['governor_name']}",
                                category='virtue',
                                metadata=TraitMetadata(
                                    source=str(dossier),
                                    notes=f"Extracted from {data['governor_name']} dossier"
                                )
                            )
                            
        # Convert dict to sorted list
        return sorted(virtues.values(), key=lambda x: x.name)

    def _collect_flaws(self) -> List[TraitEntry]:
        """Collect all flaw definitions"""
        flaws = []
        # Collection logic for flaws
        return flaws

    def _collect_approaches(self) -> List[TraitEntry]:
        """Collect all approach definitions"""
        approaches = []
        # Collection logic for approaches
        return approaches

    def _collect_tones(self) -> List[TraitEntry]:
        """Collect all tone definitions"""
        tones = []
        # Collection logic for tones
        return tones

    def _collect_aethyrs(self) -> List[TraitEntry]:
        """Collect all aethyr definitions"""
        aethyrs = []
        # Collection logic for aethyrs
        return aethyrs

    def _collect_traditions(self) -> List[TraitEntry]:
        """Collect all tradition definitions"""
        traditions = []
        # Collection logic for traditions
        return traditions

    def _collect_practices(self) -> List[TraitEntry]:
        """Collect all practice definitions"""
        practices = []
        # Collection logic for practices
        return practices

    def _collect_forms(self) -> List[TraitEntry]:
        """Collect all form definitions"""
        forms = []
        # Collection logic for forms
        return forms

    def _collect_colors(self) -> List[TraitEntry]:
        """Collect all color definitions"""
        colors = []
        # Collection logic for colors
        return colors

    def _collect_patterns(self) -> List[TraitEntry]:
        """Collect all pattern definitions"""
        patterns = []
        # Collection logic for patterns
        return patterns

    def _collect_governor_relationships(self) -> List[TraitEntry]:
        """Collect all governor relationship definitions"""
        relationships = []
        # Collection logic for governor relationships
        return relationships

    def _collect_tradition_relationships(self) -> List[TraitEntry]:
        """Collect all tradition relationship definitions"""
        relationships = []
        # Collection logic for tradition relationships
        return relationships
        
    def _write_trait_index(self, relative_path: str, entries: List[TraitEntry]):
        """Write trait entries to index file"""
        index = TraitIndex(
            schema_version='1.0.0',
            last_updated=datetime.now(),
            entries=entries
        )
        
        # Validate before writing
        errors = index.validate()
        if errors:
            logger.error(f"Validation errors in {relative_path}:")
            for error in errors:
                logger.error(f"  - {error}")
            raise ValueError(f"Invalid trait index: {relative_path}")
            
        # Write to file
        target_file = self.target_path / relative_path
        with open(target_file, 'w') as f:
            json.dump({
                'schema_version': index.schema_version,
                'last_updated': index.last_updated.isoformat(),
                'entries': [
                    {
                        'id': e.id,
                        'name': e.name,
                        'definition': e.definition,
                        'category': e.category,
                        'subcategory': e.subcategory,
                        'correspondences': e.correspondences,
                        'metadata': {
                            'source': e.metadata.source,
                            'notes': e.metadata.notes
                        }
                    }
                    for e in index.entries
                ]
            }, f, indent=2)
        logger.info(f"Wrote {len(index.entries)} entries to {relative_path}")

if __name__ == '__main__':
    migrator = TraitMigrator()
    migrator.migrate_all() 