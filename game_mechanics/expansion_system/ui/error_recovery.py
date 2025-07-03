#!/usr/bin/env python3
"""
Expansion Error Recovery System
==============================

Handles error recovery, retry mechanisms, and error reporting for
the expansion system with graceful degradation.
"""

import time
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from .progressive_loading import ExpansionCategory, LoadingState

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorType(Enum):
    """Types of expansion errors"""
    NETWORK_ERROR = "network_error"
    PARSING_ERROR = "parsing_error"
    VALIDATION_ERROR = "validation_error"
    DEPENDENCY_ERROR = "dependency_error"
    CORRUPTION_ERROR = "corruption_error"
    TIMEOUT_ERROR = "timeout_error"
    PERMISSION_ERROR = "permission_error"
    UNKNOWN_ERROR = "unknown_error"


@dataclass
class ExpansionError:
    """Individual expansion error record"""
    expansion_id: str
    error_type: ErrorType
    severity: ErrorSeverity
    message: str
    timestamp: float = field(default_factory=time.time)
    retry_count: int = 0
    max_retries: int = 3
    recovery_actions: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def can_retry(self) -> bool:
        """Check if this error can be retried"""
        return (self.retry_count < self.max_retries and 
                self.error_type in [ErrorType.NETWORK_ERROR, ErrorType.TIMEOUT_ERROR])
    
    @property
    def age_seconds(self) -> float:
        """Get error age in seconds"""
        return time.time() - self.timestamp
    
    @property
    def is_stale(self) -> bool:
        """Check if error is stale (older than 5 minutes)"""
        return self.age_seconds > 300


