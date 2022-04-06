from coffea import processor
from coffea import analysis_tools
from coffea import lumi_tools

import awkward as ak
import numpy as np


from HZUpsilonPhotonRun2NanoAOD.HistAccumulator import HistAccumulator
import HZUpsilonPhotonRun2NanoAOD.Filters as Filters
from HZUpsilonPhotonRun2NanoAOD.utils import (
    cutflow_filling_parameters,
    build_dimuons,
    save_dimuon_masses,
    build_bosons,
    save_kinematical_information,
)
from HZUpsilonPhotonRun2NanoAOD.pu_weight import pu_weights
from HZUpsilonPhotonRun2NanoAOD.muon_sf import muon_id_weights, muon_iso_weights
from HZUpsilonPhotonRun2NanoAOD.photon_sf import photon_id_weights, photon_electron_veto_weights


def sample_processor(events, dataset, year, data_or_mc, output):
    # LumiSection filter
    if year == "2016":
        golden_json_file = "data/golden_jsons/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt"
    if year == "2017":
        golden_json_file = "data/golden_jsons/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt"
    if year == "2018":
        golden_json_file = "data/golden_jsons/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt"
    lumisection_filter = lumi_tools.LumiMask(golden_json_file)(
        events.run, events.luminosityBlock
    )

    # if Data, filter by lumisection
    if data_or_mc == "data":
        events = events[lumisection_filter]

    # Event weight holder
    weights = analysis_tools.Weights(size=len(events), storeIndividual=True)

    # if MC, get pu weights
    if data_or_mc == "mc":
        weights.add(
            name="pu",
            weight=pu_weights(events.Pileup.nTrueInt, year, syst_var="nominal"),
            weightUp=pu_weights(events.Pileup.nTrueInt, year, syst_var="plus"),
            weightDown=pu_weights(events.Pileup.nTrueInt, year, syst_var="minus"),
        )

    # filter masks holder
    filters_masks = Filters.Mask(dataset=dataset, year=year)

    # trigger
    filters_masks.trigger = Filters.trigger_selection(events, year)

    # muons filters
    (
        filters_masks.nmuons,
        filters_masks.muon_eta,
        filters_masks.muon_pt,
        filters_masks.muon_id,
        filters_masks.iso_muon,
    ) = Filters.muon_selection(events)

    # photons filters
    (
        filters_masks.nphotons,
        filters_masks.photon_eta,
        filters_masks.photon_pt,
        filters_masks.photon_sc_eta,
        filters_masks.photon_electron_veto,
        filters_masks.photon_tight_id,
    ) = Filters.photon_selection(events)

    # build dimuons sample
    dimuon_combinations = build_dimuons(events, filters_masks)

    # select dimuons
    filters_masks.ndimuons = Filters.dimuon_selection(dimuon_combinations)

    # save dimuon masses
    if data_or_mc == "data":
        save_dimuon_masses(dimuon_combinations, dataset, year, filters_masks.ndimuons)

    # build bosons
    boson_combinations = build_bosons(events, dimuon_combinations, filters_masks)

    # select bosons - preselection
    filters_masks.nbosons = Filters.boson_selection(boson_combinations)

    # if MC, get Muon SFs
    if data_or_mc == "mc":
        mu_1 = boson_combinations["0"]["0"]
        mu_2 = boson_combinations["0"]["1"]
        photon = boson_combinations["1"]

        # Muon ID
        weights.add(
            name="muon_id",
            weight=muon_id_weights(mu_1, mu_2, year, syst_var="nominal"),
            weightUp=muon_id_weights(mu_1, mu_2, year, syst_var="plus"),
            weightDown=muon_id_weights(mu_1, mu_2, year, syst_var="minus"),
        )
        # Muon ISO
        weights.add(
            name="muon_iso",
            weight=muon_iso_weights(mu_1, mu_2, year, syst_var="nominal"),
            weightUp=muon_iso_weights(mu_1, mu_2, year, syst_var="plus"),
            weightDown=muon_iso_weights(mu_1, mu_2, year, syst_var="minus"),
        )

        # Photon ID
        weights.add(
            name="photon_id",
            weight=photon_id_weights(photon, year, syst_var="nominal"),
            weightUp=photon_id_weights(photon, year, syst_var="plus"),
            weightDown=photon_id_weights(photon, year, syst_var="minus"),
        )
        # PhotonElectron Veto
        weights.add(
            name="photon_electron_veto",
            weight=photon_electron_veto_weights(photon, year, syst_var="nominal"),
            weightUp=photon_electron_veto_weights(photon, year, syst_var="plus"),
            weightDown=photon_electron_veto_weights(photon, year, syst_var="minus"),
        )

    # save kinematical information of preselected events
    save_kinematical_information(
        boson_combinations,
        dataset,
        year,
        "preselected_events",
        weights.weight(),
        filters_masks.trigger & filters_masks.nbosons,
    )

    # signal selection
    filters_masks.signal = Filters.signal_selection(boson_combinations)

    # save kinematical information of selected events
    save_kinematical_information(
        boson_combinations,
        dataset,
        year,
        "selected_events",
        weights.weight(),
        filters_masks.trigger & filters_masks.nbosons & filters_masks.signal,
    )

    # mass selection
    filters_masks.mass_selection = Filters.mass_selection(boson_combinations)

    # cutflow
    output["cutflow"].histogram.fill(
        **cutflow_filling_parameters(events, filters_masks, weights)
    )

    # end processing
    return output
