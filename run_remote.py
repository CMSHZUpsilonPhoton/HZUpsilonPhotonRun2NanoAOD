#!/usr/bin/env python

import os

import typer


def execute_command(command: str) -> None:
    print(f"\n\n\n\n--> Will execute:\n {command}")
    os.system(command)


def run_analysis(
    hostname: str,
    username: str,
    working_dir: str,
    uerj_usr: bool = False,
    debug: bool = True,
) -> None:
    inner_commands = f"cd {working_dir} ; conda activate ../HZUpsilonPhotonRun2NanoAOD_env ; ./run_analysis.py all"
    if debug:
        inner_commands += " --debug"
    inner_commands += " ; rm -rf outputs/buffer"
    full_command = f"stdbuf -oL ssh {username}@{hostname} '{inner_commands}'"
    if uerj_usr:
        full_command = (
            f"stdbuf -oL ssh {username}@{hostname} 'ssh uerj-usr \"{inner_commands}\"'"
        )

    execute_command(full_command)


def sync_working_directories(
    hostname: str, username: str, working_dir: str, uerj_usr: bool = False
) -> None:
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
) -> None:
    remove_old_buffered_stuff = "rm -rf outputs"
    execute_command(remove_old_buffered_stuff)
    if uerj_usr:
        create_temp_dir = f"ssh {username}@{hostname} 'mkdir -p /tmp/{username}/analysis_temp_dir/outputs'"
        execute_command(create_temp_dir)
        sync_command = f"ssh {username}@{hostname} 'rsync -ah --info=progress2 --no-inc-recursive uerj-usr:{working_dir}/outputs/ /tmp/{username}/analysis_temp_dir/outputs'"
        execute_command(sync_command)
        tar_files = f"rm -rf /eos/user/f/{username}/www/analysis_buffer/hzupsilonphoton_outputs_buffer.tar.gz ; tar -zcvf /eos/user/f/{username}/www/analysis_buffer/hzupsilonphoton_outputs_buffer.tar.gz /tmp/{username}/analysis_temp_dir/outputs/*.root"
        re_sync_command = f"ssh {username}@{hostname} '{tar_files}'"
        execute_command(re_sync_command)
    else:
        create_outputs_dir = "mkdir -p outputs"
        execute_command(create_outputs_dir)
        tar_files = f"rm -rf /eos/user/f/{username}/www/analysis_buffer/hzupsilonphoton_outputs_buffer.tar.gz ; tar -zcvf /eos/user/f/{username}/www/analysis_buffer/hzupsilonphoton_outputs_buffer.tar.gz {working_dir}/outputs/*.root"
        copy_to_www = f"ssh {username}@{hostname} '{tar_files}'"
        execute_command(copy_to_www)
        # sync_command = f"rsync -ah --info=progress2 --exclude='buffer' --no-inc-recursive {username}@{hostname}:{working_dir}/outputs/ ./outputs "
        # execute_command(sync_command)

    download = "mkdir -p outputs ; wget -c https://ftorresd.web.cern.ch/ftorresd/analysis_buffer/hzupsilonphoton_outputs_buffer.tar.gz -O outputs/hzupsilonphoton_outputs_buffer.tar.gz ; cd outputs ; tar -xzvf hzupsilonphoton_outputs_buffer.tar.gz"
    execute_command(download)


def main(
    hostname: str,
    username: str,
    working_dir: str,
    uerj_usr: bool = False,
    outputs: bool = False,
    debug: bool = True,
) -> None:
    sync_working_directories(hostname, username, working_dir, uerj_usr)
    run_analysis(hostname, username, working_dir, uerj_usr, debug)
    if outputs:
        sync_outputs(hostname, username, working_dir, uerj_usr)


if __name__ == "__main__":
    typer.run(main)