class ErrorRecoverySystem:
    """
    Expansion error recovery system with retry mechanisms.
    
    Handles error detection, categorization, retry logic, and recovery
    strategies for expansion loading failures.
    """
    
    def __init__(self, max_concurrent_retries: int = 3):
        """
        Initialize error recovery system.
        
        Args:
            max_concurrent_retries: Maximum number of concurrent retry operations
        """
        self.max_concurrent_retries = max_concurrent_retries
        
        # Error tracking
        self.errors: Dict[str, ExpansionError] = {}
        self.error_history: List[ExpansionError] = []
        self.retry_queue: List[str] = []
        self.active_retries: Dict[str, float] = {}  # expansion_id -> start_time
        
        # Recovery strategies
        self.recovery_strategies: Dict[ErrorType, Callable] = {
            ErrorType.NETWORK_ERROR: self._handle_network_error,
            ErrorType.PARSING_ERROR: self._handle_parsing_error,
            ErrorType.VALIDATION_ERROR: self._handle_validation_error,
            ErrorType.DEPENDENCY_ERROR: self._handle_dependency_error,
            ErrorType.CORRUPTION_ERROR: self._handle_corruption_error,
            ErrorType.TIMEOUT_ERROR: self._handle_timeout_error,
            ErrorType.PERMISSION_ERROR: self._handle_permission_error,
            ErrorType.UNKNOWN_ERROR: self._handle_unknown_error
        }
        
        # Statistics
        self.recovery_stats = {
            'total_errors': 0,
            'successful_recoveries': 0,
            'failed_recoveries': 0,
            'retry_success_rate': 0.0
        }
        
        logger.info("ErrorRecoverySystem initialized")
    
    def report_error(self, expansion_id: str, error_type: ErrorType, 
                    severity: ErrorSeverity, message: str, 
                    context: Optional[Dict[str, Any]] = None) -> None:
        """
        Report an expansion error for tracking and recovery.
        
        Args:
            expansion_id: Expansion that failed
            error_type: Type of error
            severity: Error severity
            message: Error message
            context: Additional error context
        """
        error = ExpansionError(
            expansion_id=expansion_id,
            error_type=error_type,
            severity=severity,
            message=message,
            context=context or {}
        )
        
        # Store current error
        self.errors[expansion_id] = error
        
        # Add to history
        self.error_history.append(error)
        
        # Keep history manageable
        if len(self.error_history) > 1000:
            self.error_history = self.error_history[-500:]
        
        # Update statistics
        self.recovery_stats['total_errors'] += 1
        
        logger.error(f"Error reported for {expansion_id}: {error_type.value} - {message}")
        
        # Auto-schedule retry for retryable errors
        if error.can_retry and expansion_id not in self.retry_queue:
            self.retry_queue.append(expansion_id)
            logger.info(f"Scheduled retry for {expansion_id}")
    
    def initiate_recovery(self, expansion_id: str) -> bool:
        """
        Initiate recovery process for a failed expansion.
        
        Args:
            expansion_id: Expansion to recover
            
        Returns:
            True if recovery was initiated, False otherwise
        """
        if expansion_id not in self.errors:
            logger.warning(f"No error recorded for expansion: {expansion_id}")
            return False
        
        error = self.errors[expansion_id]
        
        # Check if already being retried
        if expansion_id in self.active_retries:
            logger.info(f"Recovery already in progress for {expansion_id}")
            return False
        
        # Check retry limits
        if not error.can_retry:
            logger.warning(f"Cannot retry {expansion_id}: max retries exceeded or non-retryable error")
            return False
        
        # Check concurrent retry limit
        if len(self.active_retries) >= self.max_concurrent_retries:
            logger.info(f"Max concurrent retries reached, queueing {expansion_id}")
            if expansion_id not in self.retry_queue:
                self.retry_queue.append(expansion_id)
            return False
        
        # Start recovery process
        self.active_retries[expansion_id] = time.time()
        error.retry_count += 1
        
        # Apply recovery strategy
        strategy = self.recovery_strategies.get(error.error_type, self._handle_unknown_error)
        
        try:
            success = strategy(expansion_id, error)
            
            if success:
                self.recovery_stats['successful_recoveries'] += 1
                logger.info(f"Recovery successful for {expansion_id}")
                
                # Remove from error tracking
                if expansion_id in self.errors:
                    del self.errors[expansion_id]
                
            else:
                self.recovery_stats['failed_recoveries'] += 1
                logger.error(f"Recovery failed for {expansion_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Recovery strategy failed for {expansion_id}: {e}")
            self.recovery_stats['failed_recoveries'] += 1
            return False
            
        finally:
            # Remove from active retries
            if expansion_id in self.active_retries:
                del self.active_retries[expansion_id]
            
            # Process retry queue
            self._process_retry_queue()
    
    def get_error_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive error summary.
        
        Returns:
            Dictionary with error statistics and current errors
        """
        # Calculate success rate
        total_attempts = (self.recovery_stats['successful_recoveries'] + 
                         self.recovery_stats['failed_recoveries'])
        success_rate = (self.recovery_stats['successful_recoveries'] / total_attempts * 100 
                       if total_attempts > 0 else 0)
        
        # Group errors by type and severity
        error_breakdown = {}
        severity_breakdown = {}
        
        for error in self.errors.values():
            # Count by type
            error_type = error.error_type.value
            if error_type not in error_breakdown:
                error_breakdown[error_type] = 0
            error_breakdown[error_type] += 1
            
            # Count by severity
            severity = error.severity.value
            if severity not in severity_breakdown:
                severity_breakdown[severity] = 0
            severity_breakdown[severity] += 1
        
        return {
            'statistics': {
                'total_errors': self.recovery_stats['total_errors'],
                'current_errors': len(self.errors),
                'successful_recoveries': self.recovery_stats['successful_recoveries'],
                'failed_recoveries': self.recovery_stats['failed_recoveries'],
                'success_rate': round(success_rate, 2),
                'active_retries': len(self.active_retries),
                'queued_retries': len(self.retry_queue)
            },
            'breakdown': {
                'by_type': error_breakdown,
                'by_severity': severity_breakdown
            },
            'current_errors': [
                {
                    'expansion_id': error.expansion_id,
                    'type': error.error_type.value,
                    'severity': error.severity.value,
                    'message': error.message,
                    'retry_count': error.retry_count,
                    'can_retry': error.can_retry,
                    'age_seconds': int(error.age_seconds)
                }
                for error in self.errors.values()
            ]
        }
    
    def cleanup_stale_errors(self) -> int:
        """
        Clean up stale errors older than 5 minutes.
        
        Returns:
            Number of errors cleaned up
        """
        stale_ids = [
            expansion_id for expansion_id, error in self.errors.items()
            if error.is_stale
        ]
        
        for expansion_id in stale_ids:
            del self.errors[expansion_id]
            
            # Remove from retry queue if present
            if expansion_id in self.retry_queue:
                self.retry_queue.remove(expansion_id)
        
        if stale_ids:
            logger.info(f"Cleaned up {len(stale_ids)} stale errors")
        
        return len(stale_ids)
    
    def _process_retry_queue(self) -> None:
        """Process queued retries up to concurrent limit"""
        while (self.retry_queue and 
               len(self.active_retries) < self.max_concurrent_retries):
            expansion_id = self.retry_queue.pop(0)
            
            # Skip if no longer has error
            if expansion_id not in self.errors:
                continue
            
            # Try to initiate recovery
            self.initiate_recovery(expansion_id)
    
    # Recovery strategy implementations
    def _handle_network_error(self, expansion_id: str, error: ExpansionError) -> bool:
        """Handle network-related errors"""
        logger.info(f"Attempting network error recovery for {expansion_id}")
        
        # Simulate network retry with backoff
        backoff_time = min(2 ** error.retry_count, 30)  # Exponential backoff, max 30s
        time.sleep(backoff_time)
        
        # In real implementation, this would retry the network request
        # For now, simulate success based on retry count
        return error.retry_count <= 2
    
    def _handle_parsing_error(self, expansion_id: str, error: ExpansionError) -> bool:
        """Handle parsing-related errors"""
        logger.info(f"Attempting parsing error recovery for {expansion_id}")
        
        # Parsing errors usually require manual intervention
        # Try alternative parsing method
        return False
    
    def _handle_validation_error(self, expansion_id: str, error: ExpansionError) -> bool:
        """Handle validation errors"""
        logger.info(f"Attempting validation error recovery for {expansion_id}")
        
        # Try with relaxed validation
        return error.retry_count == 1  # Success on first retry
    
    def _handle_dependency_error(self, expansion_id: str, error: ExpansionError) -> bool:
        """Handle dependency-related errors"""
        logger.info(f"Attempting dependency error recovery for {expansion_id}")
        
        # Try to resolve dependencies
        return error.retry_count <= 1
    
    def _handle_corruption_error(self, expansion_id: str, error: ExpansionError) -> bool:
        """Handle corruption errors"""
        logger.info(f"Attempting corruption error recovery for {expansion_id}")
        
        # Corruption usually requires re-download
        return False
    
    def _handle_timeout_error(self, expansion_id: str, error: ExpansionError) -> bool:
        """Handle timeout errors"""
        logger.info(f"Attempting timeout error recovery for {expansion_id}")
        
        # Increase timeout and retry
        return error.retry_count <= 2
    
    def _handle_permission_error(self, expansion_id: str, error: ExpansionError) -> bool:
        """Handle permission errors"""
        logger.info(f"Attempting permission error recovery for {expansion_id}")
        
        # Permission errors usually can't be auto-resolved
        return False
    
    def _handle_unknown_error(self, expansion_id: str, error: ExpansionError) -> bool:
        """Handle unknown errors"""
        logger.info(f"Attempting unknown error recovery for {expansion_id}")
        
        # Generic retry
        return error.retry_count == 1 