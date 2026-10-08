#!/usr/bin/env python3

import sys

for line in sys.stdin:
    words = line.strip().lower().split()

    for word in words:
        print(word, "\t", 1, sep="")
