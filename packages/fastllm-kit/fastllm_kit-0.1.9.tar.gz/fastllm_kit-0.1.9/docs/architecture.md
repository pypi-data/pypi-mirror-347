# FastLLM Architecture

This document provides an overview of the FastLLM architecture and design decisions.

## Project Structure

```
fastllm/                  # Main package directory
├── __init__.py           # Package exports
├── core.py               # Core functionality (RequestBatch, RequestManager)
├── cache.py              # Caching implementations
└── providers/            # LLM provider implementations
    ├── __init__.py
    ├── base.py           # Base Provider class
    └── openai.py         # OpenAI API implementation
```

## Package and Distribution

The package follows these important design decisions:

- **PyPI Package Name**: `fastllm-kit` (since `fastllm` was already taken on PyPI)
- **Import Name**: `fastllm` (users import with `from fastllm import ...`)
- **GitHub Repository**: Maintained at `github.com/rexhaif/fastllm`

The import redirection is implemented using Hatchling's build configuration in `pyproject.toml`, which ensures that the package is published as `fastllm-kit` but exposes a top-level `fastllm` module for imports.

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     RequestManager                      │
├─────────────────────────────────────────────────────────┤
│ - Manages parallel request processing                   │
│ - Handles concurrency and batching                      │
│ - Coordinates between components                        │
└───────────────────┬───────────────────┬─────────────────┘
                    │                   │
    ┌───────────────▼──────┐   ┌────────▼──────────┐
    │      Provider        │   │   CacheProvider   │
    ├──────────────────────┤   ├───────────────────┤
    │ - API communication  │   │ - Request caching │
    │ - Response parsing   │   │ - Cache management│
    └──────────────────────┘   └───────────────────┘
