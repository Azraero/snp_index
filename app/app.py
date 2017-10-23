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
    tables = interface.get_db_data(cmd)
    tables = [table[0] for table in tables]
    return render_template('index.html', files=tables)


@app.route('/select_file', methods=['GET'])
def select_file():
    filename = request.args.get('file', '')
    cmd = get_head_cmd.format(filename)
    header = interface.get_db_data(cmd)
    if header[0]:
        samples = [each[0] for each in header]
        # return all samples
        samples = samples[5:]
        return jsonify({'msg': samples})
    else:
        return jsonify({'msg': 'error'})


@app.route('/get_info', methods=['POST'])
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
        query_header, query_data = interface.calculate_table(table,
                                                             chrom,
                                                             start_pos,
                                                             end_pos,
                                                             groupA,
                                                             groupB)
        return jsonify({'msg': 'ok',
                        'headData': query_header,
                        'bodyData': query_data})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
