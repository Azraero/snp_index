# coding=utf-8
from . import tools
from flask import render_template, request
from ..utils import get_locus_result

@tools.route('/locus_identifier_search')
def locus_identifier_search():
    if request.args.get('gene', ''):
        genename = request.args['gene']
        locus_result = get_locus_result(genename)
        return render_template('tools/locus_gene_result.html',
                               locus_result=locus_result)
    return render_template('tools/locus_gene.html')
