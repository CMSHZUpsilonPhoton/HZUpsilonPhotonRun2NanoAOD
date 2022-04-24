import awkward as ak
from coffea import processor
from coffea.processor import Accumulatable, defaultdict_accumulator, dict_accumulator

from HZUpsilonPhotonRun2NanoAOD.events import Events
from HZUpsilonPhotonRun2NanoAOD.forward_events import forward_events
from HZUpsilonPhotonRun2NanoAOD.utils import (
    fill_cutflow,
    save_dimuon_masses,
    save_events,
)


class Analyzer(processor.ProcessorABC):  # type: ignore
    def __init__(self) -> None:
        self._accumulator = dict_accumulator({})

    @property
    def accumulator(self) -> Accumulatable:
        return self._accumulator

    # we will receive NanoEvents
    def process(self, events: ak.Array) -> Accumulatable:

        # Forward events over the defined analysis workflow
        evts = forward_events(Events(events))

        # Fill cutflow
        systematics_variations = evts.weights.systematics_names + ["nominal"]
        for variation in systematics_variations:
            cutflow_dict = dict_accumulator(
                {
                    "total": defaultdict_accumulator(float),
                    "preselected": defaultdict_accumulator(float),
                    "selected": defaultdict_accumulator(float),
                    "mass_window": defaultdict_accumulator(float),
                }
            )

            # Add total number of events
            fill_cutflow(
                accumulator=cutflow_dict,
                evts=evts,
                key="total",
                variation=variation,
                list_of_weights=["pileup", "generator"],
                list_of_filters=["lumisection"],
            )

            # Add number of preselected events
            fill_cutflow(
                accumulator=cutflow_dict,
                evts=evts,
                key="preselected",
                variation=variation,
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

            # Add number of selected events
            fill_cutflow(
                accumulator=cutflow_dict,
                evts=evts,
                key="selected",
                variation=variation,
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

            # Add number of events within mass_window
            fill_cutflow(
                accumulator=cutflow_dict,
                evts=evts,
                key="mass_window",
                variation=variation,
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
            self._accumulator[f"cutflow_{variation}"] = cutflow_dict

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
