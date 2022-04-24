from __future__ import annotations

from typing import Callable

from HZUpsilonPhotonRun2NanoAOD.events import Events


class FeedForwardSequence:
    def __init__(self, name: str) -> None:
        """Base Sequence."""
        self.name = name
        self.sequences = []

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"Sequence name: {self.name}"

    def __call__(self, evts: Events, from_register: bool = True) -> Events:
        # will call sequences from its register
        if from_register:
            for seq in self.sequences:
                evts = seq(evts)
            return evts

        # default behavior
        return self.forward(evts)

    def register_sequence(self, sequence: FeedForwardSequence) -> None:
        self.sequences.append(sequence)

    def forward(self, evts: Events) -> Events:
        return evts


class FilterSequence(FeedForwardSequence):
    def __init__(self, name: str, filter_function: Callable) -> None:
        """Lambda Filter Sequence."""
        super().__init__(name)
        self.filter_function = filter_function

    def __call__(self, evts: Events) -> Events:
        return self.forward(evts)

    def forward(self, evts: Events) -> Events:
        evts.add_filter(self.name, self.filter_function(evts))
        return evts


class WeightSequence(FeedForwardSequence):
    def __init__(self, name: str, weight_function: Callable) -> None:
        """Lambda Filter Sequence."""
        super().__init__(name)
        self.weight_function = weight_function

    def __call__(self, evts: Events) -> Events:
        return self.forward(evts)

    def forward(self, evts: Events) -> Events:
        evts.add_weight(self.name, self.weight_function(evts))
        return evts


class ObjectSequence(FeedForwardSequence):
    def __init__(self, name: str, object_function: Callable) -> None:
        """Lambda Filter Sequence."""
        super().__init__(name)
        self.object_function = object_function

    def __call__(self, evts: Events) -> Events:
        return self.forward(evts)

    def forward(self, evts: Events) -> Events:
        evts.add_object(self.name, self.object_function(evts))
        return evts
