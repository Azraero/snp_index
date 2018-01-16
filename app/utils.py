# coding=utf-8
import os
import sys
import MySQLdb
from .db import DB
from .db_const import get_head_cmd, HOSTNAME, USERNAME, PASSWORD, DATABASE
from settings import basedir

SNP_INDEX_PATH = os.path.join(basedir, 'app', 'static', 'snp_results')
MAP_GROUP_PATH = os.path.join(basedir, 'data', 'mRNA_group_cut')
RENDER_PATH = '/static/snp_results'
PLOT_HEADER = 2
SPLIT_GROUP = 4
SNP_TABLE_HEADER = 6


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


def get_row_count_by_group(row_list, cell_len, out_split='|'):
    count_row = [0] * cell_len
    for i in range(len(row_list)):
        cell_list = [int(cell) for cell in row_list[i].split(',')]
        for j in range(cell_len):
            count_row[j] = count_row[j] + cell_list[j]
    count_str = out_split.join([str(cell) for cell in count_row])
    if cell_len > SPLIT_GROUP:
        return [count_str]
    count_sum = sum(count_row)
    if count_sum == 0:
        return [count_str] + ['NA'] * cell_len
    count_row = [str(float(cell) / count_sum) for cell in count_row]
    return [count_str] + count_row


def get_group_data(groupList):
    # divide table into 4
    # include header
    results_split2 = []
    results_split3 = []
    results_split4 = []
    results_splitn = []
    for row in groupList:
        # only check split not over 2
        filter_cell = [cell for cell in row[SNP_TABLE_HEADER:] if cell != '0' and cell != '0,0' and cell != '.']
        if len(filter_cell) == 0:
            results_split2.append(row[:SNP_TABLE_HEADER] + ['0|0', 'NA', 'NA'])
        else:
            # each row's cell len must be same
            cell_len = len(filter_cell[0].split(','))
            count_row = get_row_count_by_group(filter_cell, cell_len)
            if cell_len == 2:
                results_split2.append(row[:SNP_TABLE_HEADER] + count_row)
            elif cell_len == 3:
                results_split3.append(row[:SNP_TABLE_HEADER] + count_row)
            elif cell_len == 4:
                results_split4.append(row[:SNP_TABLE_HEADER] + count_row)
            else:
                results_splitn.append(row[:SNP_TABLE_HEADER] + count_row)
    results_split_list = [results_split2, results_split3, results_split4, results_splitn]
    return results_split_list


def get_plot_group_data(groupList, groupLen, filter=True):
    results = []
    for each in groupList:
        filter_cell = [cell for cell in each if cell != '0' and cell != '0,0' and cell != '.']
        if len(filter_cell) == 0:
            results.append('0,0')
        else:
            # deal split over 3
            for i in range(len(filter_cell)):
                tmpList = filter_cell[i].split(',')
                if len(tmpList) >= 3:
                    maxOne = max([int(cell) for cell in tmpList])
                    minOne = min([int(cell) for cell in tmpList])
                    filter_cell[i] = ','.join([str(maxOne), str(minOne)])

            first_pos = sum([int(cell.split(',')[0]) for cell in filter_cell]) / groupLen
            second_pos = sum([int(cell.split(',')[1]) for cell in filter_cell]) / groupLen
            new_cell = ','.join([str(first_pos), str(second_pos)])
            results.append(new_cell)
    if filter:
        results = [result for result in results if sum([float(each) for each in result.split(',')]) > 1]
        return results
    return results


def get_merge_group_data(group_info, groupALen, groupBLen,
                         output, filename, chrom):
    filename_chr = '_'.join([filename, chrom])
    if output:
        groupAList = [list(each[SNP_TABLE_HEADER:(groupALen + SNP_TABLE_HEADER)]) for each in group_info]
        groupBList = [list(each[(groupALen + SNP_TABLE_HEADER):]) for each in group_info]
        header_line = [list(each[:PLOT_HEADER]) for each in group_info]
        mergeGroupA = get_plot_group_data(groupAList, groupALen)
        mergeGroupB = get_plot_group_data(groupBList, groupBLen)
        mergeGroup = []
        for eachA, eachB in zip(mergeGroupA, mergeGroupB):
            mergeGroup.append(eachA.split(',') + eachB.split(','))
        group_dir = os.path.join(SNP_INDEX_PATH, '_'.join(filename.split('vs')))
        if not os.path.exists(group_dir):
            os.mkdir(group_dir)
        with open(os.path.join(group_dir, filename_chr), 'w+') as f:
            for head, each in zip(header_line, mergeGroup):
                f.write('\t'.join(head + each) + '\n')
        # return file name
        return filename_chr
    else:
        groupAList = [list(each[:(groupALen + SNP_TABLE_HEADER)]) for each in group_info]
        groupBList = [list(each[:SNP_TABLE_HEADER] + each[(groupALen + SNP_TABLE_HEADER):]) for each in group_info]
        mergeGroup_list = [list() for i in range(SPLIT_GROUP)]
        mergeA_split_list = get_group_data(groupAList)
        mergeB_split_list = get_group_data(groupBList)
        for i in range(SPLIT_GROUP):
            for ListA, ListB in zip(mergeA_split_list[i], mergeB_split_list[i]):
                tmpList = []
                tmpList.extend(ListA[:SNP_TABLE_HEADER])
                for cellA, cellB in zip(ListA[SNP_TABLE_HEADER:], ListB[SNP_TABLE_HEADER:]):  # drop listB's header
                    tmpList.append(cellA)
                    tmpList.append(cellB)
                # add extra three columns
                tmpList = add_direction(tmpList)
                mergeGroup_list[i].append(tmpList)
        # results_split2, results_split3, results_split4, results_splitn = mergeGroup_list
        # print mergeGroup_list
        return mergeGroup_list


