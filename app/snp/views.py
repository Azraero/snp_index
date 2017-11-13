# coding:utf-8
import os
import json
from flask import render_template, request, jsonify
from ..utils import run_snpplot_script, get_cmd_by_regin, \
    calculate_table, get_select_group_info, \
    get_snp_info
from . import snp
from settings import basedir

SNP_INDEX_PATH = os.path.join(basedir, 'app', 'static', 'snp_results')
RENDER_PATH = '/static/snp_results'

@snp.route('/get_snp_plot')
def get_snp_plot():
    tables, groups = get_snp_info()
    return render_template('snp/get_snp_plot.html', files=tables, groups=groups)


@snp.route('/select_group')
def select_group():
    select_group = request.args.get('group')
    plot_files = get_select_group_info(select_group)
    return jsonify({'msg': 'ok',
                    'files': plot_files,
                    'name': 'vs'.join(select_group.split('_'))})


@snp.route('/generate_snp_plot', methods=['POST'])
def generate_snp_plot():
    if request.method == 'POST':
        info = json.loads(request.form['info'])
        table = info['table']
        groupA = info['groupA']
        groupB = info['groupB']
        groupA_name = info['customGroupA']
        groupB_name = info['customGroupB']
        filename = "%svs%s" %(groupA_name, groupB_name)
        cmd, groupA_len, groupB_len = get_cmd_by_regin(table,
                                                       groupA,
                                                       groupB,
                                                       get_all=True)
        query_header, query_data = calculate_table(cmd,
                                                   groupA_len,
                                                   groupB_len,
                                                   filename,
                                                   output=True,
                                                   only_group=True
                                                   )
        msg = run_snpplot_script(filepath=os.path.join(SNP_INDEX_PATH,
                                                       '_'.join([groupA_name, groupB_name]),
                                                       query_data),
                                 outdir=os.path.join(SNP_INDEX_PATH,
                                                     '_'.join([groupA_name, groupB_name]),
                                                     query_data + '_plot'))
        files = os.listdir(os.path.join(SNP_INDEX_PATH,
                                        '_'.join([groupA_name, groupB_name]),
                                        query_data + '_plot'))
        # test frontend code:
        # snp_results = basedir
        # files = glob.glob( + '/*.png')
        '''
        files = ['mhd_vs_whd_chr3D.png', 'mhd_vs_whd_chr4A.png',
                 'mhd_vs_whd_chr4B.png', 'mhd_vs_whd_chr4D.png']
        '''
        path = os.path.join(RENDER_PATH,
                            '_'.join([groupA_name, groupB_name]),
                            query_data + '_plot')

        return jsonify({'msg': query_data,
                        'name': 'vs'.join([groupA_name, groupB_name]),
                        'files': [os.path.join(path, each) for each in files]})