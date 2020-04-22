import json.encoder
from logextension import *
from crawlertxtobj import *
from configsettings import *
settingsfile = configSettings("settings.json").configjson
#from configtwo import *

try:
    logger = UserdefinedLogging(__name__, 'main.log', False)
except TypeError as err:
    print(err)
    pass


urldict = dict(settingsfile["url"])

for key, value in urldict.items():
    #url = "https://www.visir.is"

    if key == "Visir":
        url = value
        txtprinter = webSiteTxt(url)
        articleList = []
        IncludeExtractBool = True
        IncludeImageBool = True

        articlesHandler = VisirArticles(key,
                                        IncludeExtractBool, IncludeImageBool, txtprinter)
        articlesResultSet = articlesHandler.ArticleList


print("Ok")
ArticleResultJSON = open(settingsfile["outputfile"], "w+")
#ArticleResultJSON = open("ArticleResult.json" , "w+")

ArticleResultJSON.write('[')
Counter = 1
for article in articlesResultSet:
    logger.debug(article.url)
    articleJson = json.dumps(article.__dict__)
    ArticleResultJSON.write(articleJson+"\r")

    if Counter != len(articlesResultSet):
        ArticleResultJSON.write(",")
    Counter += 1

ArticleResultJSON.write(']')
print("Program end. Exit code 0")

with open(settingsfile["outputfile"], "r") as siteContent:
    for line in siteContent.readlines():
        pass
        # print(line)
