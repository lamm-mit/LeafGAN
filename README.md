# LeafGAN
**Using StyleGAN to generate nature-inspired structures in 2 and 3 dimensions**
Sabrina Shen, Markus Buehler

Abstract: *Nature-inspired material design is driven by superior properties found in natural architected materials and enabled by recent developments in additive manufacturing and machine learning. Existing approaches to push design beyond biomimicry typically use supervised deep learning algorithms to predict and optimize properties based on experimental or simulation data. However, these methods constrain generated material designs to abstracted labels and to “black box” outputs that are only indirectly manipulable. Here we report an alternative approach using an unsupervised generative adversarial network (GAN) model. Training the model on unlabeled data constructs a latent space free of human intervention, which can then be explored through seeding, image encoding, and vector arithmetic to control specific parameters of de novo generated material designs and to push them beyond training data distributions for broad applicability. We illustrate this end-to-end with new materials inspired by leaf microstructures, showing how biological 2D structures can be used to develop novel architected materials in 2 and 3 dimensions. We further utilize a genetic algorithm to optimize generated microstructures for mechanical properties, operating directly on the latent space. This approach allows for transfer of information across manifestations using the latent space as mediator, opening new avenues for exploration of nature-inspired materials.*

## Getting Started
Code and instructions for training the StyleGAN architecture can be found [here](https://github.com/NVlabs/stylegan2-ada-pytorch). Once trained, images can be seeded and processed into 2D structures with leafgan_GA.ipynb.
