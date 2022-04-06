import numpy as np
import awkward as ak
from collections import namedtuple

from coffea.lookup_tools import extractor


SFFile = namedtuple("SFFile", ["electron_veto", "id"])

files = {}
files["2016APV"] = SFFile(
    "data/photon_sfs/2016APV/Photons/CSEV_SummaryPlot_UL16_preVFP.root",
    "data/photon_sfs/2016APV/Photons/egammaEffi.txt_EGM2D_Pho_wp80_UL16.root",
)
files["2016"] = SFFile(
    "data/photon_sfs/2016/Photons/CSEV_SummaryPlot_UL16_postVFP.root",
    "data/photon_sfs/2016/Photons/egammaEffi.txt_EGM2D_Pho_MVA80_UL16_postVFP.root",
)
files["2017"] = SFFile(
    "data/photon_sfs/2017/Photons/CSEV_SummaryPlot_UL17.root",
    "data/photon_sfs/2017/Photons/egammaEffi.txt_EGM2D_PHO_MVA80_UL17.root",
)
files["2018"] = SFFile(
    "data/photon_sfs/2018/Photons/CSEV_SummaryPlot_UL18.root",
    "data/photon_sfs/2018/Photons/egammaEffi.txt_EGM2D_Pho_wp80.root_UL18.root",
)

# setup a extractor
ext = extractor()
for y in ["2016APV", "2016", "2017", "2018"]:
    # Photon Electron Veto
    ext.add_weight_sets(
        [
            f"photon_electron_veto_{y} MVAID/SF_CSEV_MVAID {files[y].electron_veto}"
        ]
    )
    ext.add_weight_sets(
        [
            f"photon_electron_veto_{y}_error MVAID/SF_CSEV_MVAID_error {files[y].electron_veto}"
        ]
    )

    # Photon ID
    ext.add_weight_sets(
        [
            f"photon_id_{y} EGamma_SF2D {files[y].id}"
        ]
    )
    ext.add_weight_sets(
        [
            f"photon_id_{y}_error EGamma_SF2D_error {files[y].id}"
        ]
    )

ext.finalize()


# get an evaluator
evaluator = ext.make_evaluator()


def photon_electron_veto_weights(photon, year, syst_var="nominal"):
    """Returns Photon Electron Veto SFs.
    References: https://twiki.cern.ch/twiki/bin/view/CMS/EgammaUL2016To2018
    """

    # Photon.isScEtaEB
    # Photon.isScEtaEE

    photon_sc_region = ak.where(Photon.isScEtaEB == 1 , 0, 3)
    print(photon_sc_region)

    muon_1_iso_sf = evaluator[f"muon_iso_{year}_nominal"](
        np.absolute(muon_1.eta), muon_1.pt
    )
    muon_2_iso_sf = evaluator[f"muon_iso_{year}_nominal"](
        np.absolute(muon_2.eta), muon_2.pt
    )

    if syst_var != "nominal":
        if syst_var != "plus":
            pass

        if syst_var != "minus":
            pass

    return ak.firsts(ak.fill_none(ak.ones_like(photon.pt), 1.0))


def photon_id_weights(photon, year, syst_var="nominal"):
    """Returns Photon ID SFs.
    References: https://twiki.cern.ch/twiki/bin/view/CMS/EgammaUL2016To2018
    """
    if syst_var != "nominal":
        pass

        if syst_var != "plus":
            pass

        if syst_var != "minus":
            pass

    return ak.firsts(ak.fill_none(ak.ones_like(photon.pt), 1.0))

