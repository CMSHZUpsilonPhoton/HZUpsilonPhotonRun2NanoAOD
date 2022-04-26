import subprocess

from samples.samples_details import data_samples_files, samples_files


def execute_command(command: str) -> str:
    """Will execute a given `command` and return its output."""
    print(f"\n\n\n--> Will execute:\n {command}")
    try:
        output = subprocess.check_output(
            command, stderr=subprocess.STDOUT, shell=True, universal_newlines=True
        )
    except subprocess.CalledProcessError as exc:
        error_message = f"--> ERROR: Command execution failled. \nError code: {exc.returncode}, \nError output: {exc.output}"
        print(error_message)
        return error_message
    else:
        return output


def output_merger() -> str:
    # merge dimuon masses
    print("--> merging dimuon masses...")
    merger_output = ""
    for sample in data_samples_files.keys():
        merger_output += execute_command(
            f"hadd -f outputs/dimuons_mass_{sample}.root outputs/buffer/dimuons_mass_{sample}*.root "
        )

    # merger_output += execute_command(
    #     f"hadd -f outputs/dimuons_mass_Run2016APV.root outputs/dimuons_mass_Run2016APV*.root "
    # )
    # merger_output += execute_command(
    #     f"hadd -f outputs/dimuons_mass_Run2016.root outputs/dimuons_mass_Run2016*.root "
    # )
    # merger_output += execute_command(
    #     f"hadd -f outputs/dimuons_mass_Run2017.root outputs/dimuons_mass_Run2017*.root "
    # )
    merger_output += execute_command(
        "hadd -f outputs/dimuons_mass_Run2018.root outputs/dimuons_mass_Run2018*.root "
    )
    # merger_output += execute_command(
    #     f"hadd -f outputs/dimuons_mass_Run2.root outputs/dimuons_mass_Run2016APV.root outputs/dimuons_mass_Run2016.root outputs/dimuons_mass_Run2017.root outputs/dimuons_mass_Run2018.root "
    # )

    # merge preselected events
    print("--> merging preselected events...")
    for sample in samples_files.keys():
        merger_output += execute_command(
            f"hadd -f outputs/preselected_{sample}.root outputs/buffer/preselected*{sample}*.root "
        )

    # merger_output += execute_command(
    #     f"hadd -f outputs/preselected_Run2016APV.root outputs/preselected_Run2016APV*.root "
    # )
    # merger_output += execute_command(
    #     f"hadd -f outputs/preselected_Run2016.root outputs/preselected_Run2016*.root "
    # )
    # merger_output += execute_command(
    #     f"hadd -f outputs/preselected_Run2017.root outputs/preselected_Run2017*.root "
    # )
    merger_output += execute_command(
        "hadd -f outputs/preselected_Run2018.root outputs/preselected_Run2018*.root "
    )

    # execute_command(
    #     f"hadd -f outputs/preselected_Run2.root outputs/preselected_Run2016APV.root outputs/preselected_Run2016.root outputs/preselected_Run2017.root outputs/preselected_Run2018.root "
    # )

    # merge selected events
    print("--> merging preselected events...")
    for sample in samples_files.keys():
        merger_output += execute_command(
            f"hadd -f outputs/selected_{sample}.root outputs/buffer/selected*{sample}*.root "
        )

    # merger_output += execute_command(
    #     f"hadd -f outputs/selected_Run2016APV.root outputs/selected_Run2016AVP*.root "
    # )
    # merger_output += execute_command(
    #     f"hadd -f outputs/selected_Run2016.root outputs/selected_Run2016*.root "
    # )
    # merger_output += execute_command(
    #     f"hadd -f outputs/selected_Run2017.root outputs/selected_Run2017*.root "
    # )
    merger_output += execute_command(
        "hadd -f outputs/selected_Run2018.root outputs/selected_Run2018*.root "
    )
    # merger_output += execute_command(
    #     f"hadd -f outputs/selected_Run2.root outputs/selected_Run2016APV.root outputs/selected_Run2016.root outputs/selected_Run2017.root outputs/selected_Run2018.root "
    # )

    return merger_output
