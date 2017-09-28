# coding=utf-8
import os
import json
import interface
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
get_head_cmd = "select column_name from information_schema.columns where table_schema='snp_index' and table_name='{}';"
basedir = os.path.abspath(os.path.dirname(__file__))
app.secret_key = 'djaildhjsdfhjsofjilsfjsfjpjfojgogj'


@app.route('/')
def index():
    cmd = 'show tables'
    tables = interface.get_db_data(cmd)
    tables = [table[0] for table in tables]
    return render_template('index.html', user='chencheng', files=tables)


@app.route('/select_file', methods=['GET'])
def select_file():
    filename = request.args.get('file', '')
    cmd = get_head_cmd.format(filename)
    header = interface.get_db_data(cmd)
    samples = [each[0] for each in header]
    samples = samples[5:]
    # only show 30 samples
    if len(samples) > 30:
        samples = samples[:30]
    return jsonify({'msg': samples})


@app.route('/search_sampe', methods=['GET'])
def search_sampe():
    table = request.args.get('table', '')
    sample = request.args.get('sample', '')
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
