# coding:utf-8
'''
test table: users
'''
import pytest
from test.tools import clean_db_cache, DB


@pytest.fixture
def setup_db():
    clean_db_cache('test_users')
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


def test_delete():
    db = DB()
    result = db.delete('test_users', {'username': u'佳绩正'})
    assert result is None


def test_update():
    db = DB()
    result = db.update('test_users', {'snp_table': 'snp_mRNA_table:mRNA_table'}, {'username': 'chencheng'})
    assert result is None


def test_insert():
    db = DB()
    result = db.insert('test_users', {'username': u'郑和',
                                 'email': 'zhenghe@test.com',
                                 'password': '123',
                                 'create_at': '2017-11-30 16:07'})
    assert result is None