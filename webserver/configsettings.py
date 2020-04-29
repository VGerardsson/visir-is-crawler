#!/usr/bin/env python3
import os
import datetime
import json
from logextension import *


class configSettings():
    configdict = None

    def __init__(self, settingsfilepath=None):
        self._loadconfigfile(settingsfilepath)

    def _loadconfigfile(self, settingsfilepath):
        try:
            if not os.path.exists(settingsfilepath):
                raise IOError
            else:
                with open(settingsfilepath, "r") as f:
                    self.configdict = f.read()
                self.configdict = json.loads(self.configdict)
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
