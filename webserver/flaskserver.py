import flask
import dash
import dash_html_components as html

server = flask.Flask(__name__)


if server.config["ENV"] == "production":
    server.config.from_object("config.ProductionConfig")
else:
    server.config.from_object("config.DevelopmentConfig")


@server.route('/')
def index():
    return 'Hello Flask app'


app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/frettir/'
)

app.layout = html.Div("My Dash app")

if __name__ == '__main__':
    app.run_server(debug=False)
