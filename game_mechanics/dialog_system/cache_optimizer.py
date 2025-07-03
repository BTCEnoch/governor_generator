"""
Cache Optimizer for Governor Dialog System
==========================================

This module implements advanced caching and optimization strategies for the
Governor Preferences System to maximize performance in production environments.

Key Components:
- AdvancedCache: Multi-level caching with intelligent eviction
- PreferenceOptimizer: Performance optimization for preference operations
- MemoryManager: Memory usage optimization and monitoring
"""

import time
import logging
import threading
import hashlib
import pickle
import gzip
import re
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple, Callable
from dataclasses import dataclass, field
from collections import OrderedDict
from enum import Enum

from .preference_structures import GovernorPreferences, PreferenceEncoding
from .core_structures import GovernorProfile

logger = logging.getLogger(__name__)


class CacheLevel(Enum):
    """Cache level priorities for multi-level caching"""
    L1_MEMORY = "l1_memory"        # Fast in-memory cache
    L2_COMPRESSED = "l2_compressed" # Compressed memory cache
    L3_PERSISTENT = "l3_persistent" # Persistent disk cache


@dataclass
class CacheEntry:
    """Single cache entry with metadata"""
    key: str
    data: Any
    timestamp: float
    access_count: int = 0
    last_access: float = field(default_factory=time.time)
    cache_level: CacheLevel = CacheLevel.L1_MEMORY
    compressed_size: int = 0
    
    def __post_init__(self):
        """Update access metadata"""
        self.access_count += 1
        self.last_access = time.time()


class L3StorageManager:
    """
    Persistent storage manager for L3 cache level.
    
    Provides disk-based caching with compression and integrity verification.
    """
    
    def __init__(self, storage_dir: str = "cache_storage"):
        """Initialize L3 storage manager"""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.compression_level = 6  # Balanced compression
        logger.info(f"L3StorageManager initialized: {self.storage_dir}")
    
    def save_to_persistent_cache(self, key: str, data: Any) -> bool:
        """
        Save data to persistent storage.
        
        Args:
            key: Cache key
            data: Data to save
            
        Returns:
            True if saved successfully
        """
        try:
            # Create safe filename from key
            safe_filename = self._create_safe_filename(key)
            file_path = self.storage_dir / f"{safe_filename}.cache"
            
            # Serialize and compress data
            serialized_data = pickle.dumps(data)
            compressed_data = gzip.compress(serialized_data, self.compression_level)
            
            # Write to file with metadata
            cache_data = {
                'key': key,
                'data': compressed_data,
                'timestamp': time.time(),
                'checksum': hashlib.md5(compressed_data).hexdigest()
            }
            
            with open(file_path, 'wb') as f:
                pickle.dump(cache_data, f)
            
            logger.debug(f"Saved to L3 cache: {key} -> {file_path}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to save to L3 cache: {key}, error: {e}")
            return False
    
    def load_from_persistent_cache(self, key: str) -> Optional[Any]:
        """
        Load data from persistent storage.
        
        Args:
            key: Cache key to load
            
        Returns:
            Cached data if found and valid, None otherwise
        """
        try:
            safe_filename = self._create_safe_filename(key)
            file_path = self.storage_dir / f"{safe_filename}.cache"
            
            if not file_path.exists():
                return None
            
            # Load cache data
            with open(file_path, 'rb') as f:
                cache_data = pickle.load(f)
            
            # Verify integrity
            if not self._verify_cache_integrity(cache_data):
                logger.warning(f"L3 cache corruption detected for key: {key}")
                file_path.unlink()  # Remove corrupted file
                return None
            
            # Check if expired (24 hours for L3)
            if time.time() - cache_data['timestamp'] > 86400:
                logger.debug(f"L3 cache expired for key: {key}")
                file_path.unlink()  # Remove expired file
                return None
            
            # Decompress and deserialize
            compressed_data = cache_data['data']
            serialized_data = gzip.decompress(compressed_data)
            data = pickle.loads(serialized_data)
            
            logger.debug(f"Loaded from L3 cache: {key}")
            return data
        
        except Exception as e:
            logger.error(f"Failed to load from L3 cache: {key}, error: {e}")
            return None
    
    def clear_persistent_cache(self) -> bool:
        """Clear all persistent cache files"""
        try:
            for cache_file in self.storage_dir.glob("*.cache"):
                cache_file.unlink()
            logger.info("L3 persistent cache cleared")
            return True
        except Exception as e:
            logger.error(f"Failed to clear L3 cache: {e}")
            return False
    
    def get_cache_size(self) -> int:
        """Get total size of persistent cache in bytes"""
        total_size = 0
        try:
            for cache_file in self.storage_dir.glob("*.cache"):
                total_size += cache_file.stat().st_size
        except Exception as e:
            logger.error(f"Error calculating cache size: {e}")
        return total_size
    
    def _create_safe_filename(self, key: str) -> str:
        """Create filesystem-safe filename from cache key"""
        # Hash key to ensure safe filename
        key_hash = hashlib.md5(key.encode()).hexdigest()
        # Keep first part of key for debugging, add hash for uniqueness
        safe_key = re.sub(r'[^\w\-_\.]', '_', key[:20])
        return f"{safe_key}_{key_hash}"
    
    def _verify_cache_integrity(self, cache_data: Dict[str, Any]) -> bool:
        """Verify cache data integrity using checksum"""
        if 'checksum' not in cache_data or 'data' not in cache_data:
            return False
        
        computed_checksum = hashlib.md5(cache_data['data']).hexdigest()
        return computed_checksum == cache_data['checksum']


