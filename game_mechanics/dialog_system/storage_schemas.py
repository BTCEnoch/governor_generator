"""
On-Chain Dialog Storage Schemas
==============================

This module defines schemas and utilities for storing dialog content on Bitcoin
as ordinal inscriptions, with compression and efficient reference systems.

Key Components:
- DialogLibrarySchema: Structure for storing governor dialog content
- InscriptionReference: Pointers to on-chain dialog data
- CompressionUtils: Utilities for compacting dialog content
- StorageManager: Interface for reading/writing dialog data
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
import json
import gzip
import base64
import hashlib
from enum import Enum

from .core_structures import DialogNode, ResponseType, IntentCategory


class CompressionType(Enum):
    """Types of compression available for dialog content."""
    NONE = "none"
    GZIP = "gzip"
    CUSTOM = "custom"


class InscriptionType(Enum):
    """Types of inscriptions for different dialog content."""
    DIALOG_LIBRARY = "dialog_library"
    GOVERNOR_PROFILE = "governor_profile"
    STORY_GRAPH = "story_graph"
    METADATA = "metadata"


@dataclass
class InscriptionReference:
    """
    Reference to dialog content stored as Bitcoin ordinal inscription.
    
    This lightweight structure allows the game to efficiently locate
    and retrieve specific pieces of dialog content from the blockchain.
    """
    inscription_id: str
    content_type: InscriptionType
    governor_id: str
    content_hash: str
    compression: CompressionType = CompressionType.GZIP
    size_bytes: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate inscription reference after initialization."""
        if not self.inscription_id:
            raise ValueError("InscriptionReference must have a non-empty inscription_id")
        if not self.governor_id:
            raise ValueError("InscriptionReference must have a non-empty governor_id")
        if not self.content_hash:
            raise ValueError("InscriptionReference must have a non-empty content_hash")
    
    def verify_content_hash(self, content: bytes) -> bool:
        """Verify that content matches the stored hash."""
        computed_hash = hashlib.sha256(content).hexdigest()
        return computed_hash == self.content_hash
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "inscription_id": self.inscription_id,
            "content_type": self.content_type.value,
            "governor_id": self.governor_id,
            "content_hash": self.content_hash,
            "compression": self.compression.value,
            "size_bytes": self.size_bytes,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InscriptionReference':
        """Create from dictionary data."""
        return cls(
            inscription_id=data["inscription_id"],
            content_type=InscriptionType(data["content_type"]),
            governor_id=data["governor_id"],
            content_hash=data["content_hash"],
            compression=CompressionType(data.get("compression", "gzip")),
            size_bytes=data.get("size_bytes", 0),
            metadata=data.get("metadata", {})
        )


