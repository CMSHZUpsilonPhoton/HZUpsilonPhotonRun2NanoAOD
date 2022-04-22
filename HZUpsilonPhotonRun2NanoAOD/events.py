import numpy as np
import awkward as ak

from coffea import analysis_tools
from coffea.processor import LazyDataFrame

from HZUpsilonPhotonRun2NanoAOD import array_like

from samples import samples_descriptions


class Events:
    def __init__(self, events: LazyDataFrame) -> None:
        self.events = events
        self.length = len(self.events)
        self.dataset = events.metadata["dataset"]
        self.year = samples_descriptions[self.dataset]["year"]
        self.data_or_mc = samples_descriptions[self.dataset]["data_or_mc"]

        # Build event weight holder
        self.weights = analysis_tools.Weights(size=self.length, storeIndividual=True)

        # Build event filters holder
        self.filters = analysis_tools.PackedSelection()

        # fill a no_cut filter with all True values
        self.filters.add(
            "no_cut", np.full(shape=self.length, fill_value=True, dtype=np.bool)
        )

        self._stop_filtering = False

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"Dataset: {self.dataset} - Is: {self.data_or_mc} - Year: {self.year} - Number of events: {self.length}"

    def filter_events(self, filter: array_like) -> None:
        if self._stop_filtering == True:
            raise Exception(
                "Can not filter an instance which has already been modified (add_filter/add_weight/add_object). Please, filter before any of those operations."
            )

        self.events = self.events[filter]
        self.length = len(self.events)

        # Re-Build event weight holder
        self.weights = analysis_tools.Weights(size=self.length, storeIndividual=True)

        # Re-Build event filters holder
        self.filters = analysis_tools.PackedSelection()

        # fill a no_cut filter with all True values
        self.filters.add(
            "no_cut", np.full(shape=self.length, fill_value=True, dtype=np.bool)
        )

    def add_weight(self, weight_name: str, weight: array_like) -> None:
        if isinstance(weight, tuple):
            weight, weightUp, weightDown = weight
            self.weights.add(
                name=weight_name,
                weight=weight,
                weightUp=weightUp,
                weightDown=weightDown,
            )
        else:
            self.weights.add(
                name=weight_name,
                weight=weight,
                weightUp=weight,
                weightDown=weight,
            )
        self._stop_filtering = True

    def add_filter(self, filter_name: str, filter: array_like) -> None:
        self.filters.add(filter_name, filter)
        self._stop_filtering = True

    def add_object(self, object_name: str, object: ak.Array) -> None:
        self.events[object_name] = object
        self._stop_filtering = True

    @property
    def ones(self) -> np.ndarray:
        return np.ones(self.length)

    @property
    def trues(self) -> np.ndarray:
        return np.full(shape=self.length, fill_value=True, dtype=np.bool)
