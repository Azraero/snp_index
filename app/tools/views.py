# coding=utf-8
import os
import glob
import json
from . import tools
from settings import basedir
from flask_login import login_required, current_user
from flask import render_template, request, jsonify
from app.utils import get_cmd_by_regin, calculate_table, get_samples_by_table, get_map, map_sample
from .actions import get_select_group_info, get_snp_info, run_snpplot_script, get_locus_result, run_blast_result


SNP_INDEX_PATH = os.path.join(basedir, 'app', 'static', 'snp_results')
RENDER_PATH = '/static/snp_results'
db2web_dict, web2db_dict = get_map()


@tools.route('/locus_identifier_search/')
@login_required
def locus_identifier_search():
    if request.args.get('gene', ''):
        genename = request.args['gene']
        blast_results = run_blast_result(genename)
        locus_result = get_locus_result(genename, blast_results)
        return render_template('tools/locus_gene_result.html',
                               locus_result=locus_result)
    return render_template('tools/locus_gene.html')


@tools.route('/select_file/')
def select_file_by_plot():
    filename = request.args.get('file', '')
    if filename:
        samples = get_samples_by_table(filename, type='snp')
        samples = map_sample(samples, db2web_dict)
        if not samples:
            return jsonify({'msg': 'error'})
        return jsonify({'msg': samples})
    return jsonify({'msg': 'error'})


@tools.route('/get_snp_plot/')
def get_snp_plot():
    tables, groups = get_snp_info(current_user.username)
    return render_template('tools/get_snp_plot.html', files=tables, groups=groups)


@tools.route('/get_pca_plot/')
def get_pca_plot():
    return render_template('tools/get_pca_plot.html')


@tools.route('/select_group/')
def select_group():
    select_group = request.args.get('group')
    plot_files = get_select_group_info(select_group)
    return jsonify({'msg': 'ok',
                    'files': plot_files,
                    'name': 'vs'.join(select_group.split('_'))})


@tools.route('/generate_snp_plot/', methods=['POST'])
def generate_snp_plot():
    if request.method == 'POST':
        info = json.loads(request.form['info'])
        table = info['table']
        groupA = map_sample(info['groupA'], map_dict=web2db_dict)
        groupB = map_sample(info['groupB'], map_dict=web2db_dict)
        groupA_name = info['customGroupA']
        groupB_name = info['customGroupB']
        chrom = info['chrom']
        filename = "%svs%s" % (groupA_name, groupB_name)
        cmd, groupA_len, groupB_len = get_cmd_by_regin(table,
                                                       groupA,
                                                       groupB,
                                                       chrom=chrom,
                                                       get_all=True)
        query_data = calculate_table(cmd,
                                     groupA_len,
                                     groupB_len,
                                     filename,
                                     output=True,
                                     chrom=chrom)
        msg = run_snpplot_script(filepath=os.path.join(SNP_INDEX_PATH,
                                                       '_'.join([groupA_name, groupB_name]),
                                                       query_data),
                                 outdir=os.path.join(SNP_INDEX_PATH,
                                                     '_'.join([groupA_name, groupB_name]),
                                                     'vs'.join([groupA_name, groupB_name]) + '_plot'))
        files = glob.glob(os.path.join(SNP_INDEX_PATH, '_'.join([groupA_name, groupB_name]), 'vs'.join([groupA_name, groupB_name]) + '_plot') + '/*png')
        files_short = [each.rsplit('/', 1)[1] for each in files]

        path = os.path.join(RENDER_PATH,
                            '_'.join([groupA_name, groupB_name]),
                            'vs'.join([groupA_name, groupB_name]) + '_plot')

        return jsonify({'msg': query_data,
                        'name': 'vs'.join([groupA_name, groupB_name]),
                        'files': [os.path.join(path, each) for each in files_short]})