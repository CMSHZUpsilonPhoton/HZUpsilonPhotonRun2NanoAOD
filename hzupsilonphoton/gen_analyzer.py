import awkward as ak
import numpy as np
from coffea import analysis_tools, processor
from coffea.processor import Accumulatable

from hzupsilonphoton.utils import mc_sample_filter


class GenAnalyzer(processor.ProcessorABC):  # type: ignore
    def __init__(self) -> None:
        self._accumulator = processor.dict_accumulator(
            {
                "unweighted_sum_of_events": processor.defaultdict_accumulator(float),
                "weighted_sum_of_events": processor.defaultdict_accumulator(float),
            }
        )

    @property
    def accumulator(self) -> Accumulatable:
        return self._accumulator

    # we will receive a NanoEvents
    def process(self, events: ak.Array) -> Accumulatable:
        dataset = events.metadata["dataset"]
        # year = samples[dataset]["year"]
        # data_or_mc = samples[dataset]["data_or_mc"]
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

    def postprocess(self, accumulator: Accumulatable) -> Accumulatable:
        return accumulator
