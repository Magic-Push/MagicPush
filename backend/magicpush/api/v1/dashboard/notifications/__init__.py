from apiflask import APIBlueprint

notifications = APIBlueprint('notifications', __name__, enable_openapi=False)

from .routes import *