def calculate_table(cmd, groupA_len, groupB_len,
                    filename='GroupAvsGroupB',
                    output=False,
                    chrom=''):
    header = ['CHR', 'POS', 'REF', 'ALT',
              'FEATURE', 'GENE',
              'GroupA', 'GroupB']
    header_end = ['GroupA Direction', 'GroupB Direction', 'Total Depth']

    split_two = ['GroupA Frequency Primary Allele',
                 'GroupB Frequency Primary Allele',
                 'GroupA Frequency Second Allele',
                 'GroupB Frequency Second Allele']

    split_three = ['GroupA Frequency Third Allele',
                   'GroupB Frequency Third Allele']

    split_four = ['GroupA Frequency Four Allele',
                  'GroupB Frequency Four Allele']
    if output:
        # results is a str for filename
        results = get_merge_group_data(get_db_data(cmd),
                                       groupA_len,
                                       groupB_len,
                                       output,
                                       filename,
                                       chrom=chrom)
    else:
        results_split2, results_split3, results_split4, results_splitn = get_merge_group_data(get_db_data(cmd),
                                                                                              groupA_len,
                                                                                              groupB_len,
                                                                                              output,
                                                                                              filename,
                                                                                              chrom)
        results = {}
        results['split2'] = (header + split_two + header_end, results_split2)
        results['split3'] = (header + split_two + split_three + header_end, results_split3)
        results['split4'] = (header + split_two + split_three + split_four + header_end, results_split4)
        results['splitn'] = (header + header_end, results_splitn)

    return results


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


def get_map(filename=MAP_GROUP_PATH, split='\t'):
    db2web_dict = {}
    web2db_dict = {}
    try:
        info = open(filename, 'r+')
        map_list = info.readlines()
        Id_list = [each.strip().split(split)[0].replace('-','_') for each in map_list]
        key_list = [each.strip().split(split)[1].replace('-','_') for each in map_list]
        for k, v in zip(Id_list, key_list):
            db2web_dict[k] = v
            web2db_dict[v] = k
        info.close()
    except IOError:
        print 'not find map sample file'
        return db2web_dict, web2db_dict
    return db2web_dict, web2db_dict


def map_sample(samples, map_dict):
    if samples:
        return [map_dict[sample] for sample in samples]
    return []

'''
add 2017-12-22 add three extra columns on snp table
'''


def get_direction(row):
    groupList = [int(cell) for cell in row]
    if groupList[0] < groupList[1]:
        groupDirect = '1'
    else:
        groupDirect = '0'
    return groupDirect


def add_direction(row, sp='|'):
    groupA = row[SNP_TABLE_HEADER].split(sp)
    groupB = row[SNP_TABLE_HEADER + 1].split(sp)
    groupADirect = get_direction(groupA[:2])
    groupBDirect = get_direction(groupB[:2])
    totalDepth = sum([int(cell) for cell in groupA + groupB])
    row.extend([groupADirect, groupBDirect, str(totalDepth)])
    return row


def humanize_bytes(bytesize, precision=2):
    abbrevs = (
        (1 << 50, 'PB'),
        (1 << 40, 'TB'),
        (1 << 30, 'GB'),
        (1 << 20, 'MB'),
        (1 << 10, 'KB'),
        (1, 'bytes')
    )
    if bytesize == 1:
        return '1 bytes'
    for factor, suffix in abbrevs:
        if bytesize >= factor:
            break

    return '%.*f %s' % (precision, bytesize / factor, suffix)


'''
add on 2018-01-15 
'''


def get_table(user, type):
    from auth.models import Snptable
    results = Snptable.query.filter_by(owner=user, tabletype=type)
    tables = [result.tablename for result in results]
    return tables