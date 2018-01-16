from flask import Blueprint
variation = Blueprint('variation', __name__, url_prefix='/variation')

from . import views