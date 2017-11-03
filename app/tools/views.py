# coding=utf-8
import os
import json
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


'''
UPLOAD_FOLDER = os.path.abspath(os.path.join(basedir, 'app/blast_file'))


@tools.route('/blast')
def blast():
    return render_template('tools/blast.html')


@tools.route('/get_blast_info', methods=['POST'])
def get_blast_info():
    if request.method == 'POST':
        info = json.loads(request.form['info'])
        if 'seqfile' in request.files:
            # file not check content size
            seqstr = request.files['seqfile'].read()
        elif info.get('seqstr', ''):
            seqstr = info['seqstr']
        else:
            return jsonify({'msg': 'not find seq file or seq string!'})
        program = info['program']
        database = info['database']
'''