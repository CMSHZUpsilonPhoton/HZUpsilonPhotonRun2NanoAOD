import json

from coffea import analysis_tools
from coffea import lumi_tools

from samples import samples_descriptions

import HZUpsilonPhotonRun2NanoAOD.filters as filters
from HZUpsilonPhotonRun2NanoAOD.utils import (
    cutflow_filling_parameters,
    build_dimuons,
    save_dimuon_masses,
    build_bosons,
    save_kinematical_information,
)
from HZUpsilonPhotonRun2NanoAOD.pu_weight import pu_weights
from HZUpsilonPhotonRun2NanoAOD.muon_sf import muon_id_weights, muon_iso_weights
from HZUpsilonPhotonRun2NanoAOD.photon_sf import (
    photon_id_weights,
    photon_electron_veto_weights,
)
from HZUpsilonPhotonRun2NanoAOD.l1prefiring_sf import l1prefiring_weights
from samples import lumis, x_section


class SampleProcessor:
    def __init__(self, events, output, filter_by_lumisec=True):
        self.events = events
        self.dataset = events.metadata["dataset"]
        self.year = samples_descriptions[self.dataset]["year"]
        self.data_or_mc = samples_descriptions[self.dataset]["data_or_mc"]
        self.output = output

        # gets weights per event (from gen analysis output)
        gen_output_filename = "outputs/gen_output.json"
        with open(gen_output_filename, "r") as f:
            gen_output = json.load(f)
        self.weighted_sum_of_events = gen_output[
            "weighted_sum_of_events"  # <-- the one to use for plotting and normalization
        ]
        self.unweighted_sum_of_events = gen_output["unweighted_sum_of_events"]

        if filter_by_lumisec:
            # if data, reduce the events to the golden lumisections filter
            # that is the the only filtering made a priori

            # LumiSection filter
            if self.year == "2016":
                golden_json_file = "data/golden_jsons/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt"
            if self.year == "2017":
                golden_json_file = "data/golden_jsons/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt"
            if self.year == "2018":
                golden_json_file = "data/golden_jsons/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt"
            lumisection_filter = lumi_tools.LumiMask(golden_json_file)(
                self.events.run, self.events.luminosityBlock
            )

            if self.data_or_mc == "data":
                self.events = self.events[lumisection_filter]

        # Event weight holder
        self.weights = analysis_tools.Weights(
            size=len(self.events), storeIndividual=True
        )
        self.filters = analysis_tools.PackedSelection()

    def __call__(self):
        self.forward()
        return self.output

    def forward(self):

        # testing
        self.events["dummyMuons"] = self.events.Muon
        print(f'events["dummyMuons"] --- {self.events["dummyMuons"].pt}')
        print(f"events.dummyMuons --- {self.events.dummyMuons.pt}")

        # if MC, get pu weights
        if self.data_or_mc == "mc":
            self.weights.add(
                name="pu",
                weight=pu_weights(
                    self.events.Pileup.nTrueInt, self.year, syst_var="nominal"
                ),
                weightUp=pu_weights(
                    self.events.Pileup.nTrueInt, self.year, syst_var="plus"
                ),
                weightDown=pu_weights(
                    self.events.Pileup.nTrueInt, self.year, syst_var="minus"
                ),
            )

        # if MC, get gen weights
        if self.data_or_mc == "mc":
            self.weights.add(
                name="genWeight",
                weight=self.events.genWeight
                * lumis[self.year]
                * x_section(self.dataset)
                / self.weighted_sum_of_events[self.dataset],
            )

            # if MC, get L1 PreFiring
            self.weights.add(
                name="L1PreFiring",
                weight=l1prefiring_weights(
                    len(self.events), self.year, syst_var="nominal"
                ),
                weightUp=l1prefiring_weights(
                    len(self.events), self.year, syst_var="plus"
                ),
                weightDown=l1prefiring_weights(
                    len(self.events), self.year, syst_var="minus"
                ),
            )

        # filter masks holder
        filters_masks = filters.Mask(dataset=self.dataset, year=self.year)

        # trigger
        filters_masks.trigger = filters.trigger_selection(self.events, self.year)

        # muons filters
        (
            filters_masks.nmuons,
            filters_masks.muon_eta,
            filters_masks.muon_pt,
            filters_masks.muon_id,
            filters_masks.iso_muon,
        ) = filters.muon_selection(self.events)

        # photons filters
        (
            filters_masks.nphotons,
            filters_masks.photon_eta,
            filters_masks.photon_pt,
            filters_masks.photon_sc_eta,
            filters_masks.photon_electron_veto,
            filters_masks.photon_tight_id,
        ) = filters.photon_selection(self.events)

        # build dimuons sample
        dimuon_combinations = build_dimuons(self.events, filters_masks)

        # select dimuons
        filters_masks.ndimuons = filters.dimuon_selection(dimuon_combinations)

        # save dimuon masses
        if self.data_or_mc == "data":
            save_dimuon_masses(
                dimuon_combinations, self.dataset, self.year, filters_masks.ndimuons
            )

        # build bosons
        boson_combinations = build_bosons(
            self.events, dimuon_combinations, filters_masks
        )

        # select bosons - preselection
        filters_masks.nbosons = filters.boson_selection(boson_combinations)

        # if MC, get SFs
        if self.data_or_mc == "mc":
            mu_1 = boson_combinations["0"]["0"]
            mu_2 = boson_combinations["0"]["1"]
            photon = boson_combinations["1"]

            # Muon ID
            self.weights.add(
                name="muon_id",
                weight=muon_id_weights(mu_1, mu_2, self.year, syst_var="nominal"),
                weightUp=muon_id_weights(mu_1, mu_2, self.year, syst_var="plus"),
                weightDown=muon_id_weights(mu_1, mu_2, self.year, syst_var="minus"),
            )
            # Muon ISO
            self.weights.add(
                name="muon_iso",
                weight=muon_iso_weights(mu_1, mu_2, self.year, syst_var="nominal"),
                weightUp=muon_iso_weights(mu_1, mu_2, self.year, syst_var="plus"),
                weightDown=muon_iso_weights(mu_1, mu_2, self.year, syst_var="minus"),
            )

            # Photon ID
            self.weights.add(
                name="photon_id",
                weight=photon_id_weights(photon, self.year, syst_var="nominal"),
                weightUp=photon_id_weights(photon, self.year, syst_var="plus"),
                weightDown=photon_id_weights(photon, self.year, syst_var="minus"),
            )
            # PhotonElectron Veto
            self.weights.add(
                name="photon_electron_veto",
                weight=photon_electron_veto_weights(
                    photon, self.year, syst_var="nominal"
                ),
                weightUp=photon_electron_veto_weights(
                    photon, self.year, syst_var="plus"
                ),
                weightDown=photon_electron_veto_weights(
                    photon, self.year, syst_var="minus"
                ),
            )

        # save kinematical information of preselected self.events
        save_kinematical_information(
            boson_combinations,
            self.dataset,
            self.year,
            "preselected_self.events",
            self.weights.weight(),
            filters_masks.trigger & filters_masks.nbosons,
        )

        # signal selection
        filters_masks.signal = filters.signal_selection(boson_combinations)

        # save kinematical information of selected self.events
        save_kinematical_information(
            boson_combinations,
            self.dataset,
            self.year,
            "selected_self.events",
            self.weights.weight(),
            filters_masks.trigger & filters_masks.nbosons & filters_masks.signal,
        )

        # mass selection
        filters_masks.mass_selection = filters.mass_selection(boson_combinations)

        # cutflow
        self.output["cutflow"].histogram.fill(
            **cutflow_filling_parameters(self.events, filters_masks, self.weights)
        )

        # end processing
        # return self.output
