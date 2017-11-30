# coding=utf-8
import os
import glob
import MySQLdb
import subprocess
from db_const import get_head_cmd, HOSTNAME, USERNAME, PASSWORD, DATABASE
from settings import basedir
from .db import DB

SNP_INDEX_PATH = os.path.join(basedir, 'app', 'static', 'snp_results')
RENDER_PATH = '/static/snp_results'


def get_db_data(cmd, fetchall=True):
    con = MySQLdb.connect(HOSTNAME, USERNAME, PASSWORD, DATABASE)
    with con as cur:
        cur.execute(cmd)
        if fetchall:
            rows = cur.fetchall()
            return rows
        else:
            row = cur.fetchone()
            return row


def get_group_data(groupList):
    results = []
    for each in groupList:
        filter_cell = [cell for cell in each if cell != '0' and cell != '0,0' and cell != '0,0,0' and cell != '.']
        if len(filter_cell) == 0:
            results.append(['0,0', 'NA', 'NA'])
        else:
            # deal three comma numbers
            for i in range(len(filter_cell)):
                tmpList = filter_cell[i].split(',')
                if len(tmpList) == 3:
                    maxOne = max([int(cell) for cell in tmpList])
                    minOne = min([int(cell) for cell in tmpList])
                    filter_cell[i] = ','.join([str(maxOne), str(minOne)])

            first_pos = sum([int(cell.split(',')[0]) for cell in filter_cell])
            second_pos = sum([int(cell.split(',')[1]) for cell in filter_cell])
            # other condition
            if first_pos + second_pos == 0:
                results.append(['0,0', 'NA', 'NA'])
            else:
                first_ratio = round(float(first_pos) / (first_pos + second_pos), 2)
                second_ratio = round(float(second_pos) / (first_pos + second_pos), 2)
                new_cell = ','.join([str(first_pos), str(second_pos)])
                results.append([new_cell, str(first_ratio), str(second_ratio)])
    return results


def get_only_group_data(groupList, groupLen):
    results = []
    for each in groupList:
        filter_cell = [cell for cell in each if cell != '0' and cell != '0,0' and cell != '0,0,0' and cell != '.']
        if len(filter_cell) == 0:
            results.append('0,0')
        else:
            # deal three comma numbers
            for i in range(len(filter_cell)):
                tmpList = filter_cell[i].split(',')
                if len(tmpList) == 3:
                    maxOne = max([int(cell) for cell in tmpList])
                    minOne = min([int(cell) for cell in tmpList])
                    filter_cell[i] = ','.join([str(maxOne), str(minOne)])

            first_pos = sum([int(cell.split(',')[0]) for cell in filter_cell]) / groupLen
            second_pos = sum([int(cell.split(',')[1]) for cell in filter_cell]) / groupLen
            # other condition
            if first_pos + second_pos == 0:
                results.append('0,0')
            else:
                new_cell = ','.join([str(first_pos), str(second_pos)])
                results.append(new_cell)
    return results


def get_merge_group_data(group_info, groupALen, groupBLen,
                         output, filename, only_group):
    results = []
    groupAList = [list(each[6:(groupALen+6)]) for each in group_info]
    groupBList = [list(each[(groupBLen+6):]) for each in group_info]
    if only_group:
        header_line = [list(each[:2]) + ['1'] for each in group_info]
        mergeGroupA = get_only_group_data(groupAList, groupALen)
        mergeGroupB = get_only_group_data(groupBList, groupBLen)
        mergeGroup = []
        for eachA, eachB in zip(mergeGroupA, mergeGroupB):
            mergeGroup.append(eachA.split(',') + eachB.split(','))
    else:
        header_line = [list(each[:6]) for each in group_info]
        mergeGroupA = get_group_data(groupAList)
        mergeGroupB = get_group_data(groupBList)
        mergeGroup = []
        for ListA, ListB in zip(mergeGroupA, mergeGroupB):
            tmpList = []
            for cellA, cellB in zip(ListA, ListB):
                tmpList.append(cellA)
                tmpList.append(cellB)
            mergeGroup.append(tmpList)
    if output:
        group_dir = os.path.join(SNP_INDEX_PATH, '_'.join(filename.split('vs')))
        if not os.path.exists(group_dir):
            os.mkdir(group_dir)

        with open(os.path.join(group_dir, filename), 'w+') as f:
            for head, each in zip(header_line, mergeGroup):
                # print head
                f.write('\t'.join(head + each) + '\n')
        return filename
    else:
        for head, each in zip(header_line, mergeGroup):
            results.append(head + each)
        return results


def calculate_table(cmd, groupA_len, groupB_len,
                    filename='GroupAvsGroupB',
                    output=False,
                    only_group=False):
    header = ['CHR', 'POS', 'REF', 'ALT',
              'FEATURE', 'GENE',
              'GroupA', 'GroupB',
              'GroupA Frequency Primary Allele',
              'GroupB Frequency Primary Allele',
              'GroupA Frequency Second Allele',
              'GroupB Frequency Second Allele']
    results = get_merge_group_data(get_db_data(cmd),
                                   groupA_len,
                                   groupB_len,
                                   output,
                                   filename,
                                   only_group)
    return header, results


'''
add on 2017-10-26
'''


