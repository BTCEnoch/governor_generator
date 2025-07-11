# Governor Trait System

This directory contains the standardized trait data for all 91 Enochian Governors. The system is designed to maintain consistency and provide a single source of truth for all governor traits.

## Directory Structure

```
traits/
├── canonical/       # Core defining traits (name, aethyr, region, etc.)
├── enhanced/        # Expanded trait definitions and correspondences
├── mystical/        # Mystical alignments and correspondences
├── personality/     # Personality traits and teaching styles
└── visual/         # Visual manifestation aspects
```

## File Naming Convention

All trait files follow the format: `{governor_id_lowercase}_{trait_type}.json`

Example:
- `occodon_canonical.json`
- `occodon_enhanced.json`
- `occodon_mystical.json`
- `occodon_personality.json`
- `occodon_visual.json`

## Trait Types

### Canonical Traits
Core traits that define a governor's fundamental nature:
- Name
- Aethyr
- Region
- Correspondence
- Personality traits
- Domain
- Visual motif
- Letter influence

### Enhanced Traits
Expanded definitions and practical applications:
- Trait name
- Definition
- Source
- Correspondences
- Practical application

### Mystical Traits
Mystical alignments and correspondences:
- Element
- Alignment
- Zodiac
- Tarot
- Sephirot
- Angel
- Number

### Personality Traits
Behavioral and teaching characteristics:
- Archetype
- Primary traits
- Secondary traits
- Teaching style
- Approach
- Tone

### Visual Traits
Visual manifestation aspects:
- Form type
- Color scheme
- Sacred geometry
- Manifestation
- Effects

## Version Control

Each trait file includes a version field to track schema evolution:
```json
{
    "version": "1.0.0",
    "trait_data": {
        // ... trait specific fields
    }
}
```

## Usage

The trait system is accessed through the `TraitLoader` class in `core/governors/traits/loader.py`. Example usage:

```python
from core.governors.traits.loader import TraitLoader

# Initialize loader
loader = TraitLoader()

# Load all traits for a governor
traits = loader.load_all_traits("OCCODON", 1)

# Access specific traits
canonical = traits.canonical
enhanced = traits.enhanced
mystical = traits.mystical
personality = traits.personality
visual = traits.visual
```

## Data Migration

To migrate data from the old index-based system to this new structure:

```bash
python scripts/migrate_traits.py
```

The migration script will:
1. Extract data from the old index files
2. Convert to the new schema format
3. Save in the appropriate trait subdirectories
4. Maintain data integrity and relationships

## Schema Validation

All trait data is validated against schemas defined in `core/governors/traits/schemas/trait_schemas.py`. The schemas ensure:
- Required fields are present
- Field types are correct
- Enums are valid
- Relationships are maintained

## Contributing

When adding or modifying governor traits:
1. Use the appropriate trait type directory
2. Follow the file naming convention
3. Validate against the schema
4. Update version number if schema changes
5. Run tests to ensure integrity

## Testing

Run the trait system tests:

```bash
python -m pytest tests/core/governors/traits/
python -m pytest tests/scripts/test_migrate_traits.py
``` 