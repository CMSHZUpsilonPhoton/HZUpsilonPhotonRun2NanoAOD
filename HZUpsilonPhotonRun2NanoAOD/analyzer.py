from coffea import processor
import awkward as ak

from data.samples import samples_files, samples_descriptions

from functools import partial

import hist
# from hist import Hist

import uproot3

import secrets

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
        muon_pt_filter =  events.Muon.pt > 3
        tight_muon_filter = events.Muon.tightId == 1
        iso_muon_filter = events.Muon.pfRelIso03_all < 0.35
        
        # photons
        nphotons_filter = ak.num(events.Photon) >= 1
        photon_pt_filter = events.Photon.eCorr * events.Photon.pt > 33
        photon_sc_eta_filter = (events.Photon.isScEtaEB == 1) | (events.Photon.isScEtaEE == 1)
        photon_electron_veto_filter = events.Photon.electronVeto == 1
        photon_tight_id_filter = events.Photon.cutBased == 3

        # cutflow
        output['cutflow'].histogram.fill(
            dataset=dataset,
            year=year,
            trigger=trigger_filter,
            nmuons=nmuons_filter,
            muon_pt=ak.num(events.Muon[muon_pt_filter]) >= 2,
            tight_muon=ak.num(events.Muon[tight_muon_filter]) >= 2,
            iso_muon=ak.num(events.Muon[iso_muon_filter]) >= 2,
            nphotons=nphotons_filter,
            photon_pt=ak.num(events.Photon[photon_pt_filter]) >= 1,
            photon_sc_eta=ak.num(events.Photon[photon_sc_eta_filter]) >= 1,
            photon_electron_veto=ak.num(events.Photon[photon_electron_veto_filter]) >= 1,
            photon_tight_id=ak.num(events.Photon[photon_tight_id_filter]) >= 1,
            # signal_selection=,
            # dimuon_mass=,
            # boson_mass=,
            )

        # dimuon sample
        dimuon = ak.combinations(events.Muon[muon_pt_filter & tight_muon_filter & iso_muon_filter], 2)
        dimuon = dimuon[(dimuon["0"].charge + dimuon["1"].charge) == 0]
        dimuon_mass = (dimuon["0"] + dimuon["1"]).mass

        dimuon_mass_filename = f'outputs/buffer/dimuon_mass_{dataset}_{year}_{secrets.token_hex(nbytes=20)}.root'
        with uproot3.recreate(dimuon_mass_filename) as f:
            f["dimuon_mass"] = uproot3.newtree({"mass": "float"})
            f["dimuon_mass"].extend({"mass": ak.flatten(dimuon_mass)})

        # boson
        boson = ak.cartesian([dimuon, events.Photon[photon_pt_filter & photon_electron_veto_filter & photon_sc_eta_filter & photon_tight_id_filter]])
        boson_pt = (boson["0"]["0"] + boson["0"]["1"] + boson["1"]).pt
        boson = ak.flatten(boson[ak.argsort(boson_pt, ascending=False)][:,:1])
        boson_mass = (boson["0"]["0"] + boson["0"]["1"] + boson["1"]).mass
        # print(boson_mass)

        
        # end processing
        return output

    def postprocess(self, accumulator):
        return accumulator
        