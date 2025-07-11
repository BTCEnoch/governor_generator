"""
Bitcoin L1 optimized visual traits system.
Provides compact storage and deterministic generation of governor visual aspects.
"""

import hashlib
import struct
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Dict, List, Optional, Tuple, Any, cast
from core.utils.batch import UnifiedBatchProcessor, BatchConfig

# Constants
HEADER_VERSION = b'VIS1'  # 4-byte header/version
TRAITS_SIZE = 16  # Total size in bytes

class FormType(IntEnum):
    """Visual form types (3 bits)"""
    ETHEREAL = 0
    GEOMETRIC = 1
    FLAME = 2
    FLUID = 3
    CRYSTALLINE = 4
    PLASMA = 5
    COMPOSITE = 6
    TRANSCENDENT = 7

class ColorScheme(IntEnum):
    """Color schemes (3 bits)"""
    PRISMATIC = 0
    GOLDEN = 1
    SILVER = 2
    AZURE = 3
    EMERALD = 4
    PLASMA = 5
    OBSIDIAN = 6
    OPALESCENT = 7

class GeometryPattern(IntEnum):
    """Geometry pattern flags (1 byte)"""
    MERKABA = 1 << 0
    METATRON = 1 << 1
    FLOWER_OF_LIFE = 1 << 2
    TORUS = 1 << 3
    SPIRAL = 1 << 4
    FRACTAL = 1 << 5
    TESSERACT = 1 << 6
    CUSTOM = 1 << 7

class EnvironmentalEffectType(IntEnum):
    """Environmental effect types (3 bits)"""
    REALITY_DISTORTION = 0
    ELEMENTAL = 1
    DIMENSIONAL = 2
    TIME_DILATION = 3
    GRAVITY = 4
    ENERGY_FIELD = 5
    PSYCHIC = 6
    QUANTUM = 7

class EffectRadius(IntEnum):
    """Effect radius (2 bits)"""
    PERSONAL = 0  # 2m
    ROOM = 1      # 5m
    BUILDING = 2  # 20m
    REGION = 3    # 100m

class EffectIntensity(IntEnum):
    """Effect intensity (3 bits)"""
    SUBTLE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4
    EXTREME = 5
    OVERWHELMING = 6
    REALITY_SHATTERING = 7

@dataclass
class EnvironmentalEffect:
    """Packed environmental effect data"""
    effect_type: EnvironmentalEffectType
    radius: EffectRadius
    intensity: EffectIntensity

    def to_byte(self) -> int:
        """Pack into single byte"""
        return (
            (self.effect_type & 0x7) |
            ((self.radius & 0x3) << 3) |
            ((self.intensity & 0x7) << 5)
        )

    @classmethod
    def from_byte(cls, byte: int) -> 'EnvironmentalEffect':
        """Unpack from single byte"""
        return cls(
            effect_type=EnvironmentalEffectType(byte & 0x7),
            radius=EffectRadius((byte >> 3) & 0x3),
            intensity=EffectIntensity((byte >> 5) & 0x7)
        )

def hash_governor_data(name: str, aethyr_num: int, element: str) -> bytes:
    """Create deterministic seed from governor data"""
    data = f"{name}:{aethyr_num}:{element}".encode()
    return hashlib.sha256(data).digest()

def get_form_type(seed: bytes) -> int:
    """Deterministically get form type from seed"""
    return seed[0] & 0x7  # Use first 3 bits

def get_color_scheme(seed: bytes, element: str) -> int:
    """Get color scheme based on seed and element"""
    element_colors = {
        'Fire': ColorScheme.GOLDEN,
        'Air': ColorScheme.SILVER,
        'Water': ColorScheme.AZURE,
        'Earth': ColorScheme.EMERALD,
        'Spirit': ColorScheme.PLASMA
    }
    if element in element_colors:
        return element_colors[element]
    return seed[1] & 0x7  # Use 3 bits if no element match

