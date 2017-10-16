# coding=utf-8
import os
import json
import interface
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
get_head_cmd = "select column_name from information_schema.columns where table_schema='snp_index' and table_name='{}';"
get_unique_cmd = "select distinct() from {};"
basedir = os.path.abspath(os.path.dirname(__file__))
app.secret_key = 'djaildhjsdfhjsofjilsfjsfjpjfojgogj'


@app.route('/')
def index():
    cmd = 'show tables'
    allTable = interface.get_db_data(cmd)
    tables = [table[0] for table in allTable if table[0].split('_')[0] == 'table']
    groups = [table[0] for table in allTable if table[0].split('_')[0] == 'group']
    return render_template('index.html',
                           table_files=tables,
                           group_files=groups)


@app.route('/select_group', methods=['GET'])
def select_group():
    filename = request.args.get('file', '')
    cmd = get_head_cmd.format(filename)
    header = interface.get_db_data(cmd)
    cultivar = [each[0] for each in header]
    cultivar = cultivar[2:]
    if cultivar:
        group_dict = dict.fromkeys(cultivar)
        for key, value in group_dict.items():
            result = interface.get_db_data(get_unique_cmd.format(key))
            result = [each[0] for each in result]
            group_dict[key] = result
        return jsonify({'msg': group_dict})
    else:
        return jsonify({'msg': 'error'})


@app.route('/search_descibe', methods=['GET'])
def search_descibe():
    table = request.args.get('table', '')
    descibe = request.args.get('descibe', '')
    # check whether sample in table
    cmd = get_head_cmd.format(table)
    header = interface.get_db_data(cmd)
    samples = [each[0] for each in header]
    if sample in samples:
        msg = sample
    else:
        msg = 'error'
    return jsonify({'msg': msg})


@app.route('/get_info', methods=['POST'])
def get_info():
    if request.method == 'POST':
        info = request.form['all_info']
        info = json.loads(info)
        table = info['table']
        chrom = info['chr']
        start_pos = info['start_pos']
        end_pos = info['end_pos']
        samples = info['selected_sample']
        query_header, query_data = interface.query_table(table,
                                                         chrom,
                                                         start_pos,
                                                         end_pos,
                                                         samples)

        return jsonify({'msg': 'ok',
                        'headData': query_header,
                        'bodyData': query_data})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
