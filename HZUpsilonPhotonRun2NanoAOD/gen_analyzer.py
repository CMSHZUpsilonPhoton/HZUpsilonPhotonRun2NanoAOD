from coffea import processor
from coffea import analysis_tools

import numpy as np

from samples import samples_descriptions
from HZUpsilonPhotonRun2NanoAOD.utils import mc_sample_filter


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
        weights.add("Generator_weight", events.genWeight)
        # weights.add("Generator_weight", np.sign(events.genWeight))
        # weights.add("Generator_weight", np.sign(events.Generator.weight))

        output["unweighted_sum_of_events"][dataset] += len(events)
        output["weighted_sum_of_events"][dataset] += np.sum(weights.weight())

        # end processing
        return output

    def postprocess(self, accumulator):
        return accumulator
