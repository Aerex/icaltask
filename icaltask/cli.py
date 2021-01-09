#!/usr/bin/env python3

from os import symlink, path, unlink, makedirs, chmod
from sys import platform
from pathlib import Path
import subprocess
import argparse

PROJ_DIR = Path(__file__).resolve().parent.parent
HOOKS_PY: str = '{PROJ_DIR}/hook.py'.format(PROJ_DIR=PROJ_DIR)
ICALTASKRC: str = 'icaltaskrc'
TASK_HOOK_DIR: str = path.expanduser('~/.task/hooks')
ON_ADD_PY: str = '{TASKS_HOOKS_DIR}/on-add.icaltask.py'.format(TASKS_HOOKS_DIR=TASK_HOOK_DIR)
ON_MODIFY_PY: str = '{TASKS_HOOKS_DIR}/on-modify.icaltask.py'.format(TASKS_HOOKS_DIR=TASK_HOOK_DIR)
UDA_CONFIGS = {
    'uda.uid.type': 'string',
    'uda.uid.label': '"iCal UID"',
    'uda.geo.type': 'string',
    'uda.geo.label': '"iCal GEO"'
}
SYSTEM: str
if 'linux' in platform:
    SYSTEM = 'Linux'
elif 'bsd' in platform:
    SYSTEM = 'BSD'
elif 'darwin' in platform:
    SYSTEM = 'MacOS'
else:
    SYSTEM = 'Windows'


def _uninstall():
    for file in [ON_ADD_PY, ON_MODIFY_PY]:
        if not path.exists(file):
            print('{FILE} already uninstalled'.format(FILE=file))
        else:
            unlink(file)
            print('{FILE} hook has been successfully unlinked from system'.format(FILE=file))

    for uda_config in UDA_CONFIGS.keys():
        cmd = 'task rc.confirmation=off rc.verbose=off config {CONFIG_LABEL}'.format(
            CONFIG_LABEL=uda_config
        )
        subprocess.run(cmd, shell=True, check=True)
        print('Removed {} configuration from taskrc'.format(uda_config))

def _copy_config():
    '''
    Copy over the same configuration file into the configuration directory.
    If the file already exists the user will have the option to override the existing config
    For Linux/MacOS the configuration directory will under `~/.config/icaltask` folder
    For Windows the configuration directory will under the `AppData/icaltask` folder
    '''
    fname: str = path.join(
        path.dirname(__file__),
        '../icaltaskrc'
    )
    with open(fname, 'r') as f:
        config = f.read()

    config_dir: str = path.expanduser('~/.config/icaltask')
    if SYSTEM == 'Windows':
        config_dir: str = 'AppData/icaltask/'

    if not path.exists(config_dir):
        makedirs(config_dir)
    fname = config_dir + '/' + ICALTASKRC
    if path.exists(fname):
        override_config_res = input('{} already exists. Are you sure you want to override it? [Yy]: '.format(ICALTASKRC))
        if override_config_res not in ['y', 'Y']:
            return
    with open(fname, 'w') as c:
        c.write(config)
        chmod(config_dir, 0o755)


def _install():
    for file in [ON_ADD_PY, ON_MODIFY_PY]:
        if path.exists(file):
            print('{FILE} already installed'.format(FILE=file))
        else:
            symlink(HOOKS_PY, file)
            print('{FILE} hook has been successfully symlinked to system'.format(FILE=file))

    for uda_config in UDA_CONFIGS.keys():
        cmd = 'task rc.confirmation=off rc.verbose=off config {CONFIG_LABEL} {CONFIG_VALUE}'.format(
            CONFIG_LABEL=uda_config,
            CONFIG_VALUE=UDA_CONFIGS[uda_config]
        )
        subprocess.run(cmd, shell=True, check=True)
        print('Added {} configuration to taskrc'.format(uda_config))


def main():
    cmd = argparse.ArgumentParser(prog='icaltask', description='Synchronize taskwarrior tasks with an iCalendar server')
    subcmds = cmd.add_subparsers(dest='icaltask')

    subcmds.add_parser('install', help='Install taskwarrior hooks and configs for icaltask')
    subcmds.add_parser('uninstall', help='Uninstall taskwarrior hooks and configs for icaltask')

    subcmds.add_parser('push', help='Execute a one-way sync to push non-iCal tasks to iCalendar server')

    subcmds.add_parser('copy-config', help='Copy sample configuration to configuration directory.')
    args = cmd.parse_args()

    if args.icaltask == 'install':
        _install()
    elif args.icaltask == 'uninstall':
        _uninstall()
    elif args.icaltask == 'copy-config':
        _copy_config()
    else:
        cmd.print_help()


if __name__ == "__main__":
    main()
