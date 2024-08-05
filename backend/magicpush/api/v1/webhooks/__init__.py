from apiflask import APIBlueprint

webhooks = APIBlueprint('webhooks', __name__, enable_openapi=False)

from .routes import *
