# from __future__ import annotations

# import hist
# from coffea.processor import AccumulatorABC


# class HistAccumulator(AccumulatorABC):
#     """A histogram accumulator based 'hist' module."""

#     def __init__(self, histo: hist.Hist) -> None:
#         if not isinstance(histo, hist.Hist):
#             raise ValueError("HistAccumulator only works with 'hist' histograms.")
#         self._histo = histo

#     def __repr__(self) -> hist.Hist:
#         return self._histo

#     @property
#     def histogram(self) -> hist.Hist:
#         return self._histo

#     def identity(self) -> HistAccumulator:
#         return HistAccumulator(
#             hist.Hist(*self._histo.axes, storage=hist.storage.Double())
#         )

#     def add(self, other: hist.Hist) -> None:
#         """Add another accumulator to this one in-place"""
#         if isinstance(other, HistAccumulator(hist.Hist)):
#             self._histo = self._histo + other.histogram
#         else:
#             raise ValueError

#     # inplace add operator
#     def __iadd__(self, other: hist.Hist) -> hist.Hist:
#         self._histo = self._histo + other.histogram
#         return self

#     # add operator
#     def __add__(self, other: hist.Hist) -> hist.Hist:
#         return self._histo + other.histogram
