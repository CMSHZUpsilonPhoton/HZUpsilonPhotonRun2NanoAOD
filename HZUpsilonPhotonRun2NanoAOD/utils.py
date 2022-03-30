import awkward as ak
import uproot3
import secrets


def cutflow_filling_parameters(events, filters_masks, weights):
    return {
        "dataset": filters_masks.dataset,
        "year": filters_masks.year,
        "trigger": filters_masks.trigger,
        "nmuons": filters_masks.nmuons,
        "muon_pt": ak.num(events.Muon[filters_masks.muon_pt]) >= 2,
        "mediumPrompt_muon": ak.num(events.Muon[filters_masks.muon_id]) >= 2,
        "iso_muon": ak.num(events.Muon[filters_masks.iso_muon]) >= 2,
        "nphotons": filters_masks.nphotons,
        "photon_pt": ak.num(events.Photon[filters_masks.photon_pt]) >= 1,
        "photon_sc_eta": ak.num(events.Photon[filters_masks.photon_sc_eta]) >= 1,
        "photon_electron_veto": ak.num(
            events.Photon[filters_masks.photon_electron_veto]
        )
        >= 1,
        "photon_tight_id": ak.num(events.Photon[filters_masks.photon_tight_id]) >= 1,
        # signal_selection=,
        "weight": weights.weight(),
    }


def build_dimuons(events, filters_masks):
    dimuons = ak.combinations(
        events.Muon[
            filters_masks.muon_pt & filters_masks.muon_id & filters_masks.iso_muon
        ],
        2,
    )
    charge_filter = (dimuons["0"].charge + dimuons["1"].charge) == 0
    muon_pt_filter_0 = (dimuons["0"].pt >= 18 )  # at least one muon with pT > 18 GeV
    muon_pt_filter_1 = (dimuons["1"].pt >= 18 ) # at least one muon with pT > 18 GeV
    
    return dimuons[charge_filter & (muon_pt_filter_0 | muon_pt_filter_1)]


def save_dimuon_masses(dimuons, dataset, year):
    dimuons_mass = (dimuons["0"] + dimuons["1"]).mass

    dimuons_mass_filename = f"outputs/buffer/dimuons_mass_{dataset}_{year}_{secrets.token_hex(nbytes=20)}.root"
    with uproot3.recreate(dimuons_mass_filename) as f:
        f["dimuons_mass"] = uproot3.newtree({"mass": "float"})
        f["dimuons_mass"].extend({"mass": ak.flatten(dimuons_mass)})

def save_kinematical_information(boson_combinations, dataset, year, prefix, weights):
    """Save kinematical information about selected events."""
    bosons = boson_combinations["0"]["0"] + boson_combinations["0"]["1"] + boson_combinations["1"]
    upsilons = boson_combinations["0"]["0"] + boson_combinations["0"]["1"]
    photons = boson_combinations["1"]
    mu_1 = boson_combinations["0"]["0"]
    mu_2 = boson_combinations["0"]["1"]

    output_filename = f"outputs/buffer/{prefix}_{dataset}_{year}_{secrets.token_hex(nbytes=20)}.root"
    with uproot3.recreate(output_filename) as f:
        f["Events"] = uproot3.newtree({
            "boson_mass": "float",
            "boson_pt": "float",
            "boson_eta": "float",
            "boson_phi": "float",
            "upsilon_mass": "float",
            "upsilon_pt": "float",
            "upsilon_eta": "float",
            "upsilon_phi": "float",
            "photon_mass": "float",
            "photon_pt": "float",
            "photon_eta": "float",
            "photon_phi": "float",
            "mu_1_mass": "float",
            "mu_1_pt": "float",
            "mu_1_eta": "float",
            "mu_1_phi": "float",
            "mu_2_mass": "float",
            "mu_2_pt": "float",
            "mu_2_eta": "float",
            "mu_2_phi": "float",
            "weight" : "float",
            })
        f["Events"].extend({
            "boson_mass": bosons.mass,
            "boson_pt": bosons.pt,
            "boson_eta": bosons.eta,
            "boson_phi": bosons.phi,
            "upsilon_mass": upsilons.mass,
            "upsilon_pt": upsilons.pt,
            "upsilon_eta": upsilons.eta,
            "upsilon_phi": upsilons.phi,
            "photon_mass": photons.mass,
            "photon_pt": photons.pt,
            "photon_eta": photons.eta,
            "photon_phi": photons.phi,
            "mu_1_mass": mu_1.mass,
            "mu_1_pt": mu_1.pt,
            "mu_1_eta": mu_1.eta,
            "mu_1_phi": mu_1.phi,
            "mu_2_mass": mu_2.mass,
            "mu_2_pt": mu_2.pt,
            "mu_2_eta": mu_2.eta,
            "mu_2_phi": mu_2.phi,
            "weight": weights,
            })

def build_bosons(events, dimuons, filters_masks):
    bosons = ak.cartesian(
        [
            dimuons,
            events.Photon[
                filters_masks.photon_pt
                & filters_masks.photon_electron_veto
                & filters_masks.photon_sc_eta
                & filters_masks.photon_tight_id
            ],
        ]
    )
    bosons_pt = (bosons["0"]["0"] + bosons["0"]["1"] + bosons["1"]).pt
    preselected_bosons = bosons[ak.argsort(bosons_pt, ascending=False)][:, :1]
    preselected_events_filter = ak.num(bosons_pt) > 0
    return ak.flatten(preselected_bosons), preselected_events_filter
