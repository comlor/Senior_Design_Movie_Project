#!/usr/bin/env python

import sys

for input in sys.stdin:
    input = input.strip()
    frames = input.split()

    index = 0
    while index < len(frames):
        start = index
        end = index + 1
        print(str(frames[start]) + "\t" + str(frames[end]))
        index += 2
