import json.encoder
from logextension import *
from crawlertxtobj import *
from configsettings import *
from dataobjects import ArticleLinks
settingsfile = configSettings("settings.json").configjson
# from configtwo import *

try:
    logger = UserdefinedLogging(__name__, 'main.log', False)
except TypeError as err:
    print(err)
    pass


urldict = dict(settingsfile["url"])
mblArticlesResultSet = []
visirArticlesResultSet = []
for key, value in urldict.items():
    # if key == "MBL":
    #     url = value
    #     txtprinter = webSiteTxt(url)
    #     articleList = []
    #     IncludeExtractBool = True
    #     IncludeImageBool = False
    #     articlesHandler = mblarticles(key,
    #                                   IncludeExtractBool, IncludeImageBool, txtprinter)
    #     mblArticlesResultSet = articlesHandler.ArticleList

    if key == "Visir":
        url = value
        txtprinter = webSiteTxt(url)
        articleList = []
        IncludeExtractBool = True
        IncludeImageBool = True
        articlesHandler = VisirArticles(key,
                                        IncludeExtractBool, IncludeImageBool, txtprinter)
        visirArticlesResultSet = articlesHandler.ArticleList

articlesResultSet = visirArticlesResultSet+mblArticlesResultSet
sorted_ArticleList = sorted(
    articlesResultSet, key=lambda ArticleLinks: [ArticleLinks.difficultylevel, ArticleLinks.datevalue])

print("Ok")
ArticleResultJSON = open(settingsfile["outputfile"], "w+")
# ArticleResultJSON = open("ArticleResult.json" , "w+")

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
