from typing import Union
import awkward as ak
import numpy as np
import uproot
import secrets
import numpy as np
from particle import Particle
from coffea.nanoevents.methods.candidate import Candidate

from HZUpsilonPhotonRun2NanoAOD.events import Events
from coffea.processor import Accumulatable


def file_tester(file_path: str) -> None:
    try:
        uproot.open(file_path).close()
    except Exception:
        print(f"An exception occurred trying to open: {file_path}")


def safe_mass(candidate: Candidate):
    """Get the mass of a canditate, taking care of negative mass**2 due to NanoAOD precision issues."""
    squared_mass = candidate.mass2
    return np.sqrt(ak.where(squared_mass < 0, 0, squared_mass))


def get_pdgid_by_name(name: str) -> int:
    return Particle.from_name(name).pdgid


def mc_sample_filter(dataset, events):
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
        "boson_mass": ak.flatten(safe_mass(boson)),
        "boson_pt": ak.flatten(boson.pt),
        "boson_eta": ak.flatten(boson.eta),
        "boson_phi": ak.flatten(boson.phi),
        "upsilon_mass": ak.flatten(safe_mass(upsilon)),
        "upsilon_pt": ak.flatten(upsilon.pt),
        "upsilon_eta": ak.flatten(upsilon.eta),
        "upsilon_phi": ak.flatten(upsilon.phi),
        "photon_mass": ak.flatten(photon.mass),
        "photon_pt": ak.flatten(photon.pt),
        "photon_eta": ak.flatten(photon.eta),
        "photon_phi": ak.flatten(photon.phi),
        "mu_1_mass": ak.flatten(mu_1.mass),
        "mu_1_pt": ak.flatten(mu_1.pt),
        "mu_1_eta": ak.flatten(mu_1.eta),
        "mu_1_phi": ak.flatten(mu_1.phi),
        "mu_2_mass": ak.flatten(mu_2.mass),
        "mu_2_pt": ak.flatten(mu_2.pt),
        "mu_2_eta": ak.flatten(mu_2.eta),
        "mu_2_phi": ak.flatten(mu_2.phi),
        "delta_eta_upsilon_photon": ak.flatten(np.absolute(upsilon.eta - photon.eta)),
        "delta_phi_upsilon_photon": ak.flatten(np.absolute(upsilon.delta_phi(photon))),
        "delta_r_upsilon_photon": ak.flatten(upsilon.delta_r(photon)),
        "weight": evts.weights.weight()[selection_filter],
    }
    for w in evts.weights.names:
        buffer[f"weight_{w}"] = evts.weights.individual_weight(w)[selection_filter]

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
