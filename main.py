import logging
from crawlertxtobj import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('main.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


url = "https://www.visir.is/"
txtprinter = webSiteTxt(url)
txtprinter.buildArtVisir()
