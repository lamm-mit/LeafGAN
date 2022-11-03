# LeafGAN
**Using StyleGAN to generate nature-inspired structures in 2 and 3 dimensions**

Sabrina Shen, Markus Buehler

Shen, S.C., Buehler, M.J. Nature-inspired Architected materials using unsupervised deep learning. Accepted (2022).

Abstract: *Nature-inspired material design is driven by superior properties found in natural architected materials and enabled by recent developments in additive manufacturing and machine learning. Existing approaches to push design beyond biomimicry typically use supervised deep learning algorithms to predict and optimize properties based on experimental or simulation data. However, these methods constrain generated material designs to abstracted labels and to “black box” outputs that are only indirectly manipulable. Here we report an alternative approach using an unsupervised generative adversarial network (GAN) model. Training the model on unlabeled data constructs a latent space free of human intervention, which can then be explored through seeding, image encoding, and vector arithmetic to control specific parameters of de novo generated material designs and to push them beyond training data distributions for broad applicability. We illustrate this end-to-end with new materials inspired by leaf microstructures, showing how biological 2D structures can be used to develop novel architected materials in 2 and 3 dimensions. We further utilize a genetic algorithm to optimize generated microstructures for mechanical properties, operating directly on the latent space. This approach allows for transfer of information across manifestations using the latent space as mediator, opening new avenues for exploration of nature-inspired materials.*

## Getting Started
Code and instructions for training the StyleGAN architecture can be found [here](https://github.com/NVlabs/stylegan2-ada-pytorch). Once trained, simple operations for seeding images, processing into 2D structures, style mixing, creating STLs etc. can be found in *SG2_leaf.ipynb*.

## Simulation and Analysis
Code for creating coarse-grained models of structures can be found in *img2lat.py*. *MD_analysis.ipynb* contains code for extracting modulus from simulation results. *leafgan_cnn.ipynb* and *leafgan_GA.ipynb* contain code for constructing and training a convolutional neural network for predicting modulus and a genetic algorithm for optimizing structures, respectively. 
