import dash
from dash import dcc, html

from app import app, server as application

# Connect to your app pages
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div("Hello I am DIV")
], className="App")


if __name__ == '__main__':
    print("access the server on http://127.0.0.1:8050/ http://127.0.0.1 or your defined address")
    app.run_server(host="0.0.0.0", debug=False, port=8050)
