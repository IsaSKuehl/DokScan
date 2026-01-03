import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .processor import process_file
from .config import load_config
import asyncio
import logging

config = load_config()
logging.basicConfig(level=config['logging_level'])

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(('.pdf', '.jpg', '.png', '.tiff')):
            # Wait for file to be stable
            time.sleep(5)  # Simple wait, could be improved
            asyncio.run(process_file(event.src_path, config))

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(FileHandler(), config['hotfolder_path'], recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()