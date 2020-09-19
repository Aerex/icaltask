# -*- coding: utf-8 -*-
from requests.auth import HTTPDigestAuth, HTTPBasicAuth
from requests_toolbelt import GuessAuth
from six.moves import configparser
import subprocess
import logging
from os import environ, path, makedirs

logger = logging.getLogger(__name__)

def validate(cp):
    pass
def get_log_level(level):
    return getattr(logging, level)

def load_sample_config(configparser):
    xdg_config_file_path = path.join(environ.get('XDG_CONFIG_HOME'), 'icaltask', 'icaltaskrc')
    makedirs(xdg_config_file_path)
    sample_config_file_path = path.join(
        path.dirname(__file__),
        'icaltaskrc'
    )
    with open(sample_config_file_path, 'r') as sc, \
            open(xdg_config_file_path, 'w') as cf:
        cf.write(sc.read())
        sample_config = configparser.read_file(sc)
        return sample_config

def load_config():
    """ Get config file on the following priority
    - The envionrment variable ICAL_TASK_RC is defined
            - $XDG_CONFIG_HOME/icaltask/icaltaskrc exists
            - ~/.icaltaskrc exists
        If neither can be found. A sample configuration will be generated under $XDG_CONFIG_HOME/icaltask/icaltaskrc
    """
    # TODO: Add defaults using sample or something else
    cp = CalConfig(default_section="general")
    xdg_config_home = (environ.get('XDG_CONFIG_HOME') or path.expanduser('~/.config'))
    config_file_paths = [
        (environ.get('ICAL_TASK_RC') or ''),
        path.join(xdg_config_home, 'icaltask', 'icaltaskrc'),
        path.expanduser('~/.icaltaskrc')
    ]

    # TODO: Validate config
    #validate(cp)

    if len(cp.read(config_file_paths, encoding='utf8')) == 0:
        load_sample_config(cp)

    logging.basicConfig(
        level=get_log_level(cp.get('general', 'log.level')),
        filename=path.expanduser(cp.get('general', 'log.file'))
    )

    return cp

class CalConfig(configparser.ConfigParser, object):
    # TODO: Handle not requiring section or option keyword
    # TODO: Use general as default section if section is not provided

    def getboolean(self, section='general', option=''):
        return super(CalConfig, self).getboolean(section, option)

    @property
    def auth(self):
        creds = []
        for cred in ['username', 'password']:
            cred_eval = '{}.eval'.format(cred)
            if self.has_option(section='general', option=cred_eval):
                creds.append(self.eval(self.get(section='general', option=cred_eval).strip()))
            elif self.has_option(section='general', option=cred):
                creds.append(self.get(section='general', option=cred))
            else:
                raise ValueError('{cred} or {cred_eval} is missing'
                        .format(cred=cred, cred_eval=cred_eval))

        method = self.get('general', option='auth_type', fallback='')
        if method == 'digest':
            return HTTPDigestAuth(creds[0], creds[1])
        if method == 'basic':
            return HTTPBasicAuth(creds[0], creds[1])
        return GuessAuth(creds[0], creds[1])

    def eval(self, command):
        process = subprocess.run(command, shell=True, capture_output=True, check=True)
        return process.stdout.strip().decode('utf-8')