def get_aethyr_number(aethyr: str) -> int:
    """Convert aethyr name to numeric value (1-30)"""
    aethyr_map = {
        'LIL': 1, 'ARN': 2, 'ZOM': 3, 'PAZ': 4, 'LIT': 5,
        'MAZ': 6, 'DEO': 7, 'ZID': 8, 'ZIP': 9, 'ZAX': 10,
        'ICH': 11, 'LOE': 12, 'ZIM': 13, 'UTA': 14, 'OXO': 15,
        'LEA': 16, 'TAN': 17, 'ZEN': 18, 'POP': 19, 'CHR': 20,
        'ASP': 21, 'LIN': 22, 'TOR': 23, 'NIA': 24, 'UTI': 25,
        'DES': 26, 'ZAA': 27, 'BAG': 28, 'RII': 29, 'TEX': 30
    }
    return aethyr_map.get(aethyr.upper(), 15)  # Default to middle aethyr if unknown

def get_aethyr_name(number: int) -> str:
    """Convert aethyr number (1-30) to name"""
    aethyr_names = {
        1: 'LIL', 2: 'ARN', 3: 'ZOM', 4: 'PAZ', 5: 'LIT',
        6: 'MAZ', 7: 'DEO', 8: 'ZID', 9: 'ZIP', 10: 'ZAX',
        11: 'ICH', 12: 'LOE', 13: 'ZIM', 14: 'UTA', 15: 'OXO',
        16: 'LEA', 17: 'TAN', 18: 'ZEN', 19: 'POP', 20: 'CHR',
        21: 'ASP', 22: 'LIN', 23: 'TOR', 24: 'NIA', 25: 'UTI',
        26: 'DES', 27: 'ZAA', 28: 'BAG', 29: 'RII', 30: 'TEX'
    }
    return aethyr_names.get(number, 'OXO')  # Default to middle aethyr if unknown

def get_geometry_patterns(seed: bytes, aethyr: str) -> int:
    """Get geometry patterns based on seed and aethyr"""
    patterns = 0
    aethyr_num = get_aethyr_number(aethyr)
    
    # Higher aethyrs get more complex patterns
    if aethyr_num <= 3:  # Highest aethyrs
        patterns |= GeometryPattern.MERKABA | GeometryPattern.METATRON
    elif aethyr_num <= 7:
        patterns |= GeometryPattern.FLOWER_OF_LIFE | GeometryPattern.TORUS
    elif aethyr_num <= 12:
        patterns |= GeometryPattern.SPIRAL | GeometryPattern.FRACTAL
    
    # Add random pattern based on seed
    patterns |= (1 << (seed[2] & 0x7))
    
    return patterns & 0xFF  # Ensure 8 bits only

def get_environmental_effects(seed: bytes, element: str) -> int:
    """Get environmental effects based on seed and element"""
    # Map elements to effect types
    element_effects = {
        'Fire': EnvironmentalEffectType.ELEMENTAL,
        'Air': EnvironmentalEffectType.DIMENSIONAL,
        'Water': EnvironmentalEffectType.TIME_DILATION,
        'Earth': EnvironmentalEffectType.GRAVITY,
        'Spirit': EnvironmentalEffectType.QUANTUM
    }
    
    effect = EnvironmentalEffect(
        effect_type=element_effects.get(element, EnvironmentalEffectType.REALITY_DISTORTION),
        radius=EffectRadius(seed[3] & 0x3),  # 2 bits for radius
        intensity=EffectIntensity((seed[3] >> 2) & 0x7)  # 3 bits for intensity
    )
    
    return effect.to_byte()

def generate_visual_traits(governor_name: str, aethyr: str, element: str) -> bytes:
    """Generate compact binary visual traits"""
    seed = hash_governor_data(governor_name, get_aethyr_number(aethyr), element)
    traits = bytearray(TRAITS_SIZE)
    
    # Generate each trait deterministically
    traits[0:4] = HEADER_VERSION
    traits[4] = get_form_type(seed)
    traits[5] = get_color_scheme(seed, element)
    traits[6] = get_geometry_patterns(seed, aethyr)
    traits[7] = get_environmental_effects(seed, element)
    traits[8] = seed[4] & 0xFF  # Time variations
    traits[9] = seed[5] & 0xFF  # Energy signature
    traits[10] = seed[6] & 0xFF  # Symbol set
    traits[11] = seed[7] & 0xFF  # Light/shadow
    traits[12:16] = seed[8:12]   # Special properties
    
    return bytes(traits)

