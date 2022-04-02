#!/usr/bin/env python


import os
from pprint import pprint
import json


from HZUpsilonPhotonRun2NanoAOD import file_tester
from HZUpsilonPhotonRun2NanoAOD.Analyzer import Analyzer
from HZUpsilonPhotonRun2NanoAOD.GenAnalyzer import GenAnalyzer
from HZUpsilonPhotonRun2NanoAOD.file_tester import file_tester
from samples import samples, mc_samples_files, samples_files, samples_descriptions

from coffea import processor
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
from HZUpsilonPhotonRun2NanoAOD.HistAccumulator import HistAccumulator
from HZUpsilonPhotonRun2NanoAOD.output_merger import output_merger

from coffea.util import save

def main():
    # # test uproot.open each sample
    # for k in samples_files.keys():
    #     for f in samples_files[k]:
    #         file_tester(f)

    # clear buffer
    os.system("rm -rf outputs/*")
    os.system("mkdir -p outputs/buffer")

    # run gen level analysis 
    print("--> Running GEN level analysis...")
    gen_output = processor.run_uproot_job(
        fileset=mc_samples_files,
        treename="Events",
        processor_instance=GenAnalyzer(),
        executor=processor.futures_executor,
        # executor = processor.iterative_executor,
        executor_args={"schema": NanoAODSchema, "workers": 60},
        # executor_args = {"schema": NanoAODSchema},
        # chunksize =
        # maxchunks = 100,
    )

    # save gen level outputs
    print("--> saving GEN level output...")
    gen_output_filename = "outputs/gen_output.json"
    os.system(f"rm -rf {gen_output_filename}")
    # create json object from dictionary
    with open(gen_output_filename,"w") as f:
        f.write(json.dumps(gen_output))

    # run analysis 
    print("--> Running MAIN level analysis...")
    output = processor.run_uproot_job(
        fileset=samples_files,
        treename="Events",
        processor_instance=Analyzer(gen_output=gen_output),
        executor=processor.futures_executor,
        # executor = processor.iterative_executor,
        executor_args={"schema": NanoAODSchema, "workers": 60},
        # executor_args = {"schema": NanoAODSchema},
        # chunksize =
        # maxchunks = 100,
    )

    # save outputs
    print("--> saving output...")
    output_filename = "outputs/cutflow.hist"
    os.system(f"rm -rf {output_filename}")
    save(output["cutflow"].histogram, output_filename)

    # # how to access the saved object
    # # from coffea.util import load
    # # import hist
    # # load('outputs/buffer/cutflow.hist')

    # Merge the many outputs 
    print("--> Merging analysis outputs...")
    # output_merger()


if __name__ =="__main__":
    main()