from collections import namedtuple

import awkward as ak
from coffea.lookup_tools import extractor

SFFile = namedtuple("SFFile", ["electron_veto", "id"])

files = {}
files["2016APV"] = SFFile(
    "data/photon_sfs/2016APV/Photons/CSEV_SummaryPlot_UL16_preVFP.root",
    "data/photon_sfs/2016APV/Photons/egammaEffi_txt_EGM2D_Pho_wp80_UL16.root",
)
files["2016"] = SFFile(
    "data/photon_sfs/2016/Photons/CSEV_SummaryPlot_UL16_postVFP.root",
    "data/photon_sfs/2016/Photons/egammaEffi_txt_EGM2D_Pho_MVA80_UL16_postVFP.root",
)
files["2017"] = SFFile(
    "data/photon_sfs/2017/Photons/CSEV_SummaryPlot_UL17.root",
    "data/photon_sfs/2017/Photons/egammaEffi_txt_EGM2D_PHO_MVA80_UL17.root",
)
files["2018"] = SFFile(
    "data/photon_sfs/2018/Photons/CSEV_SummaryPlot_UL18.root",
    "data/photon_sfs/2018/Photons/egammaEffi_txt_EGM2D_Pho_wp80_root_UL18.root",
)

# setup a extractor
ext = extractor()
for y in ["2016APV", "2016", "2017", "2018"]:
    # Photon Electron Veto
    ext.add_weight_sets(
        [f"photon_electron_veto_{y} MVAID/SF_CSEV_MVAID {files[y].electron_veto}"]
    )
    ext.add_weight_sets(
        [
            f"photon_electron_veto_{y}_error MVAID/SF_CSEV_MVAID_error {files[y].electron_veto}"
        ]
    )

    # Photon ID
    ext.add_weight_sets([f"photon_id_{y} EGamma_SF2D {files[y].id}"])
    ext.add_weight_sets([f"photon_id_{y}_error EGamma_SF2D_error {files[y].id}"])

ext.finalize()


# get an evaluator
evaluator = ext.make_evaluator()


def photon_electron_veto_weights(
    photon: ak.Array, year: str, syst_var: str = "nominal"
) -> ak.Array:
    """Returns Photon Electron Veto SFs.
    References: https://twiki.cern.ch/twiki/bin/view/CMS/EgammaUL2016To2018
    """

    photon_sc_region = ak.where(photon.isScEtaEB == 1, 0, 3)

    photon_electron_veto_sf = evaluator[f"photon_electron_veto_{year}"](
        photon_sc_region
    )

    if syst_var != "nominal":
        if syst_var != "plus":
            photon_electron_veto_sf = photon_electron_veto_sf + evaluator[
                f"photon_electron_veto_{year}_error"
            ](photon_sc_region)

        if syst_var != "minus":
            photon_electron_veto_sf = photon_electron_veto_sf - evaluator[
                f"photon_electron_veto_{year}_error"
            ](photon_sc_region)

    return ak.firsts(ak.fill_none(ak.ones_like(photon_electron_veto_sf), 1.0))


def photon_id_weights(
    photon: ak.Array, year: str, syst_var: str = "nominal"
) -> ak.Array:
    """Returns Photon ID SFs.
    References: https://twiki.cern.ch/twiki/bin/view/CMS/EgammaUL2016To2018
    """

    photon_id_sf = evaluator[f"photon_id_{year}"](photon.eta, photon.pt)

    if syst_var != "nominal":
        if syst_var != "plus":
            photon_id_sf = photon_id_sf + evaluator[f"photon_id_{year}_error"](
                photon.eta, photon.pt
            )

        if syst_var != "minus":
            photon_id_sf = photon_id_sf - evaluator[f"photon_id_{year}_error"](
                photon.eta, photon.pt
            )

    return ak.firsts(ak.fill_none(ak.ones_like(photon_id_sf), 1.0))
