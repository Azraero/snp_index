from flask import Blueprint

snp = Blueprint('snp', __name__)

from . import views, errors