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
    groupBList = [list(each[(groupBLen+6):]) for each in group_info]
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


def calculate_table(cmd, groupA_len, groupB_len):
    header = ['CHR', 'POS', 'REF', 'ALT',
              'FEATURE', 'GENE',
              'GroupA', 'GroupB',
              'GroupA Frequency Primary Allele',
              'GroupB Frequency Primary Allele',
              'GroupA Frequency Second Allele',
              'GroupB Frequency Second Allele']
    results = get_merge_group_data(get_db_data(cmd), groupA_len, groupB_len)
    return (header, results)


'''
add on 2017-10-26
'''


def get_cmd_by_regin(table, chrom, start_pos, end_pos, groupA, groupB):
    select_columns = ['CHR', 'POS', 'REF', 'ALT', 'FEATURE', 'GENE'] + groupA + groupB
    get_group_cmd = "select {columns} from {table} where POS >= {start_pos} and \
    POS <= {end_pos} and CHR='{chrom}';"
    select_columns_str = ','.join(select_columns)
    cmd = get_group_cmd.format(
        columns=select_columns_str,
        table=table,
        start_pos=int(start_pos),
        end_pos=int(end_pos),
        chrom=chrom)
    return (cmd, len(groupA), len(groupB))


def get_cmd_by_gene(table, gene_id, up, down, groupA, groupB):
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
add on 2017-10-27
'''


def get_expr_table(table, gene_ids, groupA, groupB):
    select_columns = ['GENE_ID', 'CHR', 'POS_START', 'POS_END'] + groupA + groupB
    select_columns_str = ','.join(select_columns)
    results = []
    for gene in gene_ids:
        cmd = "select {columns} from {table} where GENE_ID='{gene_id}';".format(
            columns=select_columns_str,
            table=table,
            gene_id=gene
        )
        result = get_db_data(cmd, fetchall=False)
        if not result:
            return (gene, '')
        results.append(list(result))
    return (select_columns, results)


'''
add on 2017-11-3
'''


def get_locus_result(genename):
    locus_result = {}
    cmd = """select l.*, f.BLAST_Hit_Accession, f.Description, f.Pfam_ID,
             f.Interpro_ID, f.GO_ID from locus l left join func f
             on l.GENE_ID=f.GENE_ID where l.GENE_ID='{0}';
          """.format(genename)
    result = get_db_data(cmd, fetchall=False)
    if result:
        gene_id, chr, pos_start, pos_end = result[1:5]
        blast_hit, description, pfam_id, interpro_id, go_id = result[5:]
        locus_result['gene_identification'] = {'Gene Product Name': description,
                                               'Locus Name': genename}
        locus_result['gene_attributes'] = {'Chromosome': chr,
                                           "CDS Coordinates (5'-3')":'{0} - {1}'.format(pos_start,
                                                                                        pos_end)}
        header = ['Accession', 'Description', 'Pfam_ID', 'Interpro_ID', 'GO_ID']
        locus_result['gene_annotation'] = {}
        locus_result['gene_annotation']['header'] = header
        locus_result['gene_annotation']['body'] = [blast_hit, description, pfam_id, interpro_id, go_id]
    return locus_result