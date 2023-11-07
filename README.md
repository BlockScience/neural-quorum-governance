# neural-quroum-governance

Repository for an cadCAD demo for Neural Quorum Governance

![Collage](assets/collage_nqg_demo.png "Title")
*Visualizations from simulation-generated data by using this repo.*

## Introduction 

Neural Governance is a framework for defining a User's Voting Power for a given project by using the abstractions of Voting Neurons, which are arranged and aggregated together in layers. Each Voting Neuron represents an independent piece of logic on how a User's Voting Power should be defined and consists of an Oracle Function and a Weighting Function, whereas the first encodes the core logic and the second encodes how it should be weighted. The outputs from all Voting Neurons are aggregated together in layers, and then passed as an input to the next layer, until a final value is reached. 

This repository provides a cadCAD simulation for generating synthetic datasets for both user behavior (eg. what drives one to vote, delegate and trust?) and for the resulting outcomes from using pre-defined NQG parametrizations.

![Collage](assets/nqg.png "Title")
*Neural Governance in a glance. In this stylized implementation, User Vote Power starts with a default voting power (such as zero), which gets replaced by the voting power that is computed by aggregating the Reputation and Past Voting Neurons weighted outputs. This is then fed to the Trust Neuron, which will then provide the Final User Vote Power.*


## How to run it

- Option 1 (CLI): Just pass `python -m nqg_model`
This will generate an pickled file at `data/simulations/` using the default single run
system parameters & initial state.
    - To perform a multiple run, pass `python -m nqg_model -e`
- Option 2 (cadCAD-tools easy run method): Import the objects at `nqg_model/__init__.py`
and use them as arguments to the `cadCAD_tools.execution.easy_run` method. Refer to `nqg_model/__main__.py` to an example.
- Option 3 (Notebooks)
  - Use any of the provided notebooks on the `notebooks/` folder.

## What is cadCAD

### Installing cadCAD for running this repo

#### 1. Pre-installation Virtual Environments with [`venv`](https://docs.python.org/3/library/venv.html) (Optional):
It's a good package managing practice to create an easy to use virtual environment to install cadCAD. You can use the built in `venv` package.

***Create** a virtual environment:*
```bash
$ python3 -m venv ~/cadcad
```

***Activate** an existing virtual environment:*
```bash
$ source ~/cadcad/bin/activate
(cadcad) $
```

***Deactivate** virtual environment:*
```bash
(cadcad) $ deactivate
$
```

#### 2. Installation: 
Requires [>= Python 3.6](https://www.python.org/downloads/) 

**Install Using [pip](https://pypi.org/project/cadCAD/)** 
```bash
$ pip3 install cadcad==0.4.28
```

**Install all packages with requirement.txt**
```bash
$ pip3 install -r requirements.txt