def get_cmd_by_regin(table, groupA, groupB, get_all=False, chrom='', start_pos='', end_pos=''):
    '''
    :param table: snp_table
    :param groupA: compare group
    :param groupB: compare group
    :param get_all: bool if get_all = True get whole chrom to plot snp index
    :param chrom:
    :param start_pos:
    :param end_pos:
    :return: mysql raw cmd and groups length
    '''
    select_columns = ['CHR', 'POS', 'REF', 'ALT', 'FEATURE', 'GENE'] + groupA + groupB
    select_columns_str = ','.join(select_columns)
    if get_all:
        get_group_cmd = "select {columns} from {table} where CHR='{chrom}';"
        cmd = get_group_cmd.format(
            columns=select_columns_str,
            table=table,
            chrom=chrom
        )
    else:
        get_group_cmd = "select {columns} from {table} where POS >= {start_pos} and \
                         POS <= {end_pos} and CHR='{chrom}';"
        cmd = get_group_cmd.format(
            columns=select_columns_str,
            table=table,
            start_pos=int(start_pos),
            end_pos=int(end_pos),
            chrom=chrom)
    return cmd, len(groupA), len(groupB)


def get_cmd_by_gene(table, gene_id, up, down, groupA, groupB):
    '''
    :param table: snp table
    :param gene_id: search gene id
    :param up:
    :param down:
    :param groupA:
    :param groupB:
    :return:
    '''
    select_columns = ['CHR', 'POS', 'REF', 'ALT', 'FEATURE', 'GENE'] + groupA + groupB
    get_group_cmd = "select POS from {table} where GENE='{gene_id}';"
    select_columns_str = ','.join(select_columns)
    cmd = get_group_cmd.format(
        table=table,
        gene_id=gene_id)
    results = get_db_data(cmd)
    pos_list = [int(result[0]) for result in results]
    if len(pos_list) == 0:
        return ('', gene_id, '')
    min_pos = min(pos_list)
    max_pos = max(pos_list)
    start_pos = min_pos - up
    end_pos = max_pos + down
    cmd = "select {columns} from {table} where POS>={start_pos} and POS<={end_pos};".format(
        columns=select_columns_str,
        table=table,
        start_pos=start_pos,
        end_pos=end_pos
    )
    return (cmd, len(groupA), len(groupB))


def get_region_by_gene(table, gene_id):
    select_columns = ['GENE_ID', 'CHR', 'POS_START', 'POS_END']
    select_columns_str = ','.join(select_columns)
    cmd = "select {columns} from {table} where GENE_ID='{gene_id}'".format(table=table,
                                                                           columns=select_columns_str,
                                                                           gene_id=gene_id)
    result = get_db_data(cmd, fetchall=False)
    if result:
        chrom, pos_start, pos_end = result[1:]
        return (chrom, pos_start, pos_end)
    else:
        return ('', '', '')

'''
add on 2017-11-08
'''

def run_snpplot_script(filepath, outdir):
    # run bash&R script for snp index
    # bash generate bed.out file
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    bedCmd = 'sh cmd.sh snp_w2m_s10k_.bed {0}'.format(filepath)
    subprocess.call(args=bedCmd, shell=True)
    Rcmd = 'Rscript {path} {bed_path} {outpath}'.format(path=os.path.join(basedir,
                                                                'app',
                                                                'snp_index_by_bed.R'),
                                                        bed_path=filepath + '.bed.out',
                                                        outpath=outdir
                                                        )
    subprocess.call(args=Rcmd, shell=True)

    return 'done'

'''
add on 2017-11-10
'''


def get_select_group_info(select_group):
    plot_path = 'vs'.join(select_group.split('_')) + '_plot'
    select_group_path = os.path.join(SNP_INDEX_PATH, select_group, plot_path)
    print select_group_path
    plot_files = glob.glob(select_group_path + '/*.png')
    plot_files = [os.path.join(RENDER_PATH, select_group, plot_path, each.rsplit('/', 1)[1]) for each in plot_files]
    return plot_files


def get_snp_info(rm_len=3):
    cmd = 'show tables'
    tables = get_db_data(cmd)
    tables = [table[0] for table in tables if table[0].split('_')[0] == 'snp']
    groups = os.listdir(SNP_INDEX_PATH)
    # rm group dir when > 3
    if len(groups) > rm_len:
        rm_groups = groups[rm_len:]
        for dir in rm_groups:
            try:
                subprocess.call('rm -rf {0}'.format(os.path.join(SNP_INDEX_PATH,
                                                                dir)))
            except:
                pass

    return tables, groups

'''
add on 2017-11-28
'''

from flask import session, redirect, url_for
from functools import wraps
def login_require(views):
    @wraps(views)
    def wrapper(*args, **kwargs):
        user = session.get('login_id', '')
        if user:
            return views(*args, **kwargs)
        return redirect(url_for('auth.login'))
    return wrapper


def get_db_tables(user, type):
    db = DB()
    get_table_cmd = "select {table} from users where username='{user}'"
    result = db.execute(get_table_cmd.format(table=type + '_table', user=user.encode('utf-8')))
    if not result:
        return []
    else:
        print result
        tables = result[0][0].split(':')
        return tables


def get_samples_by_table(table, type):
    # expr 5
    if type == 'snp':
        fixed_column_num = 7
    elif type == 'expr':
        fixed_column_num = 5
    else:
        return []
    cmd = get_head_cmd.format(table)
    db = DB()
    header = db.execute(cmd)
    samples = [each[0] for each in header][fixed_column_num:]
    return samples




