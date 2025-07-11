"""
Base Mystical System Utilities
Common functionality for all mystical systems
"""

import logging
from typing import Any, Dict, List, Optional, TypeVar, Generic
from dataclasses import dataclass, field
from pathlib import Path
from ..data.validation import ValidationResult

logger = logging.getLogger(__name__)

T = TypeVar('T')

@dataclass
class MysticalAttribute:
    """Base class for mystical attributes"""
    name: str
    value: Any
    description: Optional[str] = None
    correspondences: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MysticalEntity:
    """Base class for mystical entities"""
    id: str
    name: str
    attributes: List[MysticalAttribute] = field(default_factory=list)
    relationships: Dict[str, List[str]] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

class MysticalSystem:
    """Base class for mystical systems"""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self.logger = logging.getLogger(f"mystical.{name}")
        
    def validate_input(self, data: Any) -> ValidationResult:
        """
        Validate input data for the mystical system
        
        Args:
            data: Input data to validate
            
        Returns:
            ValidationResult with validation status and errors
        """
        raise NotImplementedError("Subclasses must implement validate_input")
        
    def format_output(self, result: Any) -> Any:
        """
        Format output data from the mystical system
        
        Args:
            result: Raw output data
            
        Returns:
            Formatted output data
        """
        raise NotImplementedError("Subclasses must implement format_output")
        
    def calculate_correspondences(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate mystical correspondences
        
        Args:
            data: Input data
            
        Returns:
            Dictionary of calculated correspondences
        """
        raise NotImplementedError("Subclasses must implement calculate_correspondences")

class BitcoinMysticalSystem(MysticalSystem):
    """Base class for Bitcoin-integrated mystical systems"""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(name, config)
        self.ordinal_data: Dict[str, Any] = {}
        self.inscription_data: Dict[str, Any] = {}
        
    def generate_deterministic_seed(self, txid: str) -> bytes:
        """
        Generate a deterministic seed from a Bitcoin transaction ID
        
        Args:
            txid: Bitcoin transaction ID
            
        Returns:
            Deterministic seed bytes
        """
        import hashlib
        return hashlib.sha256(txid.encode()).digest()
        
    def derive_mystical_attributes(self, txid: str) -> List[MysticalAttribute]:
        """
        Derive mystical attributes from Bitcoin transaction data
        
        Args:
            txid: Bitcoin transaction ID
            
        Returns:
            List of derived mystical attributes
        """
        seed = self.generate_deterministic_seed(txid)
        
        # Use different parts of the seed for various attributes
        resonance = int.from_bytes(seed[:4], 'big')
        harmony = int.from_bytes(seed[4:8], 'big')
        elemental = int.from_bytes(seed[8:12], 'big')
        celestial = int.from_bytes(seed[12:16], 'big')
        temporal = int.from_bytes(seed[16:20], 'big')
        
        # Calculate elemental affinity (Fire, Water, Air, Earth)
        elements = ["fire", "water", "air", "earth"]
        element_idx = elemental % len(elements)
        element_strength = (elemental % 100) / 100.0
        
        # Calculate celestial influence (Sun, Moon, Stars)
        celestials = ["solar", "lunar", "stellar"]
        celestial_idx = celestial % len(celestials)
        celestial_strength = (celestial % 100) / 100.0
        
        # Calculate temporal cycle (Dawn, Noon, Dusk, Night)
        cycles = ["dawn", "noon", "dusk", "night"]
        cycle_idx = temporal % len(cycles)
        cycle_strength = (temporal % 100) / 100.0
        
        return [
            MysticalAttribute(
                name="bitcoin_resonance",
                value=resonance,
                description="Primary mystical resonance derived from Bitcoin transaction",
                correspondences={
                    "vibrational_frequency": resonance % 144,  # Significant number in mystical traditions
                    "harmonic_pattern": format(resonance, 'b')[-8:],  # Last 8 bits as binary pattern
                    "numerological_sum": sum(int(x) for x in str(resonance)[-4:])  # Sum of last 4 digits
                }
            ),
            MysticalAttribute(
                name="chain_harmony",
                value=harmony,
                description="Secondary mystical harmony derived from Bitcoin transaction",
                correspondences={
                    "harmonic_ratio": (harmony % 100) / 100.0,
                    "resonance_pattern": [int(x) for x in format(harmony, 'b')[-7:]],  # 7-bit pattern
                    "cyclic_position": harmony % 28  # 28-day lunar cycle position
                }
            ),
            MysticalAttribute(
                name="elemental_affinity",
                value=elements[element_idx],
                description=f"Elemental affinity derived from Bitcoin transaction",
                correspondences={
                    "element": elements[element_idx],
                    "strength": element_strength,
                    "polarity": "active" if element_idx in [0, 2] else "passive",
                    "quality": "hot" if element_idx < 2 else "cold"
                }
            ),
            MysticalAttribute(
                name="celestial_influence",
                value=celestials[celestial_idx],
                description=f"Celestial influence derived from Bitcoin transaction",
                correspondences={
                    "body": celestials[celestial_idx],
                    "strength": celestial_strength,
                    "phase": celestial % 8,  # 8 phases
                    "aspect": celestial % 12  # 12 zodiacal aspects
                }
            ),
            MysticalAttribute(
                name="temporal_cycle",
                value=cycles[cycle_idx],
                description=f"Temporal cycle position derived from Bitcoin transaction",
                correspondences={
                    "cycle": cycles[cycle_idx],
                    "strength": cycle_strength,
                    "hour": temporal % 24,  # 24-hour cycle
                    "day": temporal % 7  # 7-day cycle
                }
            )
        ]
        
    def bind_to_ordinal(self, ordinal_id: str) -> None:
        """
        Bind mystical system to a Bitcoin Ordinal
        
        Args:
            ordinal_id: Ordinal inscription ID
        """
        from core.governors.bitcoin.ordinals import get_ordinal_data
        self.ordinal_data = get_ordinal_data(ordinal_id)
        
        # Add mystical interpretations of ordinal data
        if self.ordinal_data:
            sat_number = self.ordinal_data.get("sat", 0)
            self.ordinal_data["mystical_properties"] = {
                "sat_degree": sat_number % 360,  # Astrological degree
                "sat_cycle": sat_number % 28,  # Lunar cycle day
                "sat_element": ["fire", "earth", "air", "water"][sat_number % 4],
                "sat_quality": ["cardinal", "fixed", "mutable"][sat_number % 3],
                "sat_resonance": format(sat_number, 'b')[-12:],  # Binary pattern
                "sat_harmonic": sat_number % 22  # Major Arcana correspondence
            }
        
    def bind_to_inscription(self, inscription_id: str) -> None:
        """
        Bind mystical system to a Bitcoin inscription
        
        Args:
            inscription_id: Inscription ID
        """
        from core.governors.bitcoin.inscriptions import get_inscription_data
        self.inscription_data = get_inscription_data(inscription_id)
        
        # Add mystical interpretations of inscription data
        if self.inscription_data:
            insc_number = self.inscription_data.get("number", 0)
            self.inscription_data["mystical_properties"] = {
                "inscription_phase": insc_number % 8,  # 8 phases
                "inscription_element": ["fire", "earth", "air", "water"][insc_number % 4],
                "inscription_planet": ["sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"][insc_number % 7],
                "inscription_path": insc_number % 22,  # 22 paths on Tree of Life
                "inscription_pattern": format(insc_number, 'b')[-7:],  # Binary pattern
                "inscription_seal": insc_number % 49  # 7x7 mystical seal
            }
            
    def calculate_bitcoin_influence(self, txid: str, base_score: float) -> float:
        """
        Calculate Bitcoin's influence on a base mystical score
        
        Args:
            txid: Bitcoin transaction ID
            base_score: Original score to be influenced (0.0 to 1.0)
            
        Returns:
            Modified score (0.0 to 1.0)
        """
        seed = self.generate_deterministic_seed(txid)
        influence = int.from_bytes(seed[:4], 'big') / (2**32)  # 0.0 to 1.0
        
        # Blend original score with Bitcoin influence
        # Use golden ratio (φ ≈ 0.618) for aesthetic balance
        golden_ratio = 0.618033988749895
        bitcoin_weight = golden_ratio
        original_weight = 1.0 - golden_ratio
        
        return min(1.0, (base_score * original_weight) + (influence * bitcoin_weight))
        
    def get_bitcoin_correspondences(self, txid: str) -> Dict[str, Any]:
        """
        Get comprehensive Bitcoin-derived mystical correspondences
        
        Args:
            txid: Bitcoin transaction ID
            
        Returns:
            Dictionary of mystical correspondences
        """
        attributes = self.derive_mystical_attributes(txid)
        
        # Organize attributes into a structured correspondence system
        correspondences = {
            "resonance": {
                "primary": attributes[0].value,
                "secondary": attributes[1].value,
                "patterns": {
                    "vibrational": attributes[0].correspondences["vibrational_frequency"],
                    "harmonic": attributes[0].correspondences["harmonic_pattern"],
                    "numerological": attributes[0].correspondences["numerological_sum"]
                }
            },
            "elements": {
                "primary": attributes[2].value,
                "strength": attributes[2].correspondences["strength"],
                "polarity": attributes[2].correspondences["polarity"],
                "quality": attributes[2].correspondences["quality"]
            },
            "celestial": {
                "body": attributes[3].value,
                "strength": attributes[3].correspondences["strength"],
                "phase": attributes[3].correspondences["phase"],
                "aspect": attributes[3].correspondences["aspect"]
            },
            "temporal": {
                "cycle": attributes[4].value,
                "strength": attributes[4].correspondences["strength"],
                "hour": attributes[4].correspondences["hour"],
                "day": attributes[4].correspondences["day"]
            }
        }
        
        # Add ordinal correspondences if available
        if self.ordinal_data:
            correspondences["ordinal"] = self.ordinal_data.get("mystical_properties", {})
            
        # Add inscription correspondences if available
        if self.inscription_data:
            correspondences["inscription"] = self.inscription_data.get("mystical_properties", {})
            
        return correspondences

class MysticalSystemRegistry:
    """Registry for mystical systems"""
    
    def __init__(self):
        self._systems: Dict[str, MysticalSystem] = {}
        self.logger = logging.getLogger(f"{__name__}.registry")
        
    def register(self, system: MysticalSystem) -> None:
        """Register a mystical system"""
        self.logger.info(f"Registering mystical system: {system.name}")
        self._systems[system.name] = system
        
    def get_system(self, name: str) -> Optional[MysticalSystem]:
        """Get a registered mystical system by name"""
        return self._systems.get(name)
        
    def list_systems(self) -> List[str]:
        """List all registered mystical systems"""
        return list(self._systems.keys()) 