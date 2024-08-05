from apiflask import APIBlueprint

admin = APIBlueprint('admin', __name__, enable_openapi=False)

from .routes import *
