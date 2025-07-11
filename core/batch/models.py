"""
Batch Processing Models

Defines the core data models for batch processing operations.
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from pathlib import Path
from datetime import datetime

class BatchJobType(str, Enum):
    """Types of batch jobs supported by the system"""
    STORYLINE_GENERATION = "storyline_generation"
    TRAIT_GENERATION = "trait_generation"
    GOVERNOR_ANALYSIS = "governor_analysis"
    MYSTICAL_MAPPING = "mystical_mapping"
    BITCOIN_INTEGRATION = "bitcoin_integration"

class BatchJobStatus(str, Enum):
    """Status states for batch jobs"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class BatchJobConfig(BaseModel):
    """Configuration for a batch processing job"""
    job_type: BatchJobType
    job_id: str
    input_data: List[Dict[str, Any]]
    output_directory: Path
    batch_size: int = Field(default=10, gt=0)
    total_items: int = Field(default=0, ge=0)
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class BatchJobResult(BaseModel):
    """Results and status of a batch job"""
    job_id: str
    status: BatchJobStatus
    processed_items: int = 0
    total_items: int = 0
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    error_messages: List[str] = Field(default_factory=list)
    output_files: List[Path] = Field(default_factory=list)
    metrics: Optional[Dict[str, Any]] = None 