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

mesh_names = ['out_N4_p3-p2-p4-1tet.msh', 'out_N4_p3-p2-p4-2tet.msh']
dist_name = 'c_tot.mat'
calcium_key = 'c_tot'
#cell_num = '7init'

print
print 'reading data file: ' + dist_name 
dist = sc.loadmat(dist_name)
#print 'keys:', dist.keys()
node_data = np.transpose(dist[calcium_key])
#print node_data.shape
#print 'max =', '{:0.3f}'.format(node_data[0,0].max())
#plt.plot(node_data[0,0][100,:])
#plt.plot(node_data[0,1][100,:])
#plt.show()

for i in range(len(mesh_names)):
  print 'reading mesh file: ' + mesh_names[i]
  f1 = open(mesh_names[i], 'r') # open the mesh file
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
  #print xyz.shape

  # write vtk time series files
  print 'creating vtk files...'
  cell_dir = 'cell' + str(i)
  if os.path.isdir(cell_dir):
    os.system("rm -rf " + cell_dir)
  os.mkdir(cell_dir)
  i_start = 0
  i_finish = node_data[0,i].shape[1]
  #print i_finish
  node_count = node_data[0,i].shape[0]
  #print node_count
  for ii in xrange(i_start, i_finish, 1):
    d = {}
    d["c"] = node_data[0,i][:,ii]
    #d["dnl"] = dnl
    fname = cell_dir + '/' + cell_dir + '_' + str(ii).zfill(4)
    pointsToVTK(fname, xyz[0,:], xyz[1,:], xyz[2,:], data = d)


