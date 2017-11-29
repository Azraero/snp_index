# coding=utf-8
import json
from . import variation
from flask import render_template, jsonify, request, session
from ..utils import login_require
from .actions import

@variation.route('/search_by_regin')
@login_require
def search_by_regin():
    user = session['login_id']
    get_db_tables(user, type='snp')
    return render_template('gene_variation/search_by_regin.html', files=tables)


@variation.route('/search_by_gene')
@login_require
def search_by_gene():
    cmd = 'show tables'
    tables = get_db_data(cmd)
    tables = [table[0] for table in tables if table[0].split('_')[0] == 'snp']
    return render_template('gene_variation/search_by_gene.html', files=tables)


@variation.route('/select_file', methods=['GET'])
def select_file():
    filename = request.args.get('file', '')
    if filename:
        if filename.split('_')[0] == 'snp':
            fixed_column_num = 7
        elif filename.split('_')[0] == 'expr':
            fixed_column_num = 5

        cmd = get_head_cmd.format(filename)
        header = get_db_data(cmd)
        if header[0]:
            samples = [each[0] for each in header]
            samples = samples[fixed_column_num:]
            return jsonify({'msg': samples})
        else:
            return jsonify({'msg': 'error'})
    else:
        return jsonify({'msg': 'error'})


'''
post methods
'''


@variation.route('/get_snp_info', methods=['POST'])
def get_snp_info():
    if request.method == 'POST':
        info = request.form['info']
        info = json.loads(info)
        table = info['table']
        groupA = info['groupA']
        groupB = info['groupB']
        if info['search'] == 'regin':
            chrom = info['chr']
            start_pos = info['start_pos']
            end_pos = info['end_pos']
            cmd, groupA_len, groupB_len = get_cmd_by_regin(table,
                                                           groupA,
                                                           groupB,
                                                           chrom=chrom,
                                                           start_pos=start_pos,
                                                           end_pos=end_pos)
        else:
            gene_id = info['gene_name']
            gene_upstream = int(info['gene_upstream'])
            gene_downstream = int(info['gene_downstream'])
            cmd, groupA_len, groupB_len = get_cmd_by_gene(table,
                                                          gene_id,
                                                          gene_upstream,
                                                          gene_downstream,
                                                          groupA,
                                                          groupB)
            if not cmd:
                return jsonify({'msg': 'not search {0} in database'.format(
                    groupA_len
                )})
        query_header, query_data = calculate_table(cmd,
                                                   groupA_len,
                                                   groupB_len)
        return jsonify({'msg': 'ok',
                        'headData': query_header,
                        'bodyData': query_data})


