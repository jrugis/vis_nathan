# -*- coding: utf-8 -*-
#
# bin2vtk-all.py

import numpy as np
import os
import subprocess
from evtk.hl import pointsToVTK

import cs

##################################################################
# main program
##################################################################

dist_names = subprocess.check_output("ls *.txt", shell=True).split()

for dist_name in dist_names:
  cell_num = dist_name.split('.')[0][-1]
  mesh_name = 'out_N4_p3-p2-p4-' + cell_num + 'tet.msh'
  print
  print '*** ' + cell_num + ' ***'
  print 'reading mesh file: ' + mesh_name 
  #xyz = np.transpose(cs.get_mesh_coords(mesh_name))
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

  print 'reading data file: ' + dist_name 
  dist = cs.get_data_txt(dist_name)

  # get start and finish indices for a single cycle
  #i_start = 0
  #i_finish = dist.shape[1]-1
  i_start = 55
  i_finish = 340

  # write vtk time series files
  if os.path.isdir(cell_num):
    os.system("rm -rf " + cell_num)
  os.mkdir(cell_num)
  print 'creating vtk files...'
  for i in xrange(i_start, i_finish, 1):
    d = {}
    d["c"] = dist[i, :]
    fname = cell_num + '/' + cell_num + '_' + str(i).zfill(4)
    print xyz[0,:].shape
    print dist[:, i].shape   
    pointsToVTK(fname, xyz[0,:], xyz[1,:], xyz[2,:], data = d)
  print 'max =', '{:0.3f}'.format(dist.max())

