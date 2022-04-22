#!/usr/bin/env python

import os
import typer


def execute_command(command):
    print(f"\n\n\n\n--> Will execute:\n {command}")
    os.system(command)


def run_analysis(
    hostname: str,
    username: str,
    working_dir: str,
    uerj_usr: bool = False,
    debug: bool = True,
):
    inner_commands = f"cd {working_dir} ; conda activate ../HZUpsilonPhotonRun2NanoAOD_env ; ./run_analysis.py all"
    if debug:
        inner_commands += " --debug"
    inner_commands += " ; rm -rf outputs/buffer"
    full_command = f"ssh {username}@{hostname} '{inner_commands}'"
    if uerj_usr:
        full_command = f"ssh {username}@{hostname} 'ssh uerj-usr \"{inner_commands}\"'"

    execute_command(full_command)


def sync_working_directories(
    hostname: str, username: str, working_dir: str, uerj_usr: bool = False
):
    if uerj_usr:
        create_temp_dir = (
            f"ssh {username}@{hostname} 'mkdir -p /tmp/{username}/analysis_temp_dir'"
        )
        execute_command(create_temp_dir)
        sync_command = f"rsync -ah --info=progress2 --no-inc-recursive --delete --exclude='*.pyc' --exclude='.git' --exclude='__pycache__' --exclude='plots' --exclude='outputs' ./ {username}@lxplus.cern.ch:/tmp/{username}/analysis_temp_dir"
        execute_command(sync_command)
        re_sync_command = f"ssh {username}@{hostname} 'rsync -ah --info=progress2 --no-inc-recursive --exclude='*.pyc' --exclude='.git' --exclude='__pycache__' --exclude='plots' --exclude='outputs' --delete /tmp/{username}/analysis_temp_dir/ uerj-usr:{working_dir}'"
        execute_command(re_sync_command)
    else:
        sync_command = f"rsync -ah --info=progress2 --no-inc-recursive --delete --exclude='*.pyc' --exclude='.git' --exclude='__pycache__' --exclude='plots' --exclude='outputs' ./ {username}@{hostname}:{working_dir}"
        execute_command(sync_command)


def sync_outputs(
    hostname: str, username: str, working_dir: str, uerj_usr: bool = False
):
    if uerj_usr:
        create_temp_dir = f"ssh {username}@{hostname} 'mkdir -p /tmp/{username}/analysis_temp_dir/outputs'"
        execute_command(create_temp_dir)
        sync_command = f"ssh {username}@{hostname} 'rsync -ah --info=progress2 --no-inc-recursive uerj-usr:{working_dir}/outputs/ /tmp/{username}/analysis_temp_dir/outputs'"
        execute_command(sync_command)
        re_sync_command = f"rsync -ah --info=progress2 --no-inc-recursive {username}@lxplus.cern.ch:/tmp/{username}/analysis_temp_dir/outputs/ ./outputs "
        execute_command(re_sync_command)
    else:
        create_outputs_dir = f"mkdir -p outputs"
        execute_command(create_outputs_dir)
        sync_command = f"rsync -ah --info=progress2 --no-inc-recursive {username}@{hostname}:{working_dir}/outputs/ ./outputs "
        execute_command(sync_command)


def main(
    hostname: str,
    username: str,
    working_dir: str,
    uerj_usr: bool = False,
    outputs: bool = False,
    debug: bool = True,
):
    sync_working_directories(hostname, username, working_dir, uerj_usr)
    run_analysis(hostname, username, working_dir, uerj_usr, debug)
    if outputs:
        sync_outputs(hostname, username, working_dir, uerj_usr)


if __name__ == "__main__":
    typer.run(main)
