
from bs4 import BeautifulSoup
import requests
import logging
# Local file imports
from errors import *
from dataobjects import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler(
    'crawlertxtobj.log', mode='w', encoding='windows-1252')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class webSiteTxt:
    webxTxtObj = None
    url = None
    SiteContent = None
    ArticleList = []

    def __init__(self, url):
        self.url = url
        self.getSiteText()

    def getSiteText(self):

        try:
            print("Retrieving news from {}".format(self.url))
            webxTxtObj = requests.get(self.url)
            soup = BeautifulSoup(webxTxtObj.content, 'html.parser')
            # html5lib,html.parser
            logger.debug("Printing web data to file")

            print(soup)
            self.SiteContent = soup
            if webxTxtObj.status_code != 200:
                raise ConnectionFailed("Connection failed:\n Status code: {}\n Reason:{}".format(
                    webxTxtObj.status_code, webxTxtObj.reason))
               # print("Connection failed: Status code: {}/r Reason:{}".format(
                #   webxTxtObj.status_code, webxTxtObj.reason))

            if webxTxtObj is None:
                raise UndefinedObjectException(
                    "Could not establish connection. Unable to retrieve data from {}".format(self.url))
        except ConnectionFailed as err:
            logger.debug("Connection failed: Status code: {}/r Reason:{}".format(
                webxTxtObj.status_code, webxTxtObj.reason))
        except ConnectionFailed as err:
            logger.debug(
                "Could not establish connection. Unable to retrieve data from {}".format(self.url))
        except ConnectionRefusedError as err:
            logger.debug("User defined error was raised" + err)
        except FileNotFoundError as err:
            logger.debug("User defined error was raised" + err)
        except SyntaxError as err:
            print("User defined error was raised" + err)

    def buildArtVisir(self):
        soup = self.SiteContent
        counter = 1
        for article in soup.find_all('article', {"class": "article-item article-item--simple"}):
            for subcontent in article.h1:
                try:
                    if (subcontent.get('title') != None and subcontent.get('href') != None):
                        datevalue = str(article.h1.a['href'])
                        datevalue = datevalue[3:14]
                        self.ArticleList.append(ArticleLinks(
                            # url=None, title=None, htmltag=None, datevalue=None
                            self.url + article.h1.a['href'],
                            article.h1.a['title'],
                            str(article.h1.a),
                            datevalue
                        ))
                        logger.debug('Article {}:{} \n at {}'.format(counter,
                                                                     article.h1.a['title'], article.h1.a['href']))
                        counter = counter + 1
                    elif subcontent.get('title') == None:
                        datevalue = str(article.h1.a['href'])
                        datevalue = datevalue[3:14]
                        self.ArticleList.append(ArticleLinks(
                            # url=None, title=None, htmltag=None, datevalue=None
                            self.url + article.h1.a['href'],
                            str(str(article.h1.a.contents).replace(
                                '[', '')).replace(']', ''),
                            str(article.h1.a),
                            datevalue
                        ))
                        logger.debug('Article {}:{} \n at {}'.format(counter,
                                                                     str(str(article.h1.a.contents).replace('[', '')).replace(']', ''), article.h1.a['href']))
                    else:
                        logger.debug(
                            "Could not read all tags for {}".format(str(article.h1.a)))
                except KeyError as err:
                    print(err)
                    logger.debug("KeyError occurred while reading {}".format(str(article.h1.a))
                                 )

        if len(self.ArticleList) >= 0:
            sorted_ArticleList = sorted(
                self.ArticleList, key=lambda ArticleLinks: ArticleLinks.datevalue)
            print(sorted_ArticleList)
            print("asdlfkjah")
            return sorted_ArticleList
