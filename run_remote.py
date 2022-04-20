#!/usr/bin/env python

import subprocess
import typer

def run_analysis(hostname: str, username: str, working_dir: str, uerj_usr: bool = False):
    # inner_commands = f"cd {working_dir} ; conda activate ../HZUpsilonPhotonRun2NanoAOD_env ; ./run_analysis.py all"
    inner_commands = f"cd {working_dir} ; conda activate ../HZUpsilonPhotonRun2NanoAOD_env ; pwd"
    full_command = f"ssh {username}@{hostname} '{inner_commands}'"
    if uerj_usr:
        full_command = f"ssh {username}@{hostname} 'ssh uerj-usr \"{inner_commands}\"'"
     

    print(f"--> Will execute:\n {full_command}")
    try:
        output = subprocess.check_output(full_command, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
    except subprocess.CalledProcessError as exc:
        print("--> ERROR: Command execution failled. Error code:", exc.returncode, exc.output)
        exit(1)
    else:
        print("\n{}\n".format(output))

def sync_working_directories(hostname: str, username: str, working_dir: str, uerj_usr: bool = False):
    sync_command = f"rsync -azP --delete --exclude={'outputs','.git'} ./ {username}@{hostname}:{working_dir}"
    
    print(f"--> Will execute:\n {full_command}")
    try:
        output = subprocess.check_output(sync_command, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
    except subprocess.CalledProcessError as exc:
        print("--> ERROR: Command execution failled. Error code:", exc.returncode, exc.output)
        exit(1)
    else:
        print("\n{}\n".format(output))

def main(hostname: str, username: str, working_dir: str, uerj_usr: bool = False):
    sync_working_directories(hostname, username, working_dir, uerj_usr)
    run_analysis(hostname, username, working_dir, uerj_usr)

if __name__ == "__main__":
    typer.run(main)

    