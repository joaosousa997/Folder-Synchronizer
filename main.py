from logic import sync_folders, parsing
import time


def main():
    print(">>> Starting...")
    source, replica, interval = parsing()
    while True:
        sync_folders(source, replica)
        print(f">>> Ended sync, waiting for user defined interval: {interval} seconds")
        time.sleep(interval)


if __name__ == "__main__":
    main()
