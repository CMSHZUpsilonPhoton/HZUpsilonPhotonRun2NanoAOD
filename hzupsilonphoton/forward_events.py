import awkward as ak

from hzupsilonphoton.builders import (
    build_boson,
    build_bosons_combination,
    build_dimuons,
    build_good_muons,
    build_good_photons,
    build_mu_1,
    build_mu_2,
    build_photon,
    build_upsilon,
)
from hzupsilonphoton.feed_forward import (
    FeedForwardSequence,
    FilterSequence,
    ObjectSequence,
    WeightSequence,
)
from hzupsilonphoton.filters import (
    lumisection_filter,
    mass_selection_filter,
    signal_selection_filter,
    trigger_filter,
)
from hzupsilonphoton.weighters import (
    generator_weight,
    l1prefr_weights,
    muon_id_weight,
    muon_iso_weight,
    photon_electron_veto_weight,
    photon_id_weight,
    pileup_weight,
)

forward_events = FeedForwardSequence("base_sequence")
forward_events.register_sequence(FilterSequence("lumisection", lumisection_filter))

forward_events.register_sequence(WeightSequence("pileup", pileup_weight))
forward_events.register_sequence(WeightSequence("generator", generator_weight))
forward_events.register_sequence(WeightSequence("l1_prefiring", l1prefr_weights))

forward_events.register_sequence(FilterSequence("trigger", trigger_filter))

forward_events.register_sequence(ObjectSequence("good_muons", build_good_muons))
forward_events.register_sequence(ObjectSequence("good_photons", build_good_photons))

forward_events.register_sequence(
    FilterSequence("n_muons", lambda evts: ak.num(evts.events.good_muons) >= 2)
)
forward_events.register_sequence(
    FilterSequence("n_photons", lambda evts: ak.num(evts.events.good_photons) >= 1)
)

forward_events.register_sequence(ObjectSequence("dimuons", build_dimuons))
forward_events.register_sequence(
    FilterSequence("n_dimuons", lambda evts: ak.num(evts.events.dimuons) >= 1)
)

forward_events.register_sequence(
    ObjectSequence("bosons_combinations", build_bosons_combination)
)
forward_events.register_sequence(
    FilterSequence(
        "n_bosons", lambda evts: ak.num(evts.events.bosons_combinations) >= 1
    )
)

forward_events.register_sequence(ObjectSequence("boson", build_boson))
forward_events.register_sequence(ObjectSequence("mu_1", build_mu_1))
forward_events.register_sequence(ObjectSequence("mu_2", build_mu_2))
forward_events.register_sequence(ObjectSequence("upsilon", build_upsilon))
forward_events.register_sequence(ObjectSequence("photon", build_photon))

forward_events.register_sequence(WeightSequence("muon_id", muon_id_weight))
forward_events.register_sequence(WeightSequence("muon_iso", muon_iso_weight))
forward_events.register_sequence(WeightSequence("photon_id", photon_id_weight))
forward_events.register_sequence(
    WeightSequence("photon_electron_veto", photon_electron_veto_weight)
)

forward_events.register_sequence(
    FilterSequence("signal_selection", signal_selection_filter)
)
forward_events.register_sequence(
    FilterSequence("mass_selection", mass_selection_filter)
)
