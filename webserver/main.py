#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import dash
import flask
import dash_core_components as dcc
import dash_html_components as html
from pageload import *
from dash.dependencies import Input, Output, State


server = flask.Flask(__name__)
if server.config["ENV"] == "production":
    server.config.from_object("config.ProductionConfig")
else:
    server.config.from_object("config.DevelopmentConfig")

external_scripts = [
    'https://cdn.jsdelivr.net/npm/cookie-bar/cookiebar-latest.min.js?tracking=1&thirdparty=1&always=1&noGeoIp=1&refreshPage=1']

FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"
app = dash.Dash(__name__,
                server=server,
                routes_pathname_prefix='/frettir/', external_scripts=external_scripts,
                external_stylesheets=[dbc.themes.BOOTSTRAP, FA], )

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
            <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta
    name="News from Iceland"
    content="Daily news articles in Icelandic. Sorted by difficulty to help language students and teachers select articles that are at their level."
    />
    <meta name="robots" content="index, frettir" />
    <meta name="google" content="notranslate" />
    <meta http-equiv="Content-Type" content="UTF-8; charset=UTF-8" />
    <meta charset="UTF-8" />
        <title>Iceland Fréttir</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

pagecontent = []
pageloaderhandler = pageload()
pagecontent = pageloaderhandler.pageload
visirarticles = []
mblarticles = []
articlesdeleted = []
for page in pagecontent:
    if hasattr(page, "className"):
        if page.className == 'visirart':
            visirarticles.append(page)
            articlesdeleted.append(pagecontent.index(page))
        elif page.className == 'mblart':
            mblarticles.append(page)


tabshandler = html.Div([
    dcc.Tabs(id='tabsnewspaper', value='visir', children=[
        dcc.Tab(label='VISIR', value='visir'),
        dcc.Tab(label='MBL', value='mbl'),
    ]),
    html.Div(id='tabs-content')

], className="tabslayout")

facebookscript = html.Script(src="https://connect.facebook.net/nl_NL/sdk.js#xfbml=1&version=v6.0",
                             crossOrigin="anonymous", defer=True)
finalpage = []
finalpage.append(html.Title("Iceland Fréttir"))
finalpage.append(facebookscript)
finalpage.append(pagecontent[0])
finalpage.append(pagecontent[1])
finalpage.append(tabshandler)


@app.callback(Output('tabs-content', 'children'),
              [Input('tabsnewspaper', 'value')])
def render_content(tab):
    if tab == 'visir':
        return visirarticles
    elif tab == 'mbl':
        return mblarticles


app.layout = html.Div(finalpage)


if __name__ == "__main__":
    app.run_server(debug=False)
