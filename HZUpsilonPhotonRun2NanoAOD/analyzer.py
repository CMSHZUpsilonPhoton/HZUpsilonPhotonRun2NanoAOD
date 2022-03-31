from coffea import processor
from coffea import analysis_tools
from coffea import lumi_tools

import awkward as ak
import numpy as np
import hist
import uproot3
import secrets

from samples import samples_files, samples_descriptions
from HZUpsilonPhotonRun2NanoAOD.sample_processor import sample_processor
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
                    .Bool(name="mediumPrompt_muon")
                    .Bool(name="iso_muon")
                    .Bool(name="nphotons")
                    .Bool(name="photon_pt")
                    .Bool(name="photon_sc_eta")
                    .Bool(name="photon_electron_veto")
                    .Bool(name="photon_tight_id")
                    .Bool(name="signal_selection")
                    .Bool(name="mass_selection")
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
        output = self.accumulator.identity()

        # print(f"--> Processing: {dataset} - {year}")

        return sample_processor(events, dataset, year, data_or_mc, output)

    def postprocess(self, accumulator):
        return accumulator
