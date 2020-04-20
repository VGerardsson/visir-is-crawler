import os
from logextension import *


class configSettings():
    def __init__(self, settingsfilepath=None):
        _loadconfigfile(settingsfilepath)

    def _loadconfigfile(self, settingsfilepath):
        configsettings = None
        try:
            if not os.path.exists(settingsfilepath):
                raise IOError
            else:
                configSettings = open(settingsfilepath, "r")
        except IOError as err:
            msg = "Error reading file" + settingsfilepath + " "+err
            _errorlogging(msg)
        return configSettings

    def _errorlogging(self, msg):
        logger = UserdefinedLogging(__name__, 'configsettings.log', True)
        logger.error(msg)