class AdvancedCache:
    """
    Multi-level caching system with intelligent eviction policies.
    
    Implements L1 (fast memory), L2 (compressed), and L3 (persistent) caching
    with LRU eviction and performance monitoring.
    """
    
    def __init__(self, max_l1_size: int = 1000, max_l2_size: int = 5000, 
                 ttl_seconds: int = 3600):
        """Initialize advanced cache system"""
        self.max_l1_size = max_l1_size
        self.max_l2_size = max_l2_size
        self.ttl_seconds = ttl_seconds
        
        # Multi-level cache storage
        self.l1_cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self.l2_cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self.l3_cache: Dict[str, str] = {}  # file paths for persistent storage
        
        # Performance metrics
        self.cache_stats = {
            'l1_hits': 0, 'l1_misses': 0,
            'l2_hits': 0, 'l2_misses': 0,
            'l3_hits': 0, 'l3_misses': 0,
            'evictions': 0, 'compressions': 0
        }
        
        # Thread safety
        self._lock = threading.RLock()
        
        # L3 persistent storage manager
        self._l3_storage_manager = L3StorageManager()
        
        logger.info("AdvancedCache initialized with multi-level storage")
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get item from cache with automatic level promotion.
        
        Args:
            key: Cache key to retrieve
            
        Returns:
            Cached item if found, None otherwise
        """
        with self._lock:
            # Check L1 cache first (fastest)
            if key in self.l1_cache:
                entry = self.l1_cache[key]
                if self._is_valid_entry(entry):
                    self._update_access_stats(entry)
                    self.cache_stats['l1_hits'] += 1
                    # Move to end (LRU)
                    self.l1_cache.move_to_end(key)
                    logger.debug(f"L1 cache hit for key: {key}")
                    return entry.data
                else:
                    del self.l1_cache[key]
            
            # Check L2 cache (compressed memory)
            if key in self.l2_cache:
                entry = self.l2_cache[key]
                if self._is_valid_entry(entry):
                    self._update_access_stats(entry)
                    self.cache_stats['l2_hits'] += 1
                    # Promote to L1
                    self._promote_to_l1(key, entry)
                    logger.debug(f"L2 cache hit for key: {key}, promoted to L1")
                    return entry.data
                else:
                    del self.l2_cache[key]
            
            # Check L3 cache (persistent)
            if key in self.l3_cache:
                data = self._load_from_l3(key)
                if data is not None:
                    self.cache_stats['l3_hits'] += 1
                    # Promote to L1
                    self.put(key, data, promote_from_l3=True)
                    logger.debug(f"L3 cache hit for key: {key}, promoted to L1")
                    return data
                else:
                    del self.l3_cache[key]
            
            # Cache miss
            self.cache_stats['l1_misses'] += 1
            logger.debug(f"Cache miss for key: {key}")
            return None
    
    def put(self, key: str, data: Any, promote_from_l3: bool = False) -> None:
        """
        Store item in cache with automatic level management.
        
        Args:
            key: Cache key
            data: Data to cache
            promote_from_l3: Whether this is a promotion from L3
        """
        with self._lock:
            entry = CacheEntry(
                key=key,
                data=data,
                timestamp=time.time(),
                cache_level=CacheLevel.L1_MEMORY
            )
            
            # Store in L1 cache
            self.l1_cache[key] = entry
            
            # Manage L1 cache size
            if len(self.l1_cache) > self.max_l1_size:
                self._evict_from_l1()
            
            logger.debug(f"Stored in L1 cache: {key}")
    
    def clear(self, governor_id: Optional[str] = None) -> None:
        """Clear cache entries, optionally for specific governor"""
        with self._lock:
            if governor_id:
                # Clear entries for specific governor
                keys_to_remove = [k for k in self.l1_cache.keys() 
                                if k.startswith(governor_id)]
                for key in keys_to_remove:
                    del self.l1_cache[key]
                
                keys_to_remove = [k for k in self.l2_cache.keys() 
                                if k.startswith(governor_id)]
                for key in keys_to_remove:
                    del self.l2_cache[key]
                
                logger.info(f"Cleared cache for governor: {governor_id}")
            else:
                # Clear all caches
                self.l1_cache.clear()
                self.l2_cache.clear()
                self.l3_cache.clear()
                logger.info("Cleared all caches")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics"""
        with self._lock:
            total_requests = (self.cache_stats['l1_hits'] + self.cache_stats['l1_misses'])
            hit_rate = 0.0
            if total_requests > 0:
                total_hits = (self.cache_stats['l1_hits'] + 
                            self.cache_stats['l2_hits'] + 
                            self.cache_stats['l3_hits'])
                hit_rate = total_hits / total_requests
            
            return {
                'l1_size': len(self.l1_cache),
                'l2_size': len(self.l2_cache),
                'l3_size': len(self.l3_cache),
                'hit_rate': hit_rate,
                'cache_levels': self.cache_stats.copy(),
                'memory_efficiency': self._calculate_memory_efficiency()
            }
    
    def _is_valid_entry(self, entry: CacheEntry) -> bool:
        """Check if cache entry is still valid (not expired)"""
        age = time.time() - entry.timestamp
        return age < self.ttl_seconds
    
    def _update_access_stats(self, entry: CacheEntry) -> None:
        """Update access statistics for cache entry"""
        entry.access_count += 1
        entry.last_access = time.time()
    
    def _promote_to_l1(self, key: str, entry: CacheEntry) -> None:
        """Promote entry from L2 to L1 cache"""
        entry.cache_level = CacheLevel.L1_MEMORY
        self.l1_cache[key] = entry
        
        # Remove from L2
        if key in self.l2_cache:
            del self.l2_cache[key]
        
        # Manage L1 size
        if len(self.l1_cache) > self.max_l1_size:
            self._evict_from_l1()
    
    def _evict_from_l1(self) -> None:
        """Evict least recently used item from L1 to L2"""
        if not self.l1_cache:
            return
        
        # Get LRU item (first in OrderedDict)
        lru_key, lru_entry = self.l1_cache.popitem(last=False)
        
        # Move to L2 if space available
        if len(self.l2_cache) < self.max_l2_size:
            lru_entry.cache_level = CacheLevel.L2_COMPRESSED
            self.l2_cache[lru_key] = lru_entry
            logger.debug(f"Evicted {lru_key} from L1 to L2")
        else:
            # L2 is full, evict to L3 or discard
            self._evict_from_l2()
            self.l2_cache[lru_key] = lru_entry
        
        self.cache_stats['evictions'] += 1
    
    def _evict_from_l2(self) -> None:
        """Evict least recently used item from L2"""
        if not self.l2_cache:
            return
        
        # Get LRU item from L2
        lru_key, lru_entry = self.l2_cache.popitem(last=False)
        
        # Save to L3 persistent storage
        if self._l3_storage_manager.save_to_persistent_cache(lru_key, lru_entry.data):
            self.l3_cache[lru_key] = "persistent"  # Mark as stored in L3
            logger.debug(f"Evicted {lru_key} from L2 to L3 persistent storage")
        else:
            logger.debug(f"Failed to save {lru_key} to L3, discarded")
    
    def _load_from_l3(self, key: str) -> Optional[Any]:
        """Load data from L3 persistent storage"""
        return self._l3_storage_manager.load_from_persistent_cache(key)
    
    def _calculate_memory_efficiency(self) -> float:
        """Calculate memory efficiency metric"""
        if not self.l1_cache and not self.l2_cache:
            return 1.0
        
        total_entries = len(self.l1_cache) + len(self.l2_cache)
        total_accesses = sum(entry.access_count 
                           for entry in list(self.l1_cache.values()) + list(self.l2_cache.values()))
        
        if total_entries == 0:
            return 1.0
        
        return min(total_accesses / total_entries / 10.0, 1.0)  # Normalized efficiency


