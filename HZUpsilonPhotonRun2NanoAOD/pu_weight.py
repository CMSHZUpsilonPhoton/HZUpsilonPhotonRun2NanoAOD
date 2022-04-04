import numpy as np
import uproot

pu_hist = {}
pu_hist["data"] = {}
pu_hist["data"]["minus"] = {}
pu_hist["data"]["nominal"] = {}
pu_hist["data"]["plus"] = {}

# 2016APV - Data
pu_hist["data"]["minus"]["2016APV"] = uproot.open("data/pu_histos/data/2016/PileupHistogram-goldenJSON-13tev-2016-preVFP-66000ub-99bins.root:pileup")
pu_hist["data"]["nominal"]["2016APV"] = uproot.open("data/pu_histos/data/2016/PileupHistogram-goldenJSON-13tev-2016-preVFP-69200ub-99bins.root:pileup")
pu_hist["data"]["plus"]["2016APV"] = uproot.open("data/pu_histos/data/2016/PileupHistogram-goldenJSON-13tev-2016-preVFP-72400ub-99bins.root:pileup")
# data/pu_histos/data/2016/PileupHistogram-goldenJSON-13tev-2016-preVFP-80000ub-99bins.root


# 2016 - Data
# data/pu_histos/data/2016/PileupHistogram-goldenJSON-13tev-2016-66000ub-99bins.root
# data/pu_histos/data/2016/PileupHistogram-goldenJSON-13tev-2016-69200ub-99bins.root
# data/pu_histos/data/2016/PileupHistogram-goldenJSON-13tev-2016-72400ub-99bins.root
# data/pu_histos/data/2016/PileupHistogram-goldenJSON-13tev-2016-80000ub-99bins.root
pu_hist["data"]["minus"]["2016"] = uproot.open("data/pu_histos/data/2016/PileupHistogram-goldenJSON-13tev-2016-postVFP-66000ub-99bins.root:pileup")
pu_hist["data"]["nominal"]["2016"] = uproot.open("data/pu_histos/data/2016/PileupHistogram-goldenJSON-13tev-2016-postVFP-69200ub-99bins.root:pileup")
pu_hist["data"]["plus"]["2016"] = uproot.open("data/pu_histos/data/2016/PileupHistogram-goldenJSON-13tev-2016-postVFP-72400ub-99bins.root:pileup")
# data/pu_histos/data/2016/PileupHistogram-goldenJSON-13tev-2016-postVFP-80000ub-99bins.root


# 2017 - Data
pu_hist["data"]["minus"]["2017"] = uproot.open("data/pu_histos/data/2017/PileupHistogram-goldenJSON-13tev-2017-66000ub-99bins.root:pileup")
pu_hist["data"]["nominal"]["2017"] = uproot.open("data/pu_histos/data/2017/PileupHistogram-goldenJSON-13tev-2017-69200ub-99bins.root:pileup")
pu_hist["data"]["plus"]["2017"] = uproot.open("data/pu_histos/data/2017/PileupHistogram-goldenJSON-13tev-2017-72400ub-99bins.root:pileup")
# data/pu_histos/data/2017/PileupHistogram-goldenJSON-13tev-2017-80000ub-99bins.root


# 2018 - Data
pu_hist["data"]["minus"]["2018"] = uproot.open("data/pu_histos/data/2018/PileupHistogram-goldenJSON-13tev-2018-66000ub-99bins.root:pileup")
pu_hist["data"]["nominal"]["2018"] = uproot.open("data/pu_histos/data/2018/PileupHistogram-goldenJSON-13tev-2018-69200ub-99bins.root:pileup")
pu_hist["data"]["plus"]["2018"] = uproot.open("data/pu_histos/data/2018/PileupHistogram-goldenJSON-13tev-2018-72400ub-99bins.root:pileup")
# data/pu_histos/data/2018/PileupHistogram-goldenJSON-13tev-2018-80000ub-99bins.root

pu_hist["mc"] = {}

# 2016APV - MC
pu_hist["mc"]["2016APV"] = uproot.open("data/pu_histos/mc/pileup_2016APV_shifts.root:pileup")

# 2016 - MC
pu_hist["mc"]["2016"] = uproot.open("data/pu_histos/mc/pileup_2016_shifts.root:pileup")

# 2017 - MC
pu_hist["mc"]["2017"] = uproot.open("data/pu_histos/mc/pileup_2017_shifts.root:pileup")

# 2018 - MC
pu_hist["mc"]["2018"] = uproot.open("data/pu_histos/mc/pileup_2018_shifts.root:pileup")

def get_bin(values, histo_edges):
    """Get corresponding bins of a given histogram."""
    
    bins = np.argmin(np.absolute(histo_edges-values[..., np.newaxis]), axis=-1)
    return np.where(bins >= len(histo_edges)-1, len(histo_edges)-2, bins) # correct underflow by setting to last bin


def pu_weights(n_pu, year, syst_var):
    """Returns PU weight.
    Reference: https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/3689/1/1.html"""

    pu_hist_data = pu_hist["data"][syst_var][year]
    pu_hist_mc = pu_hist["mc"][year]

    bins_data = get_bin(n_pu, pu_hist_data.axis().edges())
    bins_mc = get_bin(n_pu-1, pu_hist_mc.axis().edges())

    pu_data = pu_hist_data.values()[bins_data]
    pu_mc = np.where(pu_hist_mc.values()[bins_mc] <= 0, 1, pu_hist_mc.values()[bins_mc])


    return pu_data/pu_mc
    