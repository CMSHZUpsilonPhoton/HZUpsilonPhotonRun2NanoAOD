#!/usr/bin/env bash

conda create -y -c conda-forge -p ./HZUpsilonPhotonRun2NanoAOD_env python=3.9.12 mamba

which conda
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/ftorresd/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/ftorresd/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/home/ftorresd/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/ftorresd/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

conda activate ./HZUpsilonPhotonRun2NanoAOD_env
mamba install -y -c conda-forge --file environment.yml
pdoc hzupsilonphoton --math -o ./docs
