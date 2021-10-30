from glob import glob

# samples to process
samples_files = {
    # Data
    "Run2018A": glob(
        "/eos/cms/store/user/ftorresd/HZUpsilonPhotonRun2/NanoAOD/Data/2018/A/*.root"
    ),
    "Run2018B": glob(
        "/eos/cms/store/user/ftorresd/HZUpsilonPhotonRun2/NanoAOD/Data/2018/B/*.root"
    ),
    "Run2018C": glob(
        "/eos/cms/store/user/ftorresd/HZUpsilonPhotonRun2/NanoAOD/Data/2018/C/*.root"
    ),
    "Run2018D": glob(
        "/eos/cms/store/user/ftorresd/HZUpsilonPhotonRun2/NanoAOD/Data/2018/D/*.root"
    ),
    # MC
    "ZToUpsilon1SGamma": glob(
        "/eos/cms/store/user/ftorresd/HZUpsilonPhotonRun2/NanoAOD/MC/2018/ZToUpsilon1SGamma_TuneCP5_13TeV-amcatnloFXFX-pythia8/*.root"
    ),
}

samples_descriptions = {
    # Data
    "Run2018A": {
        "year": "2018",
        "data_or_mc": "data",
    },
    "Run2018B": {
        "year": "2018",
        "data_or_mc": "data",
    },
    "Run2018C": {
        "year": "2018",
        "data_or_mc": "data",
    },
    "Run2018D": {
        "year": "2018",
        "data_or_mc": "data",
    },
    # MC
    "ZToUpsilon1SGamma": {
        "year": "2018",
        "data_or_mc": "mc",
    },
}
