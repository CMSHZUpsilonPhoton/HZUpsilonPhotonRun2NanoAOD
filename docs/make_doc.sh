#!/usr/bin/env bash

conda create -y -c conda-forge -p ./HZUpsilonPhotonRun2NanoAOD_env python=3.9.12 mamba
conda activate ./HZUpsilonPhotonRun2NanoAOD_env
mamba install -y -c conda-forge --file environment.yml
pdoc hzupsilonphoton --math -o ./docs
