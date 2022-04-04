import os
from samples import samples, samples_files, samples_descriptions


def output_merger():
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
    # os.system(
    #     f"hadd -f outputs/dimuons_mass_Run2.root outputs/dimuons_mass_Run2*.root "
    # )

    # for sample in samples:
    #     if samples[sample]["data_or_mc"] == "mc":
    #         os.system(
    #             f"hadd -f outputs/dimuons_mass_{sample}.root outputs/dimuons_mass_{sample}*.root "
    #         )

    # merge preselected events
    print("--> merging preselected events...")
    for sample in samples_files.keys():
        os.system(
            f"hadd -f outputs/preselected_{sample}.root outputs/buffer/preselected*{sample}*.root "
        )

    os.system(
        f"hadd -f outputs/preselected_Run2016.root outputs/preselected_Run2016*.root "
    )
    os.system(
        f"hadd -f outputs/preselected_Run2017.root outputs/preselected_Run2017*.root "
    )
    os.system(
        f"hadd -f outputs/preselected_Run2018.root outputs/preselected_Run2018*.root "
    )

    # os.system(
    #     f"hadd -f outputs/preselected_Run2.root outputs/preselected_Run2*.root "
    # )

    # for sample in samples:
    #     if samples[sample]["data_or_mc"] == "mc":
    #         os.system(
    #             f"hadd -f outputs/preselected_{sample}.root outputs/preselected_{sample}*.root "
    #         )

    # merge selected events
    print("--> merging preselected events...")
    for sample in samples_files.keys():
        os.system(
            f"hadd -f outputs/selected_{sample}.root outputs/buffer/selected*{sample}*.root "
        )

    os.system(
        f"hadd -f outputs/selected_Run2016.root outputs/selected_Run2016*.root "
    )
    os.system(
        f"hadd -f outputs/selected_Run2017.root outputs/selected_Run2017*.root "
    )
    os.system(
        f"hadd -f outputs/selected_Run2018.root outputs/selected_Run2018*.root "
    )
    # os.system(
    #     f"hadd -f outputs/selected_Run2.root outputs/selected_Run2*.root "
    # )

    # for sample in samples:
    #     if samples[sample]["data_or_mc"] == "mc":
    #         os.system(
    #             f"hadd -f outputs/selected_{sample}.root outputs/selected_{sample}*.root "
    #         )