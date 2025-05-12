from shiny import App
from ._live_dash_server import create_dash_server
from ._live_dash_ui import create_dash_ui

def create_dash_app(sclive_dash):
    return App(create_dash_ui(sclive_dash), create_dash_server(sclive_dash))