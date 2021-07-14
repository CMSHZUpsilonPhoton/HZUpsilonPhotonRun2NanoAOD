from coffea import processor, hist
import awkward as ak

from data.samples import samples_files, samples_descriptions

from functools import partial

import hist
# from hist import Hist

class analyzer(processor.ProcessorABC):
    def __init__(self):
        # self._histo = hist.Hist(
        #     "Events",
        #     hist.Cat("dataset", "Dataset"),
        #     hist.Cat("year", "year"),
        #     hist.Bin("mass", "Z mass", 60, 60, 120),
        # )
        # mass_axis = hist.Bin("mass", r"$m_{\mu\mu}$ [GeV]", 300, 0, 300)
        # pt_axis = hist.Bin("pt", r"$p_{T,\mu}$ [GeV]", 300, 0, 300)
        self._accumulator = processor.dict_accumulator({
            # 'cutflow': hist.Hist(
            #     "cutflow",
            #     hist.Cat("dataset", ""),
            #     hist.Cat("year", ""),
            #     hist.Bin("trigger", "", 2, 0, 2),
            #     hist.Bin("nmuons", "", 2, 0, 2),
            #     hist.Bin("muon_pt", "", 2, 0, 2),
            #     hist.Bin("tight_muon", "", 2, 0, 2),
            #     hist.Bin("iso_muon", "", 2, 0, 2),
            #     hist.Bin("nphotons", "", 2, 0, 2),
            #     hist.Bin("photon_pt", "", 2, 0, 2),
            #     hist.Bin("photon_sc_eta", "", 2, 0, 2),
            #     hist.Bin("photon_electron_veto", "", 2, 0, 2),
            #     hist.Bin("photon_tight_id", "", 2, 0, 2),
            #     # hist.Cat("signal_selection", ""),
            #     # hist.Cat("dimuon_mass", ""),
            #     # hist.Cat("boson_mass", ""),
            # ),
            # 'cutflow': Hist.new.Reg(10, -5, 5, overflow=False, underflow=False, name="A")
            #             .Bool(name="B")
            #             .Var(range(10), name="C")
            #             .Int(-5, 5, overflow=False, underflow=False, name="D")
            #             .IntCat(range(10), name="E")
            #             .StrCat(["T", "F"], name="F")
            #             .Double(),
            # 'mass': hist.Hist("Counts", dataset_axis, mass_axis),
            # 'mass_z1': hist.Hist("Counts", dataset_axis, mass_axis),
            # 'mass_z2': hist.Hist("Counts", dataset_axis, mass_axis),
            # 'pt_z1_mu1': hist.Hist("Counts", dataset_axis, pt_axis),
            # 'pt_z1_mu2': hist.Hist("Counts", dataset_axis, pt_axis),
            'cutflow': processor.defaultdict_accumulator(
                # we don't use a lambda function to avoid pickle issues
                partial(processor.defaultdict_accumulator, float)
            ),
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

        # print(trigger_filterto_numpy[0])


        # cutflow
        cutflow = (hist.Hist.new
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
                    .Double())

        cutflow.fill(
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

        # cutflow.show()
        # print(cutflow[True, True, True, True, True, True, True, True, True, True])

        # output['cutflow'][dataset]['total'] += len(events)
        # output['cutflow'][dataset]['trigger'] += ak.sum(trigger_filter)
        # output['cutflow'][dataset]['nmuons'] += ak.sum(trigger_filter & nmuons_filter)
        # output['cutflow'][dataset]['tight_muon'] += ak.sum(trigger_filter & nmuons_filter & muon_pt_filter & tight_muon_filter)
        # output['cutflow'][dataset]['iso_muon'] += ak.sum(trigger_filter & nmuons_filter & muon_pt_filter & tight_muon_filter & iso_muon_filter)
        



        # dimuon_events = events[
        #     (getattr(events.HLT, hlt_trigger_name) == 1) # pass HLT selection
        #     # (events.HLT_Mu17_Photon30_IsoCaloId == 1)
        #     & (ak.num(events.Muon) >= 2) # at least two muons
        #     # & (ak.sum(events.Muon.charge, axis=1) == 0)
        # ]
        # zmm = dimuon_events.Muon[:, 0] + dimuon_events.Muon[:, 1]
        # output.fill(
        #     dataset = dataset,
        #     year = year,
        #     mass = zmm.mass,
        # )
        return cutflow

    def postprocess(self, accumulator):
        # return accumulator
        pass