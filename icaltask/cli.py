#!/usr/bin/env python3

from os import symlink, path, unlink
from pathlib import Path
import argparse

PROJ_DIR = Path(__file__).resolve().parent.parent
HOOKS_PY = '{PROJ_DIR}/hook.py'.format(PROJ_DIR=PROJ_DIR)
TASK_HOOK_DIR = path.expanduser('~/.task/hooks')
ON_LAUNCH_PY = '{TASKS_HOOKS_DIR}/on-launch.icaltask.py'.format(TASKS_HOOKS_DIR=TASK_HOOK_DIR)
ON_MODIFY_PY = '{TASKS_HOOKS_DIR}/on-modify.icaltask.py'.format(TASKS_HOOKS_DIR=TASK_HOOK_DIR)


def _uninstall_hooks():
    unlink(ON_LAUNCH_PY)
    unlink(ON_MODIFY_PY)
    print('{FILE} hook has been successfully unlinked from system'.format(FILE=ON_LAUNCH_PY))
    print('{FILE} hook has been successfully unlinked from system'.format(FILE=ON_MODIFY_PY))

def _push(args):
    pass

def _copy_config(args):
    pass

def _install_hooks():
    symlink(HOOKS_PY, ON_LAUNCH_PY)
    symlink(HOOKS_PY, ON_MODIFY_PY)

    print('{FILE} hook has been successfully symlinked to system'.format(FILE=ON_LAUNCH_PY))
    print('{FILE} hook has been successfully symlinked to system'.format(FILE=ON_MODIFY_PY))


def main():
    cmd = argparse.ArgumentParser(prog='icaltask', description='Synchronize taskwarrior tasks with an iCalendar server')
    subcmds = cmd.add_subparsers(dest='icaltask')

    hooks = subcmds.add_parser('install-hooks', help='Install taskwarrior hooks')
    hooks = subcmds.add_parser('uninstall-hooks', help='Uninstall taskwarrior hooks')

    push = subcmds.add_parser('push', help='Execute a one-way sync to push non-iCal tasks to iCalendar server')

    copy_config = subcmds.add_parser('copy-config', help='Copy sample configuration. A prompt will appear to provide options to store configuration')
    args = cmd.parse_args()

    if args.icaltask == 'install-hooks':
        _install_hooks()
    elif args.icaltask == 'uninstall-hooks':
        _uninstall_hooks()
    elif args.icaltask == 'push':
        _push(args)
    elif args.icaltask == 'copy-config':
        _copy_config(args)
    else:
        cmd.print_help()




if __name__ == "__main__":
    main()

