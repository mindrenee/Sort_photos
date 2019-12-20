#!/usr/bin/python

import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import re
from pathlib import Path
import exifread
from PIL import Image
from datetime import datetime

track_path = "/home/renee/Pictures/"

def main():
    print("Sort photos from camera")
#    patterns = [".nef", ".jpeg", ".jpg", ".raw", ".NEF", ".JPG"]
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_created = on_created
    my_event_handler.on_moved = on_moved
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    go_recursively = False
    my_observer = Observer()
    my_observer.schedule(my_event_handler, track_path, recursive=go_recursively)
    my_observer.start()
    try:
         while True:
             time.sleep(1)
    except KeyboardInterrupt:
         my_observer.stop()
         my_observer.join()

def move_file(file):
    basefile = os.path.basename(file)
    create_date = creation_date(file)
    year = create_date.strftime('%Y')
    print("Year: ", year)
    month = create_date.strftime('%B')
    print("Month: ", month)
    day = create_date.strftime('%d')
    print("Day: ", day)
    if not os.path.exists(track_path + year + "/" + month + "/" + day):
        os.makedirs(track_path + year + "/" + month + "/" + day)
    shutil.move(file, track_path + year + "/" + month + "/" + day + "/" + basefile)

def creation_date(file):
    f = open(file, 'rb')
    tags = exifread.process_file(f)
    date_original = tags['EXIF DateTimeOriginal']
    date_format = datetime.strptime(str(date_original), '%Y:%m:%d %H:%M:%S')
    return date_format

def on_created(event):
    file = event.src_path
    print(f"{event.src_path} has been created")
    move_file(file)

def on_moved(event):
    print(f"{event.src_path} has been moved")

def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")

def on_modified(event):
    print(f"hey buddy, {event.src_path} has been modified")

main()
