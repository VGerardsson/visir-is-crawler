import logging
import datetime


class UserdefinedLogging():
    '''
    This class extends the logging base class. Only a single line call is necessary to initialize the logger in the file being executed. The logging messages in your code can be de/activated by setting the value for logging_active
    @param self
    @param FiletoLog: Name of the file that will be logged
    @param logfilename: Name of the logfile that you want to use
    @param logging_active: True=logging activated, False=logging deactivated

    Use in python file: 
    logger = UserdefinedLogging(__name__, 'example.log', True)
    logger.debug("hello world")
     '''
    logging_active = None
    logger = None

    def __init__(self, FiletoLog, logfilename, logging_active=None):
        try:
            if logging_active == True:
                self.logging_active = True
            else:
                self.logging_active = False

            if not (self.logging_active == None or self.logging_active == False):
                logger = logging.getLogger(FiletoLog)
                logger.setLevel(logging.DEBUG)
                formatter = logging.Formatter(
                    '%(levelname)s:%(name)s:%(message)s')
                file_handler = logging.FileHandler(logfilename, "w")
                file_handler.setFormatter(formatter)
                file_handler
                logger.addHandler(file_handler)
                self.logger = logger
        except TypeError as err:
            print(err)

    def debug(self, msg):
        '''
        @msg: The debug message that will be written to the log
        '''
        if self.logging_active == True:
            self.logger.debug(msg)

    def error(self, msg):
        '''
        @msg: The error message that will be written to the log
        '''
        if self.logging_active == True:
            self.logger.error(msg)


class UserDefinedDates:
    @staticmethod
    def dateinseconds():
        currentimemili = datetime.datetime.now()
        currenttimesecs = currentimemili - \
            datetime.timedelta(microseconds=currentimemili.microsecond)
        return currenttimesecs
