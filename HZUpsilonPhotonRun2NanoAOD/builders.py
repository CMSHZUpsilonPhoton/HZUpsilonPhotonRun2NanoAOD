import awkward as ak
import numpy as np

from HZUpsilonPhotonRun2NanoAOD.events import Events


def build_good_muons(evts: Events) -> ak.Array:
    nmuons_filter = ak.num(evts.events.Muon) >= 2  # at least 2 muons
    muon_eta_filter = np.absolute(evts.events.Muon.eta) < 2.4  # |eta| < 2.4
    muon_pt_filter = evts.events.Muon.pt > 5  # minimum muon pt
    muon_id_filter = evts.events.Muon.mediumPromptId == 1  # muon id: mediumPromptId
    iso_muon_filter = evts.events.Muon.pfRelIso03_all < 0.15  # PF_Isolation < 0.15

    return evts.events.Muon[
        nmuons_filter
        & muon_eta_filter
        & muon_pt_filter
        & muon_id_filter
        & iso_muon_filter
    ]


def build_good_photons(evts: Events) -> ak.Array:
    nphotons_filter = ak.num(evts.events.Photon) >= 1  # at lest one photon
    photon_eta_filter = np.absolute(evts.events.Photon.eta) < 2.5  # |eta| < 2.5
    photon_pt_filter = evts.events.Photon.pt > 32  # pt at least 32 GeV
    photon_sc_eta_filter = (evts.events.Photon.isScEtaEB == 1) | (
        evts.events.Photon.isScEtaEE == 1
    )  # is Barrel or Endacap - no "crack photons".
    photon_electron_veto_filter = evts.events.Photon.electronVeto == 1  # electron veto
    # photon_tight_id_filter = evts.events.Photon.cutBased == 3  # cut based tight photon
    photon_tight_id_filter = evts.events.Photon.mvaID_WP80 == 1  # MVA (WP: 80)% photon

    return evts.events.Photon[
        nphotons_filter
        & photon_eta_filter
        & photon_pt_filter
        & photon_sc_eta_filter
        & photon_electron_veto_filter
        & photon_tight_id_filter
    ]


def build_dimuons(evts: Events) -> ak.Array:
    dimuons = ak.combinations(evts.events.good_muons, 2)
    dimuons = dimuons[(dimuons["0"].charge + dimuons["1"].charge == 0)]

    return dimuons


def build_bosons_combination(evts: Events) -> ak.Array:
    bosons = ak.cartesian(
        [
            evts.events.dimuons,
            evts.events.good_photons,
        ]
    )
    bosons_pt = (bosons["0"]["0"] + bosons["0"]["1"] + bosons["1"]).pt
    bosons_combinations = bosons[ak.argsort(bosons_pt, ascending=False)][
        :, :1
    ]  # select the boson with highest pT
    return bosons_combinations


def build_boson(evts: Events) -> ak.Array:
    return (
        evts.events.bosons_combinations["0"]["0"]
        + evts.events.bosons_combinations["0"]["1"]
        + evts.events.bosons_combinations["1"]
    )


def build_mu_1(evts: Events) -> ak.Array:
    return evts.events.bosons_combinations["0"]["0"]


def build_mu_2(evts: Events) -> ak.Array:
    return evts.events.bosons_combinations["0"]["1"]


def build_upsilon(evts: Events) -> ak.Array:
    return (
        evts.events.bosons_combinations["0"]["0"]
        + evts.events.bosons_combinations["0"]["1"]
    )


def build_photon(evts: Events) -> ak.Array:
    return evts.events.bosons_combinations["1"]
