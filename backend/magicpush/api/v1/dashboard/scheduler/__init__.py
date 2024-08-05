from apiflask import APIBlueprint

scheduler = APIBlueprint('scheduler', __name__, enable_openapi=False)

from .routes import *
