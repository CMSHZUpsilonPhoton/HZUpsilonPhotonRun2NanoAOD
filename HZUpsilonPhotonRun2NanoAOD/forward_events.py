from HZUpsilonPhotonRun2NanoAOD.filters import *
from HZUpsilonPhotonRun2NanoAOD.builders import *
from HZUpsilonPhotonRun2NanoAOD.weighters import *


def forward_events(evts: Events) -> Events:
    evts.add_filter("lumisection", lumisection_filter(evts))
    # evts.filter_events(lumisection_filter(evts))

    evts.add_weight("pileup", pileup_weight(evts))
    evts.add_weight("generator", generator_weight(evts))
    evts.add_weight("l1_prefiring", l1prefr_weights(evts))

    evts.add_filter("trigger", trigger_filter(evts))

    evts.add_object("good_muons", build_good_muons(evts))
    evts.add_object("good_photons", build_good_photons(evts))

    evts.add_filter("n_muons", n_muons_filter(evts))
    evts.add_filter("n_photons", n_photons_filter(evts))

    evts.add_object("dimuons", build_dimuons(evts))
    evts.add_filter("n_dimuons", n_dimuons_filter(evts))

    evts.bosons_combinations = build_bosons_combination(evts)
    evts.add_filter("n_bosons", n_bosons_combination_filter(evts))

    evts.add_object("boson", build_boson(evts))
    evts.add_object("mu_1", build_mu_1(evts))
    evts.add_object("mu_2", build_mu_2(evts))
    evts.add_object("upsilon", build_upsilon(evts))
    evts.add_object("photon", build_photon(evts))

    evts.add_weight("muon_id", muon_id_weight(evts))
    evts.add_weight("muon_iso", muon_iso_weight(evts))
    evts.add_weight("photon_id", photon_id_weight(evts))
    evts.add_weight("photon_electron_veto", photon_electron_veto_weight(evts))

    evts.add_filter("signal_selection", signal_selection_filter(evts))
    evts.add_filter("mass_selection", mass_selection_filter(evts))

    # return modified events
    return evts
