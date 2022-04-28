# H/Z --> Upsilon + Photon - Run 2 - NanoAOD


## Setup
Assuming a CC7/Ubuntu 20.04 machine with Miniconda installed.

Install miniconda:

https://docs.conda.io/en/latest/miniconda.html

```bash
conda create -y -c conda-forge -p ../HZUpsilonPhotonRun2NanoAOD_env python=3.9.12 mamba
conda activate ../HZUpsilonPhotonRun2NanoAOD_env
mamba install -y -c conda-forge --file environment.yml
pre-commit install
```

## Load env

```
conda activate ./env
```
## Run

How to run the code:

`./run_analysis --help`

Usual workflow:

- Clear output buffers

`./run_analysis.py clear`

- Generator level analysis (filtering, getting total number of events, polarization, ...)

`./run_analysis.py gen`

- Main analysis code for signal selection

`./run_analysis.py main`

- Merge the many outputs [buffers], per sample and per process [Data or MC sample]

`./run_analysis.py merge`

- Produce plots

`./run_analysis.py plot`

***To run the whole chain in a single shot:***

`./run_analysis.py all`

### Remote

It is possible to run the analysis code, on a remote machine, from you local computer. It needs SSH passwordless login available.

More information:

```bash
./run_remote.py --help
```

Example:

```bash
./run_remote.py --outputs --uerj-usr lxplus ftorresd /data/ftorresd/HZUpsilonPhotonRun2NanoAOD_working_area/HZUpsilonPhotonRun2NanoAOD
```

## Notes and tips

### Produce a new `environment.yml`

```bash
conda env export --no-builds  | grep -v "prefix" > environment.yml
```
