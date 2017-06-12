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

mesh_name = 'out_N4_p3-p2-p4-7tet.msh'
ab_name = 'label.mat'
apical_key = 'apical'
basal_key = 'basal'
dist_name = 'calcium_init_c7.mat'
dist_key = 'c_init'
cell_num = '7init'
#dist_name = 'calcium_loop_c7.mat'
#dist_key = 'c_loop'
#cell_num = '7'

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
for line in f1: 
  if line.startswith('"distance to nearest lumen"'): break
for t in range(6): # skip 6 lines
  f1.next()
dnl = np.empty(pcount)
for t in range(pcount):
  v = f1.next().split()
  dnl[t] = float(v[1])
f1.close()
print xyz.shape

print
print 'reading apical/basal file: ' + ab_name 
ab_data = np.zeros([pcount])
ab = sc.loadmat(ab_name)
#print 'keys:', ab.keys()
apical_data = ab[apical_key]
print 'max =', '{:0.3f}'.format(apical_data.max())
print apical_data.shape
for i in range(0,apical_data.shape[0]):
  ab_data[apical_data[i]-1] = 0.5
basal_data = ab[basal_key]
print 'max =', '{:0.3f}'.format(basal_data.max())
print basal_data.shape
for i in range(0,basal_data.shape[0]):
  ab_data[basal_data[i]-1] = 1.0

print 'reading data file: ' + dist_name 
dist = sc.loadmat(dist_name)
#print 'keys:', dist.keys()
node_data = np.transpose(dist[dist_key])
print node_data.shape
print 'max =', '{:0.3f}'.format(node_data.max())
#plt.plot(node_data[:,0:30])
#plt.show()

# write vtk time series files
print 'creating vtk files...'
if os.path.isdir(cell_num):
  os.system("rm -rf " + cell_num)
os.mkdir(cell_num)
i_start = 0
i_finish = node_data.shape[0]
node_count = node_data.shape[1]
for i in xrange(i_start, i_finish, 1):
  d = {}
  d["c"] = node_data[i, :]
  d["dnl"] = dnl
  d["ab"] = ab_data
  fname = cell_num + '/' + cell_num + '_' + str(i).zfill(4)
  #print xyz[0,:].shape
  #print dist[:, i].shape   
  pointsToVTK(fname, xyz[0,:], xyz[1,:], xyz[2,:], data = d)

