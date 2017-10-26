# coding=utf-8
import json
from ..utils import get_db_data, calculate_table, get_region_by_gene
from . import main
from ..db import get_head_cmd, relative_table
from flask import render_template, jsonify, \
                  request, session, redirect, url_for


@main.route('/search_by_regin')
def search_by_regin():
    cmd = 'show tables'
    tables = get_db_data(cmd)
    tables = [table[0] for table in tables if table[0].split('_')[0] == 'snp']
    return render_template('gene_variation/search_by_regin.html', files=tables)


@main.route('/')
def index():
    return redirect(url_for('main.search_by_regin'))


@main.route('/search_by_gene')
def search_by_gene():
    filename = relative_table.get(session.get('table', ''), '')
    fixed_column_num = 5
    samples = []
    if filename:
        cmd = get_head_cmd.format(filename)
        header = get_db_data(cmd)
        if header[0]:
            samples = [each[0] for each in header]
            # return all samples
            samples = samples[fixed_column_num:]

    return render_template('gene_variation/search_by_gene.html',
                           samples=samples)


@main.route('/select_file', methods=['GET'])
def select_file():
    fixed_column_num = 7
    filename = request.args.get('file', '')
    cmd = get_head_cmd.format(filename)
    header = get_db_data(cmd)
    if header[0]:
        samples = [each[0] for each in header]
        session['table'] = filename
        # return all samples
        samples = samples[fixed_column_num:]
        return jsonify({'msg': samples})
    else:
        return jsonify({'msg': 'error'})


'''
post methods
'''


@main.route('/get_snp_info', methods=['POST'])
def get_snp_info():
    if request.method == 'POST':
        info = request.form['all_info']
        info = json.loads(info)
        table = info['table']
        chrom = info['chr']
        start_pos = info['start_pos']
        end_pos = info['end_pos']
        groupA = info['groupA']
        groupB = info['groupB']
        query_header, query_data = calculate_table(table,
                                                   chrom,
                                                   start_pos,
                                                   end_pos,
                                                   groupA,
                                                   groupB)
        return jsonify({'msg': 'ok',
                        'headData': query_header,
                        'bodyData': query_data})


@main.route('/get_gene_info', methods=['POST'])
def get_gene_info():
    if request.method == 'POST':
        snp_table = session.get('table', '')
        if not snp_table:
            return jsonify({'msg': 'you should select file in \
                            search by regin page first!'})
        table = relative_table.get(snp_table, '')
        info = request.form['info']
        info = json.loads(info)
        gene_name = info['gene_name']
        groupA = info['groupA']
        groupB = info['groupB']
        gene_upstream = info['gene_upstream']
        gene_downstream = info['gene_downstream']
        chrom, start_pos, end_pos = get_region_by_gene(table, gene_name)
        if chrom:
            start_pos = int(start_pos) - int(gene_upstream) * 1000
            end_pos = int(end_pos) + int(gene_downstream) * 1000
            if start_pos < 0:
                start_pos = 0
            query_header, query_data = calculate_table(snp_table,
                                                       chrom,
                                                       start_pos,
                                                       end_pos,
                                                       groupA,
                                                       groupB)
            return jsonify({'msg': 'ok',
                            'headData': query_header,
                            'bodyData': query_data})
        return jsonify({'msg': 'not find snp index data!'})
