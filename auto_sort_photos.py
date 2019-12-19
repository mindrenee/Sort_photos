#!/usr/bin/python

import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import re
from pathlib import Path

track_path = "/home/renee/Pictures/"

def main():
    print("Sort photos from camera")
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_created = on_created
    my_event_handler.on_moved = on_moved
    my_event_handler.on_deleted = on_deleted
    go_recursively = True
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
    print("Move photo" + basefile)
    create_date = os.path.getctime(file)
    year = time.strftime('%Y', time.localtime(create_date))
    print("Year: ", year)
    month = time.strftime('%B', time.localtime(create_date))
    print("Month: ", month)
    day = time.strftime('%d', time.localtime(create_date))
    print("Day: ", day)
    if not os.path.exists(track_path + year + "/" + month + "/" + day):
        os.makedirs(track_path + year + "/" + month + "/" + day)
    shutil.move(file, track_path + year + "/" + month + "/" + day + "/" + basefile)

def creation_date(file):
    stat = os.stat(file)
    try:
        return stat.st_birthtime
    except AttributeError:
        return stat.st_mtime

def on_created(event):
    file = event.src_path
    print(f"{event.src_path} has been created")
    move_file(file)

def on_moved(event):
    print(f"{event.src_path} has been moved")

def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")


main()