```

## Core Components

### RequestBatch

The `RequestBatch` class provides an OpenAI-compatible request interface that allows for batching multiple requests together.

### RequestManager

The `RequestManager` handles parallel processing of requests with configurable concurrency, retries, and caching.

### Providers

Providers implement the interface for different LLM services:

- `OpenAIProvider`: Handles requests to OpenAI-compatible APIs

### Caching

The caching system supports:

- `InMemoryCache`: Fast, in-process caching
- `DiskCache`: Persistent disk-based caching with TTL and size limits

## Design Decisions

1. **Parallel Processing**: Designed to maximize throughput by processing many requests in parallel
2. **Request Deduplication**: Automatically detects and deduplicates identical requests
3. **Response Ordering**: Maintains request ordering regardless of completion time
4. **Caching**: Optional caching with customizable providers
5. **Internal Tracking**: Uses internal tracking IDs (`_order_id` and `_request_id`) that are never sent to providers

## Development and Testing

- Tests are implemented using `pytest` and `pytest-asyncio`
- Code formatting is handled by `ruff` and `black`
- Task automation is handled by `just`
- Dependency management uses `uv`

## Key Utilities

- `compute_request_hash`: Consistent request hashing for caching and deduplication
- `TokenStats`: Tracking token usage and rate limits
- `ProgressTracker`: Visual progress bar with statistics

## Request Flow

1. Create a `RequestBatch` and add requests via APIs like `batch.chat.completions.create()`
2. Each request is directly stored in OpenAI Batch format with a `custom_id` that combines the request hash and order ID
3. Pass the batch to a `RequestManager` for parallel processing
4. The manager extracts necessary metadata from the `custom_id` and `url` fields
5. The `_order_id` and `_request_id` fields are attached to requests for internal tracking but are never sent to API providers
6. Responses are returned in the original request order

## Caching

The library implements efficient caching:
- Request hashing for consistent cache keys
- Support for both in-memory and persistent caching
- Cache hits bypass network requests

## Provider Interface

The library's provider system is designed to work with the simplified OpenAI Batch format:
- Providers receive only the request body and necessary metadata
- No conversion between formats is required during processing
- Both chat completions and embeddings use the same batch structure with different URLs
- API endpoints are determined automatically based on request type within each provider implementation
- Internal tracking IDs (`_order_id` and `_request_id`) are filtered out before sending to API providers

## Extensions

The library is designed to be easily extensible:
- Support for multiple LLM providers
- Custom cache implementations
- Flexible request formatting

## Key Features

### 1. Parallel Processing
- Async/await throughout
- Efficient request batching
- Concurrent API calls
- Progress monitoring
- Support for both chat completions and embeddings

### 2. Caching
- Multiple cache backends
- TTL support
- Async operations
- Thread-safe implementation

### 3. Rate Limiting
- Token-based limits
- Request frequency limits
- Window-based tracking
- Saturation monitoring

### 4. Error Handling
- Consistent error types
- Graceful degradation
- Detailed error messages
- Retry mechanisms

## Configuration Points

The system can be configured through:
1. Provider settings
   - API keys and endpoints
   - Organization IDs
   - Custom headers

2. Cache settings
   - Backend selection
   - TTL configuration
   - Storage directory
   - Serialization options

3. Request parameters
   - Model selection
   - Temperature and sampling
   - Token limits
   - Response streaming

4. Rate limiting
   - Token rate limits
   - Request frequency limits
   - Window sizes
   - Saturation thresholds

## Best Practices

1. **Error Handling**
   - Use try-except blocks for cache operations
   - Handle API errors gracefully
   - Provide meaningful error messages
   - Implement proper cleanup

2. **Performance**
   - Use appropriate cache backend
   - Configure batch sizes
   - Monitor rate limits
   - Track token usage

3. **Security**
   - Secure API key handling
   - Safe cache storage
   - Input validation
   - Response sanitization

4. **Maintenance**
   - Regular cache cleanup
   - Monitor disk usage
   - Update API versions
   - Track deprecations

## Data Flow

1. **Request Initialization**
   ```python
   RequestBatch
     → Chat Completion or Embedding Request
     → Provider-specific Request
   ```

2. **Request Processing**
   ```python
   RequestManager
     → Check Cache
     → Make API Request if needed
     → Update Progress
     → Store in Cache
   ```

3. **Response Handling**
   ```python
   API Response
     → ResponseWrapper
     → Update Statistics
     → Return to User
   ```

## Design Principles

1. **Modularity**
   - Clear separation of concerns
   - Extensible provider system
   - Pluggable cache providers

2. **Performance**
   - Efficient parallel processing
   - Smart resource management
   - Optimized caching

3. **Reliability**
   - Comprehensive error handling
   - Automatic retries
   - Progress tracking

4. **Developer Experience**
   - Familiar API patterns
   - Clear type hints
   - Comprehensive logging
   - Structured logging system

## Logging System

The library uses Python's built-in `logging` module for structured logging:

1. **Core Components**
   - Each module has its own logger (`logging.getLogger(__name__)`)
   - Log levels used appropriately (DEBUG, INFO, WARNING, ERROR)
   - Critical operations and errors are logged

2. **Key Logging Areas**
   - Cache operations (read/write errors)
   - Request processing status
   - Rate limiting events
   - Error conditions and exceptions

3. **Best Practices**
   - Consistent log format
   - Meaningful context in log messages
   - Error traceability
   - Performance impact consideration

## Error Handling

The system implements comprehensive error handling:
- API errors
- Rate limiting
- Timeouts
- Cache failures
- Invalid requests

Each component includes appropriate error handling and propagation to ensure system stability and reliability.

## Testing Strategy

The test suite is organized by component:

1. **Core Tests** (`test_core.py`):
   - Request/Response model validation
   - RequestManager functionality
   - Token statistics tracking

2. **Cache Tests** (`test_cache.py`):
   - Cache implementation verification
   - Request hashing consistency
   - Concurrent access handling

3. **Provider Tests** (`test_providers.py`):
   - Provider interface compliance
   - API communication
   - Response parsing

4. **Integration Tests**:
   - End-to-end request flow
   - Rate limiting behavior
   - Error handling scenarios

## Supported APIs

The library supports the following APIs:

1. **Chat Completions**
   - Multiple message support
   - Tool and function calls
   - Streaming responses
   - Temperature and top_p sampling
   
2. **Embeddings**
   - Single or batch text input
   - Dimension control
   - Format control (float/base64)
   - Efficient batch processing
   - Compatible with semantic search use cases
   