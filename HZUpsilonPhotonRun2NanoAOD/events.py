import awkward as ak
import numpy as np
from coffea import analysis_tools

from HZUpsilonPhotonRun2NanoAOD import array_like
from samples.samples_details import samples


class EventWeights(analysis_tools.Weights):  # type: ignore
    """Extension of analysis_tools.Weights to get weights names and if they are systematics."""

    def __init__(self, size: int, storeIndividual: bool = False):
        super().__init__(size, storeIndividual)

    @property
    def names(self) -> list[str]:
        list_of_weights_names = list(self._weights.keys()) + list(
            self._modifiers.keys()
        )
        list_of_weights_names.sort()
        return list_of_weights_names

    def individual_weight(self, name: str) -> np.ndarray:
        if name.endswith("Up") or name.endswith("Down"):
            return (
                self._weights[name.replace("Up", "").replace("Down", "")]
                * self._modifiers[name]
            )
        return self._weights[name]

    def partial_weight_with_variation(
        self,
        variation_name: str = "nominal",
        include: list[str] = [],
        exclude: list[str] = [],
    ) -> np.ndarray:
        if variation_name == "nominal":
            return self.partial_weight(include, exclude)
        return self.partial_weight(include, exclude) * self._modifiers[variation_name]

    @property
    def systematics_names(self) -> list[str]:
        return list(self.variations)


class Events:
    def __init__(self, events: ak.Array) -> None:
        self.events: ak.Array = events
        self.length: int = len(self.events)
        self.dataset: str = events.metadata["dataset"]
        self.year: str = samples[self.dataset]["year"]
        self.data_or_mc: str = samples[self.dataset]["data_or_mc"]

        # Build event weight holder
        self.weights = EventWeights(size=self.length, storeIndividual=True)

        # Build event filters holder
        self.filters = analysis_tools.PackedSelection()

        # fill a no_cut filter with all True values
        self.filters.add(
            "no_cut", np.full(shape=self.length, fill_value=True, dtype=np.bool_)
        )

        self._stop_filtering = False

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"Dataset: {self.dataset} - Is: {self.data_or_mc} - Year: {self.year} - Number of events: {self.length}"

    def filter_events(self, filter: array_like) -> None:
        if self._stop_filtering:
            raise Exception(
                "Can not filter an instance which has already been modified (add_filter/add_weight/add_object). Please, filter before any of those operations."
            )

        self.events = self.events[filter]
        self.length = len(self.events)

        # Re-Build event weight holder
        self.weights = EventWeights(size=self.length, storeIndividual=True)

        # Re-Build event filters holder
        self.filters = analysis_tools.PackedSelection()

        # fill a no_cut filter with all True values
        self.filters.add(
            "no_cut", np.full(shape=self.length, fill_value=True, dtype=np.bool_)
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
        return np.full(shape=self.length, fill_value=True, dtype=np.bool_)
