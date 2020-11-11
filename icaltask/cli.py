#!/usr/bin/env python3

from os import symlink, path, unlink, write, makedirs, chmod
from sys import platform
from pathlib import Path
import subprocess
import argparse

PROJ_DIR = Path(__file__).resolve().parent.parent
HOOKS_PY: str = '{PROJ_DIR}/hook.py'.format(PROJ_DIR=PROJ_DIR)
TASK_HOOK_DIR: str = path.expanduser('~/.task/hooks')
ON_ADD_PY: str = '{TASKS_HOOKS_DIR}/on-add.icaltask.py'.format(TASKS_HOOKS_DIR=TASK_HOOK_DIR)
ON_MODIFY_PY: str = '{TASKS_HOOKS_DIR}/on-modify.icaltask.py'.format(TASKS_HOOKS_DIR=TASK_HOOK_DIR)
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
    unlink(ON_ADD_PY)
    unlink(ON_MODIFY_PY)
    print('{FILE} hook has been successfully unlinked from system'.format(FILE=ON_ADD_PY))
    print('{FILE} hook has been successfully unlinked from system'.format(FILE=ON_MODIFY_PY))

def _push(args):
    pass


def _copy_config():
    fname: str = path.join(
        path.dirname(__file__),
        'docs/example_configuration.rst'
    )
    with open(fname, 'r') as f:
        readme = f.read()
        config = readme.split('.. example')[1][9:]

    config_dir: str = path.expanduser('~')
    if SYSTEM == 'Windows':
        config_dir: str = 'AppData/icaltask/'

    if not path.exists(config_dir):
        makedirs(config_dir)
    with open(fname, 'w') as c:
        c.write(config)
    chmod(config_dir, 0o755)


def _install():
    symlink(HOOKS_PY, ON_ADD_PY)
    symlink(HOOKS_PY, ON_MODIFY_PY)
    subprocess.run('task config uda.uid.type string', shell=True, check=True)
    subprocess.run('task config uda.uid.label "iCal UID"', shell=True, check=True)
    subprocess.run('task config uda.geo.type string', shell=True, check=True)
    subprocess.run('task config uda.geo.label "iCal GEO"', shell=True, check=True)

    print('{FILE} hook has been successfully symlinked to system'.format(FILE=ON_ADD_PY))
    print('{FILE} hook has been successfully symlinked to system'.format(FILE=ON_MODIFY_PY))
    print('Added uda.uid.label "iCal UID" configuration to taskrc')
    print('Added uda.uid.type string configuration to taskrc')
    print('Added uda.geo.label "iCal GEO" configuration to taskrc')
    print('Added uda.geo.type string configuration to taskrc')


def main():
    cmd = argparse.ArgumentParser(prog='icaltask', description='Synchronize taskwarrior tasks with an iCalendar server')
    subcmds = cmd.add_subparsers(dest='icaltask')

    install = subcmds.add_parser('install', help='Install taskwarrior hooks and configs for icaltask')
    uninstall = subcmds.add_parser('uninstall', help='Uninstall taskwarrior hooks and configs for icaltask')

    push = subcmds.add_parser('push', help='Execute a one-way sync to push non-iCal tasks to iCalendar server')

    copy_config = subcmds.add_parser('copy-config', help='Copy sample configuration. A prompt will appear to provide options to store configuration')
    args = cmd.parse_args()

    if args.icaltask == 'install':
        install()
    elif args.icaltask == 'uninstall':
        uninstall()
    elif args.icaltask == 'push':
        push(args)
    elif args.icaltask == 'copy-config':
        copy_config(args)
    else:
        cmd.print_help()


if __name__ == "__main__":
    main()
