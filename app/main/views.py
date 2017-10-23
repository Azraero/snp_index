# coding=utf-8
import json
from ..utils import get_db_data, calculate_table
from . import main
from ..db import get_head_cmd
from flask import render_template, jsonify, request


@main.route('/')
def index():
    cmd = 'show tables'
    tables = get_db_data(cmd)
    tables = [table[0] for table in tables]
    return render_template('index.html', files=tables)


@main.route('/select_file', methods=['GET'])
def select_file():
    filename = request.args.get('file', '')
    cmd = get_head_cmd.format(filename)
    header = get_db_data(cmd)
    if header[0]:
        samples = [each[0] for each in header]
        # return all samples
        samples = samples[7:]
        return jsonify({'msg': samples})
    else:
        return jsonify({'msg': 'error'})


@main.route('/get_info', methods=['POST'])
def get_info():
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
