from glob import glob
from typing import TypedDict


class Sample(TypedDict):
    files: list[str]
    year: str
    data_or_mc: str


# samples to process
samples: dict[str, Sample] = {
    # Data
    "Run2018A_2018": {
        "files": glob(
            "/eos/cms/store/user/ftorresd/HZUpsilonPhotonRun2/NanoAOD/Data/2018/A/*.root"
        ),
        "year": "2018",
        "data_or_mc": "data",
    },
    "Run2018B_2018": {
        "files": glob(
            "/eos/cms/store/user/ftorresd/HZUpsilonPhotonRun2/NanoAOD/Data/2018/B/*.root"
        ),
        "year": "2018",
        "data_or_mc": "data",
    },
    "Run2018C_2018": {
        "files": glob(
            "/eos/cms/store/user/ftorresd/HZUpsilonPhotonRun2/NanoAOD/Data/2018/C/*.root"
        ),
        "year": "2018",
        "data_or_mc": "data",
    },
    "Run2018D_2018": {
        "files": glob(
            "/eos/cms/store/user/ftorresd/HZUpsilonPhotonRun2/NanoAOD/Data/2018/D/*.root"
        ),
        "year": "2018",
        "data_or_mc": "data",
    },
    # MC
    "ggH_HToUps1SG_M125_NNPDF31_TuneCP5_13TeV-powheg-pythia8_2018": {
        "files": glob(
            "/eos/cms/store/user/ftorresd/HZUpsilonPhotonRun2/NanoAOD/MC/2018/ggH_HToUps1SG_M125_NNPDF31_TuneCP5_13TeV-powheg-pythia8/*.root"
        ),
        "year": "2018",
        "data_or_mc": "mc",
    },
    "ggH_HToUps2SG_M125_NNPDF31_TuneCP5_13TeV-powheg-pythia8_2018": {
        "files": glob(
            "/eos/cms/store/user/ftorresd/HZUpsilonPhotonRun2/NanoAOD/MC/2018/ggH_HToUps2SG_M125_NNPDF31_TuneCP5_13TeV-powheg-pythia8/*.root"
        ),
        "year": "2018",
        "data_or_mc": "mc",
    },
    "ggH_HToUps3SG_M125_NNPDF31_TuneCP5_13TeV-powheg-pythia8_2018": {
        "files": glob(
            "/eos/cms/store/user/ftorresd/HZUpsilonPhotonRun2/NanoAOD/MC/2018/ggH_HToUps3SG_M125_NNPDF31_TuneCP5_13TeV-powheg-pythia8/*.root"
        ),
        "year": "2018",
        "data_or_mc": "mc",
    },
    "GluGluHToMuMuG_M125_MLL-0To60_Dalitz_012j_13TeV_amcatnloFXFX_pythia8_PSWeight_2018": {
        "files": glob(
            "/eos/cms/store/user/ftorresd/HZUpsilonPhotonRun2/NanoAOD/MC/2018/GluGluHToMuMuG_M125_MLL-0To60_Dalitz_012j_13TeV_amcatnloFXFX_pythia8_PSWeight/*.root"
        ),
        "year": "2018",
        "data_or_mc": "mc",
    },
    "ZGTo2MuG_MMuMu-2To15_TuneCP5_13TeV-madgraph-pythia8_2018": {
        "files": glob(
            "/eos/cms/store/user/ftorresd/HZUpsilonPhotonRun2/NanoAOD/MC/2018/ZGTo2MuG_MMuMu-2To15_TuneCP5_13TeV-madgraph-pythia8/*.root"
        ),
        "year": "2018",
        "data_or_mc": "mc",
    },
    "ZToUpsilon1SGamma_TuneCP5_13TeV-amcatnloFXFX-pythia8_2018": {
        "files": glob(
            "/eos/cms/store/user/ftorresd/HZUpsilonPhotonRun2/NanoAOD/MC/2018/ZToUpsilon1SGamma_TuneCP5_13TeV-amcatnloFXFX-pythia8/*.root"
        ),
        "year": "2018",
        "data_or_mc": "mc",
    },
    "ZToUpsilon2SGamma_TuneCP5_13TeV-amcatnloFXFX-pythia8_2018": {
        "files": glob(
            "/eos/cms/store/user/ftorresd/HZUpsilonPhotonRun2/NanoAOD/MC/2018/ZToUpsilon2SGamma_TuneCP5_13TeV-amcatnloFXFX-pythia8/*.root"
        ),
        "year": "2018",
        "data_or_mc": "mc",
    },
    "ZToUpsilon3SGamma_TuneCP5_13TeV-amcatnloFXFX-pythia8_2018": {
        "files": glob(
            "/eos/cms/store/user/ftorresd/HZUpsilonPhotonRun2/NanoAOD/MC/2018/ZToUpsilon3SGamma_TuneCP5_13TeV-amcatnloFXFX-pythia8/*.root"
        ),
        "year": "2018",
        "data_or_mc": "mc",
    },
}


# build samples files and descriptions
samples_files = {}
for sample in samples:
    samples_files[sample] = samples[sample]["files"]

data_samples_files = {}
for sample in samples:
    if samples[sample]["data_or_mc"] == "data":
        data_samples_files[sample] = samples[sample]["files"]

mc_samples_files = {}
for sample in samples:
    if samples[sample]["data_or_mc"] == "mc":
        mc_samples_files[sample] = samples[sample]["files"]
