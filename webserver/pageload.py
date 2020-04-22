
import dash_html_components as html
import dash_core_components as dcc
import json
from logextension import *
from datetime import date
import os
import datetime
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

    def _errorlogging(self, msg):
        logger = UserdefinedLogging(__name__, 'pageload.log', True)
        logger.error(msg)

    def _pagecontentload(self):
        pageload = []
        pageload.append(

            html.Table(html.Tr([

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





            ]), className="center"
            )
        )

        for article in json.loads(self.ArticleResultJSON):
            pageload.append(
                html.Div([
                    html.Table(
                        html.Tr([

                            html.Td(
                                [
                                    html.H2(converthtml.DangerouslySetInnerHTML(
                                            article["htmltag"])),
                                    html.B(str(article["newspaper"] + "-")),
                                    article["ArticleExtract"]
                                ], className="column"
                            ),

                            html.Td(
                                converthtml.DangerouslySetInnerHTML(
                                    article["ImageLink"])
                            )
                        ]), className="center")
                ]
                ))

        self.pageload = pageload
