# LeafGAN
**Using StyleGAN to generate nature-inspired structures in 2 and 3 dimensions**

Sabrina Shen, Markus Buehler

Shen, S.C., Buehler, M.J. Nature-inspired Architected materials using unsupervised deep learning. Accepted (2022).

Abstract: *Nature-inspired material design is driven by superior properties found in natural architected materials and enabled by recent developments in additive manufacturing and machine learning. Existing approaches to push design beyond biomimicry typically use supervised deep learning algorithms to predict and optimize properties based on experimental or simulation data. However, these methods constrain generated material designs to abstracted labels and to “black box” outputs that are only indirectly manipulable. Here we report an alternative approach using an unsupervised generative adversarial network (GAN) model. Training the model on unlabeled data constructs a latent space free of human intervention, which can then be explored through seeding, image encoding, and vector arithmetic to control specific parameters of de novo generated material designs and to push them beyond training data distributions for broad applicability. We illustrate this end-to-end with new materials inspired by leaf microstructures, showing how biological 2D structures can be used to develop novel architected materials in 2 and 3 dimensions. We further utilize a genetic algorithm to optimize generated microstructures for mechanical properties, operating directly on the latent space. This approach allows for transfer of information across manifestations using the latent space as mediator, opening new avenues for exploration of nature-inspired materials.*

## Getting Started
1) Code and instructions for training the StyleGAN architecture can be found [here](https://github.com/NVlabs/stylegan2-ada-pytorch) or in *stylegan2-ada-pytorch-main*. Training images can be found in the *leaf* directory.
2) Once trained, generate images based on random seeds with:
``` 
python generate.py --outdir=./MD/5000-6000/images/ --trunc=1.0 --seeds=5000-9999 --network=./leaf-network-snapshot.pkl
```
Process images into unit cells with:
```
names, seeds, density=ImageTools.remove_small (path, dest, 20000, 1024,mirrorcopy=1, ressfinal=256, filt1=32, thicken=2, rect=0)
```
3) Gradient images can be generated with:
``` 
python generate.py --outdir=./output_leaf/gradient/frames/ --trunc=.7 --process="interpolation" --interpolation="2Dpoint_CSV" --csvfile=./gradient.csv --frames=40 --random_seed=0 --seeds=441,593,863 --network=./leaf-network-snapshot.pkl
```
after defining a CSV file with coordinates defining the desired movement in latent space. 
4) After processing into unit cells, gradient images can be stacked into an STL with:
```
vox1=vox2STL.img2vox('./output_leaf/gradient/processed/', 'png')

vox2STL.vox2stl(vox1, filename='leaf_architected')
```

6) Further detail and additional operations can be found in *SG2_leaf.ipynb*.

## Simulation and Analysis
To run a coarse-grained simulation of a generated structure:
1) Run *img2lat.py* to create a coarse-grained lattice from the image of a structure (define the image and destination paths within the code).
2) Use LAMMPS to run the compression simulation. Example LAMMPS file with our parameters can be found in *compression.crack*.
3) Use *MD_analysis.ipynb* to extract stress-strain curves and moduli from simulation results.
4) Train a convolutional neural network (CNN) on simulation results with *leafgan_cnn.ipynb*
5) Run a genetic algorithm (GA) with the trained CNN as a surrogate model with *leafgan_GA.ipynb* to generate optimized structures. 

