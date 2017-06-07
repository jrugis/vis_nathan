# -*- coding: utf-8 -*-
#
# mat2vtk.py

import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.io as sc
import subprocess
from evtk.hl import pointsToVTK

import cs

##################################################################
# main program
##################################################################

#dist_name = 'calcium_loop_c7.mat'
dist_name = 'calcium_init_c7.mat'
cell_num = '7init'
#dist_key = 'c_loop'
dist_key = 'c_init'
mesh_name = 'out_N4_p3-p2-p4-7tet.msh'

print
print 'reading mesh file: ' + mesh_name 

f1 = open(mesh_name, 'r') # open the mesh file
for line in f1: 
  if line.startswith("$Nodes"): break
pcount = int(f1.next())
xyz = np.empty([3, pcount])
for t in range(pcount):
  v = f1.next().split()
  xyz[0,t] = float(v[1])
  xyz[1,t] = float(v[2])
  xyz[2,t] = float(v[3])
f1.close()
print xyz.shape

print 'reading data file: ' + dist_name 

dist = sc.loadmat(dist_name)
#print 'keys:', dist.keys()
node_data = np.transpose(dist[dist_key])
print node_data.shape
print 'max =', '{:0.3f}'.format(node_data.max())

i_start = 0
i_finish = node_data.shape[0]
node_count = node_data.shape[1]
plt.plot(node_data[:,0:30])
plt.show()

# write vtk time series files
if os.path.isdir(cell_num):
  os.system("rm -rf " + cell_num)
os.mkdir(cell_num)
print 'creating vtk files...'
for i in xrange(i_start, i_finish, 1):
  d = {}
  d["c"] = node_data[i, :]
  fname = cell_num + '/' + cell_num + '_' + str(i).zfill(4)
  #print xyz[0,:].shape
  #print dist[:, i].shape   
  pointsToVTK(fname, xyz[0,:], xyz[1,:], xyz[2,:], data = d)

