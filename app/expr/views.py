from flask import render_template, request, jsonify
from ..utils import get_expr_table, get_db_data
import re
import json
from . import expr
from ..utils import login_require

@expr.route('/show_by_gene')
@login_require
def show_by_gene():
    cmd = 'show tables'
    tables = get_db_data(cmd)
    tables = [table[0] for table in tables if table[0].split('_')[0] == 'expr']
    return render_template('expr/show_by_gene.html', files=tables)


@expr.route('/get_expr_info', methods=['POST'])
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
