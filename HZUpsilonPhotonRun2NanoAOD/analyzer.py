from coffea import processor
import awkward as ak

from data.samples import samples_files, samples_descriptions

from functools import partial

import hist
# from hist import Hist

from HZUpsilonPhotonRun2NanoAOD.HistAccumulator import HistAccumulator

class analyzer(processor.ProcessorABC):
    def __init__(self):
        self._accumulator = processor.dict_accumulator({
            'cutflow': HistAccumulator(hist.Hist.new
                    .StrCat(samples_files.keys(), name="dataset")
                    .StrCat(["2016", "2017", "2018"], name="year")
                    .Bool(name="trigger")
                    .Bool(name="nmuons")
                    .Bool(name="muon_pt")
                    .Bool(name="tight_muon")
                    .Bool(name="iso_muon")
                    .Bool(name="nphotons")
                    .Bool(name="photon_pt")
                    .Bool(name="photon_sc_eta")
                    .Bool(name="photon_electron_veto")
                    .Bool(name="photon_tight_id")
                    .Double()),
        })

    @property
    def accumulator(self):
        return self._accumulator

    # we will receive a NanoEvents 
    def process(self, events):
        dataset = events.metadata["dataset"]
        year = samples_descriptions[dataset]['year']
        data_or_mc = samples_descriptions[dataset]['data_or_mc']

        # define HLT trigger path string
        if year == '2016':
            hlt_trigger_name = 'Mu17_Photon30_IsoCaloId'
        if year == '2017':
            hlt_trigger_name = 'Mu17_Photon30_IsoCaloId'
        if year == '2018':
            hlt_trigger_name = 'Mu17_Photon30_IsoCaloId'
        
        # define accumulator
        output = self.accumulator.identity()

        ## filters
        # trigger
        trigger_filter = getattr(events.HLT, hlt_trigger_name) == 1
        
        # muons
        nmuons_filter = ak.num(events.Muon) >= 2
        muon_pt_filter =  ak.num(events.Muon[events.Muon.pt > 3]) >= 2
        tight_muon_filter = ak.num(events.Muon[events.Muon.tightId == 1]) >= 2
        iso_muon_filter = ak.num(events.Muon[events.Muon.pfRelIso03_all < 0.35]) >= 2
        
        # photons
        nphotons_filter = ak.num(events.Photon) >= 1
        photon_pt_filter = ak.num(events.Photon[events.Photon.eCorr * events.Photon.pt > 33]) >= 1
        photon_sc_eta_filter = ak.num(events.Photon[(events.Photon.isScEtaEB == 1) | (events.Photon.isScEtaEE == 1)]) >= 2
        photon_electron_veto_filter = ak.num(events.Photon[events.Photon.electronVeto == 1]) >= 2
        photon_tight_id_filter = ak.num(events.Photon[events.Photon.cutBased == 3]) >= 2

        # cutflow
        output['cutflow'].histogram.fill(
            dataset=dataset,
            year=year,
            trigger=trigger_filter,
            nmuons=nmuons_filter,
            muon_pt=muon_pt_filter,
            tight_muon=tight_muon_filter,
            iso_muon=iso_muon_filter,
            nphotons=nphotons_filter,
            photon_pt=photon_pt_filter,
            photon_sc_eta=photon_sc_eta_filter,
            photon_electron_veto=photon_electron_veto_filter,
            photon_tight_id=photon_tight_id_filter,
            # signal_selection=,
            # dimuon_mass=,
            # boson_mass=,
            )

        return output

    def postprocess(self, accumulator):
        return accumulator
        