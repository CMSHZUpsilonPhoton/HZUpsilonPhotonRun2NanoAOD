from typing import Union

import awkward as ak
import numpy as np
from coffea import lumi_tools
from numpy.typing import ArrayLike

from hzupsilonphoton.config import config
from hzupsilonphoton.events import Events
from hzupsilonphoton.utils import safe_mass


def lumisection_filter(evts: Events) -> ArrayLike:
    if evts.data_or_mc == "mc":
        return evts.trues
    else:
        # if data, reduce the events to the golden lumisections filter
        # that is the the only filtering made a priori

        # LumiSection filter
        if evts.year == "2016":
            golden_json_file = "data/golden_jsons/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt"
        if evts.year == "2017":
            golden_json_file = "data/golden_jsons/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt"
        if evts.year == "2018":
            golden_json_file = "data/golden_jsons/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt"
        lumisection_filter = lumi_tools.LumiMask(golden_json_file)(
            evts.events.run, evts.events.luminosityBlock
        )
        return lumisection_filter


def trigger_filter(evts: Events) -> Union[ArrayLike, ak.Array]:
    if evts.data_or_mc == "data":
        return evts.trues
    else:
        # define HLT trigger path string
        if evts.year == "2016":
            hlt_trigger_name = "Mu17_Photon30_IsoCaloId"
        if evts.year == "2017":
            hlt_trigger_name = "Mu17_Photon30_IsoCaloId"
        if evts.year == "2018":
            hlt_trigger_name = "Mu17_Photon30_IsoCaloId"

        trigger_filter = getattr(evts.events.HLT, hlt_trigger_name) == 1

        return trigger_filter


def n_muons_filter(evts: Events) -> ak.Array:
    return ak.num(evts.events.good_muons) >= 2


def n_photons_filter(evts: Events) -> ak.Array:
    return ak.num(evts.events.good_photons) >= 1


def n_dimuons_filter(evts: Events) -> ak.Array:
    return ak.num(evts.events.dimuons) >= 1


def n_bosons_combination_filter(evts: Events) -> ak.Array:
    return ak.num(evts.events.bosons_combinations) >= 1


def signal_selection_filter(evts: Events) -> ak.Array:
    upsilon_vectors = (
        evts.events.bosons_combinations["0"]["0"]
        + evts.events.bosons_combinations["0"]["1"]
    )
    photons_vectors = evts.events.bosons_combinations["1"]

    delta_eta_filter = (
        np.absolute(upsilon_vectors.eta - photons_vectors.eta)
        < config.signal_selection.delta_eta_upsilon_boson
    )
    delta_phi_filter = (
        np.absolute(upsilon_vectors.delta_phi(photons_vectors))
        > config.signal_selection.delta_phi_upsilon_boson
    )
    delta_r_filter = (
        upsilon_vectors.delta_r(photons_vectors)
        >= config.signal_selection.delta_r_upsilon_boson
    )
    pt_filter = upsilon_vectors.pt > config.signal_selection.upsilon_min_pt

    signal_selection = (
        # ak.num(delta_eta_filter & delta_phi_filter & delta_r_filter & pt_filter) >= 1
        ak.fill_none(
            ak.firsts(delta_eta_filter & delta_phi_filter & delta_r_filter & pt_filter),
            False,
        )
    )

    return signal_selection


def mass_selection_filter(evts: Events) -> ak.Array:
    boson_mass_filter = (safe_mass(evts.events.boson) > 60) & (
        safe_mass(evts.events.boson) < 150
    )
    dimuon_mass_filter = (safe_mass(evts.events.upsilon) > 8) & (
        safe_mass(evts.events.upsilon) < 11
    )

    return ak.fill_none(ak.firsts(boson_mass_filter & dimuon_mass_filter), False)
