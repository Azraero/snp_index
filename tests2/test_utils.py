# coding:utf-8
'''
test snp index utils APIs
'''
import pytest
import random
import datetime
from test.tools import clean_db_cache
from app.db import DB
from app.utils import get_db_tables, get_db_data, get_samples_by_table, \
    get_map, map_sample


@pytest.fixture
def setup():
    clean_db_cache('test_users')
    db = DB()
    db.insert('test_users', {'username': 'chencheng',
                    'password': '123',
                    'email': 'jiajizhen@test.com',
                    'create_at': datetime.datetime.now().strftime("%y-%m-%d %H:%M"),
                    'is_active': 'Y',
                    'snp_table': 'snp_mRNA_table',
                    'expr_table': 'expr_gene_pos',
                    'desc_table': 'locus_gene_mlocus'})


def test_getDBTable():
    setup()
    tables = get_db_tables(user=u'佳绩正', type='snp')
    assert 'snp_mRNA_table' in tables


def test_getDBData():
    setup()
    cmd = "select password from test_users where username='chencheng';"
    results = get_db_data(cmd)
    assert '123' == results[0][0]


def test_getSamplesByTable():
    samples = get_samples_by_table(table='snp_mRNA_table', type='snp')
    test_sets = ['WTGP1_3', 'Y5_9_3', 'WHd_A20_3', 'G097_02_6']
    assert random.choice(test_sets) in samples


def test_mapSample():
    db2web_dict, web2db_dict = get_map()
    samples = get_samples_by_table(table='snp_mRNA_table', type='snp')
    test_web_sets = ['159_9_CS_P_2', '196_2_D_P', 'W3_14LL']
    test_db_sets = 'G097_0204_32bei1'
    web_samples = map_sample(samples, db2web_dict)
    db_samples = map_sample(test_web_sets, web2db_dict)
    assert test_db_sets in db_samples
    assert random.choice(test_web_sets) in web_samples