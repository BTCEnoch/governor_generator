# Batch Processing System Architecture

## Overview

The Governor Generation system uses a unified batch processing architecture to handle various types of content generation tasks efficiently. The system is designed to process large volumes of requests concurrently while maintaining consistency and error handling.

## Core Components

### UnifiedBatchProcessor

The `UnifiedBatchProcessor` class is the central component that handles all batch processing operations. It supports:

- Multiple job types (storylines, governor profiles, knowledge extraction, etc.)
- Concurrent request processing
- Automatic retries with configurable parameters
- Progress tracking and logging
- Type-safe request/response handling

### Job Types

The system supports the following job types:

1. `STORYLINE_GENERATION`: Generate storylines for governor interactions
2. `GOVERNOR_PROFILES`: Create detailed governor personality profiles
3. `KNOWLEDGE_EXTRACTION`: Extract structured knowledge from tradition sources
4. `QUESTLINE_GENERATION`: Generate interactive quest content
5. `ARTIFACT_GENERATION`: Create mystical artifacts and items
6. `TRADITION_PROCESSING`: Process mystical tradition research data

### Configuration

Each batch job is configured using the `BatchJobConfig` class, which includes:

```python
@dataclass
class BatchJobConfig:
    job_type: BatchJobType
    job_id: str
    input_data: Any
    output_directory: Path
    batch_size: int = 10
    max_retries: int = 3
    retry_delay: int = 5
    model: str = "claude-3-sonnet-20240229"
    max_tokens: int = 4096
    temperature: float = 0.7
    concurrent_requests: int = 5
    metadata: Dict[str, Any] = field(default_factory=dict)
```

### Request Processing

Individual requests within a batch are handled by the `BatchRequest` class:

```python
@dataclass
class BatchRequest:
    request_id: str
    job_type: BatchJobType
    input_data: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    custom_id: Optional[str] = None
    prompt: Optional[str] = None
    config: Optional[BatchJobConfig] = None
    attempts: int = 0
```

## Processing Flow

1. **Job Creation**
   - Client creates a `BatchJobConfig` with job parameters
   - UnifiedBatchProcessor validates configuration
   - Job is registered in the system

2. **Request Generation**
   - Input data is split into individual requests
   - Each request is assigned a unique ID
   - Job-specific handlers create appropriate prompts

3. **Concurrent Processing**
   - Requests are processed in parallel using ThreadPoolExecutor
   - Number of concurrent requests is configurable
   - Progress is tracked for each request

4. **Error Handling**
   - Failed requests are automatically retried
   - Max retries and delay are configurable
   - Detailed error logging is provided

5. **Results Collection**
   - Successful responses are collected
   - Results are saved to the specified output directory
   - Job status is updated

## Usage Example

```python
from engines.batch_processing import UnifiedBatchProcessor, BatchJobConfig, BatchJobType

# Initialize processor
processor = UnifiedBatchProcessor()

# Create job config
config = BatchJobConfig(
    job_type=BatchJobType.STORYLINE_GENERATION,
    job_id="storyline_batch_1",
    input_data=governor_data,
    output_directory=Path("storyline_output")
)

# Create and process batch job
result = processor.create_batch_job(config)
processor.process_batch_job(result.job_id)
```

## Best Practices

1. **Job Organization**
   - Group related items into single batches
   - Use meaningful job IDs and metadata
   - Keep batch sizes manageable (10-50 items)

2. **Error Handling**
   - Set appropriate retry parameters
   - Monitor job progress
   - Save intermediate results

3. **Resource Management**
   - Configure concurrent_requests based on system capacity
   - Use appropriate model parameters
   - Monitor API usage and costs

4. **Data Management**
   - Organize output directories clearly
   - Include sufficient metadata
   - Maintain job logs

## Integration Points

The batch processing system integrates with:

- Knowledge Base (The Lighthouse)
- Governor Profile Generation
- Storyline Engine
- Game Mechanics Generation
- Mystical Systems Processing

## Future Enhancements

1. Async/await support for improved concurrency
2. Enhanced progress monitoring
3. Job prioritization system
4. Resource usage optimization
5. Extended error recovery options 