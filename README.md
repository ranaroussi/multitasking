# MultiTasking: Non-blocking Python methods using decorators

[![Python version](https://img.shields.io/badge/python-3.6+-blue.svg?style=flat)](https://pypi.python.org/pypi/multitasking)
[![PyPi version](https://img.shields.io/pypi/v/multitasking.svg?maxAge=60)](https://pypi.python.org/pypi/multitasking)
[![PyPi status](https://img.shields.io/pypi/status/multitasking.svg?maxAge=2592000)](https://pypi.python.org/pypi/multitasking)
[![PyPi downloads](https://img.shields.io/pypi/dm/multitasking.svg?maxAge=2592000)](https://pypi.python.org/pypi/multitasking)
[![CodeFactor](https://www.codefactor.io/repository/github/ranaroussi/multitasking/badge)](https://www.codefactor.io/repository/github/ranaroussi/multitasking)
[![Star this repo](https://img.shields.io/github/stars/ranaroussi/multitasking.svg?style=social&label=Star&maxAge=60)](https://github.com/ranaroussi/multitasking)
[![Follow me on twitter](https://img.shields.io/twitter/follow/aroussi.svg?style=social&label=Follow%20Me&maxAge=60)](https://twitter.com/aroussi)

---

**MultiTasking** is a lightweight Python library that lets you convert your Python methods into asynchronous,
non-blocking methods simply by using a decorator. Perfect for I/O-bound tasks, API calls, web scraping,
and any scenario where you want to run multiple operations concurrently without the complexity of manual
thread or process management.

## ✨ **What's New in v0.0.12**

- 🎯 **Full Type Hint Support**: Complete type annotations for better IDE support and code safety
- 📚 **Enhanced Documentation**: Comprehensive docstrings and inline comments for better maintainability
- 🔧 **Improved Error Handling**: More robust exception handling with specific error types
- 🚀 **Better Performance**: Optimized task creation and management logic
- 🛡️ **Code Quality**: PEP8 compliant, linter-friendly codebase

## Quick Start

```python
import multitasking
import time

@multitasking.task
def fetch_data(url_id):
    # Simulate API call or I/O operation
    time.sleep(1)
    return f"Data from {url_id}"

# These run concurrently, not sequentially!
for i in range(5):
    fetch_data(i)

# Wait for all tasks to complete
multitasking.wait_for_tasks()
print("All data fetched!")
```

## Basic Example

```python
# example.py
import multitasking
import time
import random
import signal

# Kill all tasks on ctrl-c (recommended for development)
signal.signal(signal.SIGINT, multitasking.killall)

# Or, wait for tasks to finish gracefully on ctrl-c:
# signal.signal(signal.SIGINT, multitasking.wait_for_tasks)

@multitasking.task  # <== this is all it takes! 🎉
def hello(count):
    sleep_time = random.randint(1, 10) / 2
    print(f"Hello {count} (sleeping for {sleep_time}s)")
    time.sleep(sleep_time)
    print(f"Goodbye {count} (slept for {sleep_time}s)")

if __name__ == "__main__":
    # Launch 10 concurrent tasks
    for i in range(10):
        hello(i + 1)

    # Wait for all tasks to complete
    multitasking.wait_for_tasks()
    print("All tasks completed!")
```

**Output:**

```bash
$ python example.py

Hello 1 (sleeping for 0.5s)
Hello 2 (sleeping for 1.0s)
Hello 3 (sleeping for 5.0s)
Hello 4 (sleeping for 0.5s)
Hello 5 (sleeping for 2.5s)
Hello 6 (sleeping for 3.0s)
Hello 7 (sleeping for 0.5s)
Hello 8 (sleeping for 4.0s)
Hello 9 (sleeping for 3.0s)
Hello 10 (sleeping for 1.0s)
Goodbye 1 (slept for 0.5s)
Goodbye 4 (slept for 0.5s)
Goodbye 7 (slept for 0.5s)
Goodbye 2 (slept for 1.0s)
Goodbye 10 (slept for 1.0s)
Goodbye 5 (slept for 2.5s)
Goodbye 6 (slept for 3.0s)
Goodbye 9 (slept for 3.0s)
Goodbye 8 (slept for 4.0s)
Goodbye 3 (slept for 5.0s)
All tasks completed!
```

# Advanced Usage

## Real-World Examples

**Web Scraping with Concurrent Requests:**

```python
import multitasking
import requests
import signal

signal.signal(signal.SIGINT, multitasking.killall)

@multitasking.task
def fetch_url(url):
    try:
        response = requests.get(url, timeout=10)
        print(f"✅ {url}: {response.status_code}")
        return response.text
    except Exception as e:
        print(f"❌ {url}: {str(e)}")
        return None

# Fetch multiple URLs concurrently
urls = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/status/200",
    "https://httpbin.org/json"
]

for url in urls:
    fetch_url(url)

multitasking.wait_for_tasks()
print(f"Processed {len(urls)} URLs concurrently!")
```

**Database Operations:**

```python
import multitasking
import sqlite3
import time

@multitasking.task
def process_batch(batch_id, data_batch):
    # Simulate database processing
    conn = sqlite3.connect(f'batch_{batch_id}.db')
    # ... database operations ...
    conn.close()
    print(f"Processed batch {batch_id} with {len(data_batch)} records")

# Process multiple data batches concurrently
large_dataset = list(range(1000))
batch_size = 100

for i in range(0, len(large_dataset), batch_size):
    batch = large_dataset[i:i + batch_size]
    process_batch(i // batch_size, batch)

multitasking.wait_for_tasks()
```

## Pool Management

MultiTasking uses execution pools to manage concurrent tasks. You can create and configure multiple pools for different types of operations:

```python
import multitasking

# Create a pool for API calls (higher concurrency)
multitasking.createPool("api_pool", threads=20, engine="thread")

# Create a pool for CPU-intensive tasks (lower concurrency)
multitasking.createPool("cpu_pool", threads=4, engine="process")

# Switch between pools
multitasking.use_tag("api_pool")  # Future tasks use this pool

@multitasking.task
def api_call(endpoint):
    # This will use the api_pool
    pass

# Get pool information
pool_info = multitasking.getPool("api_pool")
print(f"Pool: {pool_info}")  # {'engine': 'thread', 'name': 'api_pool', 'threads': 20}
```

## Task Monitoring

Monitor and control your tasks with built-in functions:

```python
import multitasking
import time

@multitasking.task
def long_running_task(task_id):
    time.sleep(2)
    print(f"Task {task_id} completed")

# Start some tasks
for i in range(5):
    long_running_task(i)

# Monitor active tasks
while multitasking.get_active_tasks():
    active_count = len(multitasking.get_active_tasks())
    total_count = len(multitasking.get_list_of_tasks())
    print(f"Progress: {total_count - active_count}/{total_count} completed")
    time.sleep(0.5)

print("All tasks finished!")
```

# Configuration & Settings

## Thread/Process Limits

The default maximum threads equals the number of CPU cores. You can customize this:

```python
import multitasking

# Set maximum concurrent tasks
multitasking.set_max_threads(10)

# Scale based on CPU cores (good rule of thumb for I/O-bound tasks)
multitasking.set_max_threads(multitasking.config["CPU_CORES"] * 5)

# Unlimited concurrent tasks (use carefully!)
multitasking.set_max_threads(0)
```

## Execution Engine Selection

Choose between threading and multiprocessing based on your use case:

```python
import multitasking

# For I/O-bound tasks (default, recommended for most cases)
multitasking.set_engine("thread")

# For CPU-bound tasks (avoids GIL limitations)
multitasking.set_engine("process")
```

**When to use threads vs processes:**

- **Threads** (default): Best for I/O-bound tasks like file operations, network requests, database queries
- **Processes**: Best for CPU-intensive tasks like mathematical computations, image processing, data analysis

## Advanced Pool Configuration

Create specialized pools for different workloads:

```python
import multitasking

# Fast pool for quick API calls
multitasking.createPool("fast_api", threads=50, engine="thread")

# CPU pool for heavy computation
multitasking.createPool("compute", threads=2, engine="process")

# Unlimited pool for lightweight tasks
multitasking.createPool("unlimited", threads=0, engine="thread")

# Get current pool info
current_pool = multitasking.getPool()
print(f"Using pool: {current_pool['name']}")
```

# Best Practices

## Performance Tips

1. **Choose the right engine**: Use threads for I/O-bound tasks, processes for CPU-bound tasks
2. **Tune thread counts**: Start with CPU cores × 2-5 for I/O tasks, CPU cores for CPU tasks
3. **Use pools wisely**: Create separate pools for different types of operations
4. **Monitor memory usage**: Each thread/process consumes memory
5. **Handle exceptions**: Always wrap risky operations in try-catch blocks

## Error Handling

```python
import multitasking
import requests

@multitasking.task
def robust_fetch(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print(f"⏰ Timeout fetching {url}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching {url}: {e}")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
    return None
```

## Resource Management

```python
import multitasking
import signal

# Graceful shutdown on interrupt
def cleanup_handler(signum, frame):
    print("🛑 Shutting down gracefully...")
    multitasking.wait_for_tasks()
    print("✅ All tasks completed")
    exit(0)

signal.signal(signal.SIGINT, cleanup_handler)

# Your application code here...
```

# Troubleshooting

## Common Issues

**Tasks not running concurrently?**
  Check if you're calling `wait_for_tasks()` inside your task loop instead of after it.

**High memory usage?**
  Reduce the number of concurrent threads or switch to a process-based engine.

**Tasks hanging?**
  Ensure your tasks can complete (avoid infinite loops) and handle exceptions properly.

**Import errors?**
  Make sure you're using Python 3.6+ and have installed the latest version.

## Debugging

```python
import multitasking

# Enable task monitoring
active_tasks = multitasking.get_active_tasks()
all_tasks = multitasking.get_list_of_tasks()

print(f"Active: {len(active_tasks)}, Total: {len(all_tasks)}")

# Get current pool configuration
pool_info = multitasking.getPool()
print(f"Current pool: {pool_info}")
```

# Installation

**Requirements:**
- Python 3.6 or higher
- No external dependencies!

**Install via pip:**

```bash
$ pip install multitasking --upgrade --no-cache-dir
```

**Development installation:**

```bash
$ git clone https://github.com/ranaroussi/multitasking.git
$ cd multitasking
$ pip install -e .
```

# Compatibility

- **Python**: 3.6+ (type hints require 3.6+)
- **Operating Systems**: Windows, macOS, Linux
- **Environments**: Works in Jupyter notebooks, scripts, web applications
- **Frameworks**: Compatible with Flask, Django, FastAPI, and other Python frameworks

# API Reference

## Decorators

- `@multitasking.task` - Convert function to asynchronous task

## Configuration Functions

- `set_max_threads(count)` - Set maximum concurrent tasks
- `set_engine(type)` - Choose "thread" or "process" engine
- `createPool(name, threads, engine)` - Create custom execution pool

## Task Management

- `wait_for_tasks(sleep=0)` - Wait for all tasks to complete
- `get_active_tasks()` - Get list of running tasks
- `get_list_of_tasks()` - Get list of all tasks
- `killall()` - Emergency shutdown (force exit)

## Pool Management

- `getPool(name=None)` - Get pool information
- `createPool(name, threads=None, engine=None)` - Create new pool

# Performance Benchmarks

Here's a simple benchmark comparing synchronous vs asynchronous execution:

```python
import multitasking
import time
import requests

# Synchronous version
def sync_fetch():
    start = time.time()
    for i in range(10):
        requests.get("https://httpbin.org/delay/1")
    print(f"Synchronous: {time.time() - start:.2f}s")

# Asynchronous version
@multitasking.task
def async_fetch():
    requests.get("https://httpbin.org/delay/1")

def concurrent_fetch():
    start = time.time()
    for i in range(10):
        async_fetch()
    multitasking.wait_for_tasks()
    print(f"Concurrent: {time.time() - start:.2f}s")

# Results: Synchronous ~10s, Concurrent ~1s (10x speedup!)
```

# Contributing

We welcome contributions! Here's how you can help:

1. **Report bugs**: Open an issue with details and reproduction steps
2. **Suggest features**: Share your ideas for improvements
3. **Submit PRs**: Fork, create a feature branch, and submit a pull request
4. **Improve docs**: Help make the documentation even better

**Development setup:**

```bash
$ git clone https://github.com/ranaroussi/multitasking.git
$ cd multitasking
$ pip install -e .
$ python -m pytest  # Run tests
```

# Legal Stuff

**MultiTasking** is distributed under the **Apache Software License**.
See the [LICENSE.txt](./LICENSE.txt) file in the release for details.

# Support

- 📖 **Documentation**: This README and inline code documentation
- 🐛 **Issues**: [GitHub Issues](https://github.com/ranaroussi/multitasking/issues)
- 🐦 **Twitter**: [@aroussi](https://twitter.com/aroussi)

# Changelog

**v0.0.12-rc**
- ✨ Added comprehensive type hints throughout the codebase
- 📚 Enhanced documentation with detailed docstrings and inline comments
- 🔧 Improved error handling with specific exception types
- 🚀 Optimized task creation and pool management logic
- 🛡️ Made codebase fully PEP8 compliant and linter-friendly
- 🧹 Better code organization and maintainability

**v0.0.11** (Latest)
- Previous stable release

---

**Happy Multitasking! 🚀**

*Please drop me a note with any feedback you have.*

**Ran Aroussi**
