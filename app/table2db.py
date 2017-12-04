# coding=utf-8
import sys
import click
import MySQLdb
from db_const import DATABASE, HOSTNAME, USERNAME, PASSWORD, table_info

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

def deal_cell(cell):
    cell_list = cell.split(',')
    if len(cell_list) == 1:
        return 0
    else:
        if int(cell_list[1]) == 0:
            return 0
        else:
            return round(float(cell_list[1]) / (int(cell_list[0]) + int(cell_list[1])), 2)


def generateDB(db, filename, action, split, add_key=True):
    '''
    create or add data to snp index db
    '''
    try:
        with open(filename, 'r') as info:
            old_header = info.readline().strip()
            header_list = table_info[db]['header']
            if add_key:
                add_key_str = table_info[db]['add_key_str']
            else:
                add_key_str = ''
            con = MySQLdb.connect(HOSTNAME, USERNAME, PASSWORD, DATABASE)
            with con as cur:
                if action == 'create':
                    cmd = 'drop table if exists {}'.format(db)
                    cur.execute(cmd)
                    cmd = table_info[db]['cmd'].format(db) + add_key_str + ');'
                    # print cmd
                    cur.execute(cmd)

                results = get_db_data('show tables')
                results = [result[0] for result in results]
                if db not in results:
                    print '{0} is not create, please create table first!'.format(db)
                    sys.exit(1)

                row = info.readline().strip()
                header = ','.join(header_list)
                while(row):
                    tmp_list = row.split(split)
                    tmp_list = ['"'+str(k)+'"' for k in tmp_list]
                    each_line = ','.join(tmp_list)
                    cmd = "insert into {0}({1}) values({2})".format(db, header, each_line)
                    cur.execute(cmd)
                    row = info.readline().strip()
                print '{} had been wrote into mysql!'.format(db)
    except IOError:
        print 'file not find!'
    except MySQLdb.Error as e:
        print 'mysql error {}:{}'.format(e.args[0], e.args[1])


def file2db(filename, typename, split, add_key=True):
    '''
    invert file to mysql table
    '''
    tableName = filename.rsplit('/', 1)[1]
    tableName = '_'.join([typename, tableName])
    fixed_column_num = table_info[typename]['fixed_column_num']

    try:
        with open(filename, 'r') as info:
            header = info.readline().strip()
            header_list = header.split(split)
            # invert all '-' to '_'
            header_list = [each.replace('-', '_') for each in header_list]
            # print header_list
            if len(header_list) < fixed_column_num:
                print '{0} header not allowed < {1}!'.format(filename,
                                                             fixed_column_num)
                sys.exit(1)
            else:
                header_list[:fixed_column_num] = table_info[typename]['fixed_column_name']
            if add_key:
                add_key_str = table_info[typename]['add_key_str']
            else:
                add_key_str = ''
            con = MySQLdb.connect(HOSTNAME, USERNAME, PASSWORD, DATABASE)
            with con as cur:
                cmd = 'drop table if exists {}'.format(tableName)
                cur.execute(cmd)
                samples = []
                if header_list[fixed_column_num:]:
                    for i in header_list[fixed_column_num:]:
                        samples.append('{} VARCHAR(20)'.format(i))
                    cmd = table_info[typename]['cmd'].format(tableName) + ','.join(samples) + add_key_str +');'
                else:
                    cmd = table_info[typename]['cmd'].format(tableName) + add_key_str + ');'
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


@click.command()
@click.option('--filename', help='a file which want to into your mysql!')
@click.option('--typename', help="a string for 'file' or 'db'")
@click.option('--action', help="a string for 'create' or 'add'", default='add')
@click.option('--db', help="a database name which you want to connection include 'locus' and 'func'")
@click.option('--split', help="a string to field your file default '\t'", default='\t')
def table2db(filename, typename, split, action, db):
    if typename == 'db':
        generateDB(db, filename, action, split)
    else:
        file2db(filename, typename, split)


if __name__ == '__main__':
    table2db()
