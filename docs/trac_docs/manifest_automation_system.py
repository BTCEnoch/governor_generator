#!/usr/bin/env python3
"""
Manifest Automation System
==========================

Automated manifest management for content updates, inscription ID validation,
dependency resolution, and atomic rollback capabilities for the TRAC build system.
"""

import os
import json
import time
import logging
import hashlib
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)

class ManifestStatus(Enum):
    """Status of manifest operations"""
    PENDING = "pending"
    VALIDATING = "validating"
    DEPLOYING = "deploying"
    ACTIVE = "active"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

class ContentType(Enum):
    """Types of content in manifests"""
    GOVERNOR_PORTRAIT = "governor_portrait"
    GOVERNOR_METADATA = "governor_metadata"
    ARTIFACT_NFT = "artifact_nft"
    GAME_LOGIC = "game_logic"
    UI_COMPONENT = "ui_component"
    EXPANSION_PACK = "expansion_pack"
    MANIFEST = "manifest"

@dataclass
class ContentItem:
    """Individual content item in manifest"""
    content_id: str
    content_type: ContentType
    inscription_id: Optional[str] = None
    file_path: str = ""
    size_bytes: int = 0
    content_hash: str = ""
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    validation_status: str = "pending"
    created_at: float = field(default_factory=time.time)
    
    @property
    def is_inscribed(self) -> bool:
        """Check if content has been inscribed"""
        return bool(self.inscription_id)
    
    @property
    def is_valid(self) -> bool:
        """Check if content passes validation"""
        return self.validation_status == "valid"

@dataclass
class ManifestVersion:
    """Version of content manifest"""
    version: str
    manifest_id: str
    status: ManifestStatus
    content_items: Dict[str, ContentItem] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    rollback_target: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    deployed_at: Optional[float] = None
    validation_results: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_deployable(self) -> bool:
        """Check if manifest version is ready for deployment"""
        return (self.status == ManifestStatus.PENDING and 
                all(item.is_valid for item in self.content_items.values()) and
                all(item.is_inscribed for item in self.content_items.values()))
    
    @property
    def total_size_bytes(self) -> int:
        """Get total size of all content items"""
        return sum(item.size_bytes for item in self.content_items.values())

