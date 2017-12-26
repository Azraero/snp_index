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
INPUT_TABLE = os.path.join(basedir, 'data', 'mRNA_snp_ann_table')
SNP_INDEX_TABLE_PATH = os.path.join(basedir, 'app', 'static', 'variation_results')


def create_group_info(groupA, groupB, filename):
    groupA_name = filename.split('vs')[0]
    groupB_name = filename.split('vs')[1]
    with open(os.path.join(SNP_SCRIPT_DIR, filename), 'w+') as f:
        for sample in groupA:
            f.write('\t'.join([sample.replace('_', '-'), groupA_name]) + '\n')
        for sample in groupB:
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

