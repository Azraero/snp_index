# coding=utf-8
from . import expr
from flask import render_template


@expr.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@expr.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500