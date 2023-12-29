from register import main, readfile
from auto_copy import main_copy
import threading

data = readfile("settings.json")

auto_copy = data["AUTO_COPY_CODES"]

if auto_copy:
    thread_one = threading.Thread(target=main_copy)
    thread_one.start()

while True:
    thread_two = threading.Thread(target=main)
    thread_two.start()
    thread_two.join()
