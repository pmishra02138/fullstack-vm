from flask import Blueprint

moviecatalog = Blueprint('moviecatalog', __name__)

from . import routes
