#!/usr/bin/env python


import os
from pprint import pprint
import json
import typer
from tqdm import tqdm
from enum import Enum


from HZUpsilonPhotonRun2NanoAOD import file_tester
from HZUpsilonPhotonRun2NanoAOD.analyzer import Analyzer
from HZUpsilonPhotonRun2NanoAOD.gen_analyzer import GenAnalyzer
from HZUpsilonPhotonRun2NanoAOD.file_tester import file_tester
from samples import samples, mc_samples_files, samples_files, samples_descriptions

from coffea import processor
from coffea.nanoevents import NanoAODSchema
from HZUpsilonPhotonRun2NanoAOD.hist_accumulator import HistAccumulator
from HZUpsilonPhotonRun2NanoAOD.output_merger import output_merger

from coffea.util import save

# create typer app
help_str = """
H/Z \n\n\n--> Y(nS) + gamma analysis code (NanoAOD - Run2) \n\n

Usual workflow:\n
# clear output buffers\n
./run_analysis.py clear \n

# generator level analysis (filtering, getting total number of events, polarization, ...)\n
./run_analysis.py gen \n

# main analysis code for signal selection\n
./run_analysis.py main \n

# merge the many outputs [buffers], per sample and per process [Data or MC sample]\n
./run_analysis.py merge \n

\n\n\n--> To run the whole chain in a single shot: ./run_analysis.py all
"""
app = typer.Typer(help=typer.style(help_str, fg=typer.colors.BRIGHT_BLUE, bold=True))


@app.command()
def test_files():
    """Test uproot.open each sample file."""
    files = []
    for s in samples:
        for f in samples[s]["files"]:
            files.append(f)
    for f in tqdm(files):
        file_tester(f)


@app.command()
def clear():
    """Clear outputs."""

    os.system("rm -rf outputs/*")
    os.system("mkdir -p outputs/buffer")


@app.command()
def gen():
    """Run gen level analysis and saves outputs."""

    os.system("rm -rf outputs/gen_output.json")
    os.system("mkdir -p outputs/")

    # run gen level analysis
    print("\n\n\n--> Running GEN level analysis...")
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
    print("\n\n\n--> Saving GEN level output...")
    gen_output_filename = "outputs/gen_output.json"
    os.system(f"rm -rf {gen_output_filename}")
    # create json object from dictionary
    with open(gen_output_filename, "w") as f:
        f.write(json.dumps(gen_output))


class CoffeaExecutors(str, Enum):
    futures = "futures"
    iterative = "iterative"


@app.command()
def main(
    maxchunks: int = -1,
    executor: CoffeaExecutors = CoffeaExecutors.futures,
    workers: int = 60,
):
    """Run main analysis and saves outputs."""

    executor_args = {"schema": NanoAODSchema, "workers": workers}
    if executor.value == "interative":
        executor_args = {"schema": NanoAODSchema}

    executor = getattr(processor, f"{executor.value}_executor")

    if maxchunks == -1:
        maxchunks = None

    # clear buffers
    os.system("rm -rf outputs/buffer")
    os.system("mkdir -p outputs/buffer")

    # gets gen level output
    gen_output_filename = "outputs/gen_output.json"
    with open(gen_output_filename, "r") as f:
        gen_output = json.load(f)

    # run analysis
    print("\n\n\n--> Running MAIN level analysis...")
    output = processor.run_uproot_job(
        fileset=samples_files,
        treename="Events",
        processor_instance=Analyzer(gen_output=gen_output),
        # executor=processor.futures_executor,
        # executor = processor.iterative_executor,
        executor=executor,
        executor_args=executor_args,
        # executor_args = {"schema": NanoAODSchema},
        # chunksize =
        maxchunks=maxchunks,
    )

    # save outputs
    print("\n\n\n--> saving output...")
    output_filename = "outputs/cutflow.hist"
    os.system(f"rm -rf {output_filename}")
    save(output["cutflow"].histogram, output_filename)


@app.command()
def merge():
    """Merge the many outputs."""
    os.system("rm -rf outputs/*.root")

    print("\n\n\n--> Merging analysis outputs...")
    with open("outputs/output_merger.log", "w") as f:
        f.write(output_merger())


@app.command()
def all():
    """Run default workflow (CLEAR \n\n\n--> GEN \n\n\n--> MAIN \n\n\n--> MERGE)."""

    clear()
    gen()
    main()
    merge()


if __name__ == "__main__":
    app()  # start typer app
