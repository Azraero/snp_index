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
@click.option('--filename', help='a file for snp index table')
def file2db(filename, split='\t'):
    '''
    invert snp index file to mysql table
    '''
    try:
        with open(filename, 'r') as info:
            header = info.readline()
            header_list = header.split(split)
            header_list = [each.replace('-', '_') for each in header_list]
            if len(header_list) <= 4:
                print 'file header not allowed < 4!'
                sys.exit(1)
            else:
                header_list[:4] = ('CHR', 'POS', 'REF', 'ALT')
            con = MySQLdb.connect(HOSTBNAME, USERNAME, PASSWORD, DATABASE)
            tableName = filename.rsplit('/')[1]
            with con as cur:
                cmd = 'drop table if exists {}'.format(tableName)
                cur.execute(cmd)
                samples = []
                for i in header_list[4:]:
                    samples.append('{} VARCHAR(20)'.format(i))
                cmd = create_table_cmd.format(tableName) + ','.join(samples) + ')'
                cur.execute(cmd)
                row = info.readline()
                header = ','.join(header_list)
                while(row):
                    tmp_list = row.split(split)[:4]
                    tmp_list_samples = row.split(split)[4:]
                    tmp_list_samples = [deal_cell(k) for k in tmp_list_samples]
                    tmp_list.extend(tmp_list_samples)
                    tmp_list = ['"'+str(k)+'"' for k in tmp_list]
                    each_line = ','.join(tmp_list)
                    cmd = "insert into {0}({1}) values({2})".format(tableName, header, each_line)
                    cur.execute(cmd)
                    row = info.readline()
                print '{} had been wrote into mysql!'.format(tableName)
    except IOError:
        print 'file not find!'
    except MySQLdb.Error as e:
        print 'mysql error {}:{}'.format(e.args[0], e.args[1])


if __name__ == '__main__':
    file2db()
