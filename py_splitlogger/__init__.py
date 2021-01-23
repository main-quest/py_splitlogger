import os
import sys
import time
from threading import Thread


# Constantly writing to terminal from file
# Tried other approaches for splitting stdout/stderr and failed miserably
class SplitLogger(object):
    def __init__(self, file):
        self.file = file
        self.terminal = sys.stdout
        self.lines_read_so_far = 0
        self.released = False

        fs_write = open(self.file, 'w')
        sys.stderr = fs_write
        sys.stdout = fs_write

        self.t = Thread(target=self.update_terminal)
        self.t.start()

    def update_terminal(self):
        last_iter = False
        last_known_file_size = 0
        while True:
            lines_read_so_far_local = 0
            stat = os.stat(self.file)
            if stat.st_size != last_known_file_size:
                last_known_file_size = stat.st_size
                with open(self.file, 'r') as fs_read:
                    while True:
                        line = fs_read.readline()
                        if line is None or line == "":
                            break

                        lines_read_so_far_local += 1
                        if lines_read_so_far_local <= self.lines_read_so_far:
                            continue

                        self.terminal.write(line)
                        self.lines_read_so_far += 1

            if last_iter:
                break

            if self.released:
                last_iter = True
                continue

            time.sleep(.1)

    def release(self):
        self.released = True
