#!/usr/bin/env python3
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import json
from logextension import *
from datetime import date
import os
import datetime
import base64
import configsettings as cset
import dash_dangerously_set_inner_html as converthtml


class pageload():
    ArticleResultJSON = None
    pageload = None

    def __init__(self):
        # Retrieve the table data
        settingsfile = cset.configSettings(("settings.json")).configdict
        try:
            if not os.path.exists(settingsfile["inputfile"]):
                raise IOError
            else:
                with open(settingsfile["inputfile"], "r") as f:
                    self.ArticleResultJSON = f.read()
        except IOError as err:
            currentimemili = datetime.datetime.now()
            currenttimesecs = currentimemili - \
                datetime.timedelta(microseconds=currentimemili.microsecond)
            msg = str(currentimemili) + "Error reading file " + \
                settingsfile["inputfile"] + " "+str(err)
            self._errorlogging(msg)
        self._pagecontentload()

    def _headerlinks(self):
        # metatags = html.Div(
        #     [converthtml.DangerouslySetInnerHTML(
        #         '<meta name="viewport" content="width=device-width, initial-scale=1" />'
        #     ),
        #         converthtml.DangerouslySetInnerHTML(
        #         '<meta name="News from Iceland" content="Daily news articles in Icelandic. Sorted by difficulty to help language students and teachers select articles that are at their level."/>'
        #     ),

        #         converthtml.DangerouslySetInnerHTML(
        #         '< meta name="robots"content="index, follow"/>'),
        #         converthtml.DangerouslySetInnerHTML(
        #         '< meta name="google"content="notranslate"/>'),
        #         converthtml.DangerouslySetInnerHTML(
        #         '< meta http - equiv="Content-Type"content="UTF-8; charset=UTF-8"/>'),
        #         converthtml.DangerouslySetInnerHTML('< metacharset="UTF-8"/>'),
        #         converthtml.DangerouslySetInnerHTML(
        #         '< meta name="viewport" content="width=device-width, initial-scale=1"/>')]
        # )

        siteheader = None
        page1 = html.A("HOME",
                       href="http://newsfromiceland.epizy.com/index.html", className="btn")
        page2 = html.A("FRÉTTIR", href="frettir.html",
                       className="btn active")
        subheader = html.Div([html.P(), page1, html.P(), page2])
        return subheader

    def _containerheader(self):
        firstdiv = html.Div(
            "News from Iceland", className="centered centertextheader")
        containercontent = html.A(firstdiv, href="index.html")
        headercontainer = None
        headercontainer = html.Div(containercontent, className='container')
        return containercontent

    def _imageheader(self):
        headerimg = 'flag-800.png'
        image_base64 = base64.b64encode(
            open(headerimg, 'rb').read()).decode('ascii')
        headerimg = html.Img(
            src='data:image/png;base64,{}'.format(image_base64), alt='Iceland flag', className="imageheader")
        return headerimg

    def _leftsidebarload(self):
        sidebar = None
        pageheader = None

        imageheader = self._imageheader()
        headerlinks = self._headerlinks()
        facebookdiv = converthtml.DangerouslySetInnerHTML(
            '<div class="fb-like header-right" data-href="https://www.facebook.com/Iceland-Frettir-104498271250181" data-width="100" data-layout="standard" data-action="like" data-size="large" data-share="true"></div>')
        sidebar = html.Div(
            [
                imageheader,
                facebookdiv,
                headerlinks,
                html.Hr()
            ],             className="left_sidebar_style",
            id="leftsidebar",
        )

        content = html.Div(id="page-content", className="left_content_style")
        sidebar = html.Div(
            [dcc.Location(id="url"), sidebar, content])
        return sidebar

    def _rightsidebarload(self):
        sidebar = None

        imagebanner = 'rightbanner.jpg'
        test_base64 = base64.b64encode(
            open(imagebanner, 'rb').read()).decode('ascii')

        sidebar = html.Div(
            [html.Img(src='data:image/png;base64,{}'.format(test_base64))
             ], className="right_sidebar_style rightbannerimage", id="rightsidebar")

        return sidebar

    def _errorlogging(self, msg):
        logger = UserdefinedLogging(__name__, 'pageload.log', True)
        logger.error(msg)

    def _articlelistload(self):
        articlelist = []
        for article in json.loads(self.ArticleResultJSON):

            column1 = dbc.Col(
                [
                    html.H5(converthtml.DangerouslySetInnerHTML(
                        article["htmltag"])),
                    html.B(str(str(article["difficultylevel"]) + "-" +
                               article["newspaper"] + ":")),
                    html.Div(article["ArticleExtract"],
                             className="tabscontent articletext")
                ],  width=3, sm=3, md=3, lg=3, align="center")

            column2 = dbc.Col(
                converthtml.DangerouslySetInnerHTML(
                    article["ImageLink"]), width=3, sm=3, md=3, lg=3, align="end")
            row = None
            if article["newspaper"] == 'Visir':
                row = dbc.Row([column1, column2],
                              className="visirart", justify="center")
            if article["newspaper"] == 'MBL':
                row = dbc.Row([column1, column2],
                              className="mblart", justify="center")

            articlelist.append(row)

        return articlelist

    def _pagecontentload(self):
        pageload = []
        leftsidebar = None
        leftsidebar = self._leftsidebarload()
        pageload.append(leftsidebar)
        rightsidebar = self._rightsidebarload()
        pageload.append(rightsidebar)
        articletable = []
        articletable = self._articlelistload()
        pageload = pageload+articletable
        self.pageload = pageload
