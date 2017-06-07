#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np

import cs

# parameters
fname = "calcium_cell3.txt"

# input mesh data
print "input mesh data file"
cdata = cs.get_data_txt(fname)

plt.plot(cdata[55:340,0:100])
plt.show()
