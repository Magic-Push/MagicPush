from apiflask import APIBlueprint

users = APIBlueprint('users', __name__, enable_openapi=False)

from .routes import *
