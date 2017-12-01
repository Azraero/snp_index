from flask import render_template, request, jsonify, session
from app.utils import get_db_tables, get_samples_by_table, login_require
import re
import json
from . import expr
from .actions import get_expr_table


@expr.route('/expr/show_by_gene')
@login_require
def show_by_gene():
    user = session['login_id']
    tables = get_db_tables(user, type='expr')
    return render_template('expr/show_by_gene.html', files=tables)


@expr.route('/expr/select_file', methods=['GET'])
def select_file_by_expr():
    filename = request.args.get('file', '')
    if filename:
        samples = get_samples_by_table(filename, type='expr')
        if not samples:
            return jsonify({'msg': 'error'})
        return jsonify({'msg': samples})
    return jsonify({'msg': 'error'})


@expr.route('/expr/get_expr_info', methods=['POST'])
def get_expr_info():
    if request.method == 'POST':
        info = request.form['info']
        info = json.loads(info)
        table = info['table']
        groupA = info['groupA']
        groupB = info['groupB']
        gene_str = info['gene_name']
        gene_ids = re.split(r'[\s,]', gene_str.strip())
        if len(gene_ids) > 10:
            return jsonify({'msg': 'query gene number not allowed > 10'})
        query_header, query_data = get_expr_table(
            table,
            gene_ids,
            groupA,
            groupB
        )
        if not query_data:
            return jsonify({'msg': 'not search {0} in database!'.format(
                query_header
            )})

        return jsonify({'msg': 'ok',
                        'headData': query_header,
                        'bodyData': query_data})