class PreferenceOptimizer:
    """
    Performance optimizer for governor preference operations.
    
    Implements various optimization strategies including batch processing,
    lazy loading, and intelligent precomputation of frequently accessed data.
    """
    
    def __init__(self, cache: AdvancedCache):
        """Initialize preference optimizer with cache backend"""
        self.cache = cache
        self.batch_threshold = 10  # Minimum items for batch processing
        self.precompute_patterns = set()  # Patterns for precomputation
        self.optimization_stats = {
            'batch_operations': 0,
            'cache_optimizations': 0,
            'precomputed_hits': 0,
            'lazy_loads': 0
        }
        logger.info("PreferenceOptimizer initialized")
    
    def optimize_batch_encoding(self, profiles: List[GovernorProfile], 
                              encoder_func: Callable) -> Dict[str, GovernorPreferences]:
        """
        Optimize batch encoding of multiple governor preferences.
        
        Args:
            profiles: List of governor profiles to encode
            encoder_func: Function to encode individual preferences
            
        Returns:
            Dictionary mapping governor_id to preferences
        """
        logger.info(f"Optimizing batch encoding for {len(profiles)} profiles")
        
        if len(profiles) < self.batch_threshold:
            # Not worth batch optimization, process individually
            return {p.governor_id: encoder_func(p) for p in profiles}
        
        results = {}
        
        # Group profiles by similarity for batch optimization
        trait_groups = self._group_profiles_by_traits(profiles)
        
        for trait_signature, group_profiles in trait_groups.items():
            logger.debug(f"Processing trait group '{trait_signature}' with {len(group_profiles)} profiles")
            
            # Optimize similar profiles together
            for profile in group_profiles:
                cache_key = f"preferences_{profile.governor_id}"
                
                # Check cache first
                cached_result = self.cache.get(cache_key)
                if cached_result:
                    results[profile.governor_id] = cached_result
                    continue
                
                # Encode and cache
                preferences = encoder_func(profile)
                self.cache.put(cache_key, preferences)
                results[profile.governor_id] = preferences
        
        self.optimization_stats['batch_operations'] += 1
        logger.info(f"Batch encoding completed: {len(results)} preferences generated")
        return results
    
    def optimize_trait_mapping_lookup(self, traits: List[str], 
                                    mapper_func: Callable) -> Dict[str, Any]:
        """
        Optimize trait mapping lookups with intelligent caching.
        
        Args:
            traits: List of traits to map
            mapper_func: Function to perform trait mapping
            
        Returns:
            Optimized trait mapping results
        """
        # Create cache key from sorted traits
        trait_signature = "_".join(sorted(traits))
        cache_key = f"trait_mapping_{trait_signature}"
        
        # Check cache first
        cached_result = self.cache.get(cache_key)
        if cached_result:
            self.optimization_stats['cache_optimizations'] += 1
            return cached_result
        
        # Compute and cache
        result = mapper_func(traits)
        self.cache.put(cache_key, result)
        
        logger.debug(f"Trait mapping computed and cached for: {trait_signature}")
        return result
    
    def precompute_common_patterns(self, common_trait_sets: List[List[str]], 
                                 encoder_func: Callable) -> None:
        """
        Precompute preferences for common trait combinations.
        
        Args:
            common_trait_sets: List of common trait combinations
            encoder_func: Function to encode preferences
        """
        logger.info(f"Precomputing {len(common_trait_sets)} common trait patterns")
        
        for traits in common_trait_sets:
            trait_signature = "_".join(sorted(traits))
            cache_key = f"precomputed_{trait_signature}"
            
            # Skip if already cached
            if self.cache.get(cache_key):
                continue
            
            # Create dummy profile for precomputation
            dummy_profile = GovernorProfile(
                governor_id=f"precompute_{trait_signature}",
                name="Precomputed Profile",
                traits=traits
            )
            
            # Precompute and cache
            preferences = encoder_func(dummy_profile)
            self.cache.put(cache_key, preferences)
            self.precompute_patterns.add(trait_signature)
        
        logger.info(f"Precomputation completed: {len(self.precompute_patterns)} patterns cached")
    
    def optimize_response_selection(self, variants: List[str], preferences: GovernorPreferences,
                                  selector_func: Callable, context: Dict[str, Any]) -> str:
        """
        Optimize response selection with caching and smart fallbacks.
        
        Args:
            variants: Available response variants
            preferences: Governor preferences
            selector_func: Function to select response
            context: Interaction context
            
        Returns:
            Optimized selected response
        """
        # Create cache key from variants and preferences
        variants_hash = hashlib.md5("_".join(sorted(variants)).encode()).hexdigest()[:8]
        preferences_hash = hashlib.md5(str(preferences.governor_id + 
                                         preferences.tone_preference.value).encode()).hexdigest()[:8]
        cache_key = f"response_{variants_hash}_{preferences_hash}"
        
        # Check cache
        cached_result = self.cache.get(cache_key)
        if cached_result:
            self.optimization_stats['cache_optimizations'] += 1
            return cached_result
        
        # Compute selection
        selected_response = selector_func(variants, preferences, context)
        
        # Cache if deterministic (no context-specific randomness)
        if self._is_deterministic_selection(context):
            self.cache.put(cache_key, selected_response)
        
        return selected_response
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Get optimization performance statistics"""
        cache_stats = self.cache.get_stats()
        
        return {
            'optimizer_stats': self.optimization_stats.copy(),
            'cache_performance': cache_stats,
            'precompute_patterns': len(self.precompute_patterns),
            'overall_efficiency': self._calculate_efficiency()
        }
    
    def _group_profiles_by_traits(self, profiles: List[GovernorProfile]) -> Dict[str, List[GovernorProfile]]:
        """Group profiles by trait similarity for batch optimization"""
        groups = {}
        
        for profile in profiles:
            # Create signature from sorted traits
            trait_signature = "_".join(sorted(profile.traits))
            
            if trait_signature not in groups:
                groups[trait_signature] = []
            
            groups[trait_signature].append(profile)
        
        return groups
    
    def _is_deterministic_selection(self, context: Dict[str, Any]) -> bool:
        """Check if response selection is deterministic for caching"""
        # Avoid caching if context contains non-deterministic elements
        non_deterministic_keys = ['random_seed', 'timestamp', 'session_id']
        return not any(key in context for key in non_deterministic_keys)
    
    def _calculate_efficiency(self) -> float:
        """Calculate overall optimization efficiency"""
        total_operations = sum(self.optimization_stats.values())
        if total_operations == 0:
            return 1.0
        
        cache_hits = self.optimization_stats.get('cache_optimizations', 0)
        batch_ops = self.optimization_stats.get('batch_operations', 0)
        
        efficiency = (cache_hits + batch_ops * 2) / total_operations
        return min(efficiency, 1.0)


def main():
    """Test the advanced cache system"""
    print("🧪 Testing Advanced Cache System")
    
    cache = AdvancedCache(max_l1_size=3, max_l2_size=5)
    
    # Test basic operations
    cache.put("test1", {"data": "value1"})
    cache.put("test2", {"data": "value2"})
    
    result = cache.get("test1")
    print(f"✅ Retrieved: {result}")
    
    # Test cache statistics
    stats = cache.get_stats()
    print(f"📊 Cache Stats: {stats}")
    
    # Test optimizer
    optimizer = PreferenceOptimizer(cache)
    opt_stats = optimizer.get_optimization_stats()
    print(f"🚀 Optimizer Stats: {opt_stats}")


if __name__ == "__main__":
    main() 