# coding=utf-8
import sys
import MySQLdb
from consts import DATABASE, HOSTBNAME, USERNAME, PASSWORD

create_table_cmd = """
                   create table {}(Id INT PRIMARY KEY AUTO_INCREMENT,
                                   CHR VARCHAR(5),
                                   POS VARCHAR(50),
                                   REF VARCHAR(1),
                                   ALT VARCHAR(1),
                   """


def file2db(fileName, split='\t'):
    try:
        with open(fileName, 'r') as info:
            header = info.readline()
            header_list = header.split(split)
            if len(header_list) <= 4:
                print 'file header not allowed < 4!'
                sys.exit(1)
            else:
                header_list[:4] = ('CHR', 'POS', 'REF', 'ALT')
            con = MySQLdb.connect(HOSTBNAME, USERNAME, PASSWORD, DATABASE)
            with con as cur:
                cmd = 'drop table if exists {}'.format(fileName)
                cur.execute(cmd)
                samples = []
                for i in header_list[4:]:
                    samples.append('{} VARCHAR(10)'.format(i))
                cmd = create_table_cmd.format(fileName) + ','.join(samples) + ')'
                cur.execute(cmd)
                row = info.readline()
                header = ','.join(header_list)
                while(row):
                    tmp_list = row.split(split)
                    tmp_list = ['"'+k+'"' for k in tmp_list]
                    each_line = ','.join(tmp_list)
                    cmd = "insert into {0}({1}) values({2})".format(fileName, header, each_line)
                    cur.execute(cmd)
                    row = info.readline()
                print 'done!'
    except IOError:
        print 'file not find!'
    except MySQLdb.Error as e:
        print 'mysql error {}:{}'.format(e.args[0], e.args[1])


if __name__ == '__main__':
    file2db('mRNA_snp_index')
