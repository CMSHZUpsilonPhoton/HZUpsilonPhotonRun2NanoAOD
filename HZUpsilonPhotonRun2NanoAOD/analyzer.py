import awkward as ak
from pprint import pprint
from coffea import processor


from coffea.processor import Accumulatable
from coffea.processor import dict_accumulator
from coffea.processor import defaultdict_accumulator


from HZUpsilonPhotonRun2NanoAOD.events import Events
from HZUpsilonPhotonRun2NanoAOD.forward_events import forward_events
from HZUpsilonPhotonRun2NanoAOD.utils import (
    fill_cutflow,
    save_dimuon_masses,
    save_events,
)


class Analyzer(processor.ProcessorABC):
    def __init__(self) -> None:
        self._accumulator = dict_accumulator(
            {
                "cutflow": dict_accumulator(
                    {
                        "total": defaultdict_accumulator(float),
                        "preselected": defaultdict_accumulator(float),
                        "selected": defaultdict_accumulator(float),
                        "mass_window": defaultdict_accumulator(float),
                    }
                )
            }
        )

    @property
    def accumulator(self) -> Accumulatable:
        return self._accumulator

    # we will receive NanoEvents
    def process(self, events: ak.Array) -> Accumulatable:

        # Forward events over the defined analysis workflow
        evts = forward_events(Events(events))

        # Fill cutflow
        # Add total number of events
        fill_cutflow(
            accumulator=self.accumulator,
            evts=evts,
            key="total",
            list_of_weights=["pileup", "generator"],
            list_of_filters=["lumisection"],
        )

        # Add number oif preselected
        fill_cutflow(
            accumulator=self.accumulator,
            evts=evts,
            key="preselected",
            list_of_weights=[
                "pileup",
                "generator",
                "l1_prefiring",
                "muon_id",
                "muon_iso",
                "photon_id",
                "photon_electron_veto",
            ],
            list_of_filters=[
                "lumisection",
                "trigger",
                "n_muons",
                "n_photons",
                "n_dimuons",
                "n_bosons",
            ],
        )

        # Add number oif preselected
        fill_cutflow(
            accumulator=self.accumulator,
            evts=evts,
            key="selected",
            list_of_weights=[
                "pileup",
                "generator",
                "l1_prefiring",
                "muon_id",
                "muon_iso",
                "photon_id",
                "photon_electron_veto",
            ],
            list_of_filters=[
                "lumisection",
                "trigger",
                "n_muons",
                "n_photons",
                "n_dimuons",
                "n_bosons",
                "signal_selection",
            ],
        )

        # Add number oif selected
        fill_cutflow(
            accumulator=self.accumulator,
            evts=evts,
            key="mass_window",
            list_of_weights=[
                "pileup",
                "generator",
                "l1_prefiring",
                "muon_id",
                "muon_iso",
                "photon_id",
                "photon_electron_veto",
            ],
            list_of_filters=[
                "lumisection",
                "trigger",
                "n_muons",
                "n_photons",
                "n_dimuons",
                "n_bosons",
                "signal_selection",
                "mass_selection",
            ],
        )

        # Save dimuon masses
        if evts.data_or_mc == "data":
            save_dimuon_masses(
                evts=evts,
                list_of_dimuons_mass_filters=[
                    "lumisection",
                    "trigger",
                    "n_muons",
                    "n_photons",
                    "n_dimuons",
                ],
            )

        # Save kinematical information of preselected events
        save_events(
            evts=evts,
            prefix="preselected_events",
            list_of_filters=[
                "lumisection",
                "trigger",
                "n_muons",
                "n_photons",
                "n_dimuons",
                "n_bosons",
            ],
        )

        # Save kinematical information of selected events
        save_events(
            evts=evts,
            prefix="selected_events",
            list_of_filters=[
                "lumisection",
                "trigger",
                "n_muons",
                "n_photons",
                "n_dimuons",
                "n_bosons",
                "signal_selection",
                "mass_selection",
            ],
        )

        return self.accumulator

    def postprocess(self, accumulator: Accumulatable) -> Accumulatable:
        return accumulator
