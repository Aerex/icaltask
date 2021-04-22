# -*- coding: utf-8 -*-
from requests.auth import HTTPDigestAuth, HTTPBasicAuth
from requests_toolbelt import GuessAuth
from six.moves import configparser
import subprocess
import logging
from os import environ, path, makedirs
from sys import platform
from icaltask.utils import get_system, is_uri

logger = logging.getLogger(__name__)

def _validate(cp):
    """ Validate configuration file against the following criteria:
        - There must a valid url for the default calendar
        - Each calendar must have a valid url defined
        - If log level is provided the level must be valid and file must be provided.
        - If log file is provided but log level is optional. Log level will default to DEBUG
    """
    if cp.has_option(section='general', option='default_calendar'):
        general_cal_url = cp.get(section='general', option='default_calendar')
        if not is_uri(general_cal_url):
            raise configparser.ParsingError(F'{general_cal_url} is not a valid url')
    else:
        raise configparser.NoOptionError('Missing default_calendar')
    for section in cp.sections():
        for auth_field in ['username', 'password']:
            has_cal_auth = cp.has_option(section=section, option=auth_field) \
                or cp.has_option(section=section, option=F'{auth_field}.eval')
            has_global_auth = cp.has_option(section='general', option=auth_field) \
                or cp.has_option(section='general', option=F'{auth_field}.eval')
            if has_global_auth is None and has_cal_auth is None:
                raise configparser.NoOptionError(F'Cannot find a {auth_field} to authenticate {section} calendar')
            if cp.has_option(section=section, option='url'):
                cal_url = cp.get(section=section, option='url')
                if not is_uri(cal_url):
                    raise configparser.ParsingError(F'{cal_url} is not a valid url')
            else:
                raise configparser.NoOptionError(F'Missing calendar url for {section}')

def get_log_level(level):
    return getattr(logging, level)

# TODO: fix this to work with windows as well
def load_sample_config(configparser):
    xdg_config_file_path: str = path.join(environ.get('XDG_CONFIG_HOME'), 'icaltask', 'icaltaskrc')
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
    """ Load the config file.
        On Windows the config file will be retrieved in AppData/icaltask, otherwise $XDG_CONFIG_HOME/icaltask
        If config does not exist or is not valid the sample configuration file will be used
    """
    if get_system(platform) == 'Windows':
        config_file_path = path.join('AppData', 'icaltask', 'icaltaskrc')
    else:
        config_file_path = path.join(path.expanduser('~/.config'), 'icaltask', 'icaltaskrc')

    cp = CalConfig(default_section="general")
    try:
        cp.read_file(open(config_file_path, encoding='utf8'))
        _validate(cp)
    except Exception as e:
        print(e)
        print('Failed to load configuration file. Using default config')
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
            cred_eval = F'{cred}.eval'
            if self.has_option(section='general', option=cred_eval):
                creds.append(self.eval(self.get(section='general', option=cred_eval).strip()))
            elif self.has_option(section='general', option=cred):
                creds.append(self.get(section='general', option=cred))
            else:
                raise ValueError(F'{cred} or {cred_eval} is missing')

        method = self.get('general', option='auth_type', fallback='')
        if method == 'digest':
            return HTTPDigestAuth(creds[0], creds[1])
        if method == 'basic':
            return HTTPBasicAuth(creds[0], creds[1])
        return GuessAuth(creds[0], creds[1])

    def eval(self, command):
        process = subprocess.run(command, shell=True, capture_output=True, check=True)
        return process.stdout.strip().decode('utf-8')

