# HZ --> Upsilon + Photon - Run 2 - NanoAOD


## Setup
Assuming a CC7 machine with miniconda installed.

Install miniconda:

https://docs.conda.io/en/latest/miniconda.html

```bash
conda create -y -c conda-forge -p ../HZUpsilonPhotonRun2NanoAOD_env python=3.9.12 mamba
conda activate ../HZUpsilonPhotonRun2NanoAOD_env
mamba install -y -c conda-forge --file requirements.txt
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

***To run the whole chain in a single shot:***

`./run_analysis.py all`

## Notes and tips

### How to open `.hist` files

```python
from coffea.util import load
import hist
load('outputs/buffer/cutflow.hist')
```
