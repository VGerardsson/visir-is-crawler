
from bs4 import BeautifulSoup
import requests
import logging
import datetime
import re
# Local file imports
from errors import *
from dataobjects import *
from logextension import *
from is_eval import istextstats
logger = UserdefinedLogging(__name__, 'crawlertxtobj.log', True)


class webSiteTxt:
    webxTxtObj = None
    url = None
    SiteContent = None
    ArticleList = []

    def __init__(self, url):
        self.url = url
        self.SiteContent = self._getSiteHtml(url)

    def _getSiteHtml(self, htmlurl):
        '''
        @htmlobjet: Object in which the retrieved html content is loaded
        '''
        htmlobjet = None
        webxTxtObj = None
        try:
            # print("Retrieving news from {}".format(htmlurl))
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


class VisirArticles(webSiteTxt):
    def __init__(self, newspaper, includeExtractBool, includeImageBool, SiteContent):
        self.ArticleList = self._buildArtListVisir(newspaper,
                                                   includeExtractBool, includeImageBool, SiteContent)

    def _getArticleExtract(self, includeExtractBool, includeImageBool, htmlurl):

        # Get the article extract
        soup = None
        soup = self._getSiteHtml(htmlurl)
        ExtractString = None
        ImageString = None
        ArticeContentList = []
        ParagraphNumber = 1
        try:
            if includeExtractBool:
                for ArticleBody in soup.find_all('div', {"itemprop": "articleBody"}):
                    for paragraph in ArticleBody.findAll('p'):
                        CleanedUpContent = str(paragraph)
                        CleanedUpContent = re.sub(
                            r'<.+?>', '', CleanedUpContent)
                        ArticeContentList.append(CleanedUpContent)
                        if ParagraphNumber == 1:
                            ExtractString = str(CleanedUpContent.replace(
                                '[', '')).replace(']', '')+"..."
                            ExtractString = ExtractString.replace("'", "")
                            ParagraphNumber += 1
            if includeImageBool:
                for ArticleBody in soup.find_all('figure', {"class": "figure article-single__figure"}):
                    ImageString = str(ArticleBody.img)
                    if ParagraphNumber == 1:
                        break
        except TypeError as err:
            logger.debug(err)
        finally:
            return ExtractString, ImageString, ArticeContentList

    def _buildArtListVisir(self, newspaper, includeExtractBool, includeImageBool, siteContent):
        '''
        @param:includeExtractBool=Include first paragrahp of article true/false
        @param:includeImageBool=Include image from article true/false
        '''
        jobExecutionDate = UserDefinedDates.dateinseconds()
        soup = siteContent.SiteContent
        counter = 1
        for article in soup.find_all('article', {"class": "article-item article-item--simple"}):
            for subcontent in article.h1:
                try:
                    ExtractLink = None
                    ImageLink = None
                    ArticleBody = []
                    difficultylevel = None
                    ArticleBodyHandler = None
                    if (subcontent.get('title') != None and subcontent.get('href') != None):
                        # datevalue = str(article.h1.a['href'])
                        # datevalue = datevalue[3:14]
                        datevalue = str(jobExecutionDate)
                        htmlurl = siteContent.url + article.h1.a['href']
                        completeATag = (str(article.h1.a).replace(
                            'href="', 'target="_blank" href="{}'.format(siteContent.url)))  # .replace('"', '')
                        DataTuple = self._getArticleExtract(
                            includeExtractBool, includeImageBool, htmlurl)
                        if DataTuple[0] != None:
                            ExtractLink = DataTuple[0]
                        if DataTuple[1] != None:
                            ImageLink = DataTuple[1].replace(
                                'img', 'img class="imageheight"')
                        if DataTuple[2]:
                            ArticleBodyHandler = DataTuple[2]
                            try:
                                ArticleBody = ' '.join(
                                    map(str, ArticleBodyHandler))

                                difficultyHandler = istextstats.istextstats()
                                difficultylevel = difficultyHandler.automated_readability_index(
                                    ArticleBody)
                            except IndexError as err:
                                difficultylevel = 0

                        siteContent.ArticleList.append(ArticleLinks(
                            # url=None, title=None, htmltag=None, datevalue=None
                            #  ArticleExtract = None, ImageLink = None,  newspaper = None
                            # difficultylevel = None, articleBody = []
                            htmlurl,
                            article.h1.a['title'],
                            completeATag,
                            datevalue,
                            ExtractLink,
                            ImageLink,
                            newspaper,
                            difficultylevel
                            # ArticleBodyHandler
                        ))
                        # logger.debug('Article {}:{} \n at {}'.format(counter,
                        #                                             article.h1.a['title'], article.h1.a['href']))
                        counter = counter + 1
                    elif subcontent.get('title') == None:
                        datevalue = str(article.h1.a['href'])
                        datevalue = datevalue[3:14]
                        htmlurl = self.url + article.h1.a['href']

                        DataTuple = self._getArticleExtract(
                            includeExtractBool, includeImageBool, htmlurl)
                        if DataTuple[0] != None:
                            ExtractLink = DataTuple[0]
                        if DataTuple[1] != None:
                            ImageLink = DataTuple[1].replace(
                                'img', 'img height=auto width=auto')

                        if DataTuple[2]:
                            ArticleBodyHandler = DataTuple[2]
                            ArticleBodyHandler = DataTuple[2]
                            try:
                                ArticleBody = ' '.join(
                                    map(str, ArticleBodyHandler))
                                difficultyHandler = istextstats.istextstats()
                                difficultylevel = difficultyHandler.automated_readability_index(
                                    ArticleBody)
                            except IndexError as err:
                                difficultylevel = 0
                        self.ArticleList.append(ArticleLinks(
                            # url=None, title=None, htmltag=None, datevalue=None
                            #  ArticleExtract = None, ImageLink = None,  newspaper = None
                            # difficultylevel = None, articleBody = []
                            htmlurl,
                            str(str(article.h1.a.contents).replace(
                                '[', '')).replace(']', ''),
                            str(article.h1.a),
                            datevalue,
                            ExtractLink,
                            ImageLink,
                            newspaper,
                            difficultylevel
                            # ArticleBodyHandler
                        ))
                    #    logger.debug('Article {}:{} \n at {}'.format(counter,
                     #                                                str(str(article.h1.a.contents).replace('[', '')).replace(']', ''), article.h1.a['href']))
                    else:
                        logger.debug(
                            "Could not read all tags for {}".format(str(article.h1.a)))
                except KeyError as err:
                    logger.debug("KeyError occurred while reading {}".format(str(article.h1.a))
                                 )
                except TypeError as err:
                    logger.debug(err)
        sorted_ArticleList = []
        if len(self.ArticleList) >= 0:
            sorted_ArticleList = sorted(
                self.ArticleList, key=lambda ArticleLinks: [ArticleLinks.difficultylevel, ArticleLinks.datevalue])

        return sorted_ArticleList


