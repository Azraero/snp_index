# coding:utf-8
import os
import glob
import json
from flask import render_template, request, jsonify
from ..utils import get_db_data, get_cmd_by_regin, \
    calculate_table, run_snpplot_script
from . import snp
from settings import basedir


@snp.route('/get_snp_plot')
def get_snp_plot():
    cmd = 'show tables'
    tables = get_db_data(cmd)
    tables = [table[0] for table in tables if table[0].split('_')[0] == 'snp']
    return render_template('snp/get_snp_plot.html', files=tables)


@snp.route('/generate_snp_plot', methods=['POST'])
def generate_snp_plot():
    if request.method == 'POST':
        info = json.loads(request.form['info'])
        table = info['table']
        groupA = info['groupA']
        groupB = info['groupB']

        cmd, groupA_len, groupB_len = get_cmd_by_regin(table,
                                                       groupA,
                                                       groupB,
                                                       get_all=True)
        query_header, query_data = calculate_table(cmd,
                                                   groupA_len,
                                                   groupB_len,
                                                   output=True,
                                                   only_group=True
                                                   )

        # msg = run_snpplot_script(filepath=os.path.join(SNP_INDEX_PATH, query_data))
        # test frontend code:
        # snp_results = basedir
        # files = glob.glob( + '/*.png')
        path = '/static/snp_results/'
        files = ['mhd_vs_whd_chr1A.png', 'mhd_vs_whd_chr1B.png', 'mhd_vs_whd_chr2A.png']
        return jsonify({'msg': query_data,
                        'files': [os.path.join(path, each) for each in files]})