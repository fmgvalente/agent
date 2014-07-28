import sys
import os.path
import time
import subprocess

watched_dir = sys.argv[1]
watched_file = watched_dir+"/_state_finished"

while not os.path.exists(watched_file):
    time.sleep(1)

if os.path.isfile(watched_file):
    subprocess.Popen(["agent", "-ud", watched_dir])
else:
    raise ValueError("%s isn't a file!" % file_path)