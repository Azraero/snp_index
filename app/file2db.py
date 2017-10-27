# coding=utf-8
import sys
import click
import MySQLdb
from db import DATABASE, HOSTBNAME, USERNAME, PASSWORD, table_info


def deal_cell(cell):
    cell_list = cell.split(',')
    if len(cell_list) == 1:
        return 0
    else:
        if int(cell_list[1]) == 0:
            return 0
        else:
            return round(float(cell_list[1]) / (int(cell_list[0]) + int(cell_list[1])), 2)


@click.command()
@click.option('--filename', help='a file for snp index table or expr table')
@click.option('--typename', help="a type value is 'snp' or 'expr'")
def table2db(filename, typename, split='\t', add_key=True):
    '''
    invert file to mysql table
    '''
    tableName = filename.rsplit('/')[1]
    tableName = '_'.join([typename, tableName])
    fixed_column_num = table_info[typename]['fixed_column_num']

    try:
        with open(filename, 'r') as info:
            header = info.readline().strip()
            header_list = header.split(split)
            # invert all '-' to '_'
            header_list = [each.replace('-', '_') for each in header_list]
            if len(header_list) <= fixed_column_num:
                print '{0} header not allowed < {1}!'.format(filename,
                                                             fixed_column_num)
                sys.exit(1)
            else:
                header_list[:fixed_column_num] = table_info[typename]['fixed_column_name']
            if add_key:
                add_key_str = table_info[typename]['add_key_str']
            else:
                add_key_str = ''
            con = MySQLdb.connect(HOSTBNAME, USERNAME, PASSWORD, DATABASE)
            with con as cur:
                cmd = 'drop table if exists {}'.format(tableName)
                cur.execute(cmd)
                samples = []
                for i in header_list[fixed_column_num:]:
                    samples.append('{} VARCHAR(20)'.format(i))
                cmd = table_info[typename]['cmd'].format(tableName) + ','.join(samples) + add_key_str +');'
                # print cmd
                cur.execute(cmd)
                row = info.readline().strip()
                header = ','.join(header_list)
                while(row):
                    tmp_list = row.split(split)
                    tmp_list = ['"'+str(k)+'"' for k in tmp_list]
                    each_line = ','.join(tmp_list)
                    cmd = "insert into {0}({1}) values({2})".format(tableName, header, each_line)
                    cur.execute(cmd)
                    row = info.readline().strip()
                print '{} had been wrote into mysql!'.format(tableName)
    except IOError:
        print 'file not find!'
    except MySQLdb.Error as e:
        print 'mysql error {}:{}'.format(e.args[0], e.args[1])


if __name__ == '__main__':
    table2db()
