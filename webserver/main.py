# -*- coding: utf-8 -*-
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from pageload import *
from dash.dependencies import Input, Output, State

external_scripts = [
    '"https://cdn.jsdelivr.net/npm/cookie-bar/cookiebar-latest.min.js?tracking=1&thirdparty=1&always=1&noGeoIp=1&refreshPage=1"']

#settingsfile = cset.configSettings(("settings.json")).configdict
#external_stylesheets = 'http://newsfromiceland.epizy.com/style.css'
# link fontawesome to get the chevron icons
FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"

app = dash.Dash(__name__, external_scripts=external_scripts,
                external_stylesheets=[dbc.themes.BOOTSTRAP, FA])
pagecontent = []
pageloaderhandler = pageload()
pagecontent = pageloaderhandler.pageload


for i in [1, 2]:
    app.callback(
        Output(f"submenu-{i}-collapse", "is_open"),
        [Input(f"submenu-{i}", "n_clicks")],
        [State(f"submenu-{i}-collapse", "is_open")],
    )(pageload.toggle_collapse)

    app.callback(
        Output(f"submenu-{i}", "className"),
        [Input(f"submenu-{i}-collapse", "is_open")],
    )(pageload.set_navitem_class)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1/1"]:
        return html.P("This is the content of page 1.1!")
    elif pathname == "/page-1/2":
        return html.P("This is the content of page 1.2. Yay!")
    elif pathname == "/page-2/1":
        return html.P("Oh cool, this is page 2.1!")
    elif pathname == "/page-2/2":
        return html.P("No way! This is page 2.2!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


app.layout = html.Div(children=pagecontent)
if __name__ == "__main__":
    app.run_server(debug=True)
