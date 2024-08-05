from apiflask import APIBlueprint

rest = APIBlueprint('rest', __name__)

from .routes import *
