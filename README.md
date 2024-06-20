# Folder Synchronizer

Folder Synchronizer is a Python script that synchronizes the content of a source folder to a replica folder, ensuring the replica folder maintains an identical copy of the source folder. This synchronization is one-way and periodic, controlled by a user-specified interval. The script logs all file creation, copying, and removal operations to a log file and the console.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Usage](#usage)

## Features
- One-way synchronization from source to replica.
- Periodic synchronization based on a user-defined interval.
- Logging of file operations to a log file and the console.

## Requirements
- Python 3.10+
- No third-party libraries are required.


## Usage
Command syntax:

```bash
python main.py /path/to/source /path/to/replica interval_in_seconds /path/to/logfile.log
```

Example command:

```bash
python main.py /path/to/source /path/to/replica 60 /path/to/logfile.log
```

- `/path/to/source`: Path to the source directory.
- `/path/to/replica`: Path to the replica directory.
- `60`: Synchronization interval in seconds.
- `/path/to/logfile.log`: Path to the log file.

The script will start synchronizing the source folder with the replica folder every 60 seconds, logging operations to the specified log file and the console.

### File Structure

```
.
├── main.py          # Entry point of the script
├── logic.py         # Contains the core logic for synchronization and parsing
├── README.md        # Project documentation
```

### Code Explanation

#### main.py
```python
from logic import sync_folders, parsing
import time

def main():
    print(">>> Starting...")
    source, replica, interval = parsing()
    while True:
        sync_folders(source, replica)
        time.sleep(interval)

if __name__ == "__main__":
    main()
```

- **main()**: Starts the synchronization process by calling `sync_folders` in an infinite loop, with a sleep interval as specified by the user.

#### logic.py
```python
import io
import os
import shutil
import hashlib
import argparse
import logging

def calculate_md5(file_path, length=io.DEFAULT_BUFFER_SIZE):
    # Calculate the MD5 checksum of a file.
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(length), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def sync_folders(source, replica):
    # Synchronize the replica folder to match the source folder.
    if not os.path.exists(replica):
        os.makedirs(replica)
        logging.info(f">>> Created directory {replica}")

    source_files = set(os.listdir(source))
    replica_files = set(os.listdir(replica))

    for item in source_files:
        source_item = os.path.join(source, item)
        replica_item = os.path.join(replica, item)

        if os.path.isdir(source_item):
            sync_folders(source_item, replica_item)
        else:
            if not os.path.exists(replica_item) or calculate_md5(source_item) != calculate_md5(replica_item):
                shutil.copy2(source_item, replica_item)
                logging.info(f">>> Copied {source_item} to {replica_item}")

    for item in replica_files:
        replica_item = os.path.join(replica, item)
        if item not in source_files:
            if os.path.isdir(replica_item):
                shutil.rmtree(replica_item)
                logging.info(f">>> Removed directory {replica_item}")
            else:
                os.remove(replica_item)
                logging.info(f">>> Removed file {replica_item}")

def parsing():
    parser = argparse.ArgumentParser(description="Synchronize two folders.")
    parser.add_argument("source", help="Source folder path")
    parser.add_argument("replica", help="Replica folder path")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("logfile", help="Log file path")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", handlers=[logging.FileHandler(args.logfile), logging.StreamHandler()])

    source = args.source
    replica = args.replica
    interval = args.interval

    return source, replica, interval
```

- **calculate_md5()**: Calculates the MD5 checksum of a file.
- **sync_folders()**: Synchronizes the replica folder to match the source folder.
- **parsing()**: Parses command-line arguments and sets up logging.
