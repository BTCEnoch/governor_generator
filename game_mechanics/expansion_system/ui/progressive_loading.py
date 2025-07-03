#!/usr/bin/env python3
"""
Progressive Loading UI Components for Expansion System
====================================================

Provides real-time feedback for expansion loading including batch status,
queue visualization, per-category indicators, and timeout handling.
"""

import time
import logging
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class LoadingState(Enum):
    """States for expansion loading progress"""
    INITIALIZING = "initializing"
    DISCOVERING = "discovering"
    LOADING = "loading"
    RETRYING = "retrying"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


class ExpansionCategory(Enum):
    """Categories of expansions for organizational purposes"""
    ARS_GOETIA = "ars_goetia"
    ARCHANGELS = "archangels"
    ENOCHIAN_KEYS = "enochian_keys"
    WATCHTOWERS = "watchtowers"
    AETHYRS = "aethyrs"
    CUSTOM = "custom"


@dataclass
class ExpansionLoadingItem:
    """Single expansion loading item with status tracking"""
    expansion_id: str
    category: ExpansionCategory
    name: str
    inscription_id: Optional[str] = None
    state: LoadingState = LoadingState.INITIALIZING
    progress: float = 0.0  # 0.0 to 1.0
    start_time: float = field(default_factory=time.time)
    retry_count: int = 0
    error_message: Optional[str] = None
    estimated_size: int = 0  # bytes
    loaded_size: int = 0  # bytes
    
    @property
    def duration(self) -> float:
        """Get loading duration in seconds"""
        return time.time() - self.start_time
    
    @property
    def is_complete(self) -> bool:
        """Check if loading is complete (success or permanent failure)"""
        return self.state in [LoadingState.COMPLETED, LoadingState.FAILED]
    
    @property
    def needs_retry(self) -> bool:
        """Check if item needs retry"""
        return self.state in [LoadingState.FAILED, LoadingState.TIMEOUT] and self.retry_count < 3


@dataclass
class LoadingQueueStatus:
    """Overall status of the expansion loading queue"""
    total_items: int
    completed_items: int
    failed_items: int
    current_category: Optional[ExpansionCategory] = None
    current_item: Optional[str] = None
    overall_progress: float = 0.0
    estimated_time_remaining: Optional[float] = None
    
    @property
    def is_complete(self) -> bool:
        """Check if all loading is complete"""
        return self.completed_items + self.failed_items >= self.total_items


