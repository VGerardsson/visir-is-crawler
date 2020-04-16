import json.encoder
from logextension import *
from crawlertxtobj import *


try:
    logger = UserdefinedLogging(__name__, 'main.log', False)
except TypeError as err:
    print(err)
    pass


url = "https://www.visir.is"
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
