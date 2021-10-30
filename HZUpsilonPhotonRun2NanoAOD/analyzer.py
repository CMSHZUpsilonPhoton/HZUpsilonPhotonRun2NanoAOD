from coffea import processor
from coffea import analysis_tools
from coffea import lumi_tools

import awkward as ak
import numpy as np
import hist
import uproot3
import secrets

from samples.samples import samples_files, samples_descriptions
from HZUpsilonPhotonRun2NanoAOD.samples_processors import data_processor, mc_processor
from HZUpsilonPhotonRun2NanoAOD.HistAccumulator import HistAccumulator


class Analyzer(processor.ProcessorABC):
    def __init__(self):
        self._accumulator = processor.dict_accumulator(
            {
                "cutflow": HistAccumulator(
                    hist.Hist.new.StrCat(samples_files.keys(), name="dataset")
                    .StrCat(["2016", "2017", "2018"], name="year")
                    .Bool(name="trigger")
                    .Bool(name="nmuons")
                    .Bool(name="muon_pt")
                    .Bool(name="tight_muon")
                    .Bool(name="iso_muon")
                    .Bool(name="nphotons")
                    .Bool(name="photon_pt")
                    .Bool(name="photon_sc_eta")
                    .Bool(name="photon_electron_veto")
                    .Bool(name="photon_tight_id")
                    .Double()
                ),
            }
        )

    @property
    def accumulator(self):
        return self._accumulator

    # we will receive a NanoEvents
    def process(self, events):
        dataset = events.metadata["dataset"]
        year = samples_descriptions[dataset]["year"]
        data_or_mc = samples_descriptions[dataset]["data_or_mc"]

        if data_or_mc == "data":
            return data_processor(events, dataset, year, self.accumulator.identity())
        if data_or_mc == "mc":
            return mc_processor(events, dataset, year, self.accumulator.identity())

        # # define accumulator
        # output = self.accumulator.identity()

        # # Luminosity filter
        # if year == "2016":
        #     golden_json_file = "data/golden_jsons/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt"
        # if year == "2017":
        #     golden_json_file = "data/golden_jsons/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt"
        # if year == "2018":
        #     golden_json_file = "data/golden_jsons/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt"
        # luminosity_filter = lumi_tools.LumiMask(golden_json_file)(
        #     events.run, events.luminosityBlock
        # )
        # events = events[luminosity_filter]

        # ## filters
        # # trigger
        # trigger_filter = getattr(events.HLT, hlt_trigger_name) == 1

        # # muons
        # nmuons_filter = ak.num(events.Muon) >= 2  # at least 2 muons
        # muon_pt_filter = events.Muon.pt > 3  # minimum muon pt
        # muon_id_filter = events.Muon.tightId == 1  # muon id: Tight
        # iso_muon_filter = events.Muon.pfRelIso03_all < 0.35  # PF_Isolation < 0.35

        # # photons
        # nphotons_filter = ak.num(events.Photon) >= 1  # at lest one photon
        # photon_pt_filter = (
        #     events.Photon.eCorr * events.Photon.pt > 33
        # )  # pt at least 33 GeV
        # photon_sc_eta_filter = (events.Photon.isScEtaEB == 1) | (
        #     events.Photon.isScEtaEE == 1
        # )  # is Barrel or Endacap - no "crack photons".
        # photon_electron_veto_filter = events.Photon.electronVeto == 1  # electron veto
        # photon_tight_id_filter = events.Photon.cutBased == 3  # cut based tight photon

        # # cutflow
        # output["cutflow"].histogram.fill(
        #     dataset=dataset,
        #     year=year,
        #     trigger=trigger_filter,
        #     nmuons=nmuons_filter,
        #     muon_pt=ak.num(events.Muon[muon_pt_filter]) >= 2,
        #     tight_muon=ak.num(events.Muon[muon_id_filter]) >= 2,
        #     iso_muon=ak.num(events.Muon[iso_muon_filter]) >= 2,
        #     nphotons=nphotons_filter,
        #     photon_pt=ak.num(events.Photon[photon_pt_filter]) >= 1,
        #     photon_sc_eta=ak.num(events.Photon[photon_sc_eta_filter]) >= 1,
        #     photon_electron_veto=ak.num(events.Photon[photon_electron_veto_filter])
        #     >= 1,
        #     photon_tight_id=ak.num(events.Photon[photon_tight_id_filter]) >= 1,
        #     # signal_selection=,
        #     # dimuon_mass=,
        #     # boson_mass=,
        #     weight=weights.weight(),
        # )

        # # dimuon sample
        # dimuon = ak.combinations(
        #     events.Muon[muon_pt_filter & muon_id_filter & iso_muon_filter], 2
        # )
        # dimuon = dimuon[(dimuon["0"].charge + dimuon["1"].charge) == 0]
        # dimuon_mass = (dimuon["0"] + dimuon["1"]).mass

        # dimuon_mass_filename = f"outputs/buffer/dimuon_mass_{dataset}_{year}_{secrets.token_hex(nbytes=20)}.root"
        # with uproot3.recreate(dimuon_mass_filename) as f:
        #     f["dimuon_mass"] = uproot3.newtree({"mass": "float"})
        #     f["dimuon_mass"].extend({"mass": ak.flatten(dimuon_mass)})

        # # boson
        # boson = ak.cartesian(
        #     [
        #         dimuon,
        #         events.Photon[
        #             photon_pt_filter
        #             & photon_electron_veto_filter
        #             & photon_sc_eta_filter
        #             & photon_tight_id_filter
        #         ],
        #     ]
        # )
        # boson_pt = (boson["0"]["0"] + boson["0"]["1"] + boson["1"]).pt
        # boson = ak.flatten(boson[ak.argsort(boson_pt, ascending=False)][:, :1])
        # boson_mass = (boson["0"]["0"] + boson["0"]["1"] + boson["1"]).mass
        # # print(boson_mass)

        # # end processing
        # return output

    def postprocess(self, accumulator):
        return accumulator
