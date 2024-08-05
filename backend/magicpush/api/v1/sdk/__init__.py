from apiflask import APIBlueprint

sdk = APIBlueprint('sdk', __name__, enable_openapi=False)

from .routes import *