class mblarticles(webSiteTxt):
    def __init__(self, newspaper, includeExtractBool, includeImageBool, SiteContent):
        self.ArticleList = self._buildArtListMbl(newspaper,
                                                 includeExtractBool, includeImageBool, SiteContent)

    def _getArticleExtract(self, includeExtractBool, htmlurl):

        # Get the article extract
        soup = None
        soup = self._getSiteHtml(htmlurl)
        ExtractString = None
        ArticeContentList = []
        ParagraphNumber = 1
        try:
            if includeExtractBool:
                for ArticleBody in soup.find_all('div', {"class": "main-layout"}):
                    for paragraph in ArticleBody.findAll('p'):
                        CleanedUpContent = str(paragraph)
                        CleanedUpContent = re.sub(
                            r'<.+?>', '', CleanedUpContent)
                        ArticeContentList.append(CleanedUpContent)
                        if ParagraphNumber == 1:
                            ExtractString = str(CleanedUpContent.replace(
                                '[', '')).replace(']', '')
                            ExtractString = ExtractString.replace("'", "")
                            ParagraphNumber += 1

        except TypeError as err:
            logger.debug(err)
        finally:
            return ExtractString, ArticeContentList

    def _buildArtListMbl(self, newspaper, includeExtractBool, includeImageBool, siteContent):
        '''
        @param:includeExtractBool=Include first paragrahp of article true/false
        @param:includeImageBool=Include image from article true/false
        '''
        jobExecutionDate = UserDefinedDates.dateinseconds()
        soup = siteContent.SiteContent
        counter = 1
        for article in soup.find_all('div', {"class": "media smt mb-2"}):

            try:
                ArticleBodyHandler = None
                ExtractLink = None
                ImageLink = None
                ArticleBody = []
                difficultylevel = None
                ArticleTitle = None
                if (article.find("h4") != None and article.find("noscript") != None and
                        article.find('a') != None):
                    ArticleTitle = article.find("h4").contents[0]
                    datevalue = str(jobExecutionDate)
                    ImageLink = str(article.find("noscript").contents[1]).replace(
                        '<img', '<img class="imageheight"')
                    atag = article.find('a').attrs['href']
                    htmlurl = siteContent.url + atag
                    completeATag = '<a target="_blank" href="' + \
                        htmlurl + '">' + ArticleTitle + '</a>'

                    DataTuple = self._getArticleExtract(
                        includeExtractBool, htmlurl)
                    if DataTuple[0] != None:
                        ExtractLink = DataTuple[0]
                    if DataTuple[1]:
                        ArticleBodyHandler = DataTuple[1]
                    try:
                        ArticleBody = ' '.join(
                            map(str, ArticleBodyHandler))
                        difficultyHandler = istextstats.istextstats()
                        difficultylevel = difficultyHandler.automated_readability_index(
                            ArticleBody)
                    except IndexError as err:
                        difficultylevel = 0

                    siteContent.ArticleList.append(ArticleLinks(
                        # url=None, title=None, htmltag=None, datevalue=None
                        #  ArticleExtract = None, ImageLink = None,  newspaper = None
                        # difficultylevel = None, articleBody = []
                        htmlurl,
                        ArticleTitle,
                        completeATag,
                        datevalue,
                        ExtractLink,
                        ImageLink,
                        newspaper,
                        difficultylevel
                        # ArticleBodyHandler
                    ))
                    counter = counter + 1

                else:
                    logger.debug(
                        "Could not read all tags for {}".format(ArticleTitle))
            except KeyError as err:
                logger.debug("KeyError occurred while reading {}".format(str(article.h1.a))
                             )
            except TypeError as err:
                logger.debug(err)
        sorted_ArticleList = []
        if len(self.ArticleList) >= 0:
            sorted_ArticleList = sorted(
                self.ArticleList, key=lambda ArticleLinks: [ArticleLinks.difficultylevel, ArticleLinks.datevalue])

        return sorted_ArticleList
