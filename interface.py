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


def query_table(table, chr, start_pos, end_pos, samples):
    select_columns = ['CHR', 'POS', 'REF', 'ALT']
    select_columns.extend(samples)
    select_columns_str = ','.join(select_columns)
    cmd = "select " + select_columns_str + " from {table} where POS >= {start_pos} and POS <= {end_pos} and CHR='{chr}'".format(table=table,
                                                                                                                                start_pos=int(start_pos),
                                                                                                                                end_pos=int(end_pos),
                                                                                                                                chr=chr)
    results = get_db_data(cmd)
    return (select_columns, results)
