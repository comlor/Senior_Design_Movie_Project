#!/usr/bin/env python

import sys

for input in sys.stdin:
    input = input.strip()
    frames = input.split()

    index = 0
    while index < len(frames):
        start = index
        end = index + 1
        rid = index + 2
        file_name = index + 3
        print(str(frames[start]) + "\t" + str(frames[end]) + "\t" + str(frames[rid]) + "\t" + str(frames[file_name]))
        index += 4
