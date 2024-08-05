from apiflask import APIBlueprint

flow = APIBlueprint('flow', __name__, enable_openapi=False)

from .routes import *
