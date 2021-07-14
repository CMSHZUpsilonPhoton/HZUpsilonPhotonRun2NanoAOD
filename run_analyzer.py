from HZUpsilonPhotonRun2NanoAOD import file_tester
from HZUpsilonPhotonRun2NanoAOD.analyzer import analyzer
from HZUpsilonPhotonRun2NanoAOD.analyzer import analyzer
from HZUpsilonPhotonRun2NanoAOD.file_tester import file_tester
from data.samples import samples_files, samples_descriptions

from coffea import processor
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema

# # test uproot.open each sample
# for k in samples_files.keys():
#     for f in samples_files[k]:
#         file_tester(f)


# run analysis code
result = processor.run_uproot_job(
    fileset = samples_files,
    treename = "Events",
    processor_instance = analyzer(),
    executor = processor.futures_executor,
    executor_args = {"schema": NanoAODSchema, "workers": 30},
    # chunksize = 
)

# print(result[0, "2018", True, True, True, True, True, True, True, True, True, True, ])
# print(result[1, "2018", True, True, True, True, True, True, True, True, True, True, ])
# print(result[2, "2018", True, True, True, True, True, True, True, True, True, True, ])
# print(result[3, "2018", True, True, True, True, True, True, True, True, True, True, ])
print(result[:, "2018", True, True, True, True, True, True, True, True, True, True, ])