def expand_form_type(byte: int) -> Dict[str, Any]:
    """Expand form type byte into full description"""
    form = FormType(byte & 0x7)
    descriptions = {
        FormType.ETHEREAL: {
            'name': 'Ethereal',
            'description': 'A luminous, ever-shifting form of pure light and energy',
            'interactions': ['phase_shift', 'energy_resonance', 'light_manipulation']
        },
        FormType.GEOMETRIC: {
            'name': 'Geometric',
            'description': 'A perfect crystalline structure of sacred geometry',
            'interactions': ['pattern_matching', 'crystal_focus', 'geometric_alignment']
        },
        # Add other form descriptions...
    }
    return descriptions.get(form, {'name': 'Unknown', 'description': 'Undefined form'})

def expand_visual_traits(binary_data: bytes) -> Dict[str, Any]:
    """Expand binary traits into full visual description"""
    if len(binary_data) != TRAITS_SIZE:
        raise ValueError(f"Invalid traits data size: {len(binary_data)}")
        
    if binary_data[0:4] != HEADER_VERSION:
        raise ValueError(f"Invalid traits version")
        
    traits = {
        'form': expand_form_type(binary_data[4]),
        'color': ColorScheme(binary_data[5] & 0x7).name,
        'geometry': {
            'patterns': [p.name for p in GeometryPattern if binary_data[6] & p.value],
            'complexity': bin(binary_data[6]).count('1')  # Number of active patterns
        },
        'environment': EnvironmentalEffect.from_byte(binary_data[7]).__dict__,
        'time_variations': binary_data[8],
        'energy_signature': binary_data[9],
        'symbol_set': binary_data[10],
        'light_shadow': binary_data[11],
        'special_properties': list(binary_data[12:16])
    }
    
    return traits

def verify_traits(binary_data: bytes, governor_name: str, aethyr: int, element: str) -> bool:
    """Verify traits were generated correctly"""
    aethyr_name = get_aethyr_name(aethyr)
    expected = generate_visual_traits(governor_name, aethyr_name, element)
    return binary_data == expected 

class VisualAspectBatchProcessor(UnifiedBatchProcessor):
    """Batch processor for visual aspects using Bitcoin L1 optimization"""
    
    async def _process_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single governor's visual aspects"""
        try:
            # Extract and validate required fields
            governor_name = cast(str, item.get('name'))
            aethyr_num = cast(int, item.get('aethyr'))
            element = cast(str, item.get('element'))
            
            if not isinstance(governor_name, str):
                raise ValueError("governor_name must be a string")
            if not isinstance(aethyr_num, int):
                raise ValueError("aethyr must be an integer")
            if not isinstance(element, str):
                raise ValueError("element must be a string")
            
            # Convert aethyr number to name
            aethyr_name = get_aethyr_name(aethyr_num)
            
            # Generate visual traits
            binary_traits = generate_visual_traits(governor_name, aethyr_name, element)
            
            # Expand for verification
            expanded = expand_visual_traits(binary_traits)
            
            # Verify generation
            if not verify_traits(binary_traits, governor_name, aethyr_num, element):
                raise ValueError("Generated traits verification failed")
            
            return {
                "governor_id": governor_name,
                "binary_traits": binary_traits.hex(),
                "expanded_traits": expanded,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "governor_id": item.get('name', 'unknown'),
                "status": "failed",
                "error": str(e)
            }

    @staticmethod
    def create_batch_config() -> BatchConfig:
        """Create optimized batch config for visual processing"""
        return BatchConfig(
            max_retries=3,
            retry_delay=1.0,
            batch_size=50,  # Optimized for visual trait generation
            timeout=30.0,
            parallel=True,
            validation_schema={
                "required": ["name", "aethyr", "element"],
                "types": {
                    "name": str,
                    "aethyr": int,
                    "element": str
                }
            }
        ) 