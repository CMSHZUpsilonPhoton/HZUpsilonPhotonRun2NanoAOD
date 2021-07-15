# HZ --> Upsilon + Photon - Run 2 - NanoAOD


## Setup
Assuming a CC7 machine with miniconda installed.

Install miniconda:

https://docs.conda.io/en/latest/miniconda.html

```
conda create -y -c conda-forge -p HZUpsilonPhotonRun2NanoAODEnv --file requirements.txt
```

## Load env

```
conda activate ./HZUpsilonPhotonRun2NanoAODEnv
```

or simply

```
source activate_env.sh
```

## Run

```
python run_analyzer.py
```

