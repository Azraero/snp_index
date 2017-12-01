# coding:utf-8
'''
test snp index utils APIs
'''
from test.tools import clean_db_data
from app.db import DB
from app.utils import get_db_tables

clean_db_data()
db = DB()
db.insert('test_users', {'username': u'佳绩正',
                    'password': '123',
                    'email': 'jiajizhen@test.com',
                    'create_at': '2017-11-30 11:38',
                    'is_active': 'Y',
                    'snp_table': 'snp_mRNA_table',
                    'expr_table': 'expr_gene_pos',
                    'desc_table': 'locus_gene_mlocus'})

tables = get_db_tables(u'佳绩正', type='snp')
print tables
print 'test well!'