import json.encoder
from logextension import *
from crawlertxtobj import *
from configsettings import *
#from configtwo import *

try:
    logger = UserdefinedLogging(__name__, 'main.log', False)
except TypeError as err:
    print(err)
    pass

settingsfile = configSettings("settings.json").configjson
urldict = dict(settingsfile["url"])
#url = "https://www.visir.is"
url = urldict["Visir"]
txtprinter = webSiteTxt(url)
articleList = []
IncludeExtractBool = True
IncludeImageBool = True
articleList = txtprinter.buildArtListVisir(
    IncludeExtractBool, IncludeImageBool)

ArticleResultJSON = open("ArticleResult.json", "w+")
ArticleResultJSON.write('[')
Counter = 1
for article in articleList:
    logger.debug(article.url)
    articleJson = json.dumps(article.__dict__)
    ArticleResultJSON.write(articleJson+"\r")

    if Counter != len(articleList):
        ArticleResultJSON.write(",")
    Counter += 1

ArticleResultJSON.write(']')
print("Program end. Exit code 0")
