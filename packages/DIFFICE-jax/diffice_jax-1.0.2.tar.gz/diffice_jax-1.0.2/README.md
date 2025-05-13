# DIFFICE_jax
A DIFFerentiable neural-network solver for data assimilation of ICE shelves written in JAX. 

<!-- index.rst session1 start -->

## Introduction 
`DIFFICE_jax` is a Python package that solves the depth-integrated Stokes equation for **ice shelves**, and can be adopted for **ice sheets** by modifying the partial differential equations (PDE) in the neural network loss function. It uses PDEs to interpolate descretized remote-sensing data into meshless and differentible functions, and infer ice shelves' viscosity structure via back-propagation and automatic differentiation (AD). The algorithm is based on physics-informed neural networks [(PINNs)](https://www.sciencedirect.com/science/article/abs/pii/S0021999118307125) and implemented in [JAX](https://jax.readthedocs.io/en/latest/index.html). The `DIFFICE_jax` package involves several advanced features in addition to vanilla PINNs algorithms, including collocation points resampling, non-dimensionalization of the data adnd equations, extended-PINNs [(XPINNs)](https://github.com/YaoGroup/DIFFICE_jax/blob/main/docs/source/XPINNs.md) (see figure below), viscosity exponential scaling function, which are essential for accurate inversion. The package is designed to be user-friendly and accessible for beginners. The Github respository also provides **Colab Notebooks** for both the synthetic and real ice-shelf examples in the [`tutorial`](https://github.com/YaoGroup/DIFFICE_jax/tree/main/tutorial) and [`examples`](https://github.com/YaoGroup/DIFFICE_jax/tree/main/examples) folders, respectively.

<br />

<p align="center" style="margin-top:-2rem;margin-bottom:-2rem">
    <img alt="xpinns." width="90%" src="https://github.com/YaoGroup/DIFFICE_jax/raw/main/docs/figure/xpinns.png"> 
</p>

<br />

## Statement of Needs
This package provides a neural network-based approach for solving inverse problems in glaciology, specifically for estimating effective ice viscosity from high-resolution remote sensing data. Ice viscosity is a key parameter for predicting ice-shelf dynamics, but direct in-situ measurements of viscosity across Antarctica are impractical. Traditional adjoint methods require deriving additional equations and applying regularization techniques to handle noisy data. In contrast, neural networks can inherently de-noise while solving the inverse problem without explicit regularization. Finally, this solver is fully differentiable using automatic differentiation (AD), eliminating the need for manual adjoint derivations and enabling efficient exploration of complex PDEs, including anisotropic ice flow models. This neural network-based method offers a flexible framework for solving inverse problems in glaciology.


## Installation

The build of the code is tesed on Python version (3.9, 3.10 and 3.11) and JAX version (0.4.20, 0.4.23, 0.4.26)

You can install the package using pip as follows:
```python
python -m pip install DIFFICE_jax
```

<!-- stop-session1 -->


## Documentation

Find the full documentation [here](https://diffice-jax.readthedocs.io/en/latest/). We provided the documentation for both the algorithms (e.g., cost functions) and the mathematical formulation (e.g., PDEs and boundary conditions) for the data assimilation of ice shelves.

## Getting Started with a Tutorial using Synthetic Data [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YaoGroup/DIFFICE_jax/blob/main/tutorial/colab/train_syndata.ipynb)
We highly recommend new users to get familar with the software by reading the document and playing with the synthetic example prepared in the [`tutorial`](https://github.com/YaoGroup/DIFFICE_jax/tree/main/tutorial) folder. The synthetic example allow users to generate the synthetic data of velocity and thickness of an ice-shelf flow in an idealized rectangular domain with a prescribed viscosity profile. Users can use the Colab Notebook to infer the viscosity from the synthetic velocity and thickness, and compare with the given synthetic viscosity to validate the PINN result.


## Real-data Examples 
The inversion codes with the real velocity and thickness data for **four** different ice shelves surrounding the Antarctica are provided in the [`examples`](https://github.com/YaoGroup/DIFFICE_jax/tree/main/examples) folders. For each example code, the corresponding implemented features and the ice-shelf dataset it can analyze are listed in the table below. The original source and the required format for the datasets are described [here](https://github.com/YaoGroup/DIFFICE_jax/tree/main/docs/source/Data.md). In the [paper](https://github.com/YaoGroup/DIFFICE_jax/tree/main/paper.md), we
summarized **six algorithm features** of the `DIFFICE_jax` package, (1)-(6), beyond the vanilla PINNs code.  

| Example codes  | Algorithm feature # | Ice shelf |
| ------------- | ------------- | ------------- |
| train_pinns_iso | (1), (2), (3), (4) | Amery, Larsen C, synthetic |
| train_pinns_aniso | (1), (2), (3), (4), (6)  | Amery, Larsen C|
| train_xpinns_iso  | (1), (2), (3), (4), (5)  | Ross, Ronne-Filchner|
| train_xpinns_aniso  | (1), (2), (3), (4), (5), (6)   |  Ross, Ronne-Filchner|

 <br />
 
## Google Colab
Apart from the Python scripts to run locally, we also provide **Colab Notebooks** for both the synthetic and real
ice-shelf examples, provided in the [`tutorial`](https://github.com/YaoGroup/DIFFICE_jax/tree/main/tutorial) and [`examples`](https://github.com/YaoGroup/DIFFICE_jax/tree/main/examples) folders, respectively. 

 <br />
 
## Diagram of Algorithm and Results.
<p align="center" style="margin-top:-2rem;margin-bottom:-2rem">
    <img alt="setups" width="90%" src="https://github.com/YaoGroup/DIFFICE_jax/raw/main/docs/figure/PINN_setup.png"> 
</p>

<!-- index.rst session2 start -->

## Contributors
This package is written by Yongji Wang and maintained by Yongji Wang (yongjiw@stanford.edu) and Ching-Yao Lai (cyaolai@stanford.edu). If you have questions about this code and documentation, or are interested in contributing the development of the `DIFFICE_jax` package, please see the contributing [guidelines](https://github.com/YaoGroup/DIFFICE_jax/tree/main/Contribution.md) for information on submitting issues and pull requests.

## License
`DIFFICE_jax` is an open-source software. All code within the project is licensed under the MIT License. For more details, please refer to the [LICENSE](https://github.com/YaoGroup/DIFFICE_jax/tree/main/LICENSE) file.

## Citation
Wang, Y. and Lai, C.Y., 2025. DIFFICE-jax: Differentiable neural-network solver for data assimilation of ice shelves in JAX. Journal of Open Source Software, 10(109), p.7254.
```
@article{wang2025diffice,
  title={DIFFICE-jax: Differentiable neural-network solver for data assimilation of ice shelves in JAX},
  author={Wang, Yongji and Lai, Ching-Yao},
  journal={Journal of Open Source Software},
  volume={10},
  number={109},
  pages={7254},
  year={2025}
}
```

Wang, Y., Lai, C.Y., Prior, D.J. and Cowen-Breen, C., 2025. Deep learning the flow law of Antarctic ice shelves. Science, 387(6739), pp.1219-1224.
```
@article{wang2025deep,
  title={Deep learning the flow law of Antarctic ice shelves},
  author={Wang, Yongji and Lai, Ching-Yao and Prior, David J and Cowen-Breen, Charlie},
  journal={Science},
  volume={387},
  number={6739},
  pages={1219--1224},
  year={2025},
  publisher={American Association for the Advancement of Science}
}
```

<!-- stop-session2 -->

