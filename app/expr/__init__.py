from flask import Blueprint

expr = Blueprint('expr', __name__, url_prefix='/expr')

from . import views
