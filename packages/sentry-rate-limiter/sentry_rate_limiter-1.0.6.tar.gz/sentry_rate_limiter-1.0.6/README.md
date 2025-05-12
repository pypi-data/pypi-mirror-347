# Sentry Handler

A custom Sentry handler that provides PII filtering, event deduplication, and rate limiting capabilities for Sentry error reporting.

## Features

- PII (Personally Identifiable Information) filtering
- Event deduplication using Redis
- Rate limiting for error propagation
- Custom exception filtering
- Logger message filtering
- EC2 instance information tracking

## Installation

```bash
pip install rate-limiter
```

## Usage

Here's how to initialize Sentry with the SentryHandler:

```python
import sentry_sdk
from redis import Redis
from rate_limiter.sentry_helper import SentryHandler

# Initialize Redis connection
redis_client = Redis(
    host='your-redis-host',
    port=6379,
    db=0
)

# Initialize SentryHandler
sentry_handler = SentryHandler(
    redis_connection=redis_client,
    git_commit_hash='your-git-commit-hash'  # Optional
)

# Initialize Sentry with the handler
sentry_sdk.init(
    dsn="your-sentry-dsn",
    before_send=sentry_handler.before_send_sentry_handler,
    # Add other Sentry configuration options as needed
)
```

## Configuration Options

The SentryHandler accepts the following parameters:

### Required Parameters

- `redis_connection`: Redis connection instance
  ```python
  redis_client = Redis(host='localhost', port=6379, db=0)
  ```

### Optional Parameters

- `git_commit_hash`: Git commit hash for tagging events
  ```python
  git_commit_hash = "a1b2c3d4e5"  # Will be truncated to first 10 characters
  ```

- `pii_regex_patterns`: Custom PII regex patterns to mask sensitive information
  ```python
  pii_regex_patterns = {
      "email": r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)",
      "phone": r"(\+\d{1,3}[- ]?)?\d{10}[\s , )]",
      "pan": r"[A-Z]{5}[0-9]{4}[A-Z]{1}",
      "aadhar": r"[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}[" " , . )]",
      "recording_url": r'[https?: // " ]\S+\.mp3[ \ {t1} . , " ]?'
  }
  ```

- `exclude_exception_classes`: Set of exception classes to exclude from reporting
  ```python
  exclude_exception_classes = {
      "ConnectionError",
      "TimeoutError",
      "ValidationError"
  }
  ```

- `exclude_exception_msg_prefixes`: List of exception message prefixes to exclude
  ```python
  exclude_exception_msg_prefixes = [
      "Invalid input",
      "Connection refused",
      "Timeout"
  ]
  ```

- `silence_logger_messages`: Dictionary mapping logger names to lists of message prefixes to silence
  ```python
  silence_logger_messages = {
      "elasticapm.transport": [
          "Failed to submit message",
          "Unable to reach APM Server"
      ],
      "your.custom.logger": [
          "Ignorable error",
          "Expected failure"
      ]
  }
  ```

- `propagation_series`: Set of numbers for rate limiting propagation
  ```python
  # Default restricted series
  propagation_series = {1, 2, 4, 8, 16, 32, 64, 128, 256}
  
  # Alternative standard series
  propagation_series = {1, 2, 3, 4, 9, 16, 25, 36, 49}
  ```

## Features in Detail

### PII Filtering
Automatically masks sensitive information in error reports using configurable regex patterns. For example:
- Email addresses: `user@example.com` → `user@****`
- Phone numbers: `+91 9876543210` → `+91 9876****`
- PAN numbers: `ABCDE1234F` → `ABCDE****`
- Aadhar numbers: `1234 5678 9012` → `1234 **** ****`

### Event Deduplication
Uses Redis to track and deduplicate similar errors, reducing noise in your Sentry dashboard. Each unique error is tracked with a hash and timestamp.

### Rate Limiting
Controls the frequency of error propagation to Sentry using a configurable series of numbers. For example, with the default restricted series:
- First occurrence: Always sent
- Second occurrence: Sent
- Third occurrence: Skipped
- Fourth occurrence: Sent
- And so on...

### Exception Filtering
Filters out specific exception classes and messages based on configurable rules. For example:
```python
# These exceptions will be filtered out
raise ConnectionError("Connection refused")  # Filtered by class
raise ValueError("Invalid input format")     # Filtered by message prefix
```

### Logger Message Filtering
Silences specific logger messages to reduce noise in your error tracking. For example:
```python
logger.error("Failed to submit message")  # Will be silenced if configured
logger.error("Critical system error")     # Will be reported
```

### EC2 Integration
Automatically adds EC2 instance information to error reports when running on AWS infrastructure:
- Instance ID: `i-1234567890abcdef0`
- Instance Name: `production-web-server-1`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
