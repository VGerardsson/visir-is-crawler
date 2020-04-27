import os
import datetime
import json
from logextension import *


class configSettings():
    configjson = None

    def __init__(self, settingsfilepath=None):
        self._loadconfigfile(settingsfilepath)

    def _loadconfigfile(self, settingsfilepath):
        try:
            if not os.path.exists(settingsfilepath):
                raise IOError
            else:
                with open(settingsfilepath, "r") as f:
                    self.configjson = f.read()
                self.configjson = json.loads(self.configjson)
        except IOError as err:
            currentimemili = datetime.datetime.now()
            currenttimesecs = currentimemili - \
                datetime.timedelta(microseconds=currentimemili.microsecond)
            msg = str(currentimemili) + "Error reading file " + \
                settingsfilepath + " "+str(err)
            self._errorlogging(msg)

    def _errorlogging(self, msg):
        logger = UserdefinedLogging(__name__, 'configsettings.log', True)
        logger.error(msg)
