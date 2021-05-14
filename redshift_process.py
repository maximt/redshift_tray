''' redshift process '''

import subprocess
from redshift_config import RedshiftConfig


class RedshiftNotInstalledException(Exception):
    ''' Redshift Not Installed Exception '''


class RedshiftProcess:
    ''' redshift process manager '''

    config: RedshiftConfig
    bin_name = 'redshift'

    def __init__(self, config: RedshiftConfig):
        self.config = config

    def apply(self) -> None:
        ''' apply new config to redshift '''
        temp = str(self.config.get_property(RedshiftConfig.TEMP_DAY))
        brightness = str(self.config.get_property(RedshiftConfig.BRIGHTNESS))

        args = [self.bin_name, '-x', '-P', '-O',
                temp, '-b', brightness]
        try:
            subprocess.Popen(args, close_fds=True, shell=False)
        except FileNotFoundError as no_redshift:
            raise RedshiftNotInstalledException from no_redshift

    def reset(self) -> None:
        ''' apply reset redshift to default values '''
        args = [self.bin_name, '-x', '-P']
        subprocess.Popen(args, close_fds=True, shell=False)
