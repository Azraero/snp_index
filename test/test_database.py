# coding:utf-8
'''
test table: users
'''
from __future__ import absolute_import
from test.tools import clean_db_data, DB

clean_db_data()
db = DB()
db.insert_all('test_users', [{'username': 'chencheng',
                              'password': '123',
                            'email': '291552579@qq.com',
                            'create_at': '2017-11-28 16:02',
                            'is_active': 'Y',
                            'is_admin': 'Y'},
                            {'username': u'佳绩正',
                            'password': '123',
                            'email': 'jiajizhen@test.com',
                            'create_at': '2017-11-30 11:38',
                            'is_active': 'Y',
                            'snp_table': 'snp_mRNA_table',
                            'expr_table': 'expr_gene_pos',
                            'desc_table': 'locus_gene_mlocus'}])

# test_delete
db.delete('test_users', {'username': u'佳绩正'})

# test_update
db.update('test_users', {'snp_table': 'snp_mRNA_table:mRNA_table'}, {'username': u'佳绩正'})

# test_insert
db.insert('test_users', {'username': u'郑和',
                         'email': 'zhenghe@test.com',
                         'password': '123',
                         'create_at': '2017-11-30 16:07'})

# results = db.execute('select * from users')
# print results
print 'test well!'