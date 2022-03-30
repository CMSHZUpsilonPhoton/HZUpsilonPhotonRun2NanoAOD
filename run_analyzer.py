import os

from HZUpsilonPhotonRun2NanoAOD import file_tester
from HZUpsilonPhotonRun2NanoAOD.analyzer import Analyzer
from HZUpsilonPhotonRun2NanoAOD.file_tester import file_tester
from samples import samples_files, samples_descriptions

from coffea import processor
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
from HZUpsilonPhotonRun2NanoAOD.HistAccumulator import HistAccumulator

from coffea.util import save

# # test uproot.open each sample
# for k in samples_files.keys():
#     for f in samples_files[k]:
#         file_tester(f)

# clear buffer
os.system("rm -rf outputs/*")
os.system("mkdir -p outputs/buffer ; touch outputs/buffer/__PLACEHOLDER__")

# run analysis code
output = processor.run_uproot_job(
    fileset=samples_files,
    treename="Events",
    processor_instance=Analyzer(),
    executor=processor.futures_executor,
    # executor = processor.iterative_executor,
    executor_args={"schema": NanoAODSchema, "workers": 30},
    # executor_args = {"schema": NanoAODSchema},
    # chunksize =
    # maxchunks = 100,
)

# save outputs
print("--> saving output...")
output_filename = "outputs/cutflow.hist"
os.system(f"rm -rf {output_filename}")
save(output["cutflow"].histogram, output_filename)

# how to access the saved object
# from coffea.util import load
# import hist
# load('outputs/buffer/cutflow.hist')

# merge dimuon masses
print("--> merging dimuon masses...")
for sample in samples_files.keys():
    os.system(
        f"hadd -f outputs/dimuons_mass_{sample}.root outputs/buffer/dimuons_mass_{sample}*.root "
    )

os.system(
    f"hadd -f outputs/dimuons_mass_Run2016.root outputs/dimuons_mass_Run2016*.root "
)
os.system(
    f"hadd -f outputs/dimuons_mass_Run2017.root outputs/dimuons_mass_Run2017*.root "
)
os.system(
    f"hadd -f outputs/dimuons_mass_Run2018.root outputs/dimuons_mass_Run2018*.root "
)
