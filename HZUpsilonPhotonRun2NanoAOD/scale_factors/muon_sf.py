import awkward as ak
import numpy as np
from coffea.lookup_tools import extractor

# setup a extractor
ext = extractor()
for y in ["2016APV", "2016", "2017", "2018"]:
    # Muon ID
    ext.add_weight_sets(
        [
            f"muon_id_{y}_nominal NUM_MediumPromptID_DEN_TrackerMuons_abseta_pt data/muon_sfs/{y}/Efficiencies_muon_generalTracks_Z_Run{y}_UL_ID.root"
        ]
    )
    ext.add_weight_sets(
        [
            f"muon_id_{y}_stat NUM_MediumPromptID_DEN_TrackerMuons_abseta_pt_stat data/muon_sfs/{y}/Efficiencies_muon_generalTracks_Z_Run{y}_UL_ID.root"
        ]
    )
    ext.add_weight_sets(
        [
            f"muon_id_{y}_syst NUM_MediumPromptID_DEN_TrackerMuons_abseta_pt_syst data/muon_sfs/{y}/Efficiencies_muon_generalTracks_Z_Run{y}_UL_ID.root"
        ]
    )

    # Muon ISO
    ext.add_weight_sets(
        [
            f"muon_iso_{y}_nominal NUM_TightRelIso_DEN_MediumPromptID_abseta_pt data/muon_sfs/{y}/Efficiencies_muon_generalTracks_Z_Run{y}_UL_ISO.root"
        ]
    )
    ext.add_weight_sets(
        [
            f"muon_iso_{y}_stat NUM_TightRelIso_DEN_MediumPromptID_abseta_pt data/muon_sfs/{y}/Efficiencies_muon_generalTracks_Z_Run{y}_UL_ISO.root"
        ]
    )
    ext.add_weight_sets(
        [
            f"muon_iso_{y}_syst NUM_TightRelIso_DEN_MediumPromptID_abseta_pt data/muon_sfs/{y}/Efficiencies_muon_generalTracks_Z_Run{y}_UL_ISO.root"
        ]
    )

ext.finalize()


# get an evaluator
evaluator = ext.make_evaluator()


def muon_id_weights(
    muon_1: ak.Array, muon_2: ak.Array, year: str, syst_var: str = "nominal"
) -> ak.Array:
    """Returns Muon ID SFs.
    References:
    2016: https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonUL2018#Introduction
    2017: https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonUL2017#Introduction
    2018: https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonUL2016#Introduction
    """
    muon_1_id_sf = evaluator[f"muon_id_{year}_nominal"](
        np.absolute(muon_1.eta), muon_1.pt
    )
    muon_2_id_sf = evaluator[f"muon_id_{year}_nominal"](
        np.absolute(muon_2.eta), muon_2.pt
    )

    if syst_var != "nominal":
        muon_1_id_sf_stat = evaluator[f"muon_id_{year}_stat"](
            np.absolute(muon_1.eta), muon_1.pt
        )
        muon_2_id_sf_stat = evaluator[f"muon_id_{year}_stat"](
            np.absolute(muon_2.eta), muon_2.pt
        )

        muon_1_id_sf_syst = evaluator[f"muon_id_{year}_syst"](
            np.absolute(muon_1.eta), muon_1.pt
        )
        muon_2_id_sf_syst = evaluator[f"muon_id_{year}_syst"](
            np.absolute(muon_2.eta), muon_2.pt
        )

        if syst_var != "plus":
            muon_1_id_sf = muon_1_id_sf + np.sqrt(
                muon_1_id_sf_stat**2 + muon_1_id_sf_syst**2
            )
            muon_2_id_sf = muon_2_id_sf + np.sqrt(
                muon_2_id_sf_stat**2 + muon_2_id_sf_syst**2
            )

        if syst_var != "minus":
            muon_1_id_sf = muon_1_id_sf - np.sqrt(
                muon_1_id_sf_stat**2 + muon_1_id_sf_syst**2
            )
            muon_2_id_sf = muon_2_id_sf - np.sqrt(
                muon_2_id_sf_stat**2 + muon_2_id_sf_syst**2
            )

    return ak.firsts(ak.fill_none(muon_1_id_sf * muon_2_id_sf, 1.0))


def muon_iso_weights(
    muon_1: ak.Array, muon_2: ak.Array, year: str, syst_var: str = "nominal"
) -> ak.Array:
    """Returns Muon ID SFs.
    References:
    2016: https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonUL2018#Introduction
    2017: https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonUL2017#Introduction
    2018: https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonUL2016#Introduction
    """
    muon_1_iso_sf = evaluator[f"muon_iso_{year}_nominal"](
        np.absolute(muon_1.eta), muon_1.pt
    )
    muon_2_iso_sf = evaluator[f"muon_iso_{year}_nominal"](
        np.absolute(muon_2.eta), muon_2.pt
    )

    if syst_var != "nominal":
        muon_1_iso_sf_stat = evaluator[f"muon_iso_{year}_stat"](
            np.absolute(muon_1.eta), muon_1.pt
        )
        muon_2_iso_sf_stat = evaluator[f"muon_iso_{year}_stat"](
            np.absolute(muon_2.eta), muon_2.pt
        )

        muon_1_iso_sf_syst = evaluator[f"muon_iso_{year}_syst"](
            np.absolute(muon_1.eta), muon_1.pt
        )
        muon_2_iso_sf_syst = evaluator[f"muon_iso_{year}_syst"](
            np.absolute(muon_2.eta), muon_2.pt
        )

        if syst_var != "plus":
            muon_1_iso_sf = muon_1_iso_sf + np.sqrt(
                muon_1_iso_sf_stat**2 + muon_1_iso_sf_syst**2
            )
            muon_2_iso_sf = muon_2_iso_sf + np.sqrt(
                muon_2_iso_sf_stat**2 + muon_2_iso_sf_syst**2
            )

        if syst_var != "minus":
            muon_1_iso_sf = muon_1_iso_sf - np.sqrt(
                muon_1_iso_sf_stat**2 + muon_1_iso_sf_syst**2
            )
            muon_2_iso_sf = muon_2_iso_sf - np.sqrt(
                muon_2_iso_sf_stat**2 + muon_2_iso_sf_syst**2
            )

    return ak.firsts(ak.fill_none(muon_1_iso_sf * muon_2_iso_sf, 1.0))