class ExpansionLoadingProgress:
    """
    Progressive loading UI component for expansion system.
    
    Provides real-time feedback for batch expansion loading with visual
    progress indicators, queue visualization, and error handling.
    """
    
    def __init__(self, 
                 update_callback: Optional[Callable[[LoadingQueueStatus], None]] = None,
                 timeout_seconds: int = 30):
        """
        Initialize expansion loading progress tracker.
        
        Args:
            update_callback: Function called on progress updates
            timeout_seconds: Timeout for individual expansion loading
        """
        self.update_callback = update_callback
        self.timeout_seconds = timeout_seconds
        
        # Loading state
        self.loading_items: Dict[str, ExpansionLoadingItem] = {}
        self.category_order: List[ExpansionCategory] = [
            ExpansionCategory.ARS_GOETIA,
            ExpansionCategory.ARCHANGELS, 
            ExpansionCategory.ENOCHIAN_KEYS,
            ExpansionCategory.WATCHTOWERS,
            ExpansionCategory.AETHYRS,
            ExpansionCategory.CUSTOM
        ]
        self.current_category_index = 0
        self.start_time = time.time()
        
        # UI state tracking
        self.ui_state = {
            'progress_percentage': 0,
            'status_message': 'Initializing expansion loading...',
            'current_category': None,
            'failed_expansions': [],
            'show_retry_button': False,
            'estimated_time': None
        }
        
        logger.info("ExpansionLoadingProgress initialized")
    
    def add_expansion(self, expansion_id: str, category: ExpansionCategory, 
                     name: str, inscription_id: Optional[str] = None,
                     estimated_size: int = 0) -> None:
        """
        Add an expansion to the loading queue.
        
        Args:
            expansion_id: Unique identifier for expansion
            category: Category of expansion
            name: Display name for expansion
            inscription_id: Bitcoin ordinal inscription ID
            estimated_size: Estimated size in bytes
        """
        item = ExpansionLoadingItem(
            expansion_id=expansion_id,
            category=category,
            name=name,
            inscription_id=inscription_id,
            estimated_size=estimated_size
        )
        
        self.loading_items[expansion_id] = item
        logger.debug(f"Added expansion to queue: {expansion_id} ({category.value})")
        
        self._update_ui_state()
    
    def start_loading_expansion(self, expansion_id: str) -> None:
        """Start loading a specific expansion"""
        if expansion_id not in self.loading_items:
            logger.warning(f"Attempted to start loading unknown expansion: {expansion_id}")
            return
        
        item = self.loading_items[expansion_id]
        item.state = LoadingState.LOADING
        item.start_time = time.time()
        
        logger.info(f"Started loading expansion: {expansion_id}")
        self._update_ui_state()
    
    def update_expansion_progress(self, expansion_id: str, progress: float, 
                                loaded_size: int = 0) -> None:
        """
        Update progress for a specific expansion.
        
        Args:
            expansion_id: Expansion being updated
            progress: Progress from 0.0 to 1.0
            loaded_size: Bytes loaded so far
        """
        if expansion_id not in self.loading_items:
            return
        
        item = self.loading_items[expansion_id]
        item.progress = max(0.0, min(1.0, progress))
        item.loaded_size = loaded_size
        
        # Check for timeout
        if item.duration > self.timeout_seconds and item.state == LoadingState.LOADING:
            self.fail_expansion(expansion_id, "Loading timeout exceeded")
            item.state = LoadingState.TIMEOUT
            return
        
        logger.debug(f"Updated progress for {expansion_id}: {progress:.1%}")
        self._update_ui_state()
    
    def complete_expansion(self, expansion_id: str) -> None:
        """Mark an expansion as successfully loaded"""
        if expansion_id not in self.loading_items:
            return
        
        item = self.loading_items[expansion_id]
        item.state = LoadingState.COMPLETED
        item.progress = 1.0
        
        logger.info(f"Completed loading expansion: {expansion_id} ({item.duration:.1f}s)")
        self._update_ui_state()
    
    def fail_expansion(self, expansion_id: str, error_message: str) -> None:
        """Mark an expansion as failed to load"""
        if expansion_id not in self.loading_items:
            return
        
        item = self.loading_items[expansion_id]
        item.state = LoadingState.FAILED
        item.error_message = error_message
        
        logger.warning(f"Failed to load expansion {expansion_id}: {error_message}")
        self._update_ui_state()
    
    def retry_expansion(self, expansion_id: str) -> bool:
        """
        Retry loading a failed expansion.
        
        Returns:
            True if retry was initiated, False if max retries exceeded
        """
        if expansion_id not in self.loading_items:
            return False
        
        item = self.loading_items[expansion_id]
        
        if item.retry_count >= 3:
            logger.warning(f"Max retries exceeded for expansion: {expansion_id}")
            return False
        
        item.retry_count += 1
        item.state = LoadingState.RETRYING
        item.progress = 0.0
        item.start_time = time.time()
        item.error_message = None
        
        logger.info(f"Retrying expansion {expansion_id} (attempt {item.retry_count}/3)")
        self._update_ui_state()
        return True
    
    def get_queue_status(self) -> LoadingQueueStatus:
        """Get current queue status for UI updates"""
        total = len(self.loading_items)
        completed = sum(1 for item in self.loading_items.values() 
                       if item.state == LoadingState.COMPLETED)
        failed = sum(1 for item in self.loading_items.values() 
                    if item.state == LoadingState.FAILED)
        
        # Current category and item
        current_category = None
        current_item = None
        for item in self.loading_items.values():
            if item.state in [LoadingState.LOADING, LoadingState.RETRYING]:
                current_category = item.category
                current_item = item.name
                break
        
        # Overall progress calculation
        if total == 0:
            overall_progress = 1.0
        else:
            progress_sum = sum(item.progress for item in self.loading_items.values())
            overall_progress = progress_sum / total
        
        # Estimate time remaining
        elapsed_time = time.time() - self.start_time
        if overall_progress > 0.1:  # Only estimate after some progress
            estimated_total_time = elapsed_time / overall_progress
            estimated_remaining = max(0, estimated_total_time - elapsed_time)
        else:
            estimated_remaining = None
        
        return LoadingQueueStatus(
            total_items=total,
            completed_items=completed,
            failed_items=failed,
            current_category=current_category,
            current_item=current_item,
            overall_progress=overall_progress,
            estimated_time_remaining=estimated_remaining
        )
    
    def get_failed_expansions(self) -> List[ExpansionLoadingItem]:
        """Get list of failed expansions for retry interface"""
        return [item for item in self.loading_items.values() 
                if item.state == LoadingState.FAILED]
    
    def get_category_progress(self, category: ExpansionCategory) -> Dict[str, Any]:
        """
        Get progress information for a specific category.
        
        Returns:
            Dictionary with category progress details
        """
        category_items = [item for item in self.loading_items.values() 
                         if item.category == category]
        
        if not category_items:
            return {
                'total': 0,
                'completed': 0,
                'failed': 0,
                'progress': 1.0,
                'state': 'empty'
            }
        
        total = len(category_items)
        completed = sum(1 for item in category_items if item.state == LoadingState.COMPLETED)
        failed = sum(1 for item in category_items if item.state == LoadingState.FAILED)
        loading = any(item.state in [LoadingState.LOADING, LoadingState.RETRYING] 
                     for item in category_items)
        
        # Category progress
        progress_sum = sum(item.progress for item in category_items)
        category_progress = progress_sum / total if total > 0 else 1.0
        
        # Category state
        if completed == total:
            state = 'completed'
        elif failed > 0 and completed + failed == total:
            state = 'failed'
        elif loading:
            state = 'loading'
        else:
            state = 'pending'
        
        return {
            'total': total,
            'completed': completed,
            'failed': failed,
            'progress': category_progress,
            'state': state,
            'items': category_items
        }
    
    def _update_ui_state(self) -> None:
        """Update internal UI state and trigger callback"""
        status = self.get_queue_status()
        
        # Update UI state dictionary
        self.ui_state.update({
            'progress_percentage': int(status.overall_progress * 100),
            'status_message': self._generate_status_message(status),
            'current_category': status.current_category.value if status.current_category else None,
            'failed_expansions': [item.expansion_id for item in self.get_failed_expansions()],
            'show_retry_button': len(self.get_failed_expansions()) > 0,
            'estimated_time': status.estimated_time_remaining
        })
        
        # Call update callback if provided
        if self.update_callback:
            try:
                self.update_callback(status)
            except Exception as e:
                logger.error(f"Error in update callback: {e}")
    
    def _generate_status_message(self, status: LoadingQueueStatus) -> str:
        """Generate user-friendly status message"""
        if status.total_items == 0:
            return "No expansions to load"
        
        if status.is_complete:
            if status.failed_items > 0:
                return f"Loading complete: {status.completed_items} successful, {status.failed_items} failed"
            else:
                return f"All {status.completed_items} expansions loaded successfully!"
        
        if status.current_item:
            category_name = status.current_category.value.replace('_', ' ').title() if status.current_category else "Unknown"
            return f"Loading {category_name}: {status.current_item}..."
        
        return f"Loading expansions... ({status.completed_items}/{status.total_items})"
    
    def get_ui_state(self) -> Dict[str, Any]:
        """Get current UI state for rendering"""
        return self.ui_state.copy()
    
    def clear_completed(self) -> None:
        """Clear completed expansions from queue (for memory management)"""
        completed_items = [expansion_id for expansion_id, item in self.loading_items.items()
                          if item.state == LoadingState.COMPLETED]
        
        for expansion_id in completed_items:
            del self.loading_items[expansion_id]
        
        logger.info(f"Cleared {len(completed_items)} completed expansions from queue")
        self._update_ui_state() 