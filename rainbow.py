#!/usr/bin/python

colors = [(15, 0, 0), \
(15, 10, 0), \
(15, 15, 0), \
(0,   0,   15), \
(0,   8, 0), \
(4,  14, 13), \
(14, 8, 14) ]

import rgb_strand

NUM_BULBS = 100

strand = rgb_strand.RGBStrand(NUM_BULBS)
strand.set_strand_pattern(colors)
strand.set_strand_brightness(200)