@dataclass
class DialogLibrarySchema:
    """
    Schema for storing a governor's complete dialog library on-chain.
    
    This structure optimizes for compression while maintaining fast access
    to different types of dialog content and response variants.
    """
    governor_id: str
    version: str
    dialog_nodes: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    response_variants: Dict[str, List[str]] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate schema after initialization."""
        if not self.governor_id:
            raise ValueError("DialogLibrarySchema must have a non-empty governor_id")
        if not self.version:
            raise ValueError("DialogLibrarySchema must have a non-empty version")
    
    def add_dialog_node(self, node: DialogNode) -> None:
        """Add a dialog node to the library."""
        self.dialog_nodes[node.id] = {
            "content": node.content,
            "transitions": node.transitions,
            "requirements": node.requirements,
            "metadata": node.metadata
        }
    
    def get_dialog_node(self, node_id: str) -> Optional[DialogNode]:
        """Retrieve a dialog node by ID."""
        node_data = self.dialog_nodes.get(node_id)
        if not node_data:
            return None
        
        return DialogNode(
            id=node_id,
            content=node_data["content"],
            transitions=node_data["transitions"],
            requirements=node_data.get("requirements", {}),
            metadata=node_data.get("metadata", {})
        )
    
    def add_response_variants(self, response_key: str, variants: List[str]) -> None:
        """Add response variants for a specific response type."""
        self.response_variants[response_key] = variants
    
    def get_response_variants(self, response_key: str) -> List[str]:
        """Get response variants for a specific response type."""
        return self.response_variants.get(response_key, [])
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "governor_id": self.governor_id,
            "version": self.version,
            "dialog_nodes": self.dialog_nodes,
            "response_variants": self.response_variants,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DialogLibrarySchema':
        """Create from dictionary data."""
        return cls(
            governor_id=data["governor_id"],
            version=data["version"],
            dialog_nodes=data.get("dialog_nodes", {}),
            response_variants=data.get("response_variants", {}),
            metadata=data.get("metadata", {})
        )


class CompressionUtils:
    """
    Utilities for compressing and decompressing dialog content.
    
    Optimized for Bitcoin inscription storage with minimal size overhead
    while maintaining deterministic compression for consensus.
    """
    
    @staticmethod
    def compress_content(content: str, compression_type: CompressionType = CompressionType.GZIP) -> bytes:
        """
        Compress content using the specified compression type.
        
        Args:
            content: String content to compress
            compression_type: Type of compression to use
            
        Returns:
            Compressed content as bytes
        """
        content_bytes = content.encode('utf-8')
        
        if compression_type == CompressionType.NONE:
            return content_bytes
        elif compression_type == CompressionType.GZIP:
            return gzip.compress(content_bytes, compresslevel=9)
        elif compression_type == CompressionType.CUSTOM:
            # Placeholder for custom compression algorithm
            # Could implement dictionary-based compression for dialog-specific patterns
            return gzip.compress(content_bytes, compresslevel=9)
        else:
            raise ValueError(f"Unsupported compression type: {compression_type}")
    
    @staticmethod
    def decompress_content(compressed_data: bytes, compression_type: CompressionType = CompressionType.GZIP) -> str:
        """
        Decompress content using the specified compression type.
        
        Args:
            compressed_data: Compressed data as bytes
            compression_type: Type of compression used
            
        Returns:
            Decompressed content as string
        """
        if compression_type == CompressionType.NONE:
            return compressed_data.decode('utf-8')
        elif compression_type == CompressionType.GZIP:
            decompressed = gzip.decompress(compressed_data)
            return decompressed.decode('utf-8')
        elif compression_type == CompressionType.CUSTOM:
            # Placeholder for custom decompression
            decompressed = gzip.decompress(compressed_data)
            return decompressed.decode('utf-8')
        else:
            raise ValueError(f"Unsupported compression type: {compression_type}")
    
    @staticmethod
    def encode_for_inscription(data: Dict[str, Any], compression_type: CompressionType = CompressionType.GZIP) -> str:
        """
        Encode data for Bitcoin ordinal inscription.
        
        Args:
            data: Dictionary data to encode
            compression_type: Compression to apply
            
        Returns:
            Base64-encoded string ready for inscription
        """
        json_str = json.dumps(data, separators=(',', ':'), sort_keys=True)
        compressed = CompressionUtils.compress_content(json_str, compression_type)
        return base64.b64encode(compressed).decode('ascii')
    
    @staticmethod
    def decode_from_inscription(encoded_data: str, compression_type: CompressionType = CompressionType.GZIP) -> Dict[str, Any]:
        """
        Decode data from Bitcoin ordinal inscription.
        
        Args:
            encoded_data: Base64-encoded inscription data
            compression_type: Compression type used
            
        Returns:
            Decoded dictionary data
        """
        compressed_data = base64.b64decode(encoded_data.encode('ascii'))
        json_str = CompressionUtils.decompress_content(compressed_data, compression_type)
        return json.loads(json_str)


class StorageManager:
    """
    Manager for reading and writing dialog content to/from on-chain storage.
    
    Provides a clean interface for the dialog system to interact with
    Bitcoin ordinal inscriptions without handling low-level details.
    """
    
    def __init__(self):
        """Initialize storage manager."""
        self.inscription_cache: Dict[str, Any] = {}
        self.reference_index: Dict[str, InscriptionReference] = {}
    
    def store_dialog_library(self, library: DialogLibrarySchema, compression_type: CompressionType = CompressionType.GZIP) -> InscriptionReference:
        """
        Store a dialog library as an ordinal inscription.
        
        Args:
            library: Dialog library to store
            compression_type: Compression to use
            
        Returns:
            Reference to the stored inscription
        """
        # Encode library for inscription
        encoded_data = CompressionUtils.encode_for_inscription(library.to_dict(), compression_type)
        
        # Calculate content hash
        content_hash = hashlib.sha256(encoded_data.encode()).hexdigest()
        
        # In a real implementation, this would interact with Bitcoin ordinals API
        # For now, we'll simulate with a mock inscription ID
        inscription_id = f"inscription_{library.governor_id}_{content_hash[:8]}"
        
        # Create reference
        reference = InscriptionReference(
            inscription_id=inscription_id,
            content_type=InscriptionType.DIALOG_LIBRARY,
            governor_id=library.governor_id,
            content_hash=content_hash,
            compression=compression_type,
            size_bytes=len(encoded_data),
            metadata={"version": library.version}
        )
        
        # Cache the data (in real implementation, this would be on-chain)
        self.inscription_cache[inscription_id] = encoded_data
        self.reference_index[f"{library.governor_id}_dialog_library"] = reference
        
        return reference
    
    def load_dialog_library(self, governor_id: str) -> Optional[DialogLibrarySchema]:
        """
        Load a dialog library from on-chain storage.
        
        Args:
            governor_id: ID of the governor whose library to load
            
        Returns:
            Dialog library if found, None otherwise
        """
        # Get reference
        reference = self.reference_index.get(f"{governor_id}_dialog_library")
        if not reference:
            return None
        
        # Load from cache (in real implementation, would fetch from Bitcoin)
        encoded_data = self.inscription_cache.get(reference.inscription_id)
        if not encoded_data:
            return None
        
        # Verify content hash
        if not reference.verify_content_hash(encoded_data.encode()):
            raise ValueError(f"Content hash mismatch for inscription {reference.inscription_id}")
        
        # Decode and return
        library_data = CompressionUtils.decode_from_inscription(encoded_data, reference.compression)
        return DialogLibrarySchema.from_dict(library_data)
    
    def get_inscription_reference(self, governor_id: str, content_type: InscriptionType) -> Optional[InscriptionReference]:
        """Get inscription reference for specific governor and content type."""
        key = f"{governor_id}_{content_type.value}"
        return self.reference_index.get(key)
    
    def list_governor_inscriptions(self, governor_id: str) -> List[InscriptionReference]:
        """List all inscriptions for a specific governor."""
        return [ref for key, ref in self.reference_index.items() if key.startswith(f"{governor_id}_")]
    
    def clear_cache(self) -> None:
        """Clear the inscription cache."""
        self.inscription_cache.clear() 