from flask import Blueprint

inscripciones = Blueprint('inscripciones', __name__)

from . import routes
