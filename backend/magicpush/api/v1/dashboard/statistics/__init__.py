from apiflask import APIBlueprint

statistics = APIBlueprint('statistics', __name__, enable_openapi=False)

from .routes import *
