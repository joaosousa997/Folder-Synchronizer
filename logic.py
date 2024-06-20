import io
import os
import shutil
import hashlib
import argparse
import logging

def md5_check(file_path, length=io.DEFAULT_BUFFER_SIZE):
    # Calculate the MD5 checksum of a file.
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(length):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def sync_folders(source, replica):
    # Synchronize the replica folder to match the source folder.
    # Create the replica directory if it doesn't exist
    if not os.path.exists(replica):
        os.makedirs(replica)
        logging.info(f">>> Created directory {replica}")

    # Get the sets of file and directory names in source and replica
    source_files = set(os.listdir(source))
    replica_files = set(os.listdir(replica))

    # Copy or update files and directories from source to replica
    for item in source_files:
        source_item = os.path.join(source, item)
        replica_item = os.path.join(replica, item)

        if os.path.isdir(source_item):
            sync_folders(source_item, replica_item)
        else:
            if not os.path.exists(replica_item) or md5_check(source_item) != md5_check(replica_item):
                shutil.copy2(source_item, replica_item)
                logging.info(f">>> Copied {source_item} to {replica_item}")

    # Remove files and directories in replica that are not in source
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