import secrets
from typing import Union

import awkward as ak
import numpy as np
import uproot
from coffea.nanoevents.methods.candidate import Candidate
from coffea.processor import Accumulatable
from numpy.typing import ArrayLike
from particle import PDGID, Particle

from HZUpsilonPhotonRun2NanoAOD.events import Events


def file_tester(file_path: str) -> None:
    try:
        uproot.open(file_path).close()
    except Exception:
        print(f"An exception occurred trying to open: {file_path}")


def safe_mass(candidate: Candidate) -> ArrayLike:
    """Get the mass of a canditate, taking care of negative mass**2 due to NanoAOD precision issues."""
    squared_mass = candidate.mass2
    return np.sqrt(ak.where(squared_mass < 0, 0, squared_mass))


def get_pdgid_by_name(name: str) -> PDGID:
    return Particle.from_name(name).pdgid


def mc_sample_filter(dataset: str, events: ak.Array) -> Union[ArrayLike, ak.Array]:
    """Filter MC samples for special cases."""
    _filter = np.ones(len(events), dtype=bool)

    # Higss resonant m_ll < 30
    if dataset.startswith(
        "GluGluHToMuMuG_M125_MLL-0To60_Dalitz_012j_13TeV_amcatnloFXFX_pythia8"
    ):
        is_prompt_filter = events.GenPart.hasFlags("isPrompt")
        is_mu_plus_filter = events.GenPart.pdgId == get_pdgid_by_name("mu+")
        is_mu_minus_filter = events.GenPart.pdgId == get_pdgid_by_name("mu-")
        # is_gamma_filter = events.GenPart.pdgId == get_pdgid_by_name("gamma")
        is_Higgs_children = ak.fill_none(
            events.GenPart.parent.pdgId == get_pdgid_by_name("H0"), False
        )

        muons_plus = events.GenPart[
            is_prompt_filter & is_Higgs_children & is_mu_plus_filter
        ]
        muons_minus = events.GenPart[
            is_prompt_filter & is_Higgs_children & is_mu_minus_filter
        ]

        dimuons_masses = ak.flatten(safe_mass(muons_plus + muons_minus))
        dimuons_masses_filter = dimuons_masses < 30
        _filter = dimuons_masses_filter

    # Z signal m_ll > 50 (? - Not sure if it should be done)
    # if dataset.startswith("ZToUpsilon"):
    #     pass
    return _filter


def save_dimuon_masses(evts: Events, list_of_dimuons_mass_filters: list[str]) -> None:

    dimuons = evts.events.dimuons[
        evts.filters.all(*list_of_dimuons_mass_filters),
    ]
    dimuons_mass = safe_mass(dimuons["0"] + dimuons["1"])

    dimuons_mass_filename = f"outputs/buffer/dimuons_mass_{evts.dataset}_{evts.year}_{secrets.token_hex(nbytes=20)}.root"
    with uproot.recreate(dimuons_mass_filename) as f:
        f["dimuons_masses"] = {"mass": ak.flatten(dimuons_mass)}


def save_events(evts: Events, prefix: str, list_of_filters: list[str]) -> None:
    """Save kinematical information of selected events."""
    selection_filter = evts.filters.all(*list_of_filters)
    selected_events = evts.events[selection_filter]

    boson = selected_events.boson
    upsilon = selected_events.upsilon
    photon = selected_events.photon
    mu_1 = selected_events.mu_1
    mu_2 = selected_events.mu_2

    output_filename = f"outputs/buffer/{prefix}_{evts.dataset}_{evts.year}_{secrets.token_hex(nbytes=20)}.root"
    buffer = {
        "boson_mass": ak.values_astype(ak.flatten(safe_mass(boson)), np.single),
        "boson_pt": ak.values_astype(ak.flatten(boson.pt), np.single),
        "boson_eta": ak.values_astype(ak.flatten(boson.eta), np.single),
        "boson_phi": ak.values_astype(ak.flatten(boson.phi), np.single),
        "upsilon_mass": ak.values_astype(ak.flatten(safe_mass(upsilon)), np.single),
        "upsilon_pt": ak.values_astype(ak.flatten(upsilon.pt), np.single),
        "upsilon_eta": ak.values_astype(ak.flatten(upsilon.eta), np.single),
        "upsilon_phi": ak.values_astype(ak.flatten(upsilon.phi), np.single),
        "photon_mass": ak.values_astype(ak.flatten(photon.mass), np.single),
        "photon_pt": ak.values_astype(ak.flatten(photon.pt), np.single),
        "photon_eta": ak.values_astype(ak.flatten(photon.eta), np.single),
        "photon_phi": ak.values_astype(ak.flatten(photon.phi), np.single),
        "mu_1_mass": ak.values_astype(ak.flatten(mu_1.mass), np.single),
        "mu_1_pt": ak.values_astype(ak.flatten(mu_1.pt), np.single),
        "mu_1_eta": ak.values_astype(ak.flatten(mu_1.eta), np.single),
        "mu_1_phi": ak.values_astype(ak.flatten(mu_1.phi), np.single),
        "mu_2_mass": ak.values_astype(ak.flatten(mu_2.mass), np.single),
        "mu_2_pt": ak.values_astype(ak.flatten(mu_2.pt), np.single),
        "mu_2_eta": ak.values_astype(ak.flatten(mu_2.eta), np.single),
        "mu_2_phi": ak.values_astype(ak.flatten(mu_2.phi), np.single),
        "delta_eta_upsilon_photon": ak.values_astype(
            ak.flatten(np.absolute(upsilon.eta - photon.eta)), np.single
        ),
        "delta_phi_upsilon_photon": ak.values_astype(
            ak.flatten(np.absolute(upsilon.delta_phi(photon))), np.single
        ),
        "delta_r_upsilon_photon": ak.values_astype(
            ak.flatten(upsilon.delta_r(photon)), np.single
        ),
        "weight": ak.values_astype(evts.weights.weight()[selection_filter], np.single),
    }
    for w in evts.weights.names:
        buffer[f"weight_{w}"] = ak.values_astype(
            evts.weights.individual_weight(w)[selection_filter], np.single
        )

    with uproot.recreate(output_filename) as f:
        f["Events"] = buffer


def fill_cutflow(
    accumulator: Accumulatable,
    evts: Events,
    key: str,
    variation: str,
    list_of_weights: list[str],
    list_of_filters: list[str],
) -> None:
    accumulator[key][
        f"{evts.dataset}_{evts.year}"
    ] = evts.weights.partial_weight_with_variation(
        variation_name=variation, include=list_of_weights
    )[
        evts.filters.all(*list_of_filters)
    ].sum()
