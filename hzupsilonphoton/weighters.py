import json
from typing import Union

from numpy.typing import ArrayLike

from hzupsilonphoton.events import Events
from hzupsilonphoton.scale_factors.l1prefiring_sf import l1prefiring_weights
from hzupsilonphoton.scale_factors.muon_sf import muon_id_weights, muon_iso_weights
from hzupsilonphoton.scale_factors.photon_sf import (
    photon_electron_veto_weights,
    photon_id_weights,
)
from hzupsilonphoton.scale_factors.pu_weight import pu_weights
from samples.lumis import lumis
from samples.xsecs import x_section

Weight = Union[tuple[ArrayLike, ArrayLike, ArrayLike], ArrayLike]


def pileup_weight(
    evts: Events,
) -> Weight:
    # if MC, get pu weights
    if evts.data_or_mc == "data":
        return (evts.ones, evts.ones, evts.ones)
    else:
        nominal = pu_weights(evts.events.Pileup.nTrueInt, evts.year, syst_var="nominal")
        up = pu_weights(evts.events.Pileup.nTrueInt, evts.year, syst_var="plus")
        down = pu_weights(evts.events.Pileup.nTrueInt, evts.year, syst_var="minus")
        return nominal, up, down


def generator_weight(evts: Events) -> Weight:
    # if MC, get gen weights
    if evts.data_or_mc == "data":
        return evts.ones
    else:
        # gets weights per event (from gen analysis output)
        gen_output_filename = "outputs/gen_output.json"
        with open(gen_output_filename, "r") as f:
            gen_output = json.load(f)
        weighted_sum_of_events = gen_output[
            "weighted_sum_of_events"  # <-- the one to use for plotting and normalization
        ]
        # unweighted_sum_of_events = gen_output["unweighted_sum_of_events"]

        return (
            evts.events.genWeight
            * lumis[evts.year]
            * x_section(evts.dataset)
            / weighted_sum_of_events[evts.dataset]
        )


def l1prefr_weights(evts: Events) -> Weight:
    # if MC, get pu weights
    if evts.data_or_mc == "data":
        return (evts.ones, evts.ones, evts.ones)
    else:
        nominal = l1prefiring_weights(
            evts.events, evts.length, evts.year, syst_var="nominal"
        )
        up = l1prefiring_weights(evts.events, evts.length, evts.year, syst_var="plus")
        down = l1prefiring_weights(
            evts.events, evts.length, evts.year, syst_var="minus"
        )
        return nominal, up, down


def muon_id_weight(evts: Events) -> Weight:
    # if MC, get pu weights
    if evts.data_or_mc == "data":
        return (evts.ones, evts.ones, evts.ones)
    else:
        mu_1 = evts.events.bosons_combinations["0"]["0"]
        mu_2 = evts.events.bosons_combinations["0"]["1"]

        nominal = muon_id_weights(mu_1, mu_2, evts.year, syst_var="nominal")
        up = muon_id_weights(mu_1, mu_2, evts.year, syst_var="plus")
        down = muon_id_weights(mu_1, mu_2, evts.year, syst_var="minus")
        return nominal, up, down


def muon_iso_weight(evts: Events) -> Weight:
    # if MC, get pu weights
    if evts.data_or_mc == "data":
        return (evts.ones, evts.ones, evts.ones)
    else:
        mu_1 = evts.events.bosons_combinations["0"]["0"]
        mu_2 = evts.events.bosons_combinations["0"]["1"]

        nominal = muon_iso_weights(mu_1, mu_2, evts.year, syst_var="nominal")
        up = muon_iso_weights(mu_1, mu_2, evts.year, syst_var="plus")
        down = muon_iso_weights(mu_1, mu_2, evts.year, syst_var="minus")
        return nominal, up, down


def photon_id_weight(evts: Events) -> Weight:
    # if MC, get pu weights
    if evts.data_or_mc == "data":
        return (evts.ones, evts.ones, evts.ones)
    else:
        photon = evts.events.bosons_combinations["1"]

        nominal = photon_id_weights(photon, evts.year, syst_var="nominal")
        up = photon_id_weights(photon, evts.year, syst_var="plus")
        down = photon_id_weights(photon, evts.year, syst_var="minus")
        return nominal, up, down


def photon_electron_veto_weight(evts: Events) -> Weight:
    # if MC, get pu weights
    if evts.data_or_mc == "data":
        return (evts.ones, evts.ones, evts.ones)
    else:
        photon = evts.events.bosons_combinations["1"]

        nominal = photon_electron_veto_weights(photon, evts.year, syst_var="nominal")
        up = photon_electron_veto_weights(photon, evts.year, syst_var="plus")
        down = photon_electron_veto_weights(photon, evts.year, syst_var="minus")
        return nominal, up, down
