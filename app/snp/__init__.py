from flask import Blueprint

snp = Blueprint('snp', __name__, url_prefix='/snp')

from . import views
