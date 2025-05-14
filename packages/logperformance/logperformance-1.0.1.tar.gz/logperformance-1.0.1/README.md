# LogPerformance

A Python logging utility class that provides performance monitoring, error tracking, and colored console output with file logging capabilities.

## Class Overview

`LogPerformance` is a singleton class that implements a comprehensive logging system with the following features:

- Colored console output
- File logging with timestamp-based filenames
- Performance monitoring for functions
- Error tracking
- Warning messages
- Custom log levels

## Methods

### `__new__(cls, *args, **kwargs)`

Singleton pattern implementation that ensures only one instance of the class exists.

### `__init__(self)`

Initializes the logger with:

- Colored console output handler
- File logging handler (if enabled)
- Custom log level configuration
- Directory creation for log files

### `check_exists_directory(work_directory: str) -> bool`

Static method that checks if a directory exists.

### `create_directory(cls, work_directory: str) -> None`

Class method that creates a directory if it doesn't exist and logs the creation.

### `log_performance(self, func: Callable) -> Callable`

Decorator that measures and logs the execution time of a function.

- Logs function name, arguments, and execution time
- Returns the function's result

### `log_error(self, func: Callable) -> Callable`

Decorator that catches and logs exceptions in a function.

- Logs the function name and error message
- Re-raises the exception after logging

### `log_warning(self, func: Callable) -> Callable`

Decorator that logs warnings for function execution.

- Logs function name, arguments, and execution time
- Returns the function's result

### `info(self, msg: str) -> None`

Logs an informational message with a smile emoji prefix.

### `warning(self, msg: str) -> None`

Logs a warning message.

### `error(self, msg: str) -> None`

Logs an error message with an exclamation mark emoji prefix.

### `_append_log_message(self, msg: str, level: int) -> None`

Private method that appends log messages with timestamp and level.

- Handles debug level filtering
- Stores the last log message

## Usage Example

```python
from logperformance import LogPerformance

log = LogPerformance()

@log.log_performance
def example_function(arg1, arg2):
    # Your code here
    pass

@log.log_error
def error_prone_function():
    # Your code here
    pass

# Log messages
log.info("This is an info message")
log.warning("This is a warning")
log.error("This is an error")
```

## Configuration

The logger can be configured using environment variables:

- `LOG_LEVEL`: Set to "DEBUG" for debug level logging
- `DEBUG_WRITE_FILE`: Set to "True" to enable file logging (default)
