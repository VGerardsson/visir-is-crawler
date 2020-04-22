# -*- coding: utf-8 -*-
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from pageload import *


print("Ok")


#settingsfile = cset.configSettings(("settings.json")).configdict
#external_stylesheets = 'http://newsfromiceland.epizy.com/style.css'

app = dash.Dash(__name__)
pagecontent = []
pageloaderhandler = pageload()
pagecontent = pageloaderhandler.pageload


app.layout = html.Div(children=pagecontent)
if __name__ == "__main__":
    app.run_server(debug=True)
