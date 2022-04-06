from coffea import processor
from coffea import analysis_tools
from coffea import lumi_tools

import awkward as ak
import numpy as np
import hist
import uproot3
import secrets
from pprint import pprint

from samples import samples_files, samples_descriptions
from HZUpsilonPhotonRun2NanoAOD.sample_processor import sample_processor
from HZUpsilonPhotonRun2NanoAOD.HistAccumulator import HistAccumulator
from HZUpsilonPhotonRun2NanoAOD.utils import (
    get_pdgid_by_name,
    safe_mass,
    mc_sample_filter,
)


class GenAnalyzer(processor.ProcessorABC):
    def __init__(self):
        self._accumulator = processor.dict_accumulator(
            {
                "unweighted_sum_of_events": processor.defaultdict_accumulator(float),
                "weighted_sum_of_events": processor.defaultdict_accumulator(float),
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

        # Special MC sample filter
        events = events[mc_sample_filter(dataset, events)]

        # Event weight holder
        weights = analysis_tools.Weights(size=len(events), storeIndividual=True)
        weights.add("Generator_weight", np.sign(events.Generator.weight))

        output["unweighted_sum_of_events"][dataset] += len(events)
        output["weighted_sum_of_events"][dataset] += np.sum(weights.weight())

        # end processing
        return output

    def postprocess(self, accumulator):
        return accumulator
