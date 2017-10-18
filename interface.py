# coding=utf-8
import MySQLdb
from consts import DATABASE, HOSTBNAME, USERNAME, PASSWORD


def get_db_data(cmd, fetchall=True):
    con = MySQLdb.connect(HOSTBNAME, USERNAME, PASSWORD, DATABASE)
    with con as cur:
        cur.execute(cmd)
        if fetchall:
            rows = cur.fetchall()
            return rows
        else:
            row = cur.fetchone()
            return row


def query_table(table, chrom, start_pos, end_pos, groupA, groupB):
    select_columns = ['CHR', 'POS', 'REF', 'ALT']
    select_columns.extend(samples)
    select_columns_str = ','.join(select_columns)
    cmd = "select " + select_columns_str + " from {table} where POS >= {start_pos} and POS <= {end_pos} and CHR='{chrom}'".format(table=table,
                                                                                                                                  start_pos=int(start_pos),
                                                                                                                                  end_pos=int(end_pos),
                                                                                                                                  chrom=chrom)
    results = get_db_data(cmd)
    return (select_columns, results)


def get_merge_group_data(group_info):
    new_results = []
    for each in group_info:
        filter_cell = [cell for cell in each if cell != '0' and cell != '0,0' and cell != '0,0,0' and cell != '.']
        if len(filter_cell) == 0:
            new_results.append(['0,0', 'NA', 'NA'])
        else:
            first_pos = sum([int(cell.split(',')[0]) for cell in filter_cell])
            second_pos = sum([int(cell.split(',')[1]) for cell in filter_cell])
            first_ratio = round(float(first_pos) / (first_pos + second_pos), 2)
            second_ratio = round(float(second_pos) / (first_pos + second_pos), 2)
            new_cell = ','.join([str(first_pos), str(second_pos)])
            new_results.append([new_cell, first_ratio, second_ratio])

    return new_results


def calculate_table(table, chrom, start_pos, end_pos, groupA, groupB):
    extra_columns = ['CHR', 'POS', 'REF', 'ALT']
    header = ['CHR', 'POS', 'REF', 'ALT',
              'GroupA', 'GroupA Frequency Primary Allele', 'GroupB Frequency Second Allele',
              'GroupB', 'GroupA Frequency Primary Allele', 'GroupB Frequency Second Allele']
    get_group_cmd = "select {columns} from {table} where POS >= {start_pos} and POS <= {end_pos} and CHR='{chrom}';"
    groupA_columns_str = ','.join(groupA)
    groupB_columns_str = ','.join(groupB)
    extra_columns_str = ','.join(extra_columns)
    cmd = get_group_cmd.format(
        columns=groupA_columns_str,
        table=table,
        start_pos=int(start_pos),
        end_pos=int(end_pos),
        chrom=chrom)
    resultA = get_merge_group_data(get_db_data(cmd))
    cmd = get_group_cmd.format(
        columns=groupB_columns_str,
        table=table,
        start_pos=int(start_pos),
        end_pos=int(end_pos),
        chrom=chrom)
    resultB = get_merge_group_data(get_db_data(cmd))
    cmd = get_group_cmd.format(
        columns=extra_columns_str,
        table=table,
        start_pos=int(start_pos),
        end_pos=int(end_pos),
        chrom=chrom)
    extra_results = get_db_data(cmd)
    extra_results = [list(k) for k in extra_results]
    results = []
    for each, eachA, eachB in zip(extra_results, resultA, resultB):
        results.append(each + eachA + eachB)
    return (header, results)
