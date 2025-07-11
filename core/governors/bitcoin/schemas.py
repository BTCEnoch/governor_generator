"""
Bitcoin Integration Schemas

Defines data structures for Bitcoin integration including ordinal inscriptions
and state management.
"""

from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime

@dataclass
class InscriptionContent:
    """Content to be inscribed"""
    data: Dict
    mime_type: str = "application/json"
    encoding: str = "utf-8"

@dataclass
class InscriptionMetadata:
    """Metadata for an inscription"""
    content_type: str
    governor_id: Optional[str]
    block_height: int
    version: str
    timestamp: datetime
    checksum: str
    tags: List[str] = None

@dataclass
class Inscription:
    """Complete inscription data"""
    content: InscriptionContent
    metadata: InscriptionMetadata
    inscription_id: Optional[str] = None

@dataclass
class StateTransition:
    """State transition for governor profiles"""
    governor_id: str
    from_state: Dict
    to_state: Dict
    transition_type: str
    block_height: int
    proof: Optional[Dict] = None

@dataclass
class BitcoinBlock:
    """Bitcoin block data for deterministic generation"""
    height: int
    hash: str
    previous_hash: str
    timestamp: int
    merkle_root: str
    difficulty: int

@dataclass
class StateProof:
    """Proof of state validity"""
    block_height: int
    block_hash: str
    merkle_path: List[str]
    state_hash: str
    timestamp: int 