
from bs4 import BeautifulSoup
import requests
import logging
# Local file imports
from errors import *
from dataobjects import *
from logextension import *

""" logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler(
    'crawlertxtobj.log', mode='w', encoding='windows-1252')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler) """

logger = UserdefinedLogging(__name__, 'crawlertxtobj.log', True)


class webSiteTxt:
    webxTxtObj = None
    url = None
    SiteContent = None
    ArticleList = []

    def __init__(self, url):
        self.url = url
        self.SiteContent = self.getSiteHtml(url)

    def getArticleExtract(self, includeExtractBool, htmlurl):
        soup = None
        if includeExtractBool:
            soup = self.getSiteHtml(htmlurl)
            ParagraphNumber = 1
            for ArticleBody in soup.find_all('div', {"itemprop": "articleBody"}):
                returnstring = str(str(ArticleBody.p.contents).replace(
                    '[', '')).replace(']', '')
                return returnstring
                if ParagraphNumber == 1:
                    break

    def getSiteHtml(self, htmlurl):
        '''
        @htmlobjet: Object in which the retrieved html content is loaded
        '''
        htmlobjet = None
        try:
            #print("Retrieving news from {}".format(htmlurl))
            webxTxtObj = requests.get(htmlurl)
            soup = BeautifulSoup(webxTxtObj.content, 'html.parser')

            htmlobjet = soup
            if webxTxtObj.status_code != 200:
                raise ConnectionFailed("Connection failed:\n Status code: {}\n Reason:{}".format(
                    webxTxtObj.status_code, webxTxtObj.reason))

            if webxTxtObj is None:
                raise UndefinedObjectException(
                    "Could not establish connection. Unable to retrieve data from {}".format(htmlurl))
        except ConnectionFailed as err:
            logger.debug("Connection failed: Status code: {}/r Reason:{}".format(
                webxTxtObj.status_code, webxTxtObj.reason))
        except ConnectionFailed as err:
            logger.debug(
                "Could not establish connection. Unable to retrieve data from {}".format(htmlurl))
        except ConnectionRefusedError as err:
            logger.debug("User defined error was raised" + err)
        except FileNotFoundError as err:
            logger.debug("User defined error was raised" + err)
        except SyntaxError as err:
            print("User defined error was raised" + err)
        finally:
            if webxTxtObj.status_code == 200 and htmlobjet != None:
                return htmlobjet

    def buildArtListVisir(self, includeExtractBool):
        soup = self.SiteContent
        counter = 1
        for article in soup.find_all('article', {"class": "article-item article-item--simple"}):
            for subcontent in article.h1:
                try:
                    if (subcontent.get('title') != None and subcontent.get('href') != None):
                        datevalue = str(article.h1.a['href'])
                        datevalue = datevalue[3:14]
                        htmlurl = self.url + article.h1.a['href']
                        completeATag = (str(article.h1.a).replace(
                            'href="', 'target="_blank" href="{}'.format(self.url)))  # .replace('"', '')
                        self.ArticleList.append(ArticleLinks(
                            # url=None, title=None, htmltag=None, datevalue=None
                            htmlurl,
                            article.h1.a['title'],
                            completeATag,
                            datevalue,
                            self.getArticleExtract(
                                includeExtractBool, htmlurl)
                        ))
                        logger.debug('Article {}:{} \n at {}'.format(counter,
                                                                     article.h1.a['title'], article.h1.a['href']))
                        counter = counter + 1
                    elif subcontent.get('title') == None:
                        datevalue = str(article.h1.a['href'])
                        datevalue = datevalue[3:14]
                        htmlurl = self.url + article.h1.a['href']
                        self.ArticleList.append(ArticleLinks(
                            # url=None, title=None, htmltag=None, datevalue=None
                            htmlurl,
                            str(str(article.h1.a.contents).replace(
                                '[', '')).replace(']', ''),
                            str(article.h1.a),
                            datevalue, self.getArticleExtract(
                                includeExtractBool, htmlurl)
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
                except TypeError as err:
                    logger.debug(err)
        sorted_ArticleList = []
        if len(self.ArticleList) >= 0:
            sorted_ArticleList = sorted(
                self.ArticleList, key=lambda ArticleLinks: ArticleLinks.datevalue)

        return sorted_ArticleList
