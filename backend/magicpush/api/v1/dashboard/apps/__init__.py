from apiflask import APIBlueprint

apps = APIBlueprint('apps', __name__, enable_openapi=False)

from .routes import *
