#!/usr/bin/python

import numpy as np

# parameters
fname = "calcium_cell3"

# input
print "input mesh data file"
f1 = open(fname + ".txt", 'r')

i = 0
for line in f1:
  i = i + 1
  vals = line.split()
f1.close()

print "rows:", i
print "columns:", len(vals)
print vals[0]
print vals[len(vals) - 1]

