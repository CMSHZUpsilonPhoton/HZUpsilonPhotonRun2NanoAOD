import os

from HZUpsilonPhotonRun2NanoAOD import file_tester
from HZUpsilonPhotonRun2NanoAOD.analyzer import analyzer
from HZUpsilonPhotonRun2NanoAOD.analyzer import analyzer
from HZUpsilonPhotonRun2NanoAOD.file_tester import file_tester
from data.samples import samples_files, samples_descriptions

from coffea import processor
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
from HZUpsilonPhotonRun2NanoAOD.HistAccumulator import HistAccumulator

from coffea.util import save

# # test uproot.open each sample
# for k in samples_files.keys():
#     for f in samples_files[k]:
#         file_tester(f)


# run analysis code
output = processor.run_uproot_job(
    fileset = samples_files,
    treename = "Events",
    processor_instance = analyzer(),
    executor = processor.futures_executor,
    # executor = processor.iterative_executor,
    executor_args = {"schema": NanoAODSchema, "workers": 30},
    # executor_args = {"schema": NanoAODSchema},
    # chunksize = 
)

# print(result[0, "2018", True, True, True, True, True, True, True, True, True, True, ])
# print(result[1, "2018", True, True, True, True, True, True, True, True, True, True, ])
# print(result[2, "2018", True, True, True, True, True, True, True, True, True, True, ])
# print(result[3, "2018", True, True, True, True, True, True, True, True, True, True, ])
print(output['cutflow'].histogram[:, "2018", True, True, True, True, True, True, True, True, True, True, ])

# save outputs
print('--> saving output...')
output_filename = 'outputs/buffer/cutflow.hist'
os.system(f'rm -rf {output_filename}')
save(output['cutflow'].histogram, output_filename)

# how to access the saved object
# from coffea.util import load
# import hist
# load('outputs/buffer/cutflow.coffea')

