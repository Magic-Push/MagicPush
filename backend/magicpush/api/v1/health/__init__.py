from apiflask import APIBlueprint

health = APIBlueprint('health', __name__, enable_openapi=False)

from .routes import *
