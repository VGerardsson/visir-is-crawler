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
        page1 = html.A("Latest articles", href="index.html",
                       className="btn active")
        page2 = html.A("About", href="about.html", className="btn")
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
        # this function is used to toggle the is_open property of each Collapse

    def toggle_collapse(self, n, is_open):
        if n:
            return not is_open
        return is_open

    # this function applies the "open" class to rotate the chevron

    def set_navitem_class(self, is_open):
        if is_open:
            return "open"
        return ""

    def _leftsidebarload(self):
        sidebar = None
        pageheader = None
        submenu_1 = [
            html.Li(
                # use Row and Col components to position the chevrons
                dbc.Row(
                    [
                        dbc.Col("Menu 1"),
                        dbc.Col(
                            html.I(className="fas fa-chevron-right mr-3"), width="auto"
                        ),
                    ],
                    className="my-1",
                ),
                id="submenu-1",
            ),
            # we use the Collapse component to hide and reveal the navigation links
            dbc.Collapse(
                [
                    dbc.NavLink("Page 1.1", href="/page-1/1"),
                    dbc.NavLink("Page 1.2", href="/page-1/2"),
                ],
                id="submenu-1-collapse",

            ),
        ]

        submenu_2 = [
            html.Li(
                dbc.Row(
                    [
                        dbc.Col("Menu 2"),
                        dbc.Col(
                            html.I(className="fas fa-chevron-right mr-3"), width="auto"
                        ),
                    ],
                    className="my-1",
                ),
                id="submenu-2",
            ),
            dbc.Collapse(
                [
                    dbc.NavLink("Page 2.1", href="/page-2/1"),
                    dbc.NavLink("Page 2.2", href="/page-2/2"),
                ],
                id="submenu-2-collapse",
            ),
        ]
        imageheader = self._imageheader()
        headerlinks = self._headerlinks()
        #containerheader = self._containerheader()
        sidebar = html.Div(
            [
                #html.H2("Sidebar", className="display-4"),
                # containerheader,
                imageheader,
                headerlinks,
                html.Hr(),
                html.P(
                    "A sidebar with collapsible navigation links", className="lead"
                ),
                dbc.Nav(submenu_1 + submenu_2, vertical=True)
            ],             className="left_sidebar_style",
            id="leftsidebar",
        )

        content = html.Div(id="page-content", className="left_content_style")
        sidebar = html.Div([dcc.Location(id="url"), sidebar, content])
        return sidebar

    def _rightsidebarload(self):
        sidebar = None

        imagebanner = 'iceland_Banner2.jpg'
        test_base64 = base64.b64encode(
            open(imagebanner, 'rb').read()).decode('ascii')

        # app.layout = html.Div([
        #     html.Img(src='data:image/png;base64,{}'.format(test_base64)),
        # ])
        # imageurl = "<img src=\"iceland_Banner.jpg\" alt=\"Iceland\" class=\"rightbannerimage\">"

        sidebar = html.Div(
            [html.Img(src='data:image/png;base64,{}'.format(test_base64))
             ], className="right_sidebar_style rightbannerimage", id="rightsidebar")
        return sidebar

    def _errorlogging(self, msg):
        logger = UserdefinedLogging(__name__, 'pageload.log', True)
        logger.error(msg)

    def _articlemenubar(self):
        pass
        # return articlemenubar

    def _pagecontentload(self):
        pageload = []
        leftsidebar = None
        leftsidebar = self._leftsidebarload()
        pageload.append(leftsidebar)
        rightsidebar = self._rightsidebarload()
        pageload.append(rightsidebar)
        articlemenubar = dbc.Container(html.Tr([

            html.Td(dcc.DatePickerSingle(
                id='date-picker-single',
                date=date.today(),
                display_format='Do MMM-YY',
                month_format='Do MMM-YY',
                placeholder='Do MMM-YY'
            )),

            html.Td([
                dcc.Checklist(
                    options=[
                        {'label': 'Visir', 'value': 'visir'},
                        {'label': 'Frettabladid', 'value': 'frettabladid'},
                        {'label': 'MBL', 'value': 'mbl'}
                    ],
                    value=['visir', 'frettabladid', 'mbl'],
                    labelStyle={'display': 'inline-block'}
                ),
                dcc.Checklist(
                    options=[
                        {'label': 'Beginner', 'value': 'easy-is'},
                        {'label': 'Intermed', 'value': 'interm-is'},
                        {'label': 'Advanced', 'value': 'advan-is'}
                    ],
                    value=['easy-is', 'interm-is', "advan-is"],
                    labelStyle={'display': 'inline-block'}
                )

            ])

        ])
        )

        for article in json.loads(self.ArticleResultJSON):

            column1 = dbc.Col(
                [
                    html.H4(converthtml.DangerouslySetInnerHTML(
                        article["htmltag"])),
                    html.B(str(str(article["difficultylevel"]) + "-" +
                               article["newspaper"] + ":")),
                    article["ArticleExtract"]
                ], width=3, sm=3, md=3, lg=3, align="center")

            column2 = dbc.Col(
                converthtml.DangerouslySetInnerHTML(
                    article["ImageLink"]), width=3, sm=3, md=3, lg=3, align="end")

            row = dbc.Row([column1, column2],
                          justify="center")
            pageload.append(row)
            pageload.append(html.Br())

            self.pageload = pageload