class ManifestAutomationEngine:
    """
    Core engine for automated manifest management.
    
    Handles manifest patching, inscription ID validation, dependency resolution,
    and atomic rollback operations for the TRAC build system.
    """
    
    def __init__(self, manifest_dir: Path, backup_dir: Path):
        """
        Initialize manifest automation engine.
        
        Args:
            manifest_dir: Directory containing manifest files
            backup_dir: Directory for manifest backups
        """
        self.manifest_dir = Path(manifest_dir)
        self.backup_dir = Path(backup_dir)
        
        # Ensure directories exist
        self.manifest_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # State tracking
        self.manifest_versions: Dict[str, ManifestVersion] = {}
        self.active_version: Optional[str] = None
        self.rollback_history: List[Dict[str, Any]] = []
        
        # Validation rules
        self.validation_rules = self._load_validation_rules()
        
        # Load existing manifests
        self._load_existing_manifests()
        
        logger.info(f"ManifestAutomationEngine initialized with {len(self.manifest_versions)} versions")
    
    def _load_validation_rules(self) -> Dict[str, Any]:
        """Load content validation rules"""
        return {
            "max_file_size": {
                ContentType.GOVERNOR_PORTRAIT: 100 * 1024,  # 100KB
                ContentType.GOVERNOR_METADATA: 50 * 1024,   # 50KB
                ContentType.ARTIFACT_NFT: 75 * 1024,        # 75KB
                ContentType.GAME_LOGIC: 500 * 1024,         # 500KB
                ContentType.UI_COMPONENT: 200 * 1024,       # 200KB
                ContentType.EXPANSION_PACK: 1024 * 1024,    # 1MB
                ContentType.MANIFEST: 10 * 1024             # 10KB
            },
            "required_metadata": {
                ContentType.GOVERNOR_PORTRAIT: ["governor_name", "aethyr", "region"],
                ContentType.ARTIFACT_NFT: ["name", "rarity", "category"],
                ContentType.EXPANSION_PACK: ["name", "version", "dependencies"]
            },
            "allowed_extensions": {
                ContentType.GOVERNOR_PORTRAIT: [".webp", ".png", ".jpg"],
                ContentType.GOVERNOR_METADATA: [".json"],
                ContentType.ARTIFACT_NFT: [".webp", ".png", ".svg"],
                ContentType.GAME_LOGIC: [".js", ".wasm"],
                ContentType.UI_COMPONENT: [".js", ".css", ".html"],
                ContentType.EXPANSION_PACK: [".zip", ".tar.gz"],
                ContentType.MANIFEST: [".json"]
            }
        }
    
    def _load_existing_manifests(self) -> None:
        """Load existing manifest versions from disk"""
        try:
            manifest_files = list(self.manifest_dir.glob("manifest_*.json"))
            
            for manifest_file in manifest_files:
                try:
                    with open(manifest_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # TODO: Implement deserialization in next chunk
                    # version = self._deserialize_manifest_version(data)
                    # self.manifest_versions[version.version] = version
                    # if version.status == ManifestStatus.ACTIVE:
                    #     self.active_version = version.version
                    pass
                        
                except Exception as e:
                    logger.error(f"Failed to load manifest {manifest_file}: {e}")
                    
            logger.info(f"Loaded {len(self.manifest_versions)} existing manifest versions")
            
        except Exception as e:
            logger.error(f"Failed to load existing manifests: {e}")
    
    def create_manifest_version(self, version_name: str, content_items: List[Dict[str, Any]]) -> ManifestVersion:
        """
        Create a new manifest version with content items.
        
        Args:
            version_name: Unique version identifier
            content_items: List of content item dictionaries
            
        Returns:
            Created manifest version
        """
        if version_name in self.manifest_versions:
            raise ValueError(f"Manifest version {version_name} already exists")
        
        manifest_id = self._generate_manifest_id(version_name)
        
        # Create manifest version
        manifest = ManifestVersion(
            version=version_name,
            manifest_id=manifest_id,
            status=ManifestStatus.PENDING
        )
        
        # Add content items
        for item_data in content_items:
            content_item = self._create_content_item(item_data)
            manifest.content_items[content_item.content_id] = content_item
        
        # Validate dependencies
        self._resolve_dependencies(manifest)
        
        # Store manifest
        self.manifest_versions[version_name] = manifest
        self._save_manifest_version(manifest)
        
        logger.info(f"Created manifest version {version_name} with {len(content_items)} items")
        return manifest
    
    def validate_content_item(self, content_item: ContentItem) -> Tuple[bool, List[str]]:
        """
        Validate a content item against rules.
        
        Args:
            content_item: Content item to validate
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Check file exists
        if content_item.file_path and not Path(content_item.file_path).exists():
            errors.append(f"File not found: {content_item.file_path}")
        
        # Check file size
        if content_item.file_path:
            file_size = Path(content_item.file_path).stat().st_size
            max_size = self.validation_rules["max_file_size"].get(content_item.content_type, 0)
            
            if file_size > max_size:
                errors.append(f"File too large: {file_size} bytes > {max_size} bytes")
            
            # Update content item size
            content_item.size_bytes = file_size
        
        # Check file extension
        if content_item.file_path:
            file_ext = Path(content_item.file_path).suffix.lower()
            allowed_exts = self.validation_rules["allowed_extensions"].get(content_item.content_type, [])
            
            if allowed_exts and file_ext not in allowed_exts:
                errors.append(f"Invalid extension {file_ext}, allowed: {allowed_exts}")
        
        # Check required metadata
        required_meta = self.validation_rules["required_metadata"].get(content_item.content_type, [])
        for field in required_meta:
            if field not in content_item.metadata:
                errors.append(f"Missing required metadata field: {field}")
        
        # Calculate content hash
        if content_item.file_path and Path(content_item.file_path).exists():
            content_item.content_hash = self._calculate_file_hash(content_item.file_path)
        
        # Update validation status
        is_valid = len(errors) == 0
        content_item.validation_status = "valid" if is_valid else "invalid"
        
        return is_valid, errors
    
    def validate_inscription_id(self, inscription_id: str, content_item: ContentItem) -> bool:
        """
        Validate an inscription ID for a content item.
        
        Args:
            inscription_id: Bitcoin inscription ID to validate
            content_item: Associated content item
            
        Returns:
            True if valid inscription ID
        """
        # Basic inscription ID format validation
        if not inscription_id or len(inscription_id) < 64:
            return False
        
        # Check for valid hex characters (simplified validation)
        try:
            int(inscription_id[:64], 16)
        except ValueError:
            return False
        
        # TODO: Add Bitcoin network inscription ID verification
        # This would involve checking against Bitcoin Core or Ordinal indexer
        
        return True
    
    def patch_manifest_content(self, version_name: str, content_updates: Dict[str, Any]) -> bool:
        """
        Apply content patches to a manifest version.
        
        Args:
            version_name: Target manifest version
            content_updates: Dictionary of content ID -> update data
            
        Returns:
            True if patches applied successfully
        """
        if version_name not in self.manifest_versions:
            logger.error(f"Manifest version {version_name} not found")
            return False
        
        manifest = self.manifest_versions[version_name]
        
        if manifest.status != ManifestStatus.PENDING:
            logger.error(f"Cannot patch manifest {version_name} with status {manifest.status}")
            return False
        
        try:
            # Create backup before patching
            self._create_manifest_backup(manifest)
            
            # Apply patches
            for content_id, updates in content_updates.items():
                if content_id not in manifest.content_items:
                    logger.warning(f"Content item {content_id} not found in manifest")
                    continue
                
                content_item = manifest.content_items[content_id]
                
                # Apply updates
                for field, value in updates.items():
                    if hasattr(content_item, field):
                        setattr(content_item, field, value)
                    elif field == "metadata":
                        content_item.metadata.update(value)
                    else:
                        logger.warning(f"Unknown field {field} for content item")
                
                # Re-validate patched content
                is_valid, errors = self.validate_content_item(content_item)
                if not is_valid:
                    logger.error(f"Patched content {content_id} failed validation: {errors}")
                    return False
            
            # Re-resolve dependencies after patching
            self._resolve_dependencies(manifest)
            
            # Save updated manifest
            self._save_manifest_version(manifest)
            
            logger.info(f"Successfully patched {len(content_updates)} items in manifest {version_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to patch manifest {version_name}: {e}")
            return False
    
    def _generate_manifest_id(self, version_name: str) -> str:
        """Generate unique manifest ID"""
        timestamp = str(int(time.time()))
        content = f"{version_name}_{timestamp}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def _create_content_item(self, item_data: Dict[str, Any]) -> ContentItem:
        """Create content item from data dictionary"""
        content_type = ContentType(item_data.get("content_type", "ui_component"))
        
        return ContentItem(
            content_id=item_data.get("content_id", f"item_{int(time.time())}"),
            content_type=content_type,
            inscription_id=item_data.get("inscription_id"),
            file_path=item_data.get("file_path", ""),
            size_bytes=item_data.get("size_bytes", 0),
            content_hash=item_data.get("content_hash", ""),
            dependencies=item_data.get("dependencies", []),
            metadata=item_data.get("metadata", {}),
            validation_status=item_data.get("validation_status", "pending")
        )
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of file"""
        try:
            with open(file_path, 'rb') as f:
                file_hash = hashlib.sha256()
                for chunk in iter(lambda: f.read(4096), b""):
                    file_hash.update(chunk)
                return file_hash.hexdigest()
        except Exception as e:
            logger.error(f"Failed to calculate hash for {file_path}: {e}")
            return ""
    
    def _resolve_dependencies(self, manifest: ManifestVersion) -> None:
        """Resolve and validate content dependencies"""
        # Build dependency graph
        dependency_graph = {}
        for content_id, item in manifest.content_items.items():
            dependency_graph[content_id] = item.dependencies
        
        # Check for circular dependencies
        visited = set()
        rec_stack = set()
        
        def has_cycle(node):
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in dependency_graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        # Check all nodes for cycles
        for node in dependency_graph:
            if node not in visited:
                if has_cycle(node):
                    raise ValueError(f"Circular dependency detected involving {node}")
        
        # Topological sort for deployment order
        manifest.dependencies = self._topological_sort(dependency_graph)
    
    def _topological_sort(self, graph: Dict[str, List[str]]) -> List[str]:
        """Perform topological sort on dependency graph"""
        in_degree = {node: 0 for node in graph}
        
        # Calculate in-degrees
        for node in graph:
            for neighbor in graph[node]:
                if neighbor in in_degree:
                    in_degree[neighbor] += 1
        
        # Queue nodes with no dependencies
        queue = [node for node in in_degree if in_degree[node] == 0]
        result = []
        
        while queue:
            node = queue.pop(0)
            result.append(node)
            
            # Reduce in-degree for neighbors
            for neighbor in graph.get(node, []):
                if neighbor in in_degree:
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        queue.append(neighbor)
        
        return result
    
    def _save_manifest_version(self, manifest: ManifestVersion) -> None:
        """Save manifest version to disk"""
        try:
            manifest_file = self.manifest_dir / f"manifest_{manifest.version}.json"
            data = self._serialize_manifest_version(manifest)
            
            with open(manifest_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Saved manifest {manifest.version} to {manifest_file}")
            
        except Exception as e:
            logger.error(f"Failed to save manifest {manifest.version}: {e}")
    
    def _serialize_manifest_version(self, manifest: ManifestVersion) -> Dict[str, Any]:
        """Serialize manifest version to dictionary"""
        return {
            "version": manifest.version,
            "manifest_id": manifest.manifest_id,
            "status": manifest.status.value,
            "created_at": manifest.created_at,
            "deployed_at": manifest.deployed_at,
            "rollback_target": manifest.rollback_target,
            "dependencies": manifest.dependencies,
            "validation_results": manifest.validation_results,
            "content_items": {
                content_id: {
                    "content_id": item.content_id,
                    "content_type": item.content_type.value,
                    "inscription_id": item.inscription_id,
                    "file_path": item.file_path,
                    "size_bytes": item.size_bytes,
                    "content_hash": item.content_hash,
                    "dependencies": item.dependencies,
                    "metadata": item.metadata,
                    "validation_status": item.validation_status,
                    "created_at": item.created_at
                }
                for content_id, item in manifest.content_items.items()
            }
        }
    
    def _create_manifest_backup(self, manifest: ManifestVersion) -> None:
        """Create backup of manifest before modifications"""
        try:
            timestamp = int(time.time())
            backup_file = self.backup_dir / f"manifest_{manifest.version}_backup_{timestamp}.json"
            
            data = self._serialize_manifest_version(manifest)
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Created backup: {backup_file}")
            
        except Exception as e:
            logger.error(f"Failed to create backup for {manifest.version}: {e}")
    
    def deploy_manifest_version(self, version_name: str) -> bool:
        """
        Deploy a manifest version atomically.
        
        Args:
            version_name: Version to deploy
            
        Returns:
            True if deployment successful
        """
        if version_name not in self.manifest_versions:
            logger.error(f"Manifest version {version_name} not found")
            return False
        
        manifest = self.manifest_versions[version_name]
        
        if not manifest.is_deployable:
            logger.error(f"Manifest {version_name} is not deployable")
            return False
        
        try:
            # Set deploying status
            manifest.status = ManifestStatus.DEPLOYING
            self._save_manifest_version(manifest)
            
            # Validate all content before deployment
            validation_passed = True
            for content_id, item in manifest.content_items.items():
                is_valid, errors = self.validate_content_item(item)
                if not is_valid:
                    logger.error(f"Content {content_id} failed validation: {errors}")
                    validation_passed = False
            
            if not validation_passed:
                manifest.status = ManifestStatus.FAILED
                self._save_manifest_version(manifest)
                return False
            
            # Mark old active version for rollback
            if self.active_version:
                old_manifest = self.manifest_versions[self.active_version]
                old_manifest.status = ManifestStatus.PENDING
                manifest.rollback_target = self.active_version
            
            # Deploy content in dependency order
            for content_id in manifest.dependencies:
                if content_id in manifest.content_items:
                    item = manifest.content_items[content_id]
                    success = self._deploy_content_item(item)
                    if not success:
                        logger.error(f"Failed to deploy content {content_id}")
                        self._rollback_deployment(manifest)
                        return False
            
            # Mark as active
            manifest.status = ManifestStatus.ACTIVE
            manifest.deployed_at = time.time()
            self.active_version = version_name
            
            # Save final state
            self._save_manifest_version(manifest)
            
            # Record deployment
            self.rollback_history.append({
                "timestamp": time.time(),
                "action": "deploy",
                "version": version_name,
                "previous_version": manifest.rollback_target
            })
            
            logger.info(f"Successfully deployed manifest version {version_name}")
            return True
            
        except Exception as e:
            logger.error(f"Deployment failed for {version_name}: {e}")
            self._rollback_deployment(manifest)
            return False
    
    def rollback_to_version(self, target_version: Optional[str] = None) -> bool:
        """
        Rollback to a previous manifest version.
        
        Args:
            target_version: Version to rollback to, or None for automatic rollback
            
        Returns:
            True if rollback successful
        """
        if not self.active_version:
            logger.error("No active version to rollback from")
            return False
        
        current_manifest = self.manifest_versions[self.active_version]
        
        # Determine rollback target
        if target_version is None:
            target_version = current_manifest.rollback_target
        
        if not target_version or target_version not in self.manifest_versions:
            logger.error(f"Invalid rollback target: {target_version}")
            return False
        
        target_manifest = self.manifest_versions[target_version]
        
        try:
            logger.info(f"Rolling back from {self.active_version} to {target_version}")
            
            # Mark current as rolled back
            current_manifest.status = ManifestStatus.ROLLED_BACK
            
            # Reactivate target version
            target_manifest.status = ManifestStatus.ACTIVE
            self.active_version = target_version
            
            # Save states
            self._save_manifest_version(current_manifest)
            self._save_manifest_version(target_manifest)
            
            # Record rollback
            self.rollback_history.append({
                "timestamp": time.time(),
                "action": "rollback",
                "from_version": current_manifest.version,
                "to_version": target_version,
                "reason": "manual_rollback"
            })
            
            logger.info(f"Successfully rolled back to version {target_version}")
            return True
            
        except Exception as e:
            logger.error(f"Rollback failed: {e}")
            return False
    
    def _deploy_content_item(self, item: ContentItem) -> bool:
        """
        Deploy individual content item.
        
        Args:
            item: Content item to deploy
            
        Returns:
            True if deployment successful
        """
        try:
            # Simulate deployment process
            # In real implementation, this would:
            # 1. Upload content to Bitcoin network (if not inscribed)
            # 2. Wait for inscription confirmation
            # 3. Update inscription ID
            # 4. Propagate to TRAC P2P network
            
            logger.info(f"Deploying content item {item.content_id} ({item.content_type.value})")
            
            # Simulate inscription if needed
            if not item.inscription_id:
                # Generate mock inscription ID for testing
                content_for_id = f"{item.content_id}_{item.content_hash}_{time.time()}"
                mock_inscription_id = hashlib.sha256(content_for_id.encode()).hexdigest()
                item.inscription_id = mock_inscription_id
                logger.info(f"Mock inscription ID: {mock_inscription_id}")
            
            # Validate inscription ID
            if not self.validate_inscription_id(item.inscription_id, item):
                logger.error(f"Invalid inscription ID for {item.content_id}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to deploy content item {item.content_id}: {e}")
            return False
    
    def _rollback_deployment(self, manifest: ManifestVersion) -> None:
        """Rollback a failed deployment"""
        try:
            manifest.status = ManifestStatus.FAILED
            self._save_manifest_version(manifest)
            
            # Restore previous active version if available
            if manifest.rollback_target and manifest.rollback_target in self.manifest_versions:
                previous_manifest = self.manifest_versions[manifest.rollback_target]
                previous_manifest.status = ManifestStatus.ACTIVE
                self.active_version = manifest.rollback_target
                self._save_manifest_version(previous_manifest)
                
                logger.info(f"Restored previous version {manifest.rollback_target}")
            
        except Exception as e:
            logger.error(f"Failed to rollback deployment: {e}")
    
    def get_deployment_status(self) -> Dict[str, Any]:
        """Get current deployment status"""
        return {
            "active_version": self.active_version,
            "total_versions": len(self.manifest_versions),
            "version_statuses": {
                version: manifest.status.value 
                for version, manifest in self.manifest_versions.items()
            },
            "rollback_history": self.rollback_history[-10:],  # Last 10 operations
            "deployable_versions": [
                version for version, manifest in self.manifest_versions.items()
                if manifest.is_deployable
            ]
        } 