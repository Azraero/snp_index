# coding=utf-8
from . import tools
from flask import render_template


@tools.route('/blast')
def blast():
    return render_template('tools/blast.html')
