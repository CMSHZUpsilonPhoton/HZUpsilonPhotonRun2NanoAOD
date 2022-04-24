import awkward as ak
import numpy as np
from numpy.typing import ArrayLike


def l1prefiring_weights(
    events: ak.Array, n_events: int, year: str, syst_var: str = "nominal"
) -> ArrayLike:
    """Returns Photon Electron Veto SFs.
    References:
    https://twiki.cern.ch/twiki/bin/view/CMS/L1PrefiringWeightRecipe
    https://github.com/jdulemba/NanoAOD_Analyses/blob/a13406ea6d8614cfb13d738f227d4d29c4a21496/Analysis/python/MCWeights.py
    """

    l1prefiring_sf = np.ones(n_events)
    if (year != "2018") and ("L1PreFiringWeight" in events.fields):
        l1prefiring_sf = events.L1PreFiringWeight.Nom

        if syst_var != "nominal":
            if syst_var != "plus":
                l1prefiring_sf = events.L1PreFiringWeight.Up

            if syst_var != "minus":
                l1prefiring_sf = events.L1PreFiringWeight.Dn

    return l1prefiring_sf
