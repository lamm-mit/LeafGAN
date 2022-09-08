from math import *
from random import random
import img2lat_functions

import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image
import os

#Lattice param

#spacing of lattice
r0_lattice=1.12246
#r0_lattice=.93*2


#hexagonal
r0_lattice_x=r0_lattice*2
r0_lattice_y=r0_lattice * sqrt(3. )
#r0_lattice_x=2.
#r0_lattice_y=2

#2 atoms per unit cell
ucellsize=4
ux = [0, r0_lattice/2,r0_lattice, r0_lattice*3/2]
uy = [0, r0_lattice*sqrt(3)/2.,0, r0_lattice*sqrt(3)/2.   ]

path='C:/Users/sabri/Desktop/LAMM/leaf_stylegan/GA/img/880/'
dest='C:/Users/sabri/Desktop/LAMM/leaf_stylegan/GA/img/880/coord/'

i=0
for im_path in os.listdir(path):
    
    #Define paths
    source_path=path+im_path
    dest_path=dest+str(i)+'.coor'
    
    #Check for border connectivity
    if img2lat_functions.check_border(source_path):
        #build lattice
        atomlist, bondlist, anglelist, x_min, x_max, y_min, y_max = img2lat_functions.build_lattice(source_path, rotate=False)
        #write coordinate file
        img2lat_functions.write_coord(atomlist, dest_path, x_min, x_max, y_min, y_max)

    i=i+1        