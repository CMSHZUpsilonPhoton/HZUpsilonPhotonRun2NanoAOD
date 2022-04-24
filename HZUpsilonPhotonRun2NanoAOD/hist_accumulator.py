import hist
from coffea.processor import AccumulatorABC


class HistAccumulator(AccumulatorABC):
    """A histogram accumulator based 'hist' module."""

    def __init__(self, histo):
        if not isinstance(histo, hist.Hist):
            raise ValueError("HistAccumulator only works with 'hist' histograms.")
        self._histo = histo

    def __repr__(self):
        return self._histo

    @property
    def histogram(self):
        return self._histo

    def identity(self):
        return HistAccumulator(
            hist.Hist(*self._histo.axes, storage=hist.storage.Double())
        )

    def add(self, other):
        """Add another accumulator to this one in-place"""
        if isinstance(other, HistAccumulator(hist.Hist)):
            # self._histo =  self._histo
            self._histo = self._histo + other.histogram
        else:
            raise ValueError

    # inplace add operator
    def __iadd__(self, other):
        self._histo = self._histo + other.histogram
        return self

    # add operator
    def __add__(self, other):
        return self._histo + other.histogram
