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
        "tight_muon": ak.num(events.Muon[filters_masks.muon_id]) >= 2,
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

    return dimuons[(dimuons["0"].charge + dimuons["1"].charge) == 0]


def save_dimuon_masses(dimuons, dataset, year):
    dimuons_mass = (dimuons["0"] + dimuons["1"]).mass

    dimuons_mass_filename = f"outputs/buffer/dimuons_mass_{dataset}_{year}_{secrets.token_hex(nbytes=20)}.root"
    with uproot3.recreate(dimuons_mass_filename) as f:
        f["dimuons_mass"] = uproot3.newtree({"mass": "float"})
        f["dimuons_mass"].extend({"mass": ak.flatten(dimuons_mass)})


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
    return ak.flatten(bosons[ak.argsort(bosons_pt, ascending=False)][:, :1])
