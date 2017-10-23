# coding=utf-8
import MySQLdb
from db import DATABASE, HOSTBNAME, USERNAME, PASSWORD


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


def get_merge_group_data(group_info, groupALen, groupBLen):
    results = []
    header_line = [list(each[:6]) for each in group_info]
    groupAList = [list(each[6:(groupALen+6)]) for each in group_info]
    groupBList = [list(each[(groupALen+6):]) for each in group_info]
    mergeGroupA = get_group_data(groupAList)
    mergeGroupB = get_group_data(groupBList)
    mergeGroup = []
    for ListA, ListB in zip(mergeGroupA, mergeGroupB):
        tmpList = []
        for cellA, cellB in zip(ListA, ListB):
            tmpList.append(cellA)
            tmpList.append(cellB)
        mergeGroup.append(tmpList)
    for head, each in zip(header_line, mergeGroup):
        results.append(head + each)
    return results


def calculate_table(table, chrom, start_pos, end_pos, groupA, groupB):
    groupA_len = len(groupA)
    groupB_len = len(groupA)
    select_columns = ['CHR', 'POS', 'REF', 'ALT', 'FEATURE', 'GENE'] + groupA + groupB
    header = ['CHR', 'POS', 'REF', 'ALT',
              'FEATURE', 'GENE',
              'GroupA', 'GroupB',
              'GroupA Frequency Primary Allele',
              'GroupB Frequency Primary Allele',
              'GroupA Frequency Second Allele',
              'GroupB Frequency Second Allele']
    get_group_cmd = "select {columns} from {table} where POS >= {start_pos} and POS <= {end_pos} and CHR='{chrom}';"
    select_columns_str = ','.join(select_columns)
    cmd = get_group_cmd.format(
        columns=select_columns_str,
        table=table,
        start_pos=int(start_pos),
        end_pos=int(end_pos),
        chrom=chrom)
    results = get_merge_group_data(get_db_data(cmd), groupA_len, groupB_len)
    return (header, results)
