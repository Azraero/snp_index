import os
import subprocess
from settings import basedir
from app.app import celery
from app.mail import send_mail
from app.db import DB
import glob


RENDER_PATH = '/static/variation_results'
SNP_SCRIPT_DIR = '/public/script/snp_index_table'
SCRIPT_FILE = 'mergeSampleAlleSnpEff.py'
INPUT_TABLE = os.path.join(basedir, 'data', 'mRNA.filter.hq.snp.ann.table')
SNP_INDEX_TABLE_PATH = os.path.join(basedir, 'app', 'static', 'variation_results')
NOT_REP_SAMPLES = ['KYP1_1', 'KYP2_1', 'M4_19_1', 'M4_19_2', 'M4_19_3', 'M4_25_1', 'M4_25_2', 'M4_25_3',
                   'M5_3_1', 'M5_3_2', 'M5_3_3', 'M5_9_1', 'M5_9_2', 'M5_9_3', 'M9_2P1_1', 'M9_2P1_3',
                   'WTGP1_3', 'WTGP2_1', 'Y4_19_1', 'Y4_19_2', 'Y4_19_3', 'Y4_25_1', 'Y4_25_2', 'Y4_25_3',
                   'Y5_3_1', 'Y5_3_2', 'Y5_3_3', 'Y5_9_1', 'Y5_9_2', 'Y5_9_3', 'ZYP1_3', 'ZYP2_1',
                   'CDRY_L_1', 'CDRY_L_2', 'CDRY_L_3', 'CTLY_L_1', 'CTLY_L_2', 'CTLY_L_3']


def create_group_info(groupA, groupB, filename):
    groupA_name = filename.split('vs')[0]
    groupB_name = filename.split('vs')[1]
    with open(os.path.join(SNP_SCRIPT_DIR, filename), 'w+') as f:
        for sample in groupA:
            if sample in NOT_REP_SAMPLES:
                f.write('\t'.join([sample, groupA_name]) + '\n')
            else:
                f.write('\t'.join([sample.replace('_', '-'), groupA_name]) + '\n')
        for sample in groupB:
            if sample in NOT_REP_SAMPLES:
                f.write('\t'.join([sample, groupB_name]) + '\n')
            else:
                f.write('\t'.join([sample.replace('_', '-'), groupB_name]) + '\n')


@celery.task
def run_snp_variations(group_info, user):
    group_name = group_info.keys()
    groupA = group_info[group_name[0]]
    groupB = group_info[group_name[1]]
    create_group_info(groupA, groupB, filename='vs'.join(group_name))

    cmd = "python {script} -i {input} -o {output} -g {group} -d {depth}".format(
        script=os.path.join(SNP_SCRIPT_DIR, SCRIPT_FILE),
        input=INPUT_TABLE,
        output=os.path.join(basedir, 'app', 'static', 'variation_results', 'vs'.join(group_name) + '_table'),
        group=os.path.join(SNP_SCRIPT_DIR, 'vs'.join(group_name)),
        depth='5'
    )
    subprocess.call(cmd, shell=True)
    os.chdir(os.path.join(basedir, 'app', 'static', 'variation_results'))
    zip_cmd = 'zip {0} {1}'.format(
        'vs'.join(group_name) + '_table.zip',
        'vs'.join(group_name) + '_table'
    )
    subprocess.call(zip_cmd, shell=True)
    db = DB()
    results = db.execute("select email from users where username='{0}'".format(user))
    if results[0][0]:
        to = results[0][0]
        send_mail(to, 'Snp Variation Results',
                  'mail/variation_results', user=user, filename='vs'.join(group_name) + '_table')
    return 'done'


def get_select_table(table):
    select_table_path = os.path.join(SNP_INDEX_TABLE_PATH, table)
    if not os.path.exists(select_table_path):
        return 'error'
    return table


def show_calculate_tables():
    tables = glob.glob(SNP_INDEX_TABLE_PATH + '/*')
    if tables:
        return [table.rsplit('/',1)[1] for table in tables if len(table.split('.')) < 2]
    return []

