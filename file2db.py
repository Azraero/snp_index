# coding=utf-8
import sys
import click
import MySQLdb
from consts import DATABASE, HOSTBNAME, USERNAME, PASSWORD

create_table_cmd = """
                   create table {}(Id INT PRIMARY KEY AUTO_INCREMENT,
                                   CHR VARCHAR(5),
                                   POS VARCHAR(50),
                                   REF VARCHAR(10),
                                   ALT VARCHAR(10),
                                   FEATURE VARCHAR(50),
                                   GENE VARCHAR(100),
                   """

create_group_cmd = """
                   create table {}(Id INT PRIMARY KEY AUTO_INCREMENT,
                                   SAMPLE VARCHAR(20),
                                   DESCRIPTION VARCHAR(100),
                   """


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
@click.option('--filename', help='a file for snp index table or group info')
def table2db(filename, split='\t', add_key=True):
    '''
    invert snp index file to mysql table
    default add index to POS and CHR
    '''
    try:
        with open(filename, 'r') as info:
            header = info.readline().strip()
            header_list = header.split(split)
            header_list = [each.replace('-', '_') for each in header_list]
            if len(header_list) <= 6:
                print 'file header not allowed < 6!'
                sys.exit(1)
            else:
                header_list[:6] = ('CHR', 'POS', 'REF', 'ALT', 'FEATURE', 'GENE')
            if add_key:
                add_key_str = ',key chrindex (CHR), key posindex (POS), key geneindex (GENE)'
            else:
                add_key_str = ''
            con = MySQLdb.connect(HOSTBNAME, USERNAME, PASSWORD, DATABASE)
            tableName = filename.rsplit('/')[1]
            # tableName = '_'.join(['table', tableName
            with con as cur:
                cmd = 'drop table if exists {}'.format(tableName)
                cur.execute(cmd)
                samples = []
                for i in header_list[6:]:
                    samples.append('{} VARCHAR(20)'.format(i))
                cmd = create_table_cmd.format(tableName) + ','.join(samples) + add_key_str + ');'
                # print cmd
                cur.execute(cmd)
                row = info.readline().strip()
                header = ','.join(header_list)
                while (row):
                    tmp_list = row.split(split)
                    tmp_list = ['"' + str(k) + '"' for k in tmp_list]
                    each_line = ','.join(tmp_list)
                    cmd = "insert into {0}({1}) values({2})".format(tableName, header, each_line)
                    cur.execute(cmd)
                    row = info.readline().strip()
                print '{} had been wrote into mysql!'.format(tableName)
    except IOError:
        print 'file not find!'
    except MySQLdb.Error as e:
        print 'mysql error {}:{}'.format(e.args[0], e.args[1])


def group2db(filename, split='\t'):
    '''
    invert snp index group info to mysql table
    '''
    try:
        with open(filename, 'r') as info:
            header = info.readline()
            header_list = header.split(split)
            header_list = [each.replace('-', '_') for each in header_list]
            if len(header_list) <= 2:
                print 'file header not allowed < 2!'
                sys.exit(1)
            else:
                header_list[:2] = ('SAMPLE', 'DESCRIPTION')
            con = MySQLdb.connect(HOSTBNAME, USERNAME, PASSWORD, DATABASE)
            tableName = filename.rsplit('/')[1]
            tableName = '_'.join(['group', tableName])
            with con as cur:
                cmd = 'drop table if exists {}'.format(tableName)
                cur.execute(cmd)
                cultivar = []
                for i in header_list[2:]:
                    cultivar.append('{} VARCHAR(20)'.format(i))
                cmd = create_group_cmd.format(tableName) + ','.join(cultivar) + ')'
                cur.execute(cmd)
                row = info.readline().strip()
                header = ','.join(header_list)
                while (row):
                    tmp_list = row.split(split)
                    tmp_list = ['"' + str(k) + '"' for k in tmp_list]
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
@click.option('--filename', help='a file for snp index table or group info')
@click.option('--type', help="a string for 'table' or 'group'")
def data2db(filename, type):
    if type == 'table':
        table2db(filename)
    elif type == 'group':
        group2db(filename)
    else:
        print 'type error!'
        sys.exit(1)


if __name__ == '__main__':
    table2db()
