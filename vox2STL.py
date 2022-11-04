#Michael Hsu, LAMM/MIT, 2021

#Convert a stack of images into an STL file for additive manufacturing

#Hsu, Y., Yang, Z., Buehler, M.J. Generative design, manufacturing, and molecular modeling of 3D architected materials based on natural language input. APL Materials 10:041107 (2022).

import numpy as np
import os
import trimesh  
import time, warnings
from PIL import Image
import glob
import matplotlib.pyplot as plt

def img2vox(loc, end='png'):
    vox = []
    imgs = sorted(glob.glob(loc+'/*.'+end), key=lambda x: (len(x), x))

    print('found',len(imgs),'images.',imgs)
    for i in imgs:
        new_frame = Image.open(i).convert('RGB').convert('L')
        vox.append(np.array(new_frame))

    return np.array(vox)


def vox2stl(vox, loc='.', filename='', save=True, smooth=False):
    mesh = trimesh.voxel.ops.matrix_to_marching_cubes(vox)

    if smooth:
        print ("Smoothing: on")
        
        #mesh = trimesh.smoothing.filter_humphrey(mesh)
        
        #trimesh.smoothing.filter_mut_dif_laplacian(mesh, lamb=0.5, iterations=10, volume_constraint=True, laplacian_operator=None)
        mesh=  trimesh.smoothing.filter_mut_dif_laplacian(mesh, lamb=0.85, iterations=20)
        

    mesh.rezero()
    if save:

        from time import strftime
        stamp = strftime("%m_%d_%H_%M")
        os.makedirs(loc, exist_ok=True)
        mesh.export(loc+'/'+filename+'_'+stamp+'.stl')
        print('save stl model to {}'.format(loc+'/'+filename+'.stl'))

# here are four basic logical operations that can be applied to voxels

# return a vox that vox1 OR vox2 exist (A||B) 
def union(vox1, vox2): 
    return np.logical_or(vox1, vox2)

# return a vox that EITHER only vox1 OR vox2 exists (A||B-A&&B)
def xor(vox1, vox2):
    return np.logical_xor(vox1, vox2)

# return a vox that both vox1 exists BUT vox2 does not (A-B) 
def substraction(vox1, vox2):
    return np.logical_xor(np.logical_or(vox1, vox2), vox2)

# return a vox that vox1 and vox2 BOTH exist (A&&B) 
def intersection(vox1, vox2):
    return np.logical_and(vox1, vox2)

# return a vox inverse to the original (B!=A) 
def inverse(vox):
    return np.logical_not(vox)

def repeat(vox, repeatance_array):
    return np.tile(vox, repeatance_array)*1


def vox2img(vox, loc='.', filename=''):
    
    from time import strftime
    stamp = strftime("%m_%d_%H_%M")
    os.makedirs(loc+'/'+filename+'_img/', exist_ok=True)
    for i in range(vox.shape[0]):
        temp_img=vox[i]
        plt.imsave(loc+'/'+filename+'_img/'+filename+'_'+stamp+'_'+str(i)+'.png', temp_img, cmap='gray')
        from IPython import display
        display.clear_output(wait=True)
        plt.imshow(temp_img, cmap='gray')    
        plt.axis('off')
        plt.title(str(i))
        plt.show()
    
    print('save stl model as a stack of images into {}'.format(loc+'/'+filename+'_img/'))

def vox2npy(vox, loc='.', filename=''):
    from time import strftime
    stamp = strftime("%m_%d_%H_%M")
    os.makedirs(loc, exist_ok=True)
    np.save(loc+'/'+filename+'_'+stamp+'.npy', vox)
    print('save stl model as a 3D array to {}'.format(loc+'/'+filename+'_'+stamp+'.npy'))

def npy2vox(filename=''):
    return np.load(filename)*1