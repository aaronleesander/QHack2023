# QHack2023

This repository was created for the QHack2023 Hackathon.

This project was an equal collaboration between Lion Frangoulis (lion.frangoulis@tum.de), Cristian Emiliano Godinez Ramirez (cristian.godinez@tum.de), Emily Haworth (ge96puk@mytum.de),
and Aaron Sander (aaron.sander@tum.de) from the Technical University of Munich.

A detailed report on this project can be found in the report folder.

## Abstract

In this project, we explore the challenges of simulating noisy quantum algorithms, which are known to require significant computational resources. We address this issue by leveraging the GPU tools available in Xanadu's PennyLane-Lightning-GPU and NVidia's cuQuantum SDK, which enable us to scale up our simulations and gain deeper insights into the impact of noise on quantum algorithms. Our analysis sheds light on the general effects of noise on simulation and identifies areas where it can accelerate the simulation of open quantum systems and ground state optimization. Through our work, we hope to contribute to a better understanding of how to effectively simulate noisy quantum algorithms, which could have far-reaching implications for quantum computing and finding NISQ-era use cases.

## Dependencies

This project was created using Python 3.11 and Jupyter Notebooks.
The project primarily uses PennyLane-Lightning-GPU which is dependent on the NVidia cuQuantum SDK which require access to a CUDA 11.0 capable GPU.

This project was run on the Cyxtera/Run:ai cluster using NVidia A100 GPUs.
This access was given to us as a power-up from the QHack Coding Competition for being in the top 24 teams.

More information can be found at

PennyLane-Lightning: https://github.com/PennyLaneAI/pennylane-lightning

PennyLane-Lightning-GPU: https://github.com/PennyLaneAI/pennylane-lightning-gpu

NVidia cuQuantum: https://github.com/NVIDIA/cuQuantum and https://developer.nvidia.com/cuquantum-sdk